"""Write extraction.csv. D-fields are the screener's reading of abstract/README/card (basis column);
fitness grade is computed ONLY from the fields by the PROTOCOL §6 rules (no manual override)."""
import csv
PERM = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC-BY-4.0"}
NOLIC = {"none", "无"}
def grade(d1, d2, d3, d4, d5, d7):
    if d4 == "仅论文" or d5 in NOLIC:
        return "D"
    perm = d5 in PERM
    if d1 == "工件" and d2 == "能" and d3 == "可执行" and d4 == "代码和数据" and perm:
        return "A"
    if d1 == "工件" or d7 == "有" or (d3 == "可执行" and perm):
        return "B"
    if d1 in ("对话", "混合"):
        return "C"
    return "D"
# id | name | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | repo | basis/note
R = """
acl:bian-etal-2026-realmem|RealMem|对话|不能|未核实|代码和数据|不明|单轮|改造|同行评审|未提取|anonymous.4open.science/r/realmem-A1E4|摘要；匿名仓库许可不明
acl:diao-etal-2025-guidebench|GuideBench|对话|不能|未核实|代码和数据|MIT|单轮|不能|同行评审|未提取|Dlxxx/GuideBench|摘要；规则更新子任务未核实
acl:lu-etal-2025-transbench|TransBench|工件|不能|未核实|仅论文|未定位|agent多轮|不能|同行评审|未提取||GUI 版本更新，GMR 无 UI 探针
arxiv:2404.03577|KNOT|参数|不能|精确匹配|代码和数据|GPL-3.0|单轮|不能|同行评审|未提取|THU-KEG/KNOT|摘要；GPL
arxiv:2406.07411|VersiCode|工件|部分|可执行|代码和数据|Apache-2.0|单轮|不能|预印本|未提取|wutong8023/VersiCode|库版本；GMR 需锁文件或 vendor 路径
arxiv:2406.09834|Deprecated-API-LLM|工件|部分|精确匹配|代码和数据|不明|单轮|不能|同行评审|未提取|anonymous.4open.science|145 组 API 映射
arxiv:2407.06249|CodeUpdateArena|混合|不能|可执行|代码和数据|MIT|单轮|不能|同行评审|未提取|leo-liuzy/CodeUpdateArena|合成更新以文档给出，测参数编辑
arxiv:2410.10813|LongMemEval|对话|不能|LLM评审|代码和数据|MIT|单轮|改造|同行评审|未提取|xiaowu0162/LongMemEval|knowledge update 子集
arxiv:2502.16645|CodeSyncBench|工件|部分|可执行|代码和数据|MIT|单轮|不能|预印本|未提取|CGCL-codes/naturalcc|220 个真实 API 更新
arxiv:2503.04800|HoH|混合|不能|精确匹配|代码和数据|Apache-2.0|单轮|不能|同行评审|未提取|0russwest0/HoH|RAG 中过时文档
arxiv:2503.16922|RustEvo²|工件|部分|可执行|代码和数据|none|单轮|不能|预印本|未提取|SYSUSELab/RustEvo|Rust；无 LICENSE
arxiv:2504.02107|TiC-LM|参数|不能|精确匹配|代码和数据|不明|单轮|不能|同行评审|未提取|apple/ml-tic-lm|许可 NOASSERTION
arxiv:2504.09283|SemanticCommit|混合|部分|人工|仅论文|未定位|单轮|不能|预印本|未提取||初始基准未定位；意图规格文件可用 file 探针
arxiv:2505.09569|MigrationBench|工件|部分|可执行|代码和数据|Apache-2.0|agent多轮|不能|预印本|未提取|amazon-science/MigrationBench|Java；ast-map 对 Java 覆盖未核实
arxiv:2506.07270|TemporalWiki/UnifiedClark|混合|不能|精确匹配|代码和数据|MIT|单轮|不能|预印本|未提取|atahanoezer/TQA|
arxiv:2507.00014|SWE-Bench-CL|工件|能|可执行|代码和数据|MIT|agent多轮|改造|预印本|未提取|thomasjoshi/agents-never-forget|Python 仓库时序任务流；自带 FAISS 记忆模块
arxiv:2507.05257|MemoryAgentBench|对话|不能|精确匹配|代码和数据|MIT|单轮|改造|同行评审|CR 单跳约 60%|HUST-AI-HYZ/MemoryAgentBench|ICLR 2026
arxiv:2507.12367|GitChameleon2.0|工件|部分|可执行|代码和数据|Apache-2.0|agent多轮|不能|同行评审|48–51%|mrcabbage972/GitChameleonBenchmark|ACL 2026
arxiv:2510.01353|MEMTRACK|混合|部分|未核实|仅论文|未定位|agent多轮|改造|预印本|未提取||Slack/Linear/Git 时间线
arxiv:2511.03182|CodeAPIEditBench|混合|不能|可执行|仅论文|未定位|单轮|不能|预印本|未提取||140 个合成 API 修改
arxiv:2511.06668|MedContradictionRAG|混合|不能|未核实|代码和数据|none|单轮|不能|预印本|未提取|pub2026/MedicalContradictionDetection-RAG|
arxiv:2511.10523|ConvoMem|对话|不能|精确匹配|代码和数据|CC-BY-NC-4.0|单轮|改造|预印本|full-context 70–82%|SalesforceAIResearch/ConvoMem|非商业许可
arxiv:2511.21022|EDAPIBench|参数|不能|可执行|代码和数据|Apache-2.0|单轮|不能|预印本|未提取|GuanchengLin/EDAPIBench|
arxiv:2601.00205|DepDec-Bench|工件|部分|未核实|代码和数据|不明|agent多轮|不能|预印本|未提取|anonymous.4open.science|安全状态随时间变化
arxiv:2601.22597|TimeMachine-bench|工件|部分|可执行|代码和数据|Apache-2.0|agent多轮|不能|同行评审|未提取|tohoku-nlp/timemachine-bench|依赖更新致测试失败，Python
arxiv:2602.09930|JMigBench|工件|部分|精确匹配|代码和数据|none|单轮|不能|预印本|同一迁移 11%|NishilAmin1213/JMigBench|无 LICENSE
arxiv:2603.03194|BeyondSWE|工件|部分|可执行|代码和数据|不明|agent多轮|不能|预印本|最佳 56.65|AweAI-Team/BeyondSWE|仅迁移子集相关
arxiv:2603.03823|SWE-CI|工件|能|可执行|代码和数据|Apache-2.0|agent多轮|不能|预印本|未提取|SKYLENAGE-AI/SWE-CI|base→target 平均 71 次提交，Python
arxiv:2603.23848|BeliefShift|对话|不能|未核实|仅论文|未定位|单轮|不能|预印本|未提取||
arxiv:2604.09515|EvolvingAPI-Conflict|混合|部分|可执行|代码和数据|none|单轮|不能|预印本|可执行率 42.55–66.36%|AhmedNusayer/knowledge-conflict-codegen|
arxiv:2604.20006|Memora|对话|不能|未核实|代码和数据|Apache-2.0|单轮|改造|同行评审|未提取|geniesinc/Memora|FAMA 指标
arxiv:2605.02083|EditPropBench|工件|能|精确匹配|代码和数据|none|单轮|不能|预印本|未提取|kruthof/EditCoherenceBench|文档内事实依赖传播；可用 file 探针；无 LICENSE
arxiv:2605.06527|STALE|对话|不能|精确匹配|代码和数据|MIT|单轮|改造|预印本|最佳 55.2%|icedreamc/STALE|数据 CC-BY-4.0
arxiv:2605.07769|FixedBench|工件|部分|可执行|仅论文|未定位|agent多轮|不能|预印本|不当修改 35–65%||已修复的陈旧 issue
arxiv:2605.10990|SkillDrift|工件|能|可执行|仅论文|未定位|单轮|不能|预印本|精确率 100%/召回 76%||技能引用的包/API/配置漂移；与 GMR 最接近之一
arxiv:2605.11325|PrecisionMemBench|对话|不能|精确匹配|代码和数据|MIT|单轮|有|预印本|未提取|tenurehq/precisionMemBench|
arxiv:2605.13045|TempoMed-Bench|参数|不能|精确匹配|代码和数据|MIT|单轮|不能|预印本|未提取|GuanZihan/TempoMed-Bench|
arxiv:2605.14906|MemLens|对话|不能|精确匹配|代码和数据|MIT|单轮|改造|预印本|未提取|xrenaf/MEMLENS|多模态
arxiv:2605.20926|MemConflict|对话|不能|精确匹配|代码和数据|none|单轮|改造|预印本|未提取|TaoZhen1110/MemConflict|
arxiv:2605.29341|WorldMemArena|混合|不能|未核实|代码和数据|MIT|agent多轮|改造|预印本|未提取|UCSB-AI/WorldMemArena|
arxiv:2606.13681|EvoArena|工件|部分|未核实|代码和数据|none|agent多轮|改造|预印本|平均 39.6%|Aiden0526/EvoArena|终端/软件环境渐进更新
arxiv:2606.15903|ForgetEval|对话|不能|精确匹配|仅论文|未定位|单轮|有|预印本|91.7–93.2%||13 种记忆配置；仓库未定位
arxiv:2606.24775|AgentNativeMemory|对话|不能|精确匹配|代码和数据|none|单轮|有|预印本|未提取|OpenDataBox/MemoryData|另有第三方 loversky02/agent-memory-lab（MIT）
arxiv:2606.25402|LibEvoBench|工件|部分|未核实|仅数据|不明|单轮|不能|预印本|未提取|HF Anonymous-999/LibEvoBench|
arxiv:2606.25449|ReclaimEval|混合|部分|精确匹配|代码和数据|Apache-2.0|单轮|改造|预印本|未提取|collapseindex/reclaim-eval|“保留可重算来源”与 GMR 主张同构
arxiv:2606.27472|Supersede|对话|不能|精确匹配|代码和数据|Apache-2.0|agent多轮|改造|预印本|92%→77%|Vrin-cloud/supersede|RL 环境
arxiv:2607.01071|MemSyco-Bench|对话|不能|未核实|代码和数据|MIT|单轮|改造|预印本|未提取|XMUDeepLIT/MemSyco-Bench|
arxiv:2607.01213|RepoRescue|工件|部分|可执行|仅论文|未定位|agent多轮|不能|预印本|未提取||生态漂移后恢复历史测试
arxiv:2607.01935|LTP|对话|不能|未核实|仅论文|未定位|单轮|改造|预印本|未提取||
arxiv:2607.02469|TestEvo-Bench|工件|能|可执行|代码和数据|none|agent多轮|不能|预印本|未提取|AmberWJL/TestEvo-Bench|无 LICENSE
arxiv:2607.02606|ChainSWE|工件|能|可执行|仅数据|MIT|agent多轮|不能|预印本|随链长下降至多 70%|HF C-lister/ChainSWE|
arxiv:2607.04072|quantum-api-drift|工件|部分|可执行|代码和数据|none|单轮|不能|预印本|Pass@1 0.02–0.85|arasyi/quantum-api-drift|
arxiv:2607.09007|Bugs4Q-multiversion|工件|部分|可执行|代码和数据|Apache-2.0|单轮|不能|预印本|pass@10 48.8%|Z-928/Bugs4Q-Framework|基准标签随版本静默失效
arxiv:2607.12893|MemOps|对话|不能|精确匹配|代码和数据|MIT|单轮|改造|预印本|未提取|MemTensor/MemOps|
arxiv:2607.17957|DepBench|工件|部分|可执行|仅论文|未定位|单轮|不能|预印本|未提取||Docker 可执行 oracle
arxiv:2608.04003|PAST-Bench|混合|不能|未核实|仅论文|未定位|agent多轮|改造|预印本|未提取||
arxiv:2608.04574|SpatialStaleness|工件|不能|精确匹配|仅论文|未定位|agent多轮|不能|预印本|视觉 F1 0.067–0.887||
arxiv:2608.04746|TGT|对话|不能|精确匹配|仅论文|未定位|单轮|改造|预印本|82.3%||
arxiv:2608.12476|GPM-ReleaseBench|混合|部分|精确匹配|仅论文|未定位|单轮|改造|预印本|简单策略 1800/3600||来源绑定、撤回不复活，与 GMR 最接近之一
arxiv:2608.17671|PortingBenchmark|工件|部分|可执行|仅论文|未定位|单轮|不能|预印本|85.2%（Type-I）||
arxiv:2608.19652|StateMemBench|对话|不能|精确匹配|代码和数据|MIT|单轮|改造|预印本|未提取|microsoft/STATE-Bench|仓库对应关系待核
arxiv:2608.30497|Bridge|工件|部分|人工|代码和数据|none|单轮|不能|预印本|未提取|ROCK-SE/Bridge|数据集构建器
arxiv:2609.01852|MemoryTrustGap|混合|部分|精确匹配|仅论文|未定位|单轮|不能|预印本|陈旧值采纳 0.92–1.00||
arxiv:2609.11515|ChurnBench|工件|部分|精确匹配|仅论文|未定位|agent多轮|改造|预印本|未提取||append-only 真值账本；宣称开源但未定位
arxiv:2609.14976|MemRiskBench|对话|不能|精确匹配|代码和数据|none|agent多轮|改造|预印本|未提取|fuxue-mingzhu/MemRiskBench|
arxiv:2609.25786|MUDAPIBench|参数|不能|可执行|代码和数据|Apache-2.0|单轮|不能|预印本|未提取|YanzhongHe/MUDAPIBench|
gh:32andrii23/memory-freshness-lab|memory-freshness-lab|对话|不能|精确匹配|代码和数据|MIT|单轮|改造|仅代码仓库|未提取|32andrii23/memory-freshness-lab|adapter 在路线图
gh:benlloydg/sandbox-universe|SandboxUniverse|对话|不能|精确匹配|代码和数据|MIT|单轮|有|仅代码仓库|未提取|benlloydg/sandbox-universe|作者与被测记忆系统相同（已披露）
gh:dakshjain-1616/agent-memory-benchmarker|AgentMemoryBenchmarker|对话|不能|精确匹配|代码和数据|none|单轮|有|仅代码仓库|未提取|dakshjain-1616/agent-memory-benchmarker|
gh:firstbatchxyz/adopt-bench|adopt-bench|混合|部分|可执行|代码和数据|不明|agent多轮|有|仅代码仓库|未提取|firstbatchxyz/adopt-bench|README 标 Apache-2.0，GitHub 未识别
gh:jrosenbizzle/agent-memory-bench|jrosenbizzle-amb|对话|部分|精确匹配|代码和数据|MIT|单轮|有|仅代码仓库|未提取|jrosenbizzle/agent-memory-bench|接受记忆文件输入
gh:jsleekr/agentmem|agentmem|对话|不能|可执行|代码和数据|MIT|单轮|有|仅代码仓库|未提取|jsleekr/agentmem|记忆后端单元测试框架（Go）
gh:kevin1289/slicer-eval-harness|slicer-eval-harness|工件|部分|精确匹配|代码和数据|MIT|单轮|不能|仅代码仓库|expert 100%/naive 0%|kevin1289/slicer-eval-harness|
gh:likecheng110/osac-bench|OSAC-Bench|工件|部分|精确匹配|代码和数据|不明|agent多轮|改造|仅代码仓库|未提取|likecheng110/osac-bench|系统/运行时指纹变化后拒绝陈旧事实
gh:monika-bhardwaj/agentic-memory-benchmark|SACAM|对话|不能|精确匹配|代码和数据|MIT|agent多轮|有|仅代码仓库|无真实模型结果|monika-bhardwaj/agentic-memory-benchmark|
gh:smshweta/merit-bench|MERIT|混合|不能|精确匹配|代码和数据|MIT|agent多轮|有|仅代码仓库|单事实召回触顶|smshweta/merit-bench|预注册
hf:kushalicious/agent-memory-benchmark|kushalicious-amb|对话|不能|精确匹配|仅数据|MIT|单轮|不能|仅代码仓库|未提取|HF|仅 20 题
hf:notmehul/memory-bench|notmehul-memory-bench|对话|不能|精确匹配|仅数据|CC-BY-4.0|单轮|改造|仅代码仓库|未提取|HF|
hf:ruggsea/continual-eval|continual-eval|参数|不能|精确匹配|仅数据|MIT|单轮|不能|仅代码仓库|未提取|HF|
hf:solsticestudioai/mnemosyne-memory-lifecycle-benchmark|Mnemosyne|对话|不能|精确匹配|仅数据|不明|单轮|改造|仅代码仓库|未提取|HF|类别细节待核
hf:wallfacers/agent-memory-trigger-bench|agent-memory-trigger-bench|混合|部分|未核实|仅数据|CC-BY-4.0|agent多轮|有|仅代码仓库|未提取|HF|Claude Code/Codex/OpenCode + MCP 记忆
hf:xiaowu0162/longmemeval-v2|LongMemEval-V2|混合|不能|未核实|仅数据|Apache-2.0|agent多轮|改造|预印本|未提取|HF|
oa:W4389159862|Codeditor|工件|能|精确匹配|代码和数据|MIT|单轮|不能|同行评审|未提取|EngineeringSoftware/codeditor|跨语言实现的变更同步
oa:W4411119518|LibEvolutionEval|工件|部分|精确匹配|代码和数据|不明|单轮|不能|同行评审|未提取|amazon-science/LibEvolutionEval|
oa:W4412888714|CODEMENV|工件|部分|可执行|代码和数据|未核实|单轮|不能|同行评审|43.84%|未定位|摘要称数据在 GitHub，链接截断
oa:W4416293907|TemporalGap|参数|不能|精确匹配|仅论文|未定位|单轮|不能|同行评审|未提取||
oa:W7171826765|DRIFTBENCH|对话|不能|精确匹配|仅论文|未定位|单轮|有|预印本|未提取||5 种记忆架构
or:1zCrxCUNtW|StaleBench|对话|不能|精确匹配|仅论文|未定位|单轮|改造|预印本|未提取||TempLAMA 有效区间
or:2xvlW5hp0J|IsYourLLMOutdated|参数|不能|精确匹配|仅论文|未定位|单轮|不能|预印本|未提取||
or:6WYjBeIioq|CodeUnlearn-Bench|参数|不能|可执行|仅论文|未定位|单轮|不能|预印本|未提取||
or:MSXbrNExax|AgentMemoryBench(s010m00n)|混合|不能|未核实|代码和数据|MIT|agent多轮|有|预印本|未提取|s010m00n/AgentMemoryBench|repair 模式
or:Qf7hkFXLYC|ContinuousKnowledgeDrift|参数|不能|未核实|仅论文|未定位|单轮|不能|预印本|未提取||
or:ixIj874skc|DriftMedQA|参数|不能|精确匹配|仅论文|未定位|单轮|不能|预印本|未提取||摘要称数据公开，链接截断
or:l0Vfigga9Z|DeprecatedAPI-NL|工件|部分|未核实|仅论文|未定位|单轮|不能|预印本|未提取||
or:mAyyfhSGDC|DynamicQA|参数|不能|精确匹配|代码和数据|none|单轮|不能|同行评审|未提取|copenlu/dynamicqa|
arxiv:2502.13791|MemoryCode|对话|不能|精确匹配|代码和数据|Apache-2.0|单轮|不能|预印本|未提取|Cohere-Labs-Community/MemoryCode|其他途径
arxiv:2608.25553|StaleConstraints|混合|不能|精确匹配|代码和数据|CC-BY-4.0|单轮|不能|预印本|陈旧一致决策 74–77%|Zenodo 10.5281/zenodo.22147784|其他途径
gh:dextergao14/revoke|REVOKE|对话|不能|精确匹配|代码和数据|none|agent多轮|改造|仅代码仓库|脚本基线 1%|Dextergao14/REVOKE|其他途径；无 LICENSE
gh:giulioder/agent-memory-bench|agent-memory-bench|对话|不能|可执行|代码和数据|Apache-2.0|agent多轮|有|仅代码仓库|official-003 无显著差异|GiulioDER/agent-memory-bench|其他途径
gh:chains-project/bump|BUMP|工件|部分|可执行|代码和数据|MIT|单轮|不能|同行评审|未提取|chains-project/bump|引用追溯；Java
arxiv:2402.16797|SetTheClock|参数|不能|精确匹配|代码和数据|未核实|单轮|不能|同行评审|未提取|yizhongw/llm-temporal-alignment|滚雪球 R1
snow:freshbrew|FreshBrew|工件|部分|可执行|仅论文|未定位|agent多轮|不能|同行评审|未提取||滚雪球 R1；Java 迁移
snow:llms4code-editing|ModelEditing4LLMs4Code|参数|不能|可执行|仅论文|未定位|单轮|不能|同行评审|未提取||滚雪球 R1；ICSE 2025
snow:evolvebench|EvolveBench|参数|不能|精确匹配|仅论文|未定位|单轮|不能|同行评审|未提取||滚雪球 R1；ACL 2025
arxiv:2606.27124|Bugs4Q-reproducibility|工件|部分|可执行|仅论文|未定位|单轮|不能|预印本|未提取||滚雪球 R1
snow:tarbench|TaRBench|工件|部分|可执行|代码和数据|none|单轮|不能|同行评审|未提取|Ahmadreza-SY/TaRGET|滚雪球 R1；无 LICENSE
snow:coupjava|CoUpJava|工件|部分|精确匹配|仅数据|Apache-2.0|单轮|不能|同行评审|未提取|uw-swag/CoUpJava|滚雪球 R1；Java 升级历史
arxiv:2601.12262|EACG|工件|部分|可执行|仅论文|未定位|单轮|不能|同行评审|未提取||滚雪球 R1；环境/版本感知代码生成
"""
rows = []
for line in R.strip().splitlines():
    p = line.split("|")
    assert len(p) == 13, (len(p), line)
    i, name, d1, d2, d3, d4, d5, d6, d7, d8, d9, repo, note = p
    rows.append(dict(id=i, name=name, D1=d1, D2=d2, D3=d3, D4=d4, D5=d5, D6=d6, D7=d7, D8=d8, D9=d9, grade=grade(d1, d2, d3, d4, d5, d7), repo=repo, note=note))
with open("extraction.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
import collections
print(len(rows), collections.Counter(r["grade"] for r in rows))
for g in "AB":
    print(g, [r["name"] for r in rows if r["grade"] == g])
