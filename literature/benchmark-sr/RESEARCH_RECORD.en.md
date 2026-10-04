# Detailed research record: collecting, reviewing, verifying and systematically searching evaluation resources for GMR — English translation

> Translation of [RESEARCH_RECORD.md](RESEARCH_RECORD.md), which is authoritative. "The owner" is the benchmark's author. Paths outside `literature/benchmark-sr/` refer to the unpublished research package; the test plan is published as `protocol/v1/TEST_PLAN.md` ([English](../../protocol/v1/TEST_PLAN.en.md)).

Recorded 2026-09-23 (all work done the same day across two sessions). Done by Claude (Anthropic) with the owner's step-by-step authorisation.
This is a **process record**: in time order, what was done at each step, on what basis, how deeply each source was read, what was concluded, and what was later corrected. Conclusions are in [REPORT.md](REPORT.en.md) and the test plan.

How to read: every stage has action / evidence / conclusion / limitation. **Whatever is listed under "limitation" must not be presented in the paper as completed work.**

---

## Stage 0: starting point and the owner's question

- Owner's question 1: "Are there more authoritative tests for my GMR, or tests already shared on GitHub, that I can reuse or learn from?"
- Existing test assets (checked locally):
  - `GMR工程级测试套件` (engineering test suite): 38 black-box tests pinned to v0.2.3/v0.3.3; its `docs/研究依据.md` already lists nextest, llvm-cov, proptest, cargo-fuzz, SQLite testing practice, MCP Conformance, etc.
  - `GMR-v0.3.4-P03-Gemini-Benchmark`: 12 P03 stale-memory conflict cases, 11 models × 12 × 2 arms, ON 83.64 / OFF 62.20.
  - `GMR-Agent-Memory-Benchmark-Latest-20260826`: GMR ON/OFF on Hindsight's AMB (agentmemorybenchmark.ai), v0.4.6, 61 tasks × 2 models × 2 arms, both arms 100% solved.
  - `GMR-Paper-Research-20260922/literature`: 28 literature records (matrix.csv); its search log says "not saturated".

---

## Stage 1: ad hoc search (not systematic)

**Nature:** keyword searches as needed; **selection criteria were set while searching, and filtering was by "how much does it look like GMR"**. The owner then pointed this out, which led to the systematic search of stage 5. Conclusions of this stage are leads only, not an evidence base for the paper.

### 1.1 Searches used (WebSearch, US region)

| # | Query |
|---|---|
| 1 | `MemoryAgentBench conflict resolution github benchmark agent memory` |
| 2 | `CodeUpdateArena GitChameleon API version drift benchmark github` |
| 3 | `benchmark stale memory coding agent repository evolution multi-session SWE-bench continual github 2026` |
| 4 | `"Invalidation Contracts for Cross-Episode Agent Memory" code github` |
| 5 | `"When Stale Constraints Go Unchecked" inherited agent memory benchmark code release` |
| 6 | `MemoryCode multi-session coding benchmark github instructions across sessions` |
| 7 | `SWE-CI benchmark github continuous integration maintainability agent 100 tasks` (added during stage 3 verification) |

### 1.2 Pages fetched (WebFetch, abstracts or READMEs only)

The REVOKE repository, the coding-agent-memory-benchmark repository, the GiulioDER/agent-memory-bench repository; arXiv abstract pages 2605.06527 (STALE), 2507.00014 (SWE-Bench-CL), 2603.03823 (SWE-CI), 2607.02606 (ChainSWE), 2608.25553 (Stale Constraints), 2602.16313 (MemoryArena); Zenodo record 22147784.

### 1.3 Repositories cloned and reviewed (shallow clones; README, task samples, grading code, LICENSE)

