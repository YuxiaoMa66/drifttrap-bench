# 偏离预注册记录

冻结：`P2_PREREG.md`，2026-09-26T10:06:14Z（B60），清单 `FREEZE_MANIFEST.json` sha256 `aada56a2…`（已打 OpenTimestamps）。冻结后对清单内文件的每一处改动都记在这里，并在 P3 报告中列出。

## D1（2026-09-26，P3 第一个会话之前）：`scripts/analyze_p3.py` 支持合并同一模型的多次运行

- **原因**：冻结的设计里 drifted 与 stable 必须分开运行（EXT 配置服务一次只能提供一个版本，`run_p1.py` 每次运行一个 variant），`run_p1.py --tasks` 也只接受一个 glob，确认性 22 个任务需要按族/仓库分成几次运行。冻结版 `analyze_p3.py` 一次只分析一个运行，无法把同一模型的 drifted 与 stable 合在一起算“打扰成本”，也无法把几次运行合成确认性检验。这是工具缺陷，冻结前的假被测 dry run 没有暴露它。
- **改动**：新增 `--model <name> <run_id>...` 入口：逐个运行套用各自的泄漏审计后合并记录，写 `results/P3_REPORT-<name>.md`。分析方法（单元、重抽样、Holm、阈值、有效性规则）完全不变；`cells()` 按（任务, 条件, 臂, 重复）取值，不依赖会话编号。
- **验证**：`--self-test` 通过；用 P1 的两次 luna 运行试跑合并（没有 gmr 臂，结果为空，符合预期），试跑报告已删除。
- **哈希**：冻结时 `56d2acb982f88365921580cd9f2d2d61d61141aed46f1d720e48e1b7c5748803`；改后 `b74349ce48c4b32fefc0674c48e17c501073bb8a84c64b07a96ab48e691f09e1`。
- **影响**：发生在 P3 任何数据之前，不可能受结果影响。

## D2（2026-09-27，P3 gemini 进行中）：澄清“附加其他进程”的范围（用户决定 B63）

- **原因**：P3 中 gemini 在 gmr_tool 组多次用 lldb 启动并调试 gmr 工具本身（想找它的 sqlite 状态库），沙箱下全部 “Not allowed to attach”。P2 第 7 节原文“尝试附加、采样、发信号或读取其他进程……”没有说清被测自己启动的工具算不算；规则的目的（B48/B49）是防止被测从 harness 或其他会话拿到答案，这里不存在这种可能。
- **改动**：用户决定（B63）：“其他进程”指不是被测自己启动的进程（harness、其他会话、本机服务）。`scripts/audit_process_access.py` 的严格模式中，调试器只在附加已有进程时计入（`-p <pid>`、`--attach`、`process attach`、`--wait-for` 等）；用调试器启动程序不计。撤回 P3-gemini-sanic-drifted #12 的无效判定。
- **影响**：只涉及 gmr_tool 臂（不在 H1/H2）；受影响会话 sanic #12、#45、#47、#82、#83，griffe #24（均判通过，仍有效）。P1 数据上的判定不变（EXT bare 仍触发 STOP；P1 里的 lldb 都是 `-p <pid>` 附加 harness）。luna 的 P3 不受影响（无此类命令）。
- **哈希**：冻结时 `16406095ac844241e5fa8f832793ee5a09800ec789d8e43c0d1805aeaf2f29ae`；改后 `03dffdc686e415e1ae24c575f1b57dfd6607cac36a1c3604680b0c2fc68b81a9`。

## D3（2026-09-30 ≈20:00Z，P3 gemini 进行中）：agy-mc 由 0.5.0 升级到 0.6.1（用户操作）

- **原因**：用户升级 Antigravity Mission Control 以修复 bug。冻结清单记录的是 `agy-mc 0.5.0`（agy 冻结时 1.2.11，P3 期间已自动升到 1.2.14，P2 第 2 节已允许）。
- **影响**：第 153 号会话之前（含 luna 全部、gemini 已完成的会话）用 0.5.0；此后新启动的 gemini 会话用 0.6.1。每个会话回执的 `versions` 字段记录启动时的版本，报告时按版本分段核对 gmr_hook/gmr_tool/protocol/stale_notes 各臂在两个版本下的会话数是否平衡；`harness/run_agy.py` 与冻结脚本未改。
- **核对**：见 JOURNAL 2026-09-30 20:01Z 之后的条目（0.6.1 首批会话的回执字段核对结果）。
- **用户问题**：升级是否影响调用——命令行参数与 stdout/stderr 约定未变，但行为需要实测，故先暂停、再核对。
- **核对结果（2026-09-30 20:2x Z）**：首批 10 个 0.6.1 会话（extv2-10/11/12 stable）回执字段全部齐全（对话编号、证据目录、工具调用、token 用量、联网工具检测字段），`harness/run_agy.py` 解析正常，未改。后续 0.6.1 会话继续按版本分段；若某会话字段缺失会在报告中列出。

