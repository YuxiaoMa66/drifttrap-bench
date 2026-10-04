# Search protocol: evaluation resources on memory invalidation usable for evaluating GMR — English translation

> Translation of [PROTOCOL.md](PROTOCOL.md), which is authoritative (its SHA-256 before searching began is cited in REPORT.md). `literature/matrix.csv` and `research/TEST_PLAN_NEXT.md` are in the unpublished research package; the test plan is published as `protocol/v1/TEST_PLAN.md`.

Version 1.0 / 2026-09-23. This protocol was written **before** the search started. Any change after the search starts is appended to section 10 with its reason; records already screened are not re-judged.

Type: a systematic search in the style of a scoping review, reported per PRISMA-ScR. Search, screening and data extraction only; **no meta-analysis and no risk-of-bias (RoB) scoring**: the objects are evaluation resources, not intervention studies, so RoB 2 and ROBINS-I do not apply.

## 1. Why this search

The previous round of external material came from a few ad hoc keyword searches; the selection criteria were set while searching, and filtering by "how much does it look like GMR" was biased towards the conclusion that "nothing existing fits". This protocol separates **inclusion** (does the resource measure memory invalidation) from **fit** (can it be used to test GMR): inclusion ignores GMR; fit is graded after inclusion by the fixed rules of section 6.

## 2. Research questions

**Main question:** among public evaluation resources (benchmarks, datasets, test suites, evaluation protocols), which measure the behaviour of LLMs or agents when previously obtained or stored information becomes invalid because the underlying facts changed? Which of them can be reused or adapted to evaluate GMR?

**Sub-questions:**

- SQ1: where does the invalidation happen — in conversation text, in external artifacts (code, files, APIs, databases), or in model parameters?
- SQ2: how are they graded, are they public, under what licence, and is the best score already near the ceiling?
- SQ3: does any resource let an external memory layer (adapter) be plugged in and compared side by side with other memory systems? This serves the later "GMR on top of memory systems" extension.

GMR background: GMR binds memories to probeable fact coordinates (code AST, file or JSON paths, HTTP, SQL) and hands a memory back for review when its coordinate changes. It neither stores nor retrieves memory content.

## 3. Inclusion criteria (all must hold)

| ID | Criterion |
|---|---|
| I1 | **Resource type:** proposes or releases an evaluation resource (tasks, dataset, test suite or evaluation protocol) and describes how tasks are built. Papers that only evaluate their own method on existing benchmarks are not included, but the benchmarks they use are traced |
| I2 | **Construct:** at least one task condition satisfies one of: (a) information given or stored earlier later becomes outdated, superseded, overturned or invalid; (b) code, APIs, libraries, configuration or repositories evolve over time so that earlier knowledge is no longer correct |
| I3 | **Object:** LLMs, LLM agents, or memory systems used by LLMs |
| I4 | **Time:** 2023-01-01 to the search date (2026-09-23) |
| I5 | **Language:** English or Chinese |

## 4. Exclusion criteria (any one excludes)

| ID | Criterion |
|---|---|
| E1 | measures only static retrieval or recall, with no condition that changes over time |
| E2 | measures only temporal reasoning over fixed facts (date arithmetic, event ordering), with no information update |
| E3 | non-LLM objects (classical IR, human studies) |
| E4 | no primary source (only a blog, marketing page or social-media post) |
| E5 | **parametric knowledge-editing** benchmarks outside the code/API domain (e.g. CounterFact, zsRE, which only change model weights). Reason: GMR acts on external memory, a different construct from editing weights. **Knowledge-editing benchmarks in the code/API domain are not excluded**, because their API changes can serve as artifact-drift material |
| E6 | duplicates or other versions of the same resource: merged into one record, keeping the latest official version |

## 5. Search strategy

### 5.1 Sources

| Source | Access | Screening cap per query |
|---|---|---|
| arXiv | official API (`export.arxiv.org/api/query`), relevance order | top 100 |
| Semantic Scholar | Graph API `/paper/search` | top 100 |
| OpenReview | site search (ICLR/NeurIPS/COLM 2024–2026) | top 50 |
| ACL Anthology | site search | top 50 |
| GitHub | search API (`/search/repositories`, best match) | top 50 |
| Hugging Face Datasets | Hub API (`/api/datasets?search=`) | top 50 |
| Papers with Code | shut down in 2025, data moved to Hugging Face. Check its status first; if unavailable, record "unavailable" and do not substitute another source to pad the numbers | — |

Total hits are recorded as each source returns them. Screening only the top N is **deliberate truncation**, reported as a limitation. No claim of exhaustiveness.

### 5.2 Queries (four groups, rewritten per source syntax; every rewritten query logged verbatim in search-log)

- **G1 memory invalidation:** (`agent memory` OR `long-term memory` OR `memory system` OR `conversational memory`) AND (`stale` OR `outdated` OR `obsolete` OR `superseded` OR `knowledge update` OR `conflict resolution` OR `invalidation` OR `forgetting`) AND (`benchmark` OR `dataset` OR `evaluation`)
- **G2 code evolution:** (`code` OR `API` OR `library` OR `repository`) AND (`version` OR `evolution` OR `deprecated` OR `breaking change` OR `update` OR `drift`) AND (`benchmark` OR `dataset`) AND (`LLM` OR `agent`)
- **G3 multi-session coding:** (`multi-session` OR `continual` OR `long-horizon` OR `cross-session` OR `sequential`) AND (`coding agent` OR `software engineering agent` OR `SWE-bench`) AND `benchmark`
- **G4 documentation and configuration drift:** (`documentation` OR `configuration` OR `specification` OR `README`) AND (`drift` OR `inconsistency` OR `outdated` OR `stale`) AND (`LLM` OR `agent`) AND (`benchmark` OR `dataset`)

