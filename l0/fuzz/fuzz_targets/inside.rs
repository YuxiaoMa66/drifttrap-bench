#![no_main]
//! L0-PATH-1 under libFuzzer: whatever `inside` accepts stays under the root.
use std::path::{Component, Path, PathBuf};
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    let Ok(declared) = std::str::from_utf8(data) else { return };
    let root = Path::new("/r/o/o/t");
    if let Some(joined) = gmr_transport::file::inside(root, declared) {
        let mut norm = PathBuf::new();
        for c in joined.components() {
            match c {
                Component::ParentDir => { norm.pop(); }
                Component::CurDir => {}
                other => norm.push(other),
            }
        }
        assert!(norm.starts_with(root), "{declared:?} -> {joined:?}");
    }
});