| Repository | Commit | Date | Licence | Review depth |
|---|---|---|---|---|
| GiulioDER/agent-memory-bench | `abd4e6bc153582a55dda62d9c4050d78a3cc3bdd` | 2026-09-21 | Apache-2.0 | full README; `tasks/xs-evolve-lease/task.json`; `tasks/ts-append-only/checker.py`; the `harness/adapters/base.py` interface; notes in `adapters/claude_md/adapter.py`; `docs/CAPABILITY_TRACKS.md`, `docs/LIFECYCLE_CAPABILITY.md`; the first probe in `capabilities/governance.json`; how `harness/claude_exec.py` calls the model |
| Dextergao14/REVOKE | `5c193339b4668c7a782d221c423fa5b5ec5b659b` | 2026-09-20 | **no LICENSE** | README; first 80 lines of `docs/GRADING.md`; first 1.5 KB of a data sample; structure of `revoke/logic.py` |
| HUST-AI-HYZ/MemoryAgentBench | `fe1735de8cf8b9908e1e3d3b5612afc815698062` | 2026-08-20 | MIT | the metrics table in the README |
| SaravananJaichandar/coding-agent-memory-benchmark | `b57d241d2f8c691e72a6c090acb59be35d40f597` | 2026-08-24 | MIT (paper CC-BY) | first 120 lines of DESIGN.md; the paragraphs on leakage and subsets in RESULTS.md |
| Cohere-Labs-Community/MemoryCode | `1ab87e119b2f9a498de8075219e1c07f6041b394` | 2025-04-25 | Apache-2.0 | README; first 1.2 KB of dataset/dialogue_1.json |
| mrcabbage972/GitChameleonBenchmark | `3a1b6045a6b2a276bd24d715589cb041f8eccb93` | 2026-04-17 | Apache-2.0 | first 50 lines of the README; the dataset directory |
| leo-liuzy/CodeUpdateArena | `836e2d157739fd53f9cde421913eb5949d4eeeb8` | 2025-03-20 | MIT | first 40 lines of the README; the data directory |
| thomasjoshi/agents-never-forget (SWE-Bench-CL) | `74a38a90baace25635f3827ee2f98caff24b3768` | 2025-05-17 | MIT | structure and fields of `data/SWE-Bench-CL-Curriculum.json` |
| SKYLENAGE-AI/SWE-CI | `b2a0620f0168a5a89681be7919a98d9a49ab22af` | 2026-06-10 | Apache-2.0 | first 80 lines of the README (ANC metric, running cost) |

### 1.4 Computations in this stage

- **Same-function task pairs in SWE-Bench-CL:** each repository's tasks sorted by `created_at`; `(file, function)` extracted from patch hunk headers; pairs of consecutive tasks touching the same function counted: 20 pairs, involving 16 later tasks (sphinx 12, xarray 4, django 2, matplotlib 1, pytest 1). **A heuristic count**: hunk headers name the context function and can be wrong.

### 1.5 Key findings of this stage

1. **agent-memory-bench's "staleness" happens in dialogue:** `xs-evolve-lease` gives 90/45/20 seconds in three dated sessions while the code does not change. GMR's probes cannot see such a change.
2. **P03's control design is flawed** (confirmed from source in stage 2, see 2.2).
3. **coding-agent-memory-benchmark has leakage:** the within-domain arm's 4 constraints come from baseline failures on the same subset (disclosed by the authors in RESULTS.md), and `test_patch` was applied on the checkout.

### 1.6 Statements later corrected

- In the known-item check "agent-memory-bench" was recorded as found, but the match was other repositories with the same name (jrosenbizzle, dakshjain, …); the GiulioDER repository was not retrieved. Corrected in stage 5.
- The first plan said "AMB ran out of quota after about 190 calls", which is inaccurate: the 189 valid records include reused earlier evidence. Changed to "55 of 244 conditions invalid because of quota".

---

## Stage 2: reviewing the owner's P03 v0.3.4

The owner asked to include the reference project and tests of the complete v0.3.4 study.

### 2.1 Files read

