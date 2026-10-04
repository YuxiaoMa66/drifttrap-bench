"""Merge raw search results, deduplicate, and flag overlap with prior records (PROTOCOL §5.4).

Usage: python3 merge.py <rawdir>   -> writes <rawdir>/merged.json and ../search-log.csv
Dedup key: arXiv id when present, else normalised title; GitHub/HF ids stay separate records
unless their title matches a paper (repos and papers are linked later, at full-text screening).
"""
import csv, json, os, re, sys

RAW = sys.argv[1]
SR = os.path.dirname(os.path.abspath(RAW))
LIT = os.path.dirname(SR)

norm = lambda t: re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()

raw = json.load(open(os.path.join(RAW, "raw.json")))
raw["ACLAnthology"] = json.load(open(os.path.join(RAW, "acl_raw.json")))
log = json.load(open(os.path.join(RAW, "log.json"))) + json.load(open(os.path.join(RAW, "acl_log.json")))

# Prior records: literature matrix (urls/titles) + resources reviewed in TEST_PLAN_NEXT.
prior_titles, prior_ids = set(), set()
for r in csv.DictReader(open(os.path.join(LIT, "matrix.csv"))):
    prior_titles.add(norm(r["title"]))
    if m := re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", r["url"]):
        prior_ids.add("arxiv:" + m.group(1))
plan = open(os.path.join(os.path.dirname(LIT), "research", "TEST_PLAN_NEXT.md")).read()
prior_ids |= {"arxiv:" + a for a in re.findall(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", plan)}
prior_ids |= {"arxiv:" + a for a in re.findall(r"arXiv (\d{4}\.\d{4,5})", plan)}
prior_ids |= {"gh:" + g.lower() for g in re.findall(r"github\.com/([\w.-]+/[\w.-]+)", plan)}

merged, by_title = {}, {}
n_raw = 0
for source, items in raw.items():
    for it in items:
        n_raw += 1
        key = it["id"]
        nt = norm(it["title"])
        if not key.startswith(("gh:", "hf:")) and nt in by_title:
            key = by_title[nt]
        rec = merged.setdefault(key, dict(id=key, title=it["title"], year=it.get("year"), url=it.get("url"), abstract="",
                                          sources=[], groups=[], license=it.get("license"), venue=it.get("venue")))
        rec["sources"] = sorted(set(rec["sources"]) | {source})
        rec["groups"] = sorted(set(rec["groups"]) | {it["group"]})
        if len(it.get("abstract") or "") > len(rec["abstract"]):
            rec["abstract"] = it["abstract"]
        if not key.startswith(("gh:", "hf:")):
            by_title.setdefault(nt, key)

for r in merged.values():
    r["prior"] = "yes" if (r["id"] in prior_ids or norm(r["title"]) in prior_titles) else ""

json.dump(list(merged.values()), open(os.path.join(RAW, "merged.json"), "w"), ensure_ascii=False, indent=1)
with open(os.path.join(SR, "search-log.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["date", "source", "group", "query", "total_hits", "screened", "note"])
    w.writeheader()
    w.writerows(log)
print(f"raw={n_raw} unique={len(merged)} prior_overlap={sum(1 for r in merged.values() if r['prior'])}")
