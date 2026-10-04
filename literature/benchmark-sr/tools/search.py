"""Run the PROTOCOL.md §5 searches and save raw results + search-log rows.

Usage: python3 search.py <outdir>
Sources: arXiv API, Semantic Scholar Graph API, OpenReview API v2, GitHub search (gh), HF datasets API.
ACL Anthology is matched locally by acl.py from the official bib export.
"""
import json, os, subprocess, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import date

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
TODAY = date.today().isoformat()

# PROTOCOL §5.2, rewritten per source. Boolean sources get the full string.
ARXIV = {
    "G1": '(abs:"agent memory" OR abs:"long-term memory" OR abs:"memory system" OR abs:"conversational memory") AND (abs:stale OR abs:outdated OR abs:obsolete OR abs:superseded OR abs:"knowledge update" OR abs:"conflict resolution" OR abs:invalidation OR abs:forgetting) AND (abs:benchmark OR abs:dataset OR abs:evaluation)',
    "G2": '(abs:code OR abs:API OR abs:library OR abs:repository) AND (abs:version OR abs:evolution OR abs:deprecated OR abs:"breaking change" OR abs:update OR abs:drift) AND (abs:benchmark OR abs:dataset) AND (abs:LLM OR abs:agent)',
    "G3": '(abs:"multi-session" OR abs:continual OR abs:"long-horizon" OR abs:"cross-session" OR abs:sequential) AND (abs:"coding agent" OR abs:"software engineering agent" OR abs:"SWE-bench") AND abs:benchmark',
    "G4": '(abs:documentation OR abs:configuration OR abs:specification OR abs:README) AND (abs:drift OR abs:inconsistency OR abs:outdated OR abs:stale) AND (abs:LLM OR abs:agent) AND (abs:benchmark OR abs:dataset)',
}
DATE = " AND submittedDate:[202301010000 TO 202609232359]"
# Keyword sources (no boolean): one representative string per group, recorded verbatim.
KW = {
    "G1": "agent memory stale outdated knowledge update conflict benchmark",
    "G2": "LLM code API library version evolution deprecated benchmark",
    "G3": "multi-session continual coding agent software engineering benchmark",
    "G4": "LLM documentation configuration drift outdated inconsistency benchmark",
}
GH = {
    "G1": ["agent memory benchmark stale", "memory benchmark conflict resolution llm", "memory benchmark knowledge update agent"],
    "G2": ["llm api version benchmark", "code library evolution benchmark llm", "deprecated api llm benchmark"],
    "G3": ["multi-session coding agent benchmark", "continual learning swe-bench", "long-horizon coding agent benchmark"],
    "G4": ["documentation drift llm benchmark", "outdated documentation code llm dataset", "configuration drift llm agent"],
}
HF = {
    "G1": ["memory-bench", "memoryagentbench", "conflict", "knowledge-update", "longmem"],
    "G2": ["api-update", "version", "deprecat", "code-evolution", "library-version"],
    "G3": ["swe-bench", "multi-session", "continual"],
    "G4": ["documentation", "doc-drift", "config"],
}

log, raw = [], {}


CACHE = os.path.join(OUT, "cache")
os.makedirs(CACHE, exist_ok=True)


def get(url, tries=8):
    # curl, not urllib: export.arxiv.org answers urllib's multi-term queries with 406.
    # Each successful response is cached so a rate-limited run can resume without re-querying.
    import hashlib
    path = os.path.join(CACHE, hashlib.sha256(url.encode()).hexdigest()[:20])
    if os.path.exists(path):
        return open(path, "rb").read()
    for i in range(tries):
        r = subprocess.run(["curl", "-s", "-A", "gmr-sr/1.0", "-w", "\n%{http_code}", url], capture_output=True)
        body, code = r.stdout.rsplit(b"\n", 1)
        if code == b"200":
            open(path, "wb").write(body)
            return body
        if code == b"429" and i < tries - 1:
            time.sleep(min(20 * 2 ** i, 300))
            continue
        raise RuntimeError(f"HTTP {code.decode()} for {url}")


def rec(source, group, query, total, items, note=""):
    log.append(dict(date=TODAY, source=source, group=group, query=query, total_hits=total, screened=len(items), note=note))
    raw.setdefault(source, []).extend(dict(group=group, **it) for it in items)


# arXiv
ns = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/"}
for g, q in ARXIV.items():
    q2 = q + DATE
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(dict(search_query=q2, sortBy="relevance", max_results=100))
    root = ET.fromstring(get(url))
    total = int(root.find("o:totalResults", ns).text)
    items = [dict(id="arxiv:" + e.find("a:id", ns).text.rsplit("/abs/", 1)[1].split("v")[0],
                  title=" ".join(e.find("a:title", ns).text.split()),
                  year=e.find("a:published", ns).text[:4],
                  url=e.find("a:id", ns).text,
                  abstract=" ".join(e.find("a:summary", ns).text.split()))
             for e in root.findall("a:entry", ns)]
    rec("arXiv", g, q2, total, items)
    time.sleep(4)