`README.md`, `docs/研究依据.md` (full), `docs/P03-v0.3.4-设计与执行协议.md` (first 140 lines), `docs/P03-v0.3.4-完整结果分析.md` (full), `docs/P03-v0.3.4-GMR技术设计分析与不足.md` (sections 5–10), `benchmark/p03-v034/cases/p03-h01/*`, `scripts/dispatch_subject.py` (lines 250–300), `scripts/harness.py` (lines 585–640), `NOTICE.md`.

### 2.2 Findings from the source

- `scripts/harness.py:594-627`:
  - in the acquisition phase the OFF arm also reads E01 (the historical constraint) but may not persist it;
  - the recovery phase uses a fresh agent, and the OFF arm's prompt has only E02, E03 and the repository: **it never sees the historical constraint**;
  - the ON arm's recovery prompt additionally says "Current repository evidence is authoritative" and asks to check two pieces of evidence.
- Conclusion: P03's +21.44 mixes three effects — having the memory, the extra instruction, and GMR's detection; `conflict_and_evidence` (15 points) is structurally unattainable for the OFF arm. AMB v0.4.6's OFF arm also had no memory.
- P03 mechanism diagnostics: read/check 100%, stale detected 94.7%, post-read consistent 50%, reconciliation failure 40.15%.
- `NOTICE.md`: the test suite itself had no public licence and was to stay private until one was chosen.

---

## Stage 3: verification before the plan

The owner asked to "finish verifying first, then give the detailed plan, test flow, framework and whether to use AMC".

| Item | Method | Result |
|---|---|---|
| SWE-CI data | listed `skylenage-ai/SWE-CI` files via the HF API; downloaded `metadata/{default,full,lite}.csv`; queried the sizes of `image.tar.gz` and `code.zip` | 100 pairs (full 226, lite 50); licences MIT 51, Apache 15, BSD 20, ISC 9, GPL/LGPL/mixed 5; images 266–356 MB |
| SWE-CI function-level drift | `tools/mine_sweci_drift.py`, 12 pairs drawn with fixed seed 7, shallow fetch of both commits, AST comparison of non-test `.py` files | 11 of 12 pairs have ≥ 2 signature changes; body-only changes 11–145; unchanged 69–2252 (in `research/tools/sweci_drift_sample12.json`) |
| Can agent-memory-bench use AMC | read `harness/claude_exec.py`, `.env.example`, `docs/REPLICATION.md` | no: it always calls `claude -p --output-format stream-json` through an Anthropic-compatible endpoint |
| Stale Constraints data | WebFetch of the Zenodo record | CC-BY-4.0, 61.5 MB, 5,400 episodes and a frozen specification; **not downloaded** |
| MemoryArena | WebFetch of the arXiv abstract | web, planning, search, formal reasoning; no code, no staleness; excluded |
| GMR anchoring dependency files | local `gmr 0.6.6` (`GMR-latest/target/release/gmr`) in a temporary git repository: anchor / change / check | `file://deps.json#$.deps.lib1` is handed back; `vendor/lib1/api.py#fetch` reports signature-changed; `.venv/...` cannot be parsed; in one operation an unopenable anchor left other notes unbound (not classified as a defect) |
| `gmr check --json` | as above | output has `handed_back[].anchor/status/memories` and more; parses directly |
| AMC status | read-only `agy-mc usage`, `agy-mc models` | quota 100%; Gemini 3.x, claude-sonnet-4-6, claude-opus-4-6-thinking, gpt-oss-120b available |
| AMC token records | counted in AMB's evidence `matrix-pilot-full37-reconciled-summary.json` | all 5,923 calls have input/output/thinking/cache/total tokens |
| GMR memory store support (added in stage 6) | read README section 8 and `batteries/provider/src/` | native: claude_code, git, http, local_file, mem0; mem0 supports cloud and self-hosted (list limit 1,000); other stores can declare a fetch script in `.anchor/providers.toml` |

**Decision confirmed by the owner:** AMC as the subject channel (plan v0.2 section 3).

