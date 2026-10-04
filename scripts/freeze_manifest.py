#!/usr/bin/env python3
"""Freeze manifest for a preregistered run. No model calls, no network.

Hashes everything a result depends on: your preregistration text, tasks/ and oracles/, the harness, arm
assembly, detectors, run/analysis scripts, L1 scripts, the detectors' reported versions and tool versions.
Writes the manifest and prints its sha256, the single digest to timestamp (e.g. `ots stamp <manifest>`).
The v1 manifest, made by the earlier version of this script, is protocol/v1/FREEZE_MANIFEST.json.
Usage: freeze_manifest.py --prereg FILE --out FILE [--detector NAME ...] [--check]
       (--check: recompute and compare with the existing --out manifest)
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
TREES = ["tasks", "oracles", "harness", "arms", "detectors", "scripts", "i18n", "l1/run_l1.py", "l1/over_handback.py"]
SKIP = {"__pycache__", ".DS_Store"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree(root: Path) -> dict[str, str]:
    paths = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())
    return {str(p.relative_to(BENCH)): sha(p) for p in paths if not SKIP & set(p.parts)}


def version(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"unavailable: {e}"


def manifest(prereg: Path, detectors: list[str]) -> dict:
    files = {}
    for t in TREES:
        if (BENCH / t).exists():
            files.update(tree(BENCH / t))
    files[str(prereg.resolve().relative_to(BENCH))] = sha(prereg)
    return {
        "schema": "drifttrap-freeze.v2",
        "detectors": {d: version([str(BENCH / "detectors" / d / "detector"), "info"]) for d in detectors},
        "tools": {"codex": version(["codex", "--version"]), "agy": version(["agy", "--version"]),
                  "agy-mc": version(["agy-mc", "--version"]), "python": sys.version.split()[0]},
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--prereg", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--detector", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    m = manifest(args.prereg, args.detector)
    if args.check:
        old = json.loads(args.out.read_text())
        diff = sorted(k for k in set(old["files"]) | set(m["files"]) if old["files"].get(k) != m["files"].get(k))
        print(f"changed files: {len(diff)}", *diff[:20], sep="\n")
        return 0 if not diff and old["detectors"] == m["detectors"] else 1
    text = json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    args.out.write_text(text)
    print(f"{len(m['files'])} files; manifest sha256 {hashlib.sha256(text.encode()).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
