# GMR coordinate forms: regression candidates

Recorded as L1 regression cases rather than filed as issues (decision B11⑤). All measured on GMR 0.6.6 (`GMR-latest/target/release/gmr`) on 2026-09-24. Reproducing needs only a git repository and `gmr init`. The benchmark uses only the forms verified to work (`file://path#/pointer` for JSON fields, class-level `path#ClassName` for code).

## R1 `path#/json/pointer` is routed to the whole-file probe and then reports drift forever

- Reproduce: write `{"timeout":60,"mode":"prod"}` to `c/r.json`; `gmr anchor 'c/r.json#/timeout'` and `'c/r.json#/mode'`; change only timeout.
- Observed: both anchors are handed back with status `drifted`, diagnosis "path matched, name did not"; they stay handed back after the file is restored. `#timeout` and `#$.timeout` behave the same.
- Cause: the coordinate is routed to addr-map, whose `name` is the file name and never matches.
- Working form: `file://c/r.json#/timeout` (named with `--as`), which hands back only the key that changed (165/165 agreement on CAL in L1).
- Expected: a `#` coordinate that no probe can resolve by name should be refused at `anchor` time, not accepted silently.

## R2 `path#Class.method` is accepted but never resolved

- Reproduce: in a Python file, `gmr anchor 'repo/pynetbox/core/query.py#Request.__init__'`.
- Observed: `anchor` returns probe ast-map with `barren: false`, but the position has no `shape`; after any change to the repository the status is `absent` ("nothing there answered to any of file · name"), even when the method itself did not change.
- Contrast: `#Request` (the class) and `#RequestError` resolve normally and after drift report `signature-changed` and `logic-changed`.
- Expected: as R1, an unresolvable coordinate should be an error at `anchor` time.

## R3 A bare method name is ambiguous

- Reproduce: a file with both `Request.__init__` and `RequestError.__init__`; `gmr anchor 'repo/pynetbox/core/query.py#__init__'`.
- Observed: it resolves to one of them (here `Request.__init__`) with no hint that several candidates exist.
- Expected: report the number of candidates, or refuse.

## R4 `_` in an `--as` name becomes `-`

- Observed: `--as primary_region` yields the anchor name `primary-region`, and `gmr check` hands it back under the renamed name.
- Impact: a caller matching on the original name misses it (`detectors/gmr/detector` maps the names back). Path coordinates ignore `--as` and are named by the coordinate.

## R5 (semantics, not a defect) Hand-backs are sticky

- Once a `check` has seen a value differ from the baseline, it keeps being handed back even if the value returns; only `accept --baseline` clears it. L0's `tests/state_machine.rs` uses this as its reference model.
