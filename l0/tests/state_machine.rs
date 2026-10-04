//! L0-SM-1: black-box state machine over the real `gmr` binary (TEST_PLAN 4, L0 item 1).
//!
//! Random sequences of set-value / check / accept on `file://` JSON-pointer anchors are replayed
//! against a reference model and against the CLI; after every check the handed-back set must match.
//! Reference model (observed in T25 follow-up, 2026-09-24): an anchor is flagged once a check sees
//! its value differ from the baseline, stays flagged even if the value returns, and
//! `accept --baseline` re-pins the baseline to the current value and clears the flag.
//! ponytail: CLI black-box, ~0.1 s per op; proptest cases kept small. Journal-replay equivalence
//! is not covered here.

use std::collections::{BTreeMap, BTreeSet};
use std::path::{Path, PathBuf};
use std::process::Command;

use proptest::prelude::*;
use serde_json::{Value, json};

const KEYS: [&str; 3] = ["a", "b", "c"];

fn gmr() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("../../GMR-latest/target/release/gmr")
}

fn run(dir: &Path, program: &Path, args: &[&str]) -> std::process::Output {
    Command::new(program).args(args).current_dir(dir).output().expect("spawn")
}

#[derive(Debug, Clone)]
enum Op {
    Set(usize, i64),
    Check,
    Accept(usize),
}

fn op() -> impl Strategy<Value = Op> {
    prop_oneof![
        3 => (0..KEYS.len(), 0..3i64).prop_map(|(k, v)| Op::Set(k, v)),
        2 => Just(Op::Check),
        1 => (0..KEYS.len()).prop_map(Op::Accept),
    ]
}

struct Model {
    baseline: BTreeMap<&'static str, i64>,
    current: BTreeMap<&'static str, i64>,
    flagged: BTreeSet<&'static str>,
}

fn write(dir: &Path, values: &BTreeMap<&'static str, i64>) {
    let body: Value = json!(values);
    std::fs::write(dir.join("c/r.json"), body.to_string()).unwrap();
}

fn handed_back(dir: &Path) -> BTreeSet<String> {
    let out = run(dir, &gmr(), &["check", "--json"]);
    let report: Value = serde_json::from_slice(&out.stdout).expect("check --json");
    report["handed_back"].as_array().unwrap().iter().map(|h| h["anchor"].as_str().unwrap().to_string()).collect()
}

proptest! {
    #![proptest_config(ProptestConfig { cases: 24, ..ProptestConfig::default() })]

    #[test]
    fn cli_matches_reference_model(ops in proptest::collection::vec(op(), 1..12)) {
        let tmp = tempfile::tempdir().unwrap();
        let dir = tmp.path();
        std::fs::create_dir(dir.join("c")).unwrap();
        let start: BTreeMap<&'static str, i64> = KEYS.iter().map(|k| (*k, 0)).collect();
        write(dir, &start);
        let git = Path::new("git");
        run(dir, git, &["init", "-q", "."]);
        run(dir, git, &["add", "-A"]);
        run(dir, git, &["-c", "user.email=l0@local", "-c", "user.name=l0", "commit", "-qm", "a"]);
        prop_assert!(run(dir, &gmr(), &["init", "--json"]).status.success());
        for k in KEYS {
            let out = run(dir, &gmr(), &["anchor", &format!("file://c/r.json#/{k}"), "--as", k, "-m", k, "--json"]);
            prop_assert!(out.status.success(), "anchor {}: {}", k, String::from_utf8_lossy(&out.stderr));
        }
        let mut m = Model { baseline: start.clone(), current: start, flagged: BTreeSet::new() };
        for (i, op) in ops.iter().enumerate() {
            match *op {
                Op::Set(k, v) => {
                    m.current.insert(KEYS[k], v);
                    write(dir, &m.current);
                }
                Op::Check => {
                    for k in KEYS {
                        if m.current[k] != m.baseline[k] {
                            m.flagged.insert(k);
                        }
                    }
                    let want: BTreeSet<String> = m.flagged.iter().map(|k| k.to_string()).collect();
                    let got = handed_back(dir);
                    prop_assert_eq!(&got, &want, "after op {} of {:?}", i, ops);
                }
                Op::Accept(k) => {
                    let out = run(dir, &gmr(), &["accept", KEYS[k], "--baseline", "--why", "l0", "--json"]);
                    if out.status.success() {
                        m.baseline.insert(KEYS[k], m.current[KEYS[k]]);
                        m.flagged.remove(KEYS[k]);
                    }
                }
            }
        }
    }
}