---

## Stage 4: releasing, and "why not just use existing benchmarks"

- The owner asked whether to release and whether to describe it as a combined project. Advice given: release in phases, position it as a GMR evaluation, write a source table and licence compliance (advice only, no file written).
- The owner asked for the basis of the choices and why not simply run several benchmarks and compare. **The answer admitted that stage 1's choice came from ad hoc searching and that the criteria leaned towards "write our own".** Two follow-ups were proposed; the owner replied "do both, systematic search first".

---

## Stage 5: systematic search (details in PROTOCOL.md and REPORT.md)

### 5.1 Protocol registration

- [PROTOCOL.md](PROTOCOL.en.md) v1.0 written; SHA-256 before searching: `21e2e03b37575874804f05a215d441c2f1b821dc0271f8949738cd6133586f0f` (recorded in the work log).
- Core design: **inclusion looks only at "does it measure memory invalidation"; fit for GMR is an extraction field after inclusion, graded A–D by preset rules.**
- **Owner confirmed:** run the protocol as written; apply E5 (exclude weight-level knowledge editing outside code); state the single-screener limitation.

### 5.2 Search execution

| Source | Method | Hits / screened | Notes |
|---|---|---|---|
| arXiv | official API, 4 Boolean groups, 2023-01-01 to the search date | 395 | Python urllib got 406 for multi-word queries; curl used instead |
| Semantic Scholar | Graph API | 0 | persistent 429 for about 10 minutes; replaced by OpenAlex per amendment 1 |
| OpenAlex | `/works?search=`, from 2023 | 400 | weak relevance ranking, many unrelated papers |
| OpenReview | API v2 `/notes/search` | 200 | no venue limit, count=10000; old papers mixed in |
| ACL Anthology | downloaded the official `anthology+abstracts.bib.gz` (2026-09-22 version, SHA-256 `dd753c17fe34a46d8bc9e3076d59a90335589b86e3ff226c841e99205a7373ad`), local Boolean matching | 58 | the first parse found 0 hits because abstract was the last field, plus braces and plurals; fixed and rerun |
| GitHub | `gh api search/repositories`, 3 queries per group | 30 | all terms must appear, few hits |
| Hugging Face | Hub API `search=` (ID substring) | 443 | much name noise |
| Papers with Code | — | 0 | redirects to huggingface.co/papers/trending; service stopped |

- 1,526 records in total, 1,391 after de-duplication. Queries verbatim in [search-log.csv](search-log.csv); scripts `tools/search.py`, `tools/acl.py`, `tools/merge.py`.
- **Known-item recall:** 10 of 16 known resources found.

### 5.3 Title and abstract screening

- 19 batches (75 records each), every verdict and reason code recorded ([decisions.tsv](decisions.tsv) → [records.csv](records.csv)).
- Two rules established during screening and applied retroactively (both before the full-text stage):
  1. API-evolution method papers in the code domain may come with a new dataset, so they go to full text (4 records EX→FT).
  2. Hugging Face records with no data card and no linked paper are I1 (15 records FT→EX).
- Result: 166 to full text, 1,225 excluded (I2 654, I1 319, E6 107, I3 72, I4 49, E1 15, E5 9).

### 5.4 Full-text screening

- Papers: the complete abstract; repositories: README and LICENSE (17 GitHub READMEs saved in `archive/readmes/`); HF: the data card.
- Result: 95 included, 71 excluded (I1 34, I2 27, E6 6, I3 3, E2 1), details in [ft_decisions.tsv](ft_decisions.tsv).
- **Data problem recorded:** OpenAlex mislabelled the world-model-mcp paper as `arXiv:2310.06770` (which is actually SWE-bench); judged on the actual content.
- **Other routes, 7 records** ([other_methods.tsv](other_methods.tsv)): the 6 known items missed by the queries + BUMP (used by three method papers, Byam, BigBag and BreakGuard; added by citation tracing; `gh api repos/chains-project/bump` confirmed MIT). 5 included.

