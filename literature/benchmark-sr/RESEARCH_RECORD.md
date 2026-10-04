# 研究详细记录：GMR 评测资源的搜集、审阅、验证与系统检索

记录日期：2026-09-23（全部工作在同一天完成，跨两个会话）。执行者：Claude（Anthropic），在用户逐步授权下进行。
本文是**过程记录**，按时间顺序写明每一步做了什么、依据什么、读到什么深度、得出什么结论，以及后来纠正了什么。结论性内容见 [REPORT.md](REPORT.md) 和 [TEST_PLAN_NEXT.md](../../research/TEST_PLAN_NEXT.md)。

读法：每个阶段都有“动作 / 证据 / 结论 / 局限”四部分。**“局限”列出的内容不能在论文中当作已完成的工作使用。**

---

## 阶段 0：起点与用户问题

- 用户问题 1：“我的 GMR 测试有没有更权威的、或者 GitHub 上已经共享的测试可以复用或参考？”
- 已有测试资产（本地核对）：
  - `GMR工程级测试套件`：38 项黑盒测试，锁定 v0.2.3/v0.3.3；`docs/研究依据.md` 已列出 nextest、llvm-cov、proptest、cargo-fuzz、SQLite 测试法、MCP Conformance 等资料。
  - `GMR-v0.3.4-P03-Gemini-Benchmark`：P03 陈旧记忆冲突用例 12 个，11 个模型 × 12 × 2 臂，ON 83.64 / OFF 62.20。
  - `GMR-Agent-Memory-Benchmark-Latest-20260826`：在 Hindsight 的 AMB（agentmemorybenchmark.ai）上做 GMR ON/OFF，v0.4.6，61 个任务 × 2 个模型 × 2 臂，两臂 solved 都是 100%。
  - `GMR-Paper-Research-20260922/literature`：已有 28 项文献记录（matrix.csv），检索日志注明“未饱和”。

---

## 阶段 1：临时检索（非系统检索）

**性质说明：** 这一阶段是按需做的关键词搜索，**挑选标准边搜边定，而且按“和 GMR 像不像”来筛**。用户随后指出了这个问题，于是有了阶段 5 的系统检索。本阶段的结论只能作为线索，不能作为论文的证据基础。

### 1.1 使用的检索（WebSearch，美国区）

| # | 检索式 |
|---|---|
| 1 | `MemoryAgentBench conflict resolution github benchmark agent memory` |
| 2 | `CodeUpdateArena GitChameleon API version drift benchmark github` |
| 3 | `benchmark stale memory coding agent repository evolution multi-session SWE-bench continual github 2026` |
| 4 | `"Invalidation Contracts for Cross-Episode Agent Memory" code github` |
| 5 | `"When Stale Constraints Go Unchecked" inherited agent memory benchmark code release` |
| 6 | `MemoryCode multi-session coding benchmark github instructions across sessions` |
| 7 | `SWE-CI benchmark github continuous integration maintainability agent 100 tasks`（阶段 3 验证时补做） |

### 1.2 抓取的页面（WebFetch，只读摘要或 README）

REVOKE 仓库、coding-agent-memory-benchmark 仓库、GiulioDER/agent-memory-bench 仓库；arXiv 摘要页 2605.06527（STALE）、2507.00014（SWE-Bench-CL）、2603.03823（SWE-CI）、2607.02606（ChainSWE）、2608.25553（Stale Constraints）、2602.16313（MemoryArena）；Zenodo 记录 22147784。

### 1.3 克隆并审阅的仓库（浅克隆，读 README、任务样例、判分代码、LICENSE）

