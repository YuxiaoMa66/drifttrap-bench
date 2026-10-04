# Evaluation resources on memory invalidation usable for evaluating GMR: systematic search report — English translation

> Translation of [REPORT.md](REPORT.md), which is authoritative.

2026-09-23. Executed per [PROTOCOL.md](PROTOCOL.md) ([English](PROTOCOL.en.md); SHA-256 before searching `21e2e03b…`, amendments in its section 10), reported per PRISMA-ScR. The screener was Claude alone; every number in this report can be recomputed from the files in this directory.

## 1. Summary

1. **No existing resource can directly replace building our own main experiment.** Of 108 included resources, only 2 are graded A under the rules fixed in advance: SWE-CI and SWE-Bench-CL. Both are sources of "code evolving over time" tasks and contain no "memory + staleness" condition themselves (SWE-Bench-CL has a FAISS semantic-memory module, but it measures forgetting and transfer, not handing back stale memories).
2. **Only 4 resources have both "external artifact change" and "a memory layer":** SWE-Bench-CL (A), OSAC-Bench (B, licence unclear), EvoArena (D, no licence), ChurnBench (D, repository not located).
3. **Stale-memory benchmarks are plentiful, but almost all put the staleness in dialogue.** For 34 resources the invalidation is in conversation text, for 15 in model parameters, for 19 mixed; only 7 are fully probeable by GMR (D2 yes).
4. **14 resources allow an external memory layer (D7 yes)**, candidate frameworks for the "GMR on top of memory systems" extension. Of these, agent-memory-bench, MERIT and sandbox-universe grade deterministically and have permissive licences.
5. **The works closest to GMR's claims have no public code yet:** SkillDrift (drift in packages/APIs/configs a skill references counts as contract violation), GPM-ReleaseBench (provenance binding, revoked facts do not come back), FixedBench (stale issues already fixed). ReclaimEval (keep recomputable provenance rather than conclusions) is public, Apache-2.0. The paper's related work must cover these.

So the earlier conclusion "build the tasks, reuse components" holds, and this time it follows from rules written in advance. The search did change three concrete practices; see section 7.

## 2. Search and screening flow (PRISMA-ScR)

```
Identified by database search                          Identified by other routes
  arXiv 395 · OpenAlex 400 · OpenReview 200              items known from the previous round (recall check) 6
  ACL Anthology 58 · GitHub 30 · Hugging Face 443        citation tracing (Byam/BigBag/BreakGuard -> BUMP) 1
  Semantic Scholar 0 (429 rate limit, replaced by OpenAlex)
  Papers with Code 0 (service shut down)
  total 1,526
        | duplicates removed 135
        v
Title/abstract screening 1,391 --excluded 1,225-->  I2 654 · I1 319 · E6 107 · I3 72 · I4 49 · E1 15 · E5 9
        |
        v
Full-text assessment 166 --excluded 71-->  I1 34 · I2 27 · E6 6 · I3 3 · E2 1
        |                                              other routes 7 --excluded 2 (I2 1 · I1 1)
        v                                                        |
Included from databases 95 ------------------------- + included from other routes 5
        |
        v snowballing (A/B seeds)
  round 1: 396 backward + 44 forward new records -> full text 12 -> included 8 (one B: CoUpJava)
  round 2: CoUpJava as seed, 28 references + 0 citations -> included 0, stopping rule met
        |
        v
Included in total 108 (95 database + 5 other routes + 8 snowball)
```

**Recall of known items:** of the 16 resources known from the previous round, the queries found 10 by themselves (62.5%). The 6 missed (MemoryCode, Stale Constraints, MemoryArena, Invalidation Contracts, REVOKE, GiulioDER/agent-memory-bench) are counted under "other routes", not in the database counts. The queries are insensitive to repositories that do not describe themselves in standard terms and to some new preprints — a limitation.

**Screening consistency (self-consistency, not inter-rater reliability):** from the 1,225 title/abstract exclusions, 245 (20%) were drawn with a fixed seed (20260923) and re-judged without seeing the original verdict. Include/exclude agreement 244/245 (99.6%), reason-code agreement 236/245 (96.3%). The single disagreement (DEAN, detecting outdated facts in knowledge graphs) got a full-text verdict and stayed excluded (non-LLM, I3). Details in [recheck_result.json](recheck_result.json).