### 5.5 Data extraction

- Links extracted automatically from paper pages (GitHub, HF, Zenodo and anonymous repository links in arXiv HTML/abs, stored in `archive/arxiv_code_links.json`); where none was found, `gh search repos` by name (which later hit the search API rate limit).
- Licences: GitHub via `gh api repos/...` (`archive/licenses_github.tsv`), HF via the dataset API's `cardData.license`.
- D1–D9 filled from abstracts, READMEs and data cards; anything not stated is "unverified"; **fit grades are computed only by `tools/extract.py` from the protocol rules**.
- Protocol section 6, grade D "including D5 none": resources without a licence are always D; NOASSERTION and similar are "unclear", not automatically D.

### 5.6 Snowballing

- **Round 1:** OpenAlex has no reference lists for arXiv preprints (all refs=0), so backward tracing instead parsed the HTML reference entries of 17 A/B arXiv seeds. The first parse failed for 8 papers (0 entries) because of the multi-class `class="ltx_bibitem ltx_bib_article"`; after fixing the regex and refetching, 833 entries, 508 from 2023 on, 446 after de-duplication, 396 new; forward search via OpenAlex `cites:` for the 6 seeds with citations, 44 new. After title-level screening 12 went to full text and 8 were included. 14 references had only an arXiv id; titles were filled in from the arXiv abstract pages before judging.
- **Round 2:** of round 1's 8 new records only CoUpJava is B grade. Of its 28 references, only one was from 2023 on and not already recorded (a CHI EA 2024 study, I1); 0 citations. 0 new inclusions; stopping rule met.
- Records in [snowball.tsv](snowball.tsv), candidate titles in `archive/snowball/`.
- **Limitation:** the 428 records excluded in snowballing were judged at title level only, with coarser reason codes than the main screening.

### 5.7 Self-consistency check

- Fixed seed 20260923; 245 of the 1,225 exclusions drawn and re-judged with the original verdicts hidden.
- Include/exclude agreement 244/245; reason-code agreement 236/245. The single disagreement (DEAN, detecting outdated facts in knowledge graphs) got a full-text verdict and stayed excluded (I3).
- Data: [recheck_result.json](recheck_result.json), `archive/recheck/`.

### 5.8 Results

- 108 included in total (95 database, 5 other routes, 8 snowball).
- Fit grades (by the protocol rules): A 2 (SWE-CI, SWE-Bench-CL), B 31, C 23, D 52.
- One wrong citation corrected while writing the report: the draft used RoadmapBench, which had been excluded, as a ceiling reference; replaced by EvoArena.

---

## Stage 6: plan v0.3

- SWE-Bench-CL promoted to main material; ChainSWE added; closest related work added; new section 13 on the cross-memory-system extension.
- One overstatement corrected: the draft said "16 candidates can be used as traps directly"; changed to "a heuristic count that needs manual filtering".

---

## Stage 7: licence sensitivity analysis (the owner asked "would anything change if licences were ignored?")

- Method: keep every other rule, drop only the licence condition (`sensitivity_license.csv`).
- Result: A 3, B 41, C 27, D 37; 15 resources move up, all previously D for lack of a licence.
- Changes relevant to the plan: TestEvo-Bench D→A (real commits, executable, Python); EvoArena D→B (artifact change and memory); EditPropBench D→B (dependency propagation, file probe possible); REVOKE D→C.
- Conclusion unchanged: even ignoring licences, no resource combines "memory condition + artifact drift + executable grading".
- Boundary of use: internal tests may read and run these public repositories; releasing a derived benchmark needs permission first, or release only "original repository URL + commit + conversion script".

---

## Stage 8: the licence decision (owner decision)

