//! L0-STORE-1: a damaged `.anchor` store must make `gmr check` fail loudly, never panic and never
//! report a clean result (TEST_PLAN 4, L0 item 3 "corrupted SQLite", black-box over the real binary).
//! Damage: overwrite random byte ranges or truncate `memory.db`, `survey-index.sqlite`,
//! `anchors.toml` or `probes.toml`. A drifted anchor exists before the damage, so "exit 0 with an
//! empty hand-back" would be a silent loss of the drift.

use std::path::{Path, PathBuf};
use std::process::Command;

use proptest::prelude::*;

const FILES: [&str; 4] = ["state/memory.db", "state/survey-index.sqlite", "anchors.toml", "probes.toml"];

fn gmr() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("../../GMR-latest/target/release/gmr")
}

fn run(dir: &Path, program: &str, args: &[&str]) -> std::process::Output {
    Command::new(program).args(args).current_dir(dir).output().expect("spawn")
}

#[derive(Debug, Clone)]
enum Damage {
    Overwrite { at: f64, len: usize, byte: u8 },
    Truncate { keep: f64 },
}

fn damage() -> impl Strategy<Value = Damage> {
    prop_oneof![
        (0.0..1.0f64, 1..512usize, any::<u8>()).prop_map(|(at, len, byte)| Damage::Overwrite { at, len, byte }),
        (0.0..1.0f64).prop_map(|keep| Damage::Truncate { keep }),
    ]
}

proptest! {
    #![proptest_config(ProptestConfig { cases: 40, ..ProptestConfig::default() })]

    #[test]
    fn damaged_store_fails_loudly(file in 0..FILES.len(), how in damage()) {
        let tmp = tempfile::tempdir().unwrap();
        let dir = tmp.path();
        let g = gmr();
        let g = g.to_str().unwrap();
        std::fs::create_dir(dir.join("c")).unwrap();
        std::fs::write(dir.join("c/r.json"), r#"{"a":1}"#).unwrap();
        run(dir, "git", &["init", "-q", "."]);
        run(dir, "git", &["add", "-A"]);
        run(dir, "git", &["-c", "user.email=l0@local", "-c", "user.name=l0", "commit", "-qm", "a"]);
        run(dir, g, &["init", "--json"]);
        run(dir, g, &["anchor", "file://c/r.json#/a", "--as", "a", "-m", "a", "--json"]);
        std::fs::write(dir.join("c/r.json"), r#"{"a":2}"#).unwrap();

        let target = dir.join(".anchor").join(FILES[file]);
        let mut bytes = std::fs::read(&target).unwrap();
        match how {
            Damage::Overwrite { at, len, byte } => {
                let start = (at * bytes.len() as f64) as usize;
                let end = (start + len).min(bytes.len());
                bytes[start..end].iter_mut().for_each(|b| *b = byte);
            }
            Damage::Truncate { keep } => bytes.truncate((keep * bytes.len() as f64) as usize),
        }
        std::fs::write(&target, &bytes).unwrap();

        let out = run(dir, g, &["check", "--json"]);
        let stderr = String::from_utf8_lossy(&out.stderr);
        prop_assert!(!stderr.contains("panicked"), "panic on {:?} {:?}: {}", FILES[file], how, stderr);
        prop_assert_ne!(out.status.code(), Some(101));
        // Either the drift is still reported (exit 1) or the damage is reported as an error (exit >= 2).
        prop_assert_ne!(out.status.code(), Some(0), "silent clean result after damaging {:?} {:?}", FILES[file], how);
    }
}