## 3. Deviations from the protocol (all logged in its section 10)

| Deviation | Effect |
|---|---|
| Semantic Scholar kept returning 429; replaced by OpenAlex | OpenAlex ranks relevance less well; more unrelated records in its top 100 (e.g. optimisation algorithms, IoT surveys); recall may be lower |
| OpenReview searched through the API instead of venue-limited site search, count=10000 | pre-2023 records mixed in; 49 excluded under I4 |
| OpenAlex has no reference lists for arXiv preprints | backward snowballing instead parsed arXiv HTML reference entries; only seeds with HTML full text (17) are covered |
| HF records without a data card: a rule "no card and no linked paper → I1" was added during title/abstract screening and applied back to earlier batches | 15 records changed (all FT → EX); the rule was fixed before full-text screening began |
| API-evolution method papers in the code domain were moved to full text during title/abstract screening | 4 records changed EX → FT, decided at full text |

## 4. SQ1: where the invalidation happens

| D1 | Count | Representative resources |
|---|---:|---|
| external artifact (code, file, API, database, system state) | 40 | SWE-CI, SWE-Bench-CL, ChainSWE, GitChameleon 2.0, TimeMachine-bench, BUMP, OSAC-Bench, ChurnBench, SkillDrift |
| conversation text | 34 | LongMemEval, MemoryAgentBench, STALE, StateMemBench, MemConflict, Supersede, agent-memory-bench, REVOKE |
| mixed | 19 | CodeUpdateArena, HoH, Stale Constraints, GPM-ReleaseBench, ReclaimEval, MERIT |
| model parameters | 15 | TiC-LM, KNOT, EDAPIBench, MUDAPIBench, EvolveBench, DynamicQA |

Almost all 40 external-artifact resources are "code/library version evolution" benchmarks, measuring whether a model can write code for the new version, not whether an agent holding old memories notices they are stale. The two constructs belong to different research communities: the code-evolution side has no memory condition, and on the memory side the change does not land on an artifact. **GMR sits exactly in the gap between them.**

GMR probeability (D2): yes 7, partly 40, no 61. "Partly" is mostly two cases: the change is in a dependency library (needs a lock file or a `vendor/` path; `.venv` was verified unparseable), and languages such as Java/Rust whose ast-map coverage is unverified.

## 5. SQ2: grading, availability, licence, ceiling

- **Grading (D3):** exact match or deterministic rules 52, executable tests 34, LLM judge 1, human 2, unverified 19. New memory benchmarks clearly move towards deterministic grading (MemRiskBench, sandbox-universe, agent-memory-bench, StateMemBench), consistent with GMR's "recomputable" stance.
- **Availability (D4):** code and data 68, data only 9, paper only or no public link found 31.
- **Licence (D5):** permissive 47, none 16, unclear or other (NOASSERTION, GPL, CC-BY-NC, anonymous repositories) 14, not located 31. **The 16 without a licence are graded D by rule**, including REVOKE, TestEvo-Bench, EditPropBench, MemConflict, EvoArena, RustEvo².
- **Ceiling (D9):** reported best scores are generally modest (STALE 55.2%, GitChameleon 2.0 48–51%, BeyondSWE 56.65, EvoArena average 39.6%); no high ceiling risk (≥ 90%) except Supersede's full-context baseline (~92%) and MERIT's single-fact recall. **This contrasts with our AMB experiment where both arms hit 100%: the ceiling came from task design, not from the direction being unmeasurable.**

## 6. SQ3: can an external memory layer be plugged in

The 14 with D7 yes: agent-memory-bench, MERIT, sandbox-universe, SACAM, AgentMemoryBench (s010m00n), agent-memory-trigger-bench, PrecisionMemBench, jrosenbizzle/agent-memory-bench, agentmem, agent-memory-benchmarker, adopt-bench, ForgetEval, AgentNativeMemory, DRIFTBENCH. The first 11 have public code.

Recommended order for the "GMR on top of memory systems" extension (by grading determinism, licence, and whether real memory products are already connected):

