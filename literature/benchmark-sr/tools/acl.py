"""Match the PROTOCOL §5.2 boolean groups against the ACL Anthology bib export (title + abstract).

Usage: python3 acl.py <anthology+abstracts.bib.gz> <outdir>
The export has no relevance ranking, so hits are ranked by the number of distinct query terms
matched (ties: newer first) and the top 50 per group are screened, per PROTOCOL §5.1.
"""
import gzip, json, os, re, sys
from datetime import date

src, out = sys.argv[1], sys.argv[2]
# Each group is AND over OR-blocks; terms are matched case-insensitively as whole words/phrases.
G = {
    "G1": [["agent memory", "long-term memory", "memory system", "conversational memory"],
           ["stale", "outdated", "obsolete", "superseded", "knowledge update", "conflict resolution", "invalidation", "forgetting"],
           ["benchmark", "dataset", "evaluation"]],
    "G2": [["code", "API", "library", "repository"],
           ["version", "evolution", "deprecated", "breaking change", "update", "drift"],
           ["benchmark", "dataset"], ["LLM", "agent"]],
    "G3": [["multi-session", "continual", "long-horizon", "cross-session", "sequential"],
           ["coding agent", "software engineering agent", "SWE-bench"], ["benchmark"]],
    "G4": [["documentation", "configuration", "specification", "README"],
           ["drift", "inconsistency", "outdated", "stale"], ["LLM", "agent"], ["benchmark", "dataset"]],
}
# Optional plural "s" so "LLM" matches "LLMs", as arXiv's stemmed search would.
pat = {t: re.compile(r"(?<![\w-])" + re.escape(t) + r"s?(?![\w-])", re.I) for g in G.values() for blk in g for t in blk}

text = gzip.open(src, "rt", encoding="utf-8", errors="replace").read()
entries = re.split(r"\n@", text)
papers = []
for e in entries:
    y = re.search(r'\byear\s*=\s*"(\d{4})"', e)
    if not y or int(y.group(1)) < 2023:
        continue
    key = e.split("{", 1)[1].split(",", 1)[0] if "{" in e else ""
    t = re.search(r'\btitle\s*=\s*"(.*?)",\s*\n', e, re.S)
    # abstract is usually the last field, closed by `"\n}` rather than `",\n`
    a = re.search(r'\babstract\s*=\s*"(.*?)"\s*(?:,\s*\n|\n?}|$)', e, re.S)
    u = re.search(r'\burl\s*=\s*"(.*?)"', e)
    papers.append(dict(key=key, year=y.group(1), title=" ".join((t.group(1) if t else "").split()).replace("{", "").replace("}", ""),
                       abstract=" ".join((a.group(1) if a else "").split()), url=u.group(1) if u else ""))

log, raw = [], []
for g, blocks in G.items():
    hits = []
    for p in papers:
        s = (p["title"] + " " + p["abstract"]).replace("{", "").replace("}", "")
        matched = [[t for t in blk if pat[t].search(s)] for blk in blocks]
        if all(matched):
            hits.append((sum(len(m) for m in matched), p["year"], p))
    hits.sort(key=lambda h: (h[0], h[1]), reverse=True)
    top = hits[:50]
    raw += [dict(group=g, id="acl:" + p["key"], title=p["title"], year=p["year"], url=p["url"], abstract=p["abstract"]) for _, _, p in top]
    q = " AND ".join("(" + " OR ".join(blk) + ")" for blk in blocks)
    log.append(dict(date=date.today().isoformat(), source="ACLAnthology", group=g, query=q + " | title+abstract, year>=2023",
                    total_hits=len(hits), screened=len(top), note="本地匹配官方 anthology+abstracts.bib.gz；按匹配词数排序取前50"))
    print(g, len(hits))
os.makedirs(out, exist_ok=True)
json.dump(raw, open(os.path.join(out, "acl_raw.json"), "w"), ensure_ascii=False, indent=1)
json.dump(log, open(os.path.join(out, "acl_log.json"), "w"), ensure_ascii=False, indent=1)
print("papers>=2023:", len(papers))
