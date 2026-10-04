//! Property tests on GMR's pure parsing functions (TEST_PLAN 4, L0 item 3 as proptest).
//! Obligations: L0-SEL-1 selector spellings agree; L0-PATH-1 `inside` never escapes the root;
//! L0-REF-1 memory addresses round-trip.

use std::path::{Component, Path, PathBuf};

use gmr_core::Outcome;
use gmr_core::memory::Ref;
use gmr_transport::file::inside;
use gmr_transport::select::{pick, pointer};
use proptest::prelude::*;
use serde_json::json;

fn key() -> impl Strategy<Value = String> {
    // Keys without '.', which the dotted spelling reserves as a separator.
    "[a-zA-Z0-9_~/ -]{1,12}"
}

proptest! {
    /// L0-SEL-1: `/k` (escaped), `$.k` and `k` pick the same value when k has no '.' and no '/'.
    #[test]
    fn selector_spellings_agree(k in "[a-zA-Z0-9_ -]{1,12}", v in any::<i64>()) {
        let body = json!({ k.clone(): v, "other": 0 });
        let escaped = format!("/{}", k.replace('~', "~0").replace('/', "~1"));
        for select in [escaped.as_str(), &format!("$.{k}"), k.as_str()] {
            match pick(&body, Some(select)) {
                Outcome::Found { facts } => prop_assert_eq!(facts.as_value()["value"].clone(), json!(v)),
                other => prop_assert!(false, "{:?} -> {:?}", select, other),
            }
        }
    }

    /// L0-SEL-2: `pointer` never panics and always yields a JSON pointer ("" or starting with '/').
    #[test]
    fn pointer_is_a_json_pointer(s in ".{0,40}") {
        let p = pointer(&s);
        prop_assert!(p.is_empty() || p.starts_with('/'), "{:?} -> {:?}", s, p);
    }

    /// L0-SEL-3: keys containing '~' or '/' are reachable through the escaped pointer spelling.
    #[test]
    fn escaped_keys_are_reachable(k in key(), v in any::<i64>()) {
        let body = json!({ k.clone(): v });
        let escaped = format!("/{}", k.replace('~', "~0").replace('/', "~1"));
        let found = matches!(pick(&body, Some(&escaped)), Outcome::Found { .. });
        prop_assert!(found, "{:?} not reachable as {:?}", k, escaped);
    }

    /// L0-PATH-1: whatever `inside` accepts stays under the root after lexical normalisation.
    #[test]
    fn inside_never_escapes(parts in proptest::collection::vec(prop_oneof![
        Just("..".to_string()), Just(".".to_string()), "[a-z]{1,4}".prop_map(|s| s)], 0..8),
        absolute in any::<bool>()) {
        let declared = format!("{}{}", if absolute { "/" } else { "" }, parts.join("/"));
        let root = Path::new("/r/o/o/t");
        if let Some(joined) = inside(root, &declared) {
            let mut norm = PathBuf::new();
            for c in joined.components() {
                match c {
                    Component::ParentDir => { norm.pop(); }
                    Component::CurDir => {}
                    other => norm.push(other),
                }
            }
            prop_assert!(norm.starts_with(root), "{:?} -> {:?}", declared, joined);
        }
    }

    /// L0-REF-1: a parsed `<provider>:<id>` address prints back to itself.
    #[test]
    fn ref_round_trips(provider in "[a-z][a-z0-9_-]{0,10}", id in "[^\\s]{1,20}") {
        let address = format!("{provider}:{id}");
        if let Some(parsed) = Ref::parse(&address) {
            prop_assert_eq!(parsed.to_string(), address);
        }
    }
}
