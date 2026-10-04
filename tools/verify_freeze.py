#!/usr/bin/env python3
"""Check the v1 protocol against its freeze manifest (protocol/v1/FREEZE_MANIFEST.json). No network.

Reads files straight from the git tag (default v1.0-frozen), so it works from any checkout, main included.
Every file the tag holds that the manifest lists must hash the same, except the post-freeze edits logged in
protocol/v1/DEVIATIONS.md. Files the public repository never held (SWE-CI upstream code in
tasks/sweci-*/{base,variants}, results/, the developer notes) are counted, not failed.
Usage: verify_freeze.py [--ref TAG]   (exit 1 if a file differs and is not a logged deviation)
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Post-freeze edits recorded in DEVIATIONS.md (D1, D2, D4).
DEVIATIONS = {"scripts/analyze_p3.py": "D1", "scripts/audit_process_access.py": "D2",
              "harness/run_agy.py": "D4", "harness/run_codex.py": "D4"}


def blobs(ref: str) -> dict[str, bytes]:
    """path -> content of every file in `ref`, via one `git cat-file --batch`."""
    paths = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", ref],
                           capture_output=True, text=True, check=True).stdout.splitlines()
    proc = subprocess.run(["git", "-C", str(ROOT), "cat-file", "--batch"], check=True, capture_output=True,
                          input="".join(f"{ref}:{p}\n" for p in paths).encode())
    out, data, i = {}, proc.stdout, 0
    for p in paths:
        header_end = data.index(b"\n", i)
        size = int(data[i:header_end].split()[2])
        out[p] = data[header_end + 1:header_end + 1 + size]
        i = header_end + 1 + size + 1
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ref", default="v1.0-frozen")
    files_at_ref = blobs(parser.parse_args().ref)
    manifest = json.loads(files_at_ref["FREEZE_MANIFEST.json"])["files"]
    same, logged, bad, absent = 0, [], [], 0
    for rel, digest in manifest.items():
        if rel not in files_at_ref:
            absent += 1
        elif hashlib.sha256(files_at_ref[rel]).hexdigest() == digest:
            same += 1
        elif rel in DEVIATIONS:
            logged.append(f"{rel} ({DEVIATIONS[rel]})")
        else:
            bad.append(rel)
    print(f"manifest: {len(manifest)} files; identical {same}; changed per DEVIATIONS.md {len(logged)}; "
          f"not in the repository {absent}; unexpected changes {len(bad)}")
    for line in logged + [f"UNEXPECTED {r}" for r in bad]:
        print("  " + line)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
