#!/usr/bin/env python3
"""Check this public copy against the P2 freeze manifest (FREEZE_MANIFEST.json). No network.

Every file present here that the manifest lists must hash the same, except the post-freeze edits
logged in DEVIATIONS.md. Files the public copy leaves out on purpose (SWE-CI upstream code in
tasks/sweci-*/{base,variants}, results/, the developer notes) are counted, not failed; rebuild the
SWE-CI workspaces with scripts/build_sweci_pilot*.py and they become checkable too.
Usage: verify_freeze.py   (exit 1 if a present file differs and is not a logged deviation)
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Post-freeze edits recorded in DEVIATIONS.md (D1, D2, D4).
DEVIATIONS = {"scripts/analyze_p3.py": "D1", "scripts/audit_process_access.py": "D2",
              "harness/run_agy.py": "D4", "harness/run_codex.py": "D4"}


def main() -> int:
    files = json.loads((ROOT / "FREEZE_MANIFEST.json").read_text())["files"]
    same, logged, bad, absent = 0, [], [], 0
    for rel, digest in files.items():
        path = ROOT / rel
        if not path.is_file():
            absent += 1
        elif hashlib.sha256(path.read_bytes()).hexdigest() == digest:
            same += 1
        elif rel in DEVIATIONS:
            logged.append(f"{rel} ({DEVIATIONS[rel]})")
        else:
            bad.append(rel)
    print(f"manifest: {len(files)} files; identical {same}; changed per DEVIATIONS.md {len(logged)}; "
          f"not in this copy {absent}; unexpected changes {len(bad)}")
    for line in logged + [f"UNEXPECTED {r}" for r in bad]:
        print("  " + line)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