1. **agent-memory-bench** (Apache-2.0): adapters for mem0, zep, cognee, supermemory, claude_mem and others; executable grading.
2. **MERIT** (MIT): preregistered, deterministic environment, an updated-fact difficulty tier, full public trajectories.
3. **sandbox-universe** (MIT): lane plug-in mechanism; note that the author is also the author of a memory system under test (disclosed in its README).
4. **AgentMemoryBench (s010m00n)** (MIT): includes a repair mode and knowledge-conflict resolution.

## 7. Impact on the test plan

| Preset in protocol section 9 | Result | Change to the plan |
|---|---|---|
| if an A-grade resource appears, the test plan must change | A grade: SWE-CI, SWE-Bench-CL | SWE-CI is already the main material, kept; **SWE-Bench-CL promoted from "supplementary candidate" to main material**; **ChainSWE** (B, data MIT) added as multi-bug-chain material |
| the conclusion may still be "build our own" | the rules give "build our own" (no resource combines a memory condition, artifact drift, executable grading and a permissive licence) | main experiment design unchanged |
| — | new works closest to GMR (SkillDrift, GPM-ReleaseBench, FixedBench, ReclaimEval, OSAC-Bench) | added to related work to avoid overclaiming novelty; OSAC-Bench's "refuse stale facts after a system fingerprint changes" is a design reference for non-code probes (HTTP/SQL/file) (licence to be confirmed) |
| — | 14 frameworks with memory adapters | new extension "GMR on top of memory systems", agent-memory-bench first |
| — | 23 C-grade memory benchmarks (STALE, StateMemBench, Supersede, LongMemEval, …) | appendix L3 ports 2–3 of them to state the scope |

## 8. Limitations

1. **Single screener.** 99.6% self-consistency does not replace an independent second screener.
2. **Recall.** Known-item recall 62.5%; only the top 50–100 per source screened; OpenAlex ranks poorly; Chinese databases such as CNKI not covered; Papers with Code shut down.
3. **Time window.** Many resources are 2026 preprints (D8: preprint 65, peer-reviewed 26, code repository only 17) and may be updated or withdrawn soon.
4. **Extraction depth.** D fields come from abstracts, READMEs and data cards, not full methods; grading is "unverified" for 19 records; 31 have no public link located, some of which claim to be open source (ChurnBench, DriftMedQA, CODEMENV) with links truncated in the abstract. These may be underrated as D.
5. **Backward snowballing covers only seeds with arXiv HTML**; non-arXiv seeds (GitHub, HF repositories) have no references to trace.
6. **E5 excluded 9 weight-level knowledge-editing benchmarks outside code** (e.g. LeKUBE, CoME). This is the protocol's preset scope; readers who consider them relevant need a separate search.

## 9. Files

| File | Content |
|---|---|
| [PROTOCOL.md](PROTOCOL.md) | protocol and amendments ([English](PROTOCOL.en.md)) |
| [search-log.csv](search-log.csv) | every query, hits, number screened |
| [records.csv](records.csv) | title/abstract and full-text verdicts for the 1,391 database records |
| [ft_decisions.tsv](ft_decisions.tsv) | full-text verdicts with notes |
| [other_methods.tsv](other_methods.tsv) | the 7 records from other routes |
| [snowball.tsv](snowball.tsv) | both snowball rounds |
| [extraction.csv](extraction.csv) | D1–D9 and fit grade of the 108 included records (grades computed by `tools/extract.py`) |
| [recheck_result.json](recheck_result.json) | the 20% blind re-screen |
| `tools/` | search, de-duplication, screening and extraction scripts |
| `raw/` | raw search results and caches (not included in the public repository) |

AI use: the search, screening, extraction and this report were done by Claude (Anthropic) with the owner's authorisation; the owner confirmed the protocol; no verdict was reviewed by a person.

## 10. Supplement: licence sensitivity analysis

Dropping the licence condition and keeping every other rule: A 3, B 41, C 27, D 37 ([sensitivity_license.csv](sensitivity_license.csv)). 15 resources move up, all previously D for lack of a licence. TestEvo-Bench becomes A (real commits, executable, Python), EvoArena B (artifact change and a memory condition), EditPropBench B, REVOKE C. The core conclusion of section 1 is unchanged. Details in [RESEARCH_RECORD.md](RESEARCH_RECORD.md), stage 7.