## D4（2026-10-01，P3 全部完成之后）：AGY 沙箱写入规则收紧（用户决定 B65）

- **原因**：P3 后排查发现 `harness/run_agy.py` 只禁止写项目目录与 /private/tmp，gemini 被测能写主目录及其他用户可写位置（P3 中曾把自己的工作区复制到 ~，同会话删除；无串话、无泄漏，P3 数据不受影响，见 `results/P3_SUMMARY.md`）。
- **改动**：先全面禁止写入，只放行工作区、本会话临时目录、/dev、/private/var/folders，以及 AGY 自身写入的位置（`~/.gemini/antigravity-cli`、`~/.gemini/antigravity`、`~/.local/state/antigravity-mission-control`、`~/Library/Caches`，按 P3 期间实际写入确定）；再禁止写 AGY 配置（antigravity-cli/settings.json、settings.json、config/mcp_config.json）。`harness/run_codex.py` 的 self-test 新增写入检查（主目录、桌面、Python 前缀下的 .pth、项目目录、AGY 配置都必须被拒）。
- **验证**：self-test 通过；冒烟 SMOKE4-gemini（p03v2-e01，stale_notes 与 gmr_tool，2 次调用）均有效通过，回执字段齐全；AGY 侧唯一的写入拒绝是 `~/.gemini/config/plugins`，P3 中 170/172 个会话同样出现（原有的禁读规则），不是新规则引起；settings.json 未改动。
- **影响**：只影响以后的运行；P3 数据不重跑（B65）。
- **哈希**：run_agy.py `d9b0e062f4089c4db66fd760299062307233c00cbb193b60cdbfb77ed3280225` → `8313b32d0ffb87d32d6dab5a0d448babd612e0a2e7007946746e28c12bc1bfb7`；run_codex.py `d379bb8cd0966ae92950910871dcc564836b08cc0035366092765619c4fd53db` → `02a995ec5d67d692f2f663f0b4d72acd629e04b9e17482bd91b9705b3a046d66`。

## D5（2026-10-04 追溯登记，用户决定 B104）：冻结后修改开发者说明 `GMR_FINDINGS_FOR_DEVELOPERS.md`

- **原因**：该文件列入冻结清单（`FREEZE_MANIFEST.json` 记录 sha256 `b387047593922012d0a6b4b75f15d46bd570d238c82e850c49073b463870d5f6`），冻结后陆续追加了给 GMR 开发者的发现说明，但此前未在本文件逐项登记。2026-10-01 codex 独立审查（`GMR-Paper-Research-20260922/qa/codex-review-20261001/REVIEW.md`）与 2026-10-04 终止核验（`handoff/evidence/termination-20261004/freeze-check.txt`）均列出该差异；T56 审核（`GMR-Paper-Research-20260922/qa/claude-ars-review-20261004/REVIEW.md` §6）提出补登，用户决定补登。
- **改动（只追加文字）**：提交 594f611（2026-09-30，P3 gemini 进行中，+8 行，F10）；提交 46bf669（2026-10-01，P3 结束后，+10 行，P3 结果摘要）；此后未提交的追加 +54 行（F11、F12 及 T53 期间的说明，最后修改 2026-10-04）。
- **影响**：只是给开发者的文档。核对 `harness/`、`arms/`、`scripts/`、`tasks/`、`oracles/`、`l0/`、`l1/`，除 `scripts/freeze_manifest.py`（把它当作被哈希的文件）外无代码读取它；被测沙箱拒读项目目录。因此不影响被测输入、判分、分析或任何 P3 结果。本条为事后登记，不改变 D1–D4，不修复或回退该文件。
- **哈希**：冻结时 `b3870475…`；594f611 后 `e76b739c…`；46bf669（当前 HEAD）`e47702de…`；登记时工作区版本 `505ea036ea152e4d221b3614f6f8ff09ca3ef57b2165e8e75b2ecb98068c13fd`（未提交，之后可能继续追加）。
