# 检索协议：可用于评测 GMR 的记忆失效类评测资源

版本 1.0 / 2026-09-23。本协议在检索开始**之前**写定。开始检索后的任何修改都追加到第 10 节，并注明原因；已筛选的记录不回改。

类型：范围综述（scoping review）式的系统检索，按 PRISMA-ScR 报告。只做检索、筛选和数据提取，**不做 meta 分析，也不做偏倚风险（RoB）评分**：对象是评测资源而不是干预研究，RoB 2 和 ROBINS-I 不适用。

## 1. 为什么要做这次检索

上一轮外部资料是几次临时关键词搜索的结果，挑选标准是边搜边定的，而且按“和 GMR 像不像”筛，天然偏向“现成的都不合适”这个结论。本协议把**纳入**（这个资源测不测记忆失效）和**适配**（它能不能用来测 GMR）拆开：纳入不看 GMR，适配在纳入之后按第 6 节的固定规则分级。

## 2. 研究问题

**主问题：** 公开的评测资源（基准、数据集、测试套件、评测协议）中，有哪些测量 LLM 或 agent 在“先前获得或存储的信息因底层事实变化而失效”时的行为？其中哪些可以复用或改造来评测 GMR？

**子问题：**

- SQ1：这些资源里，失效发生在什么地方——对话文字、外部工件（代码、文件、API、数据库），还是模型参数？
- SQ2：它们如何判分、是否公开、使用什么许可证、最好成绩是否已经接近满分？
- SQ3：有没有资源允许把一个外部记忆层（adapter）插进来，与其他记忆系统并列比较？这一点直接服务于后续“跨记忆系统叠加 GMR”的扩展。

GMR 背景：GMR 把记忆绑定到可探测的事实坐标（代码 AST、文件或 JSON 路径、HTTP、SQL），坐标变化时把记忆交还给人复核。它不存储、也不检索记忆内容。

## 3. 纳入标准（必须全部满足）

| 编号 | 标准 |
|---|---|
| I1 | **资源类型**：提出或发布了评测资源（任务、数据集、测试套件或评测协议），并且描述了任务构造。只在现有基准上评测自己方法的论文不纳入，但会顺着它追溯所用的基准 |
| I2 | **构念**：至少一个任务条件满足以下之一：(a) 先前给出或存储的信息后来过期、被取代、被推翻或失效；(b) 代码、API、库、配置或仓库随时间演化，使先前的知识不再正确 |
| I3 | **对象**：LLM、LLM agent，或 LLM 使用的记忆系统 |
| I4 | **时间**：2023-01-01 至检索日（2026-09-23） |
| I5 | **语言**：英文或中文 |

## 4. 排除标准（满足任一即排除）

| 编号 | 标准 |
|---|---|
| E1 | 只测静态检索或回忆，没有任何“随时间变化”的条件 |
| E2 | 只测对固定事实的时间推理（时间计算、事件排序），没有信息更新 |
| E3 | 非 LLM 对象（传统 IR、人类实验） |
| E4 | 找不到主来源（只有博客、营销页或社交媒体帖子） |
| E5 | 代码/API 领域以外的**参数化知识编辑**基准（例如 CounterFact、zsRE 一类只改模型权重的）。理由：GMR 作用于外部记忆，与改权重的构念不同。**代码/API 领域的知识编辑基准不排除**，因为它们的 API 变化可以作为工件漂移素材 |
| E6 | 重复记录或同一资源的其他版本：合并为一条，保留最新的官方版本 |

## 5. 检索策略

### 5.1 数据源

| 数据源 | 访问方式 | 每条检索式的筛选上限 |
|---|---|---|
| arXiv | 官方 API（`export.arxiv.org/api/query`），按相关度排序 | 前 100 条 |
| Semantic Scholar | Graph API `/paper/search` | 前 100 条 |
| OpenReview | 网站搜索（ICLR/NeurIPS/COLM 2024–2026） | 前 50 条 |
| ACL Anthology | 网站搜索 | 前 50 条 |
| GitHub | 搜索 API（`/search/repositories`，按 best match） | 前 50 条 |
| Hugging Face Datasets | Hub API（`/api/datasets?search=`） | 前 50 条 |
| Papers with Code | 2025 年已停止服务，数据迁到 Hugging Face。检索时先确认状态；不可用就记录为“不可用”，不找替代品凑数 | — |

