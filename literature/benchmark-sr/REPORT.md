# 可用于评测 GMR 的记忆失效类评测资源：系统检索报告

2026-09-23。按 [PROTOCOL.md](PROTOCOL.md)（检索前 SHA-256 `21e2e03b…`，修订见其第 10 节）执行，按 PRISMA-ScR 报告。筛选者为 Claude 一人；报告中所有数字都可以由本目录下的文件重算。

## 1. 结论摘要

1. **没有任何现成资源能直接替代自建主实验。** 108 个纳入资源中，按预先写死的规则评为 A 级的只有 2 个：SWE-CI 和 SWE-Bench-CL。它们都是“代码随时间演化”的任务源，本身不含“记忆 + 过期”的实验条件（SWE-Bench-CL 带一个 FAISS 语义记忆模块，但测的是遗忘与迁移，不是交还过期记忆）。
2. **同时具备“外部工件变化”和“记忆层”两个要素的资源只有 4 个**：SWE-Bench-CL（A）、OSAC-Bench（B，许可证不明）、EvoArena（D，无许可证）、ChurnBench（D，仓库未定位）。
3. **记忆过期类基准大量存在，但几乎都发生在对话里。** 34 个资源的失效发生在对话文字，15 个在模型参数，19 个混合；GMR 能够探测的（D2 为“能”）只有 7 个。
4. **可插入外部记忆层（D7 为“有”）的有 14 个**，可以作为“跨记忆系统叠加 GMR”扩展的框架候选。其中 agent-memory-bench、MERIT、sandbox-universe 的判分是确定性的，许可证宽松。
5. **与 GMR 主张最接近的工作都还没有公开代码**：SkillDrift（技能引用的包/API/配置漂移即契约违反）、GPM-ReleaseBench（来源绑定、撤回后不复活）、FixedBench（问题已修复后的陈旧 issue）。ReclaimEval（保留可重算的来源而不是结论）已公开，Apache-2.0。论文的相关工作部分必须覆盖这几项。

所以上一轮“自建任务、复用组件”的结论成立，而且这次是按预先写定的规则推出来的。但检索改变了三处具体做法，见第 7 节。

## 2. 检索与筛选流程（PRISMA-ScR）

```
数据库检索识别                                        其他途径识别
  arXiv 395 · OpenAlex 400 · OpenReview 200             上一轮审阅的已知条目（召回漏检）6
  ACL Anthology 58 · GitHub 30 · Hugging Face 443       引用追溯（Byam/BigBag/BreakGuard → BUMP）1
  Semantic Scholar 0（429 限速，改用 OpenAlex）
  Papers with Code 0（服务已停止）
  合计 1,526 条
        │ 去除重复 135
        ▼
标题/摘要筛选 1,391 ──排除 1,225──►  I2 654 · I1 319 · E6 107 · I3 72 · I4 49 · E1 15 · E5 9
        │
        ▼
全文评估 166 ──排除 71──►  I1 34 · I2 27 · E6 6 · I3 3 · E2 1
        │                                                其他途径 7 ──排除 2（I2 1 · I1 1）
        ▼                                                          │
数据库纳入 95 ────────────────────────────────────────── + 其他途径纳入 5
        │
        ▼ 滚雪球（对 A/B 级种子）
  第 1 轮：后向 396 + 前向 44 条新记录 → 全文 12 → 纳入 8（其中 B 级 1 个：CoUpJava）
  第 2 轮：以 CoUpJava 为种子，28 条参考文献 + 0 条施引 → 纳入 0，满足停止规则
        │
        ▼
最终纳入 108（数据库 95 + 其他途径 5 + 滚雪球 8）
```

**已知条目召回：** 上一轮已知的 16 个资源中，检索式自行找回 10 个（62.5%）。漏检的 6 个（MemoryCode、Stale Constraints、MemoryArena、Invalidation Contracts、REVOKE、GiulioDER/agent-memory-bench）按“其他途径”计入，不计入数据库检索数。这说明检索式对“没有用标准术语自我描述的仓库”和部分新预印本敏感度不足，属于局限。

**筛选一致性（自身一致性，不是评分者间信度）：** 从 1,225 条标题摘要排除中，用固定种子（20260923）随机抽取 245 条（20%），在看不到原判定的情况下重判。纳入/排除一致 244/245（99.6%），排除原因编号一致 236/245（96.3%）。唯一不一致的一条（DEAN，知识图谱过时事实检测）补做全文判定后维持排除（非 LLM，I3）。明细见 [recheck_result.json](recheck_result.json)。