| 仓库 | 提交 | 日期 | 许可 | 审阅深度 |
|---|---|---|---|---|
| GiulioDER/agent-memory-bench | `abd4e6bc153582a55dda62d9c4050d78a3cc3bdd` | 2026-09-21 | Apache-2.0 | README 全文；`tasks/xs-evolve-lease/task.json`；`tasks/ts-append-only/checker.py`；`harness/adapters/base.py` 接口；`adapters/claude_md/adapter.py` 说明；`docs/CAPABILITY_TRACKS.md`、`docs/LIFECYCLE_CAPABILITY.md`；`capabilities/governance.json` 首个 probe；`harness/claude_exec.py` 调用方式 |
| Dextergao14/REVOKE | `5c193339b4668c7a782d221c423fa5b5ec5b659b` | 2026-09-20 | **无 LICENSE** | README；`docs/GRADING.md` 前 80 行；数据样例前 1.5KB；`revoke/logic.py` 结构 |
| HUST-AI-HYZ/MemoryAgentBench | `fe1735de8cf8b9908e1e3d3b5612afc815698062` | 2026-08-20 | MIT | README 的评测指标表 |
| SaravananJaichandar/coding-agent-memory-benchmark | `b57d241d2f8c691e72a6c090acb59be35d40f597` | 2026-08-24 | MIT（论文 CC-BY） | DESIGN.md 前 120 行；RESULTS.md 中关于泄漏与子集的段落 |
| Cohere-Labs-Community/MemoryCode | `1ab87e119b2f9a498de8075219e1c07f6041b394` | 2025-04-25 | Apache-2.0 | README；dataset/dialogue_1.json 前 1.2KB |
| mrcabbage972/GitChameleonBenchmark | `3a1b6045a6b2a276bd24d715589cb041f8eccb93` | 2026-04-17 | Apache-2.0 | README 前 50 行；dataset 目录 |
| leo-liuzy/CodeUpdateArena | `836e2d157739fd53f9cde421913eb5949d4eeeb8` | 2025-03-20 | MIT | README 前 40 行；data 目录 |
| thomasjoshi/agents-never-forget（SWE-Bench-CL） | `74a38a90baace25635f3827ee2f98caff24b3768` | 2025-05-17 | MIT | `data/SWE-Bench-CL-Curriculum.json` 结构与字段 |
| SKYLENAGE-AI/SWE-CI | `b2a0620f0168a5a89681be7919a98d9a49ab22af` | 2026-06-10 | Apache-2.0 | README 前 80 行（ANC 指标、运行成本） |

### 1.4 本阶段做的计算

- **SWE-Bench-CL 同函数任务对**：按 `created_at` 排序每个仓库的任务，用 patch 的 hunk header 提取 `(文件, 函数名)`，统计前后两个任务改到同一函数的对数：20 对，涉及 16 个后续任务（sphinx 12、xarray 4、django 2、matplotlib 1、pytest 1）。**这是启发式统计**，hunk header 标注的是上下文函数，可能有误。

### 1.5 本阶段的关键发现

1. **agent-memory-bench 的“过期”发生在对话里**：`xs-evolve-lease` 由三次带日期的会话给出 90/45/20 秒，代码不变。GMR 的探针在这类任务中看不到变化。
2. **P03 的对照组设计有缺陷**（在阶段 2 核实源码后确认，见 2.2）。
3. **coding-agent-memory-benchmark 存在泄漏**：within-domain 组的 4 条约束取自同一子集的 baseline 失败（作者在 RESULTS.md 中自己披露），并且在 checkout 上应用了 `test_patch`。

### 1.6 本阶段后来被纠正的说法

- 已知条目检查时，把“agent-memory-bench”记为找回，实际匹配到的是同名的其他仓库（jrosenbizzle、dakshjain 等），GiulioDER 仓库并未被检索到。已在阶段 5 更正。
- 初版方案写“AMB 在大约 190 次调用后耗尽额度”，不准确：189 条有效记录里包含复用的早期证据。已改为“244 个条件中 55 个因额度 invalid”。

---

## 阶段 2：审阅用户自有的 P03 v0.3.4

用户要求把 v0.3.4 完整测试的参考项目和测试一并纳入。

### 2.1 读取的文件

`README.md`、`docs/研究依据.md`（全文）、`docs/P03-v0.3.4-设计与执行协议.md`（前 140 行）、`docs/P03-v0.3.4-完整结果分析.md`（全文）、`docs/P03-v0.3.4-GMR技术设计分析与不足.md`（第 5–10 节）、`benchmark/p03-v034/cases/p03-h01/*`、`scripts/dispatch_subject.py`（第 250–300 行）、`scripts/harness.py`（第 585–640 行）、`NOTICE.md`。