### 5.3 Snowballing

For included resources graded A or B, one round of backward search (their references) and one of forward search (works citing them on Semantic Scholar). **Stopping rule:** a round of snowballing that adds no new included record. If new records are still added after two rounds, stop after the second and report "not saturated".

### 5.4 De-duplication against earlier records

De-duplicate first against `literature/matrix.csv` (28 records) and sections 1–2 of the test plan. Resources reviewed before are screened again under this protocol's criteria; earlier conclusions are not carried over.

## 6. Data extraction and fit grading (included records only)

| Field | Values |
|---|---|
| D1 where invalidation happens | conversation text / external artifact (code, file, API, database) / model parameters / mixed |
| D2 can GMR probe the artifact | yes (code AST, file or JSON, HTTP, SQL) / partly / no |
| D3 grading | executable tests / exact match / LLM judge / human |
| D4 availability | code and data / data only / paper only |
| D5 licence | recorded verbatim; none recorded as "none" |
| D6 interaction | multi-turn agent / single turn |
| D7 can an external memory layer be plugged in | has an adapter interface / needs adapting / no |
| D8 publication | peer-reviewed / preprint / code repository only |
| D9 ceiling risk | best reported score; ≥ 90% flagged high |

**Fit grades (written before seeing any search result):**

- **A, usable directly as the main experiment:** D1 external artifact, D2 yes, D3 executable tests, D4 code and data, D5 permissive (MIT, Apache, BSD, ISC, CC-BY).
- **B, usable as material or a component:** meets part of A and at least one of: D1 external artifact; D7 has an adapter interface; D3 executable tests with D5 permissive.
- **C, appendix or scope statement:** D1 conversation text or mixed, D4 at least data, D5 allows use.
- **D, cite only:** none of the above (including D4 paper only, or D5 none).

## 7. Screening process

1. **Title and abstract screening** against I1–I5 and E1–E6; anything uncertain goes to full text.
2. **Full-text screening:** for papers, the abstract, the task-construction part of the method, and the data-availability statement; for repositories, the README, data samples and LICENSE.
3. Each record gets a verdict and a reason code (e.g. `E1`, `I2 not met`).

**Screener:** a single screener (Claude). This is one of the main limitations. Mitigation: all exclusion reasons are published; after all screening, a random 20% of exclusions is re-screened by the same screener **blind to the original verdict**, and agreement is reported. This measures only self-consistency and cannot replace an independent second screener; the owner or another person may review if needed.

## 8. Output files (directory `literature/benchmark-sr/`)

| File | Content |
|---|---|
| `PROTOCOL.md` | this file |
| `search-log.csv` | date, source, query group, actual query, total hits, number screened, notes |
| `records.csv` | every de-duplicated record: ID, title, year, URL, source, overlap with earlier records, title/abstract verdict, full-text verdict, reason code |
| `extraction.csv` | D1–D9 and fit grade of each included record |
| `REPORT.md` | PRISMA-ScR flow counts, results per sub-question, limitations, and the impact on the test plan |

## 9. Protocol self-check (Devil's Advocate checkpoint 1)

| Risk | Handling |
|---|---|
| construct I2 is broad and will include many conversational "knowledge update" benchmarks | intended: include broadly and grade fit, which is the only way to answer "why not use an existing one" |
| E5 excludes parametric knowledge editing and may be questioned as cherry-picking | REPORT states the number of E5 exclusions and typical examples separately |
| relevance-order truncation per source will miss records | mitigated by snowballing; the truncation caps are reported |
| single screener | see section 7; reported as a limitation |
| many preprints of uneven quality | D8 recorded separately; preprints are not excluded for that, but are labelled |
| the conclusion may still be "build our own" | acceptable, as long as it follows from the rules of section 6; if an A-grade resource appears, the test plan must change |
| Chinese databases (CNKI etc.) are not accessible | reported as a limitation; Chinese authors' work is covered only through the English sources |

## 10. Amendments

(Changes after the search started are appended here.)

### Amendment 1 (2026-09-23, during the search)

- **Semantic Scholar → OpenAlex.** The S2 Graph API kept returning HTTP 429 to unauthenticated requests (7 exponential back-offs in about 10 minutes, plus one manual request also 429), so no results could be obtained. Replaced by OpenAlex `/works?search=`: the same queries as for S2, limited to `from_publication_date:2023-01-01`, top 100 screened. The forward and backward snowballing of section 5.3 also use OpenAlex (`referenced_works`, `cites:`). Limitation: OpenAlex's relevance ranking is clearly weaker than S2's (in a test query the top result was unrelated), which may lower recall in the top 100.
- **How ACL Anthology was searched (implementation detail, criteria unchanged).** The official `anthology+abstracts.bib.gz` (2026-09-22 version, SHA-256 `dd753c17…373ad`) was downloaded and titles and abstracts were matched locally against the G1–G4 Boolean queries, allowing plural s; ranked by the number of distinct query terms matched, top 50 taken.
- These two changes were made before any screening, without having seen any verdict on search results.
- **OpenReview was searched differently from the protocol (recorded afterwards).** The protocol says "site search, limited to ICLR/NeurIPS/COLM 2024–2026"; what was actually used is the API v2 `/notes/search?term=…&source=forum`, without a venue limit; every group returned count=10000 (any-term match), top 50 taken. Effect: records from non-target venues may be mixed in; screening handles them; inclusion criteria unaffected.
- **GitHub and Hugging Face.** GitHub repository search requires all terms to appear, so each group's 3 queries returned 0–13 hits, all screened. HF's `search=` matches only substrings of dataset IDs, so words like `version` and `config` bring many unrelated results, which screening excludes.