总命中数按各数据源返回的原样记录。只筛选前 N 条是**有意截断**，会作为局限报告。不声称穷尽。

### 5.2 检索式（四组，各数据源按语法改写，改写后的原文逐条记入 search-log）

- **G1 记忆失效**：(`agent memory` OR `long-term memory` OR `memory system` OR `conversational memory`) AND (`stale` OR `outdated` OR `obsolete` OR `superseded` OR `knowledge update` OR `conflict resolution` OR `invalidation` OR `forgetting`) AND (`benchmark` OR `dataset` OR `evaluation`)
- **G2 代码演化**：(`code` OR `API` OR `library` OR `repository`) AND (`version` OR `evolution` OR `deprecated` OR `breaking change` OR `update` OR `drift`) AND (`benchmark` OR `dataset`) AND (`LLM` OR `agent`)
- **G3 多会话编码**：(`multi-session` OR `continual` OR `long-horizon` OR `cross-session` OR `sequential`) AND (`coding agent` OR `software engineering agent` OR `SWE-bench`) AND `benchmark`
- **G4 文档与配置漂移**：(`documentation` OR `configuration` OR `specification` OR `README`) AND (`drift` OR `inconsistency` OR `outdated` OR `stale`) AND (`LLM` OR `agent`) AND (`benchmark` OR `dataset`)

### 5.3 滚雪球

对最终纳入且适配等级为 A 或 B 的资源，做一轮后向检索（它的参考文献）和一轮前向检索（Semantic Scholar 上引用它的文献）。**停止规则**：某一轮滚雪球没有新增任何纳入记录。如果两轮之后仍有新增，就停在第二轮，并报告“未饱和”。

### 5.4 去重对照

先与已有记录去重：`literature/matrix.csv`（28 条）和 `research/TEST_PLAN_NEXT.md` 第 1–2 节。已经审阅过的资源照样重新筛选，按本协议的标准重新判定，不沿用上一轮的结论。

## 6. 数据提取与适配分级（仅对纳入的记录）

| 字段 | 取值 |
|---|---|
| D1 失效发生处 | 对话文字 / 外部工件（代码、文件、API、数据库） / 模型参数 / 混合 |
| D2 GMR 能否探测该工件 | 能（代码 AST、文件或 JSON、HTTP、SQL） / 部分 / 不能 |
| D3 判分方式 | 可执行测试 / 精确匹配 / LLM 评审 / 人工 |
| D4 可得性 | 代码和数据 / 仅数据 / 仅论文 |
| D5 许可证 | 原样记录；没有许可证记为“无” |
| D6 交互形态 | agent 多轮 / 单轮 |
| D7 能否插入外部记忆层 | 有 adapter 接口 / 需要改造 / 不能 |
| D8 发表状态 | 同行评审 / 预印本 / 仅代码仓库 |
| D9 触顶风险 | 报告的最好成绩；≥ 90% 标为高 |

**适配等级（在看到任何检索结果之前写定）：**

- **A 可直接作主实验**：D1 为外部工件，D2 为“能”，D3 为可执行测试，D4 为代码和数据，D5 为宽松许可证（MIT、Apache、BSD、ISC、CC-BY）。
- **B 可作素材或组件**：满足 A 的部分条件，而且至少满足以下之一：D1 为外部工件；D7 为有 adapter 接口；D3 为可执行测试且 D5 宽松。
- **C 可作附录或范围说明**：D1 为对话文字或混合，D4 至少有数据，D5 允许使用。
- **D 仅引用**：不满足以上任何一级（包括 D4 为仅论文，或 D5 为无）。

## 7. 筛选流程