### 2.2 源码核实的发现

- `scripts/harness.py:594-627`：
  - acquisition 阶段 OFF 组也读到 E01（历史约束），但被禁止持久化；
  - recovery 阶段换全新 agent，OFF 组的 prompt 只有 E02、E03 和仓库，**看不到历史约束**；
  - ON 组的 recovery prompt 额外要求 “Current repository evidence is authoritative”，并核对两处证据。
- 结论：P03 的 +21.44 混合了“有无记忆 + 额外指令 + GMR 检测”三种效应；`conflict_and_evidence`（15 分）对 OFF 组结构上不可得。AMB v0.4.6 的 OFF 组同样没有记忆。
- P03 机制诊断：read/check 100%、stale detected 94.7%、post-read consistent 50%、reconciliation failure 40.15%。
- `NOTICE.md`：测试套件本身没有公开许可证，要求在选定许可证之前保持私有。

---

## 阶段 3：方案形成前的验证

用户要求“先验证完成，再给详细方案、测试流程、框架和是否使用 AMC”。

| 验证项 | 做法 | 结果 |
|---|---|---|
| SWE-CI 数据 | HF API 列出 `skylenage-ai/SWE-CI` 文件；下载 `metadata/{default,full,lite}.csv`；查询 `image.tar.gz`、`code.zip` 大小 | 100 对（full 226、lite 50）；许可证 MIT 51、Apache 15、BSD 20、ISC 9、GPL/LGPL/混合 5；镜像 266–356MB |
| SWE-CI 函数级漂移 | `tools/mine_sweci_drift.py`，固定种子 7 抽 12 对，浅 fetch 两个提交，AST 比较非测试 `.py` 文件 | 12 对中 11 对签名改变 ≥ 2；仅函数体改变 11–145；未改变 69–2252（结果存于 `research/tools/sweci_drift_sample12.json`） |
| agent-memory-bench 能否接 AMC | 读 `harness/claude_exec.py`、`.env.example`、`docs/REPLICATION.md` | 不能：固定调用 `claude -p --output-format stream-json`，走 Anthropic 兼容端点 |
| Stale Constraints 数据 | WebFetch Zenodo 记录 | CC-BY-4.0，61.5MB，含 5,400 个 episode 与冻结规格；**未下载** |
| MemoryArena | WebFetch arXiv 摘要 | 网页、规划、搜索、形式推理；不涉及代码和过期；排除 |
| GMR 锚定依赖文件 | 本地 `gmr 0.6.6`（`GMR-latest/target/release/gmr`）在临时 git 仓库中 anchor/改动/check | `file://deps.json#$.deps.lib1` 可交还；`vendor/lib1/api.py#fetch` 报 signature-changed；`.venv/...` 无法解析；同一次操作中一个打不开的锚点导致其他 note 未绑定（未定性为缺陷） |
| `gmr check --json` | 同上 | 输出含 `handed_back[].anchor/status/memories` 等字段，可直接解析 |
| AMC 状态 | 只读 `agy-mc usage`、`agy-mc models` | 额度 100%；可用 Gemini 3.x、claude-sonnet-4-6、claude-opus-4-6-thinking、gpt-oss-120b |
| AMC 的 token 记录 | 统计 AMB 证据 `matrix-pilot-full37-reconciled-summary.json` | 5,923 条调用均有 input/output/thinking/cache/total tokens |
| GMR 记忆存储支持（阶段 6 补做） | 读 `README.md` 第 8 节与 `batteries/provider/src/` | 原生：claude_code、git、http、local_file、mem0；mem0 同时支持云端与自托管（列表上限 1000）；其他存储可在 `.anchor/providers.toml` 声明 fetch 脚本 |

**用户确认的决定：** 使用 AMC 作为被测模型通道（方案 v0.2 第 3 节）。

---

## 阶段 4：发布与“为什么不直接套用”的讨论

- 用户问是否发布、是否说明为综合项目。给出建议：分阶段发布、定位为 GMR 评测、写出处表与许可证合规（未落文件，属建议）。
- 用户问选择依据以及为什么不直接套用多个基准再比较。**回答中承认了阶段 1 的选择是临时搜索，挑选标准偏向“自写”的结论。** 提出两项后续工作，用户回复“两个都做，先做系统检索”。