## 3. 对协议的偏离（均在协议第 10 节登记）

| 偏离 | 影响 |
|---|---|
| Semantic Scholar 持续 429，改用 OpenAlex | OpenAlex 相关度排序较弱，前 100 条里无关记录多（如优化算法、物联网综述），可能降低查全率 |
| OpenReview 用 API 而非限定会议的网站搜索，count=10000 | 混入 2023 年前的旧记录，按 I4 排除 49 条 |
| OpenAlex 对 arXiv 预印本无参考文献列表 | 后向滚雪球改为解析 arXiv HTML 参考文献条目，仅覆盖有 HTML 全文的种子（17 篇） |
| HF 数据集无数据卡的记录，在标题摘要阶段增设规则“无卡且无关联论文 → I1”，并回溯应用于前批 | 回溯修改 15 条（均为从 FT 改为 EX）；规则在全文阶段开始前确定 |
| 代码领域 API 演化方法论文，在标题摘要阶段内统一改为进入全文 | 4 条从 EX 改为 FT，全文阶段再判定 |

## 4. SQ1：失效发生在哪里

| D1 | 数量 | 代表资源 |
|---|---:|---|
| 外部工件（代码、文件、API、数据库、系统状态） | 40 | SWE-CI、SWE-Bench-CL、ChainSWE、GitChameleon 2.0、TimeMachine-bench、BUMP、OSAC-Bench、ChurnBench、SkillDrift |
| 对话文字 | 34 | LongMemEval、MemoryAgentBench、STALE、StateMemBench、MemConflict、Supersede、agent-memory-bench、REVOKE |
| 混合 | 19 | CodeUpdateArena、HoH、Stale Constraints、GPM-ReleaseBench、ReclaimEval、MERIT |
| 模型参数 | 15 | TiC-LM、KNOT、EDAPIBench、MUDAPIBench、EvolveBench、DynamicQA |

外部工件类的 40 个资源几乎都是“代码/库版本演化”基准，测的是模型能否写出适配新版本的代码，而不是“持有旧记忆的 agent 能否发现记忆过期”。两类构念分属不同的研究社区：代码演化这边没有记忆条件，记忆这边的变化没有落在工件上。**GMR 恰好处在这两块之间的空白处。**

GMR 可探测性（D2）：能 7、部分 40、不能 61。“部分”主要有两种情况：变化发生在依赖库（需要改用锁文件或 `vendor/` 路径，`.venv` 已验证不可解析），以及 Java/Rust 等 ast-map 覆盖尚未核实的语言。

## 5. SQ2：判分、可得性、许可证、触顶

- **判分（D3）：** 精确匹配或确定性规则 52，可执行测试 34，LLM 评审 1，人工 2，未核实 19。记忆类新基准明显转向确定性判分（MemRiskBench、sandbox-universe、agent-memory-bench、StateMemBench），与 GMR“可重算”的立场一致。
- **可得性（D4）：** 代码和数据 68，仅数据 9，仅论文或未定位到公开链接 31。
- **许可证（D5）：** 宽松 47，无许可证 16，不明或其他（NOASSERTION、GPL、CC-BY-NC、匿名仓库）14，未定位 31。**无许可证的 16 个按规则一律降为 D 级**，包括 REVOKE、TestEvo-Bench、EditPropBench、MemConflict、EvoArena、RustEvo²。
- **触顶（D9）：** 已报告的最好成绩普遍不高（STALE 55.2%、GitChameleon 2.0 48–51%、BeyondSWE 56.65、EvoArena 平均 39.6%），没有发现 ≥ 90% 的高触顶风险，唯二例外是 Supersede 的全上下文基线约 92%，以及 MERIT 报告的单事实召回触顶。**这与我们 AMB 实验两组都 100% 形成对照，说明触顶来自任务设计，不是这个方向天然测不出差异。**

## 6. SQ3：能否插入外部记忆层

D7 为“有”的 14 个：agent-memory-bench、MERIT、sandbox-universe、SACAM、AgentMemoryBench（s010m00n）、agent-memory-trigger-bench、PrecisionMemBench、jrosenbizzle/agent-memory-bench、agentmem、agent-memory-benchmarker、adopt-bench、ForgetEval、AgentNativeMemory、DRIFTBENCH。前 11 个有公开代码。

用于“跨记忆系统叠加 GMR”扩展的推荐顺序（按判分确定性、许可证、是否已接入真实记忆产品）：

