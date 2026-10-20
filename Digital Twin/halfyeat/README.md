# halfyeat：SII投稿、入组准备与第三篇

实验事实更新：2026-10-21；长期排期沿用原文件并受证据门槛约束。目录名称沿用用户指定的 `halfyeat`。本版按最新边界执行：**Hayashibe lab至2027年2月；3月过渡；4月前往张明明组。优先级：SII投IEEE Sensors Journal → 入组学习 → 第三篇。**

SII尚未投稿，先完成输入/配对隔离/指标/预算核验和同协议基线；**目标1月15日首投，1月31日缓冲，必要技术阻塞时2月15日应急目标**。日期是项目目标，不是期刊deadline或录用承诺。入组学习从10月固定保留时间，UWB为准备重点；第三篇首投后通过gate才扩展，不再把3月独立稿作为必须完成项。2月26日前完成现场依赖交接。

最新执行：[10/21动态诊断](SII2027_DYNAMIC_DIAGNOSIS_20261021_ZH.md)：TRAIN拟合改善，但原队列TEST仍失败；40+48次训练、33项测试与独立复算完成。[函数/源码索引](SII2027_DIAGNOSIS_CODE_INDEX_20261021.json)及[聚合数据](SII2027_DIAGNOSIS_AGGREGATES_20261021.csv)可查。原文数值不再作为还原目标，核心思路变更先沟通。

| 文件 | 内容 |
|---|---|
| [SII2027_EXPERIMENT_DECISIONS_20261020_ZH.md](SII2027_EXPERIMENT_DECISIONS_20261020_ZH.md) | 新：决策树、历次实验的目的/尝试/代码入口/实际结论；含两轮失效与修正 |
| [MASTER_MIDTERM_OUTLINE_ZH.md](MASTER_MIDTERM_OUTLINE_ZH.md) | 已回写当前证据的中期大纲、各页结果与限制 |
| [MIDTERM_LITERATURE_SYNTHESIS_20261019_ZH.md](MIDTERM_LITERATURE_SYNTHESIS_20261019_ZH.md) | 文献分析与10/20规划执行对照 |
| [SII2027_CODE_EVIDENCE_INDEX_20261020.json](SII2027_CODE_EVIDENCE_INDEX_20261020.json) | 30个本地代码文件的函数/行号/SHA和18项结果证据指纹 |
| [SII2027_AGGREGATE_RESULTS_20261020.csv](SII2027_AGGREGATE_RESULTS_20261020.csv) | 38行原队列与BLISS聚合结果，队列/参考分开 |
| [SIX_MONTH_EXECUTION_PLAN.md](SIX_MONTH_EXECUTION_PLAN.md) | 当前主排期：优先级、月度任务、工时、首投门槛、延误调整与2月交接 |
| [ZHANG_LAB_PREPARATION_PLAN.md](ZHANG_LAB_PREPARATION_PLAN.md) | 入组前UWB、OpenSim/NMS、单关节交互学习练习；资源问题与首8周 |
| [FIRST_FOUR_WEEKS_EXECUTION.md](FIRST_FOUR_WEEKS_EXECUTION.md) | 从10月6日开始的SII任务块、每周固定学习、记录字段与草稿配置 |
| [SII2027_REVISION_PLAN.md](SII2027_REVISION_PLAN.md) | 当前确定Sensors Journal目标；原稿页码问题、必要实验、统计与投稿核验 |
| [SII2027_MANUSCRIPT_REWRITE.md](SII2027_MANUSCRIPT_REWRITE.md) | 可编辑的英文摘要/引言/方法与图表槽位；方括号须真实结果填写 |
| [THIRD_PAPER_PLAN.md](THIRD_PAPER_PLAN.md) | 候选任务可靠性/观测成本问题；最新启动时间、收縮和独立成篇门槛 |
| [THIRD_PAPER_MINIMUM_PROTOCOL.md](THIRD_PAPER_MINIMUM_PROTOCOL.md) | 技术v0.2：Q/T/C评分与区间分开、参与者权重、恢复预算；排期服从当前主计划 |
| [PHD_PROPOSAL_ZH.md](PHD_PROPOSAL_ZH.md) | 完整博士计划；桥接时间已按2月离组、4月到组修订 |
| [SOURCE_AND_GAP_AUDIT.md](SOURCE_AND_GAP_AUDIT.md) | 2026-10-05两稿审阅/validated gap/最近邻与访问深度；证据历史保留 |

**共同主线：** human neuromusculoskeletal system + embodied intelligence，围绕sensing/modeling/control/interaction。SII是现有运动状态研究的整理；入组准备由UWB观测推进到外部锚定NMS和反馈。IMU仅为可选sensing modality，角度精度不自动证明神经/肌肉机制或控制疗效。

已应用[$nms-digital-twin-phd-proposal](https://github.com/InchengWang/nms-digital-twin-skills/blob/main/nms-digital-twin-phd-proposal/SKILL.md)。已有gap主要为partially-addressed；本次重排未完成新的系统gap validation，所有novelty仍回到SOURCE_AND_GAP_AUDIT的最近邻和实际实验。期刊与学习资源官方入口重新核对于2026-10-06。

资料状态（10/20）：已核验本地原稿复现工程、训练历史和连续预测。原队列单seed开发实验完成但动态拟合不足；BLISS首轮内容重复结果失效，去重118条已完成外部native角度pilot。两轮结论与限制见[实验台账](SII2027_EXPERIMENT_DECISIONS_20261020_ZH.md)。临床JCS、完整Guo物理、多seed及新BSN跨患者证据仍待补；实际答辩PPT、作者贡献与正式发表状态保持待核实。

阅读顺序：实验决策台账 → 当前中期大纲 → 文献规划执行回写 → SII修改方案；长期排期与入组准备另阅相应文件。

2026-10-05续编的技术澄清保留：任务层评分排序与区间包含率分开；全局正数缩放不改变排序；全拒答参与者risk不可估；曲线目标80%与实际部署阈值分开。2026-10-06新增入组学习优先级并收缩第三篇日程。