---

## 阶段 5：系统检索（详见 PROTOCOL.md 与 REPORT.md）

### 5.1 协议登记

- 写定 [PROTOCOL.md](PROTOCOL.md) v1.0，检索前 SHA-256：`21e2e03b37575874804f05a215d441c2f1b821dc0271f8949738cd6133586f0f`（已记入 WORK_LOG）。
- 核心设计：**纳入只看“是否测记忆失效”，GMR 适配程度作为纳入后的提取字段，按预设规则分 A–D 级。**
- **用户确认：** 协议照此执行；E5（排除代码领域以外的权重级知识编辑）照此执行；单一筛选者的局限写明即可。

### 5.2 检索执行

| 数据源 | 方式 | 实际命中/筛选 | 备注 |
|---|---|---|---|
| arXiv | 官方 API，4 组布尔式 + 2023-01-01 至检索日 | 395 | Python urllib 对多词查询返回 406，改用 curl 请求 |
| Semantic Scholar | Graph API | 0 | 约 10 分钟内持续 429；按修订 1 改用 OpenAlex |
| OpenAlex | `/works?search=`，限 2023 年起 | 400 | 相关度排序弱，混入大量无关论文 |
| OpenReview | API v2 `/notes/search` | 200 | 未加会议限制，count=10000；混入旧论文 |
| ACL Anthology | 下载官方 `anthology+abstracts.bib.gz`（2026-09-22 版，SHA-256 `dd753c17fe34a46d8bc9e3076d59a90335589b86e3ff226c841e99205a7373ad`），本地布尔匹配 | 58 | 首次解析因 abstract 为末字段、花括号、复数形式而全部 0 命中，修正后重跑 |
| GitHub | `gh api search/repositories`，每组 3 条检索式 | 30 | 所有词须同时出现，命中少 |
| Hugging Face | Hub API `search=`（按 ID 子串） | 443 | 大量名称噪声 |
| Papers with Code | — | 0 | 已跳转到 huggingface.co/papers/trending，服务停止 |

- 合计 1,526 条，去重后 1,391 条。检索式原文见 [search-log.csv](search-log.csv)，脚本见 `tools/search.py`、`tools/acl.py`、`tools/merge.py`。
- **已知条目召回：** 16 个已知资源找回 10 个。

### 5.3 标题摘要筛选

- 19 批（每批 75 条），逐条记录判定与原因编号（[decisions.tsv](decisions.tsv) → [records.csv](records.csv)）。
- 筛选中确立并回溯应用的两条规则（均在全文阶段之前）：
  1. 代码领域 API 演化方法论文可能附带新数据集，统一改为进入全文（4 条 EX→FT）。
  2. Hugging Face 记录无数据卡且无关联论文的，判 I1（15 条 FT→EX）。
- 结果：进入全文 166 条，排除 1,225 条（I2 654、I1 319、E6 107、I3 72、I4 49、E1 15、E5 9）。

### 5.4 全文筛选

- 论文读完整摘要；仓库读 README 与 LICENSE（17 个 GitHub 仓库 README 存于 `archive/readmes/`）；HF 读数据卡原文。
- 结果：纳入 95、排除 71（I1 34、I2 27、E6 6、I3 3、E2 1），明细见 [ft_decisions.tsv](ft_decisions.tsv)。
- **数据问题记录：** OpenAlex 把 world-model-mcp 的论文错标为 `arXiv:2310.06770`（该编号实为 SWE-bench），按原文内容判定。
- **其他途径 7 条**（[other_methods.tsv](other_methods.tsv)）：6 条已知条目召回漏检 + BUMP（Byam、BigBag、BreakGuard 三篇方法论文都使用它，经引用追溯补入，`gh api repos/chains-project/bump` 核实 MIT）。纳入 5 条。

### 5.5 数据提取