1. **agent-memory-bench**（Apache-2.0）：已接入 mem0、zep、cognee、supermemory、claude_mem 等产品的 adapter，可执行判分。
2. **MERIT**（MIT）：预注册，确定性环境，含 updated-fact 难度层，完整公开轨迹。
3. **sandbox-universe**（MIT）：lane 插件机制；注意作者同时是被测记忆系统的作者（已在 README 披露）。
4. **AgentMemoryBench（s010m00n）**（MIT）：含 repair 模式和知识冲突消解。

## 7. 对 TEST_PLAN_NEXT 的影响

| 协议第 9 节的预设 | 结果 | 对方案的改动 |
|---|---|---|
| 出现 A 级资源时 TEST_PLAN 必须改 | A 级为 SWE-CI、SWE-Bench-CL | SWE-CI 已是主素材，保持；**SWE-Bench-CL 从“补充候选”升为主素材之一**；另加 **ChainSWE**（B 级，数据 MIT）作为多 bug 链素材 |
| 结论可能仍是自建 | 规则推出的结论仍是自建（没有资源同时满足记忆条件、工件漂移、可执行判分和宽松许可证） | 主实验设计不变 |
| — | 新发现与 GMR 最接近的工作（SkillDrift、GPM-ReleaseBench、FixedBench、ReclaimEval、OSAC-Bench） | 写入相关工作，避免新颖性过度声称；OSAC-Bench 的“系统指纹变化后拒绝陈旧事实”可作为非代码探针（HTTP/SQL/file）的设计参照（许可证需确认） |
| — | 14 个带记忆 adapter 的框架 | 新增“跨记忆系统叠加 GMR”扩展，首选 agent-memory-bench |
| — | C 级记忆基准 23 个（STALE、StateMemBench、Supersede、LongMemEval 等） | 附录 L3 从中选 2–3 个移植，用于声明适用范围 |

## 8. 局限

1. **单一筛选者。** 自身一致性 99.6% 不能替代独立的第二位筛选者。
2. **查全率。** 已知条目召回 62.5%；各数据源只筛前 50–100 条；OpenAlex 排序弱；知网等中文数据库未覆盖；Papers with Code 已停止服务。
3. **时间窗口。** 大量资源是 2026 年的预印本（D8：预印本 65、同行评审 26、仅代码仓库 17），部分可能很快更新或撤回。
4. **提取深度。** D 字段依据摘要、README、数据卡，未逐篇读方法全文；19 条的判分方式标为“未核实”；31 条未定位到公开链接，其中有些论文声称已开源（ChurnBench、DriftMedQA、CODEMENV），链接在摘要里被截断。这些资源可能被低估为 D 级。
5. **后向滚雪球只覆盖有 arXiv HTML 的种子**；非 arXiv 种子（GitHub、HF 仓库）没有参考文献可追溯。
6. **E5 排除 9 条非代码领域的权重级知识编辑基准**（如 LeKUBE、CoME）。这是协议预设的范围选择，读者如果认为这类基准相关，需要另行检索。

## 9. 文件

| 文件 | 内容 |
|---|---|
| [PROTOCOL.md](PROTOCOL.md) | 协议与修订 |
| [search-log.csv](search-log.csv) | 每条检索式、命中数、筛选数 |
| [records.csv](records.csv) | 1,391 条数据库记录的标题摘要与全文判定 |
| [ft_decisions.tsv](ft_decisions.tsv) | 全文判定与说明 |
| [other_methods.tsv](other_methods.tsv) | 其他途径 7 条 |
| [snowball.tsv](snowball.tsv) | 两轮滚雪球 |
| [extraction.csv](extraction.csv) | 108 条纳入记录的 D1–D9 与适配等级（等级由 `tools/extract.py` 按规则计算） |
| [recheck_result.json](recheck_result.json) | 20% 盲重判结果 |
| `tools/` | 检索、去重、筛选、提取脚本 |
| `raw/` | 原始检索结果与缓存 |

AI 使用声明：检索、筛选、提取和本报告由 Claude（Anthropic）在用户授权下完成，用户确认了协议；所有判定未经人工复核。

## 10. 补充：许可证敏感性分析

去掉许可证条件、其他规则不变时：A 3、B 41、C 27、D 37（[sensitivity_license.csv](sensitivity_license.csv)）。15 个资源升级，均为原先因无许可证判 D 者。其中 TestEvo-Bench 升为 A（真实提交、可执行、Python），EvoArena 升为 B（兼具工件变化与记忆条件），EditPropBench 升为 B，REVOKE 升为 C。第 1 节的核心结论不变。详细过程见 [RESEARCH_RECORD.md](RESEARCH_RECORD.md) 阶段 7。
