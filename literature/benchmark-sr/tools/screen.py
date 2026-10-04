"""Title/abstract screening helper (PROTOCOL §7).

  python3 screen.py dump <rawdir> <batch> <size>   print a batch of merged records for screening
  python3 screen.py apply <rawdir> <decisions.tsv> write records.csv from recorded decisions

decisions.tsv: one line per record id -> "<id>\t<decision>\t<reason>", decision in {FT, EX};
FT means "go to full-text", EX must carry a reason code (E1..E6 or I1..I5 not met).
Every merged record must have exactly one decision; apply refuses otherwise.
"""
import csv, json, os, sys

cmd, RAW = sys.argv[1], sys.argv[2]
recs = json.load(open(os.path.join(RAW, "merged.json")))
recs.sort(key=lambda r: r["id"])

if cmd == "dump":
    b, n = int(sys.argv[3]), int(sys.argv[4])
    for r in recs[b * n:(b + 1) * n]:
        print(f'{r["id"]} | {r["year"]} | {",".join(r["sources"])} | {r["title"][:120]}')
        print("   ", (r["abstract"] or "")[:200].replace("\n", " "))
    print(f"-- batch {b}: {min((b + 1) * n, len(recs)) - b * n} of {len(recs)}")
elif cmd == "apply":
    dec = {}
    for line in open(sys.argv[3]):
        if line.strip() and not line.startswith("#"):
            i, d, why = (line.rstrip("\n").split("\t") + [""])[:3]
            assert i not in dec, f"duplicate decision {i}"
            assert d in ("FT", "EX") and (d == "FT" or why), f"bad decision {line!r}"
            dec[i] = (d, why)
    missing = [r["id"] for r in recs if r["id"] not in dec]
    extra = set(dec) - {r["id"] for r in recs}
    assert not missing and not extra, f"missing={missing[:5]}({len(missing)}) extra={list(extra)[:5]}"
    out = os.path.join(os.path.dirname(os.path.abspath(RAW)), "records.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "title", "year", "url", "sources", "groups", "prior", "ta_decision", "ta_reason", "ft_decision", "ft_reason"])
        for r in recs:
            d, why = dec[r["id"]]
            w.writerow([r["id"], r["title"], r["year"], r["url"], ";".join(r["sources"]), ";".join(r["groups"]), r["prior"], d, why, "", ""])
    print(out, len(recs), sum(1 for d, _ in dec.values() if d == "FT"), "to full text")