1. **标题与摘要筛选**：按 I1–I5、E1–E6 判定；不确定的一律进入全文阶段。
2. **全文筛选**：论文读摘要、方法中的任务构造部分、数据可得性声明；代码仓库读 README、数据样例和 LICENSE。
3. 每条记录记下判定和原因编号（例如 `E1`、`I2 不满足`）。

**筛选者：** 单一筛选者（Claude）。这是本研究的主要局限之一。补救措施：全部排除记录的原因都公开；随机抽取 20% 的排除记录，在全部筛选结束后由同一筛选者**盲于原判定**再判一次，报告一致率。这只能测到自身一致性，不能替代独立的第二位筛选者；如需要，由你或另一位人员复核。

## 8. 输出文件（目录 `literature/benchmark-sr/`）

| 文件 | 内容 |
|---|---|
| `PROTOCOL.md` | 本文件 |
| `search-log.csv` | 日期、数据源、检索组、实际检索式、总命中数、筛选数、备注 |
| `records.csv` | 去重后的每条记录：ID、标题、年份、URL、来源、与已有记录的重复情况、标题摘要判定、全文判定、原因编号 |
| `extraction.csv` | 纳入记录的 D1–D9 和适配等级 |
| `REPORT.md` | PRISMA-ScR 流程计数、各子问题的结果、局限，以及对 TEST_PLAN_NEXT 的影响 |

## 9. 协议自检（Devil's Advocate checkpoint 1）

| 风险 | 处理 |
|---|---|
| 构念 I2 过宽，会纳入大量对话式“知识更新”基准 | 有意为之。宽纳入、按适配分级，才能回答“为什么不直接用现成的” |
| E5 排除参数化知识编辑，可能被质疑为挑选 | 在 REPORT 中单独报告 E5 排除的数量和代表性例子 |
| 各数据源的相关度排序截断会漏检 | 通过滚雪球补救，并报告截断上限 |
| 单一筛选者 | 见第 7 节，作为局限报告 |
| 预印本多、质量参差 | D8 单独记录；预印本不会因此被排除，但会标明 |
| 结论可能仍然是“自写” | 可以接受，只要是由第 6 节的规则推出来的；如果出现 A 级资源，TEST_PLAN_NEXT 必须改 |
| 中文数据库（知网等）不可访问 | 作为局限报告，只能覆盖英文数据源中的中文作者成果 |

## 10. 修订记录

（检索开始后如有修改，追加于此。）

### 修订 1（2026-09-23，检索执行中）

- **Semantic Scholar → OpenAlex。** S2 Graph API 对未认证请求持续返回 HTTP 429（约 10 分钟内 7 次指数退避，另有一次手动请求同样 429），无法取得结果。改用 OpenAlex `/works?search=`：检索式与原 S2 相同，限 `from_publication_date:2023-01-01`，筛前 100 条。第 5.3 节的前向和后向滚雪球同样改用 OpenAlex（`referenced_works`、`cites:`）。局限：OpenAlex 的相关度排序明显弱于 S2（测试检索排第一的是无关论文），可能降低前 100 条的查全率。
- **ACL Anthology 的执行方式（实施细节，不改变标准）。** 下载官方 `anthology+abstracts.bib.gz`（2026-09-22 版，SHA-256 `dd753c17…373ad`），在本地对标题和摘要按 G1–G4 的布尔式匹配；允许检索词带复数 s；按匹配到的不同检索词数量排序，取前 50 条。
- 这两项修改发生在任何筛选之前，没有看过任何检索结果的判定。
- **OpenReview 的执行方式与协议不符（补记）。** 协议写的是“网站搜索、限 ICLR/NeurIPS/COLM 2024–2026”，实际使用的是 API v2 `/notes/search?term=…&source=forum`，没有加会议限制；每组都返回 count=10000（按任意词匹配），取前 50 条。影响：可能混入非目标会议的记录，由筛选阶段处理，不影响纳入标准。
- **GitHub 与 Hugging Face。** GitHub 仓库搜索要求所有词同时出现，每组 3 条检索式命中 0–13 条，全部筛选。HF 的 `search=` 只匹配数据集 ID 的子串，因此 `version`、`config` 等词会带来大量无关结果，由筛选阶段排除。