- 论文页面链接自动抽取（arXiv HTML/abs 中的 GitHub、HF、Zenodo、匿名仓库链接，存于 `archive/arxiv_code_links.json`）；未找到链接的用 `gh search repos` 按名称搜索（后触发搜索接口限速）。
- 许可证：GitHub 用 `gh api repos/...`（`archive/licenses_github.tsv`），HF 用数据集 API 的 `cardData.license`。
- D1–D9 依据摘要、README、数据卡填写，未写明的一律填“未核实”；**适配等级只由 `tools/extract.py` 按协议规则计算**。
- 协议第 6 节 D 级“包括 D5 为无”：无许可证的资源一律判 D；NOASSERTION 等记为“不明”，不直接判 D。

### 5.6 滚雪球

- **第 1 轮：** OpenAlex 对 arXiv 预印本没有参考文献列表（全部 refs=0），因此后向追溯改为解析 17 篇 A/B 级 arXiv 种子的 HTML 参考文献条目。首次解析因 `class="ltx_bibitem ltx_bib_article"` 多类名匹配失败，8 篇为 0 条，修正正则并重新抓取后得到 833 条，2023 年起 508 条，去重后 446 条，新增 396 条；前向用 OpenAlex `cites:` 取 6 个有施引的种子，新增 44 条。标题层筛选后 12 条进入全文，纳入 8 条。其中 14 条只有 arXiv 编号的参考文献，通过 arXiv 摘要页补出标题再判。
- **第 2 轮：** 第 1 轮新增的 8 条中只有 CoUpJava 属于 B 级。其 28 条参考文献中，2023 年起且不在已有记录里的只有一条（CHI EA 2024 研究，I1）；施引 0 条。新增纳入 0，满足停止规则。
- 记录见 [snowball.tsv](snowball.tsv)，候选标题见 `archive/snowball/`。
- **局限：** 滚雪球排除的 428 条只在标题层判定，原因编号比主筛选粗。

### 5.7 自身一致性检验

- 固定种子 20260923，从 1,225 条排除中抽 245 条，隐藏原判定重判。
- 纳入/排除一致 244/245；原因编号一致 236/245。唯一分歧（DEAN，知识图谱过时事实检测）补做全文判定后维持排除（I3）。
- 数据：[recheck_result.json](recheck_result.json)、`archive/recheck/`。

### 5.8 结果

- 最终纳入 108（数据库 95、其他途径 5、滚雪球 8）。
- 适配等级（按协议规则）：A 2（SWE-CI、SWE-Bench-CL）、B 31、C 23、D 52。
- 报告写作中纠正了一处错误引用：初稿把已被排除的 RoadmapBench 当作触顶参照，已替换为 EvoArena。

---

## 阶段 6：方案 v0.3

- SWE-Bench-CL 升为主素材；加入 ChainSWE；补充最接近的相关工作；新增第 13 节跨记忆系统扩展。
- 纠正一处过度表述：初稿写“16 个候选可直接做陷阱”，已改为“启发式统计，需人工筛选”。

---

## 阶段 7：许可证敏感性分析（用户追问“不考虑许可证会有变化吗”）

- 做法：保持其他规则不变，只去掉许可证条件（`sensitivity_license.csv`）。
- 结果：A 3、B 41、C 27、D 37；15 个资源升级，全部是原先因无许可证判为 D 的。
- 与方案相关的变化：TestEvo-Bench D→A（真实提交、可执行、Python）；EvoArena D→B（兼具工件变化与记忆）；EditPropBench D→B（依赖传播，可用 file 探针）；REVOKE D→C。
- 结论不变：即使不看许可证，仍然没有资源同时具备“记忆条件 + 工件漂移 + 可执行判分”。
- 使用边界：内部测试可以读取、运行这些公开仓库；发布派生 benchmark 时须先取得许可，或只发布“原仓库地址 + 提交号 + 转换脚本”。

---

## 阶段 8：许可证口径的决定（用户决定）

