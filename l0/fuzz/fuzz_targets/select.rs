#![no_main]
//! L0-SEL-2 under libFuzzer: any selector yields a JSON pointer, and `pick` on arbitrary JSON never panics.
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    let Ok(text) = std::str::from_utf8(data) else { return };
    let (select, body) = text.split_once('\n').unwrap_or((text, "{}"));
    let p = gmr_transport::select::pointer(select);
    assert!(p.is_empty() || p.starts_with('/'), "{select:?} -> {p:?}");
    if let Ok(value) = serde_json::from_str::<serde_json::Value>(body) {
        let _ = gmr_transport::select::pick(&value, Some(select));
    }
});
