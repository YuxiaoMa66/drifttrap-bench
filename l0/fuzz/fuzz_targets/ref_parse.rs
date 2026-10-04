#![no_main]
//! L0-REF-1 under libFuzzer: a parsed memory address prints back to itself.
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    let Ok(address) = std::str::from_utf8(data) else { return };
    if let Some(parsed) = gmr_core::memory::Ref::parse(address) {
        assert_eq!(parsed.to_string(), address);
    }
});