- 用户同意把 TestEvo-Bench、EvoArena、EditPropBench 写进方案，但决定**构建仍以许可证为准**，并要求构建后随附说明，讲清构成、来源和权威性。
- 落实：TEST_PLAN 升为 v0.4。三项资源列为“待许可”（MAIN-TE、EXP-EVO、EXP-PROP），取得作者书面许可之前只做内部可行性评估；新增第 14 节，规定构建规则、`PROVENANCE.md` + `provenance.csv` 的字段（构成、上游版本、许可证、使用内容、改动、分发形式、发表状态、检索等级、选取依据、已知问题、核验深度）以及发布前的验收项。

---

## 阶段 9：P0 第一步——SWE-CI 镜像架构与本机运行（用户批准下载并启动 Docker Desktop）

| 动作 | 结果 |
|---|---|
| 查本机与代码 | 本机 Apple M4 Pro（arm64）；Docker CLI 已装但守护进程未运行；SWE-CI 代码未写死镜像平台；官方运行器在非 Linux 上抛出 NotImplementedError |
| 选镜像 | HF paths-info 查询 100 个 `image.tar.gz`：346–595MB，合计 37.5GB；选最小的 `netbox-community__pynetbox__2cada4__fb8aa8` |
| 下载 | 经用户批准下载 346,034,810 字节到会话临时目录。原计划读到架构字段就停止，**实际下载了完整文件** |
| 读架构 | `manifest.json` → config `sha256:ba275d06…`：`architecture: amd64`，`os: linux`，Python 3.10.19，工作目录 `/app`，创建于 2026-01-15 |
| 启动 Docker Desktop | `open -a Docker`；服务端 29.7.2 linux/arm64，14 核，约 8GB 内存；设置文件中未找到 Rosetta 开关的记录 |
| 下载 `code.zip` | 1,001,808 字节；含完整 git 历史 651 个提交，HEAD 为最新提交 `34685b4`，base 与 target 都在其中 |
| 运行实测 | 载入 5 秒；启动 amd64 容器 3 秒（`x86_64`）；HEAD 全量测试 137 通过、99 报错（集成测试需 netbox-docker）；排除集成测试后，base 249 通过（约 2 秒），target 265 通过（约 1 秒） |
| 过程中的错误 | 第一次在容器内切换提交时，git 因 safe.directory 拒绝操作，两次测试实际都跑在 HEAD 上，结果作废；改为在宿主机切换后复制进容器，重跑得到上面的结果 |

结论：amd64 镜像可以在本机转译运行，速度满足判分需要，不必改用 Linux 机器或重建镜像。局限：只验证了 1 个镜像。

镜像已载入本机 Docker（约 1.06GB），下载文件在会话临时目录中。

---

## 附：本记录涉及的全部文件

| 位置 | 内容 |
|---|---|
| `literature/benchmark-sr/PROTOCOL.md` | 检索协议与修订 |
| `literature/benchmark-sr/REPORT.md` | 系统检索报告 |
| `literature/benchmark-sr/RESEARCH_RECORD.md` | 本文件 |
| `literature/benchmark-sr/search-log.csv`、`records.csv`、`decisions.tsv`、`ft_decisions.tsv`、`other_methods.tsv`、`snowball.tsv`、`extraction.csv`、`recheck_result.json`、`sensitivity_license.csv` | 检索与筛选的全部判定数据 |
| `literature/benchmark-sr/tools/` | `search.py`、`acl.py`、`merge.py`、`screen.py`、`ft_dump.py`、`extract.py` |
| `literature/benchmark-sr/raw/` | 原始检索结果、缓存、合并后的记录 |
| `literature/benchmark-sr/archive/` | README 原文、全文筛选摘要批次、滚雪球候选、许可证查询结果、论文代码链接、重判样本 |
| `research/TEST_PLAN_NEXT.md` | 测试方案 v0.3 |
| `research/tools/` | SWE-CI 漂移脚本、元数据、12 对抽样结果 |

**未归档、可重建的材料：** 9 个克隆仓库（按上表提交号重新克隆）；arXiv 全文 HTML（`archive/arxiv_html_fetched_ids.txt` 列出了编号，从 `https://arxiv.org/html/<id>` 重新抓取）；ACL 书目文件（按上面的 SHA-256 核对版本）。

**AI 使用声明：** 检索、筛选、提取、分析与本记录由 Claude 完成；协议和关键决定由用户确认；筛选判定未经人工复核。