- The owner agreed to put TestEvo-Bench, EvoArena and EditPropBench into the plan but decided that **the build still follows licences**, and asked for a document after the build that explains composition, sources and authority.
- Implemented: TEST_PLAN v0.4. The three resources are "pending permission" (MAIN-TE, EXP-EVO, EXP-PROP), assessed internally for feasibility only until the authors give written permission; new section 14 sets the build rules, the fields of `PROVENANCE.md` + `provenance.csv` (composition, upstream version, licence, what was used, changes, distribution, publication status, search grade, reason for choice, known problems, verification depth) and the pre-release acceptance checks.

---

## Stage 9: P0 step one — SWE-CI image architecture and running locally (owner approved the download and starting Docker Desktop)

| Action | Result |
|---|---|
| check the machine and code | Apple M4 Pro (arm64); Docker CLI installed but the daemon not running; SWE-CI's code does not hard-code an image platform; the official runner raises NotImplementedError outside Linux |
| choose an image | HF paths-info for all 100 `image.tar.gz`: 346–595 MB, 37.5 GB in total; the smallest chosen, `netbox-community__pynetbox__2cada4__fb8aa8` |
| download | 346,034,810 bytes downloaded to the session temp dir with the owner's approval. The plan was to stop after reading the architecture field; **the whole file was actually downloaded** |
| read the architecture | `manifest.json` → config `sha256:ba275d06…`: `architecture: amd64`, `os: linux`, Python 3.10.19, working directory `/app`, created 2026-01-15 |
| start Docker Desktop | `open -a Docker`; server 29.7.2 linux/arm64, 14 cores, ~8 GB memory; no Rosetta switch found in the settings file |
| download `code.zip` | 1,001,808 bytes; full git history of 651 commits, HEAD the latest commit `34685b4`, base and target both present |
| run | load 5 s; amd64 container start 3 s (`x86_64`); full test run at HEAD 137 passed, 99 errors (integration tests need netbox-docker); excluding integration tests, base 249 passed (~2 s), target 265 passed (~1 s) |
| mistake along the way | the first commit switch inside the container was refused by git (safe.directory), so both test runs actually ran at HEAD and were discarded; switched on the host instead, copied into the container, and reran for the results above |

Conclusion: the amd64 images run under emulation on this machine fast enough for grading; no Linux machine or rebuilt images needed. Limitation: only one image verified.

The image is loaded in the local Docker (~1.06 GB); the downloads are in the session temp dir.

---

## Appendix: all files involved in this record

| Location | Content |
|---|---|
| `literature/benchmark-sr/PROTOCOL.md` | search protocol and amendments |
| `literature/benchmark-sr/REPORT.md` | systematic search report |
| `literature/benchmark-sr/RESEARCH_RECORD.md` | this file |
| `literature/benchmark-sr/search-log.csv`, `records.csv`, `decisions.tsv`, `ft_decisions.tsv`, `other_methods.tsv`, `snowball.tsv`, `extraction.csv`, `recheck_result.json`, `sensitivity_license.csv` | every search and screening verdict |
| `literature/benchmark-sr/tools/` | `search.py`, `acl.py`, `merge.py`, `screen.py`, `ft_dump.py`, `extract.py` |
| `literature/benchmark-sr/raw/` | raw search results, caches, merged records (not in the public repository) |
| `literature/benchmark-sr/archive/` | README texts, full-text screening batches, snowball candidates, licence lookups, paper code links, re-screen sample (not in the public repository) |
| `research/TEST_PLAN_NEXT.md` | test plan v0.3 |
| `research/tools/` | SWE-CI drift script, metadata, the 12-pair sample |

**Not archived, rebuildable:** the 9 cloned repositories (re-clone at the commits above); arXiv full-text HTML (`archive/arxiv_html_fetched_ids.txt` lists the ids; refetch from `https://arxiv.org/html/<id>`); the ACL bibliography file (check the version against the SHA-256 above).

**AI use:** the search, screening, extraction, analysis and this record were done by Claude; the protocol and key decisions were confirmed by the owner; screening verdicts were not reviewed by a person.