# OpenAlex (replaces Semantic Scholar: S2 answered HTTP 429 to every unauthenticated request on
# 2026-09-23 for ~10 min / 7 retries; see PROTOCOL.md §10 amendment 1).
def oa_abstract(inv):
    if not inv:
        return ""
    pos = sorted((i, w) for w, idx in inv.items() for i in idx)
    return " ".join(w for _, w in pos)


for g, q in KW.items():
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": q, "filter": "from_publication_date:2023-01-01", "per-page": 100, "mailto": "gmr-sr@example.invalid"})
    d = json.loads(get(url))
    items = []
    for w in d.get("results", []):
        ax = next((l["landing_page_url"].rsplit("/abs/", 1)[1].split("v")[0] for l in (w.get("locations") or [])
                   if (l.get("landing_page_url") or "").startswith(("http://arxiv.org/abs/", "https://arxiv.org/abs/"))), None)
        items.append(dict(id=("arxiv:" + ax) if ax else "oa:" + w["id"].rsplit("/", 1)[1], title=w.get("title") or "",
                          year=str(w.get("publication_year")), url=w.get("doi") or w["id"],
                          venue=((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                          abstract=oa_abstract(w.get("abstract_inverted_index"))))
    rec("OpenAlex", g, q + " | from_publication_date:2023-01-01", d["meta"]["count"], items)
    time.sleep(1)
log.append(dict(date=TODAY, source="SemanticScholar", group="-", query="-", total_hits=None, screened=0,
                note="未认证请求持续 HTTP 429（约10分钟、7次指数退避），按 PROTOCOL §10 修订1 以 OpenAlex 替代"))

# OpenReview
for g, q in KW.items():
    url = "https://api2.openreview.net/notes/search?" + urllib.parse.urlencode(dict(term=q, limit=50, source="forum"))
    d = json.loads(get(url))
    items = []
    for n in d.get("notes", []):
        c = n.get("content", {})
        val = lambda k: (c.get(k) or {}).get("value", "") if isinstance(c.get(k), dict) else (c.get(k) or "")
        items.append(dict(id="or:" + n["id"], title=val("title"), year=time.strftime("%Y", time.gmtime((n.get("cdate") or 0) / 1000)),
                          url="https://openreview.net/forum?id=" + n["id"], venue=val("venue"), abstract=val("abstract")))
    rec("OpenReview", g, q, d.get("count"), items)
    time.sleep(2)

# GitHub (authenticated via gh)
for g, qs in GH.items():
    for q in qs:
        out = subprocess.run(["gh", "api", "-X", "GET", "search/repositories", "-f", f"q={q} created:>=2023-01-01", "-f", "per_page=50"],
                             capture_output=True, text=True, check=True).stdout
        d = json.loads(out)
        items = [dict(id="gh:" + r["full_name"].lower(), title=r["full_name"], year=r["created_at"][:4], url=r["html_url"],
                      abstract=r.get("description") or "", license=(r.get("license") or {}).get("spdx_id"), stars=r["stargazers_count"])
                 for r in d["items"]]
        rec("GitHub", g, q + " created:>=2023-01-01", d["total_count"], items)
        time.sleep(3)

# Hugging Face datasets
for g, qs in HF.items():
    for q in qs:
        d = json.loads(get("https://huggingface.co/api/datasets?" + urllib.parse.urlencode(dict(search=q, limit=50, full="true"))))
        items = [dict(id="hf:" + x["id"].lower(), title=x["id"], year=(x.get("createdAt") or "")[:4], url="https://huggingface.co/datasets/" + x["id"],
                      abstract=(x.get("description") or (x.get("cardData") or {}).get("pretty_name") or "")[:400]) for x in d]
        rec("HuggingFace", g, "search=" + q, None, items, note="HF API 不返回总数；已返回数即命中数（上限50）")
        time.sleep(1)

log.append(dict(date=TODAY, source="PapersWithCode", group="-", query="-", total_hits=None, screened=0,
                note="paperswithcode.com 跳转到 huggingface.co/papers/trending，服务已停止；按协议记为不可用"))
json.dump(raw, open(os.path.join(OUT, "raw.json"), "w"), ensure_ascii=False, indent=1)
json.dump(log, open(os.path.join(OUT, "log.json"), "w"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in raw.items()})
for r in log:
    print(r["source"], r["group"], r["total_hits"], r["screened"])
