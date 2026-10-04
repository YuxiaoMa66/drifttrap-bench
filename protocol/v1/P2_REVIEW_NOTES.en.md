# Review points on the P2 draft (for the owner, 2026-09-26) — English translation

> Translation of [P2_REVIEW_NOTES.md](P2_REVIEW_NOTES.md), which is authoritative.

> **Update:** under the goal "continue as you propose", points 1–3 were written into the draft and implemented as I proposed (`scripts/analyze_p3.py` resamples tasks, with a repository-level row for the API family; `scripts/audit_process_access.py --stop-check` implements the stop rule, threshold 1/3 with at least 6 sessions). All of this can be reverted; you still need to read it before the freeze (B59).

Draft: `P2_PREREG.md` (v1). I first checked it for consistency and fixed **outdated facts** directly (open questions all decided, codex version 0.157.0, a GMR version row, the B48 rule in the isolation row, P1 data for the new tasks, gemini EXT-v2 numbers 6/12 and +50, L1 over-hand-back done, numbering of section 9). Below are **the points that need your judgement**; I did not change them for you. Each has my view, which you can reject.

## 1. The API family's hierarchical bootstrap has only 3 repositories

Section 6 says "hierarchical bootstrap by repository". After B58 the API confirmatory tasks are sanic 7, griffe 2, pdfsyntax 1 — **3 repositories**, sanic 7 of 10. Resampling repositories, the 95% interval is decided almost entirely by whether sanic is drawn.

- Options: (a) keep resampling by repository (conservative, but the within-family API test carries almost no information); (b) resample tasks for the API family and state in the report that the tasks come from 3 repositories and are correlated within one; (c) confirm only on the pooled set (22 tasks of both families) and label every within-family result descriptive.
- My view: (c), with (b) reported as a sensitivity analysis. Section 6 already says differences between families are exploratory, and the pooled test is where H1/H2 have power.

## 2. P3 cannot measure the cost of over-hand-back

L1 shows class-level anchors over-hand-back 83% on real commits, but in P3's drifted tasks every anchor is genuinely invalidated, and in stable tasks nothing changed (GMR cannot hand anything back). So P3's H1/H2 measure only the benefit of "GMR hands back when it should", and **nothing about how handing back a memory that still holds disturbs the agent**.

- Options: (a) keep it (B43: `moved-still-valid` only in L1) and put the 83% next to H1/H2 in the paper, stating the blind spot; (b) before the freeze add a `changed-but-valid` condition: the repository changes the class holding the anchor but the memory's fact still holds, testing whether gmr_hook's flag makes the agent change a correct memory. New tasks needed, about 1–2 more days of work and a batch of calls.
- My view: (a). (b) would delay the freeze and change decision B43, while (a) exposes the limitation honestly. If the completeness of the paper's conclusion matters more to you, (b) is more convincing.

## 3. gemini may again be systematically missing in the EXT family

In P1, gemini's EXT **bare** arm tried to reach harness processes almost every time (recorded as missing under B50). P3 has no bare arm, but in the P1 reruns the **stale_notes** arm also ran `ps -p` once (#65). Section 7 says "if a (model, family, arm) systematically crosses the line, record it as missing". If gemini systematically crosses the line in one EXT arm, H1/H2 have no paired data for gemini × EXT.

- Options: (a) keep section 7's rule; (b) fix a threshold in advance, e.g. "stop a (model, family, arm) when more than 1/3 of its sessions cross the line, and report it as missing", to avoid ad hoc judgement during P3.
- My view: (b); a fixed threshold fits the spirit of preregistration. You choose the number.

## 4. gemini quota and time

352 sessions per model. At P1's measured ~0.23% of the weekly quota per session, gemini needs about **81% of one account's weekly quota**; the current account has about 31% left and resets on 09-30; there is a second account. About 45–50 sessions per 5-hour window, so about 7–8 windows.

- Nothing to decide, only a reminder: P3 on gemini cannot finish before 09-30 (or a switch to the second account); luna is not limited. Section 8's execution order (blocks, rerun only incomplete blocks after a quota stop) already covers interruptions.

## 5. Freeze steps

The freeze needs `git init` (local, no push) and the opentimestamps-client download (only a hash is sent to public timestamp servers). After you have read the points above and told me what to change, I will ask once more before doing these two steps.
