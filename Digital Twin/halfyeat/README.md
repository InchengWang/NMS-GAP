# halfyeat：SII投稿、入组准备与第三篇

**10/22输入、监督表示与虚拟对照更新：** [192新增神经拟合、简单线性参考及独立验收](SII2027_NATIVE_ABLATIONS_20261022_ZH.md)完成。固定53真实数据/6患者TEST；3输入mask＋RotMSE/RotGeo，虚拟31TRAIN/124假设视图与同支持同21000步控制，失败context尝试也保留。所有种子及患者级配对结果见表；论文有标定方法但本地逐人安装值仍未知。当前为I_full，原E2的G/A外层患者排除尚未完成；不称临床JCS或真实安装等价。

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




最新资料：[数据可靠性报告](SII2027_DATA_RELIABILITY_20261021_ZH.md)、[代码证据](SII2027_RELIABILITY_CODE_INDEX_20261021.json)、[聚合数据](SII2027_RELIABILITY_AGGREGATES_20261021.csv)及[汇总图](SII2027_RELIABILITY_SUMMARY_20261021.svg)。当前优先重建原Stroke事件/配对依据，维持原研究主线与BLISS正对照；投稿gate未关闭。

## 10/21新增：原数据组合配对修复（R04–R08）

[详细尝试/目的/结果与新决策树](SII2027_PAIRING_REPAIR_20261021_ZH.md)、[源码函数/行号/SHA](SII2027_REPAIR_CODE_INDEX_20261021.json)、[全部聚合与固定种子结果](SII2027_REPAIR_AGGREGATES_20261021.csv)。原PDF唯一源窗→39 TRAIN前置动作开发→冻结69条应用，18条候选；2患者、6 TRAIN/3 TEST的固定配对模型恢复，表明先修复输入配对有必要。不能分离纯时间、试次身份和条件来源的单独贡献。

正式释放仍待上游重力/滤波支持、现场条件/安装及物理split验收；不把QC筛选子集或mocap离线校时描述成未见患者/实时IMU-only验证。主线保持双小腿实测IMU估计下肢运动学；正式G/I/A、逐帧与整窗比较须在验收新数据版本后继续。历史数字保留，不按原文不保真数字反推实验。

## 10/21采集者补充后的执行（R09–R12）

[原始源、抬健侧腿标记、S6与17条native候选](SII2027_RAW_ACQUISITION_20261021_ZH.md)、[函数/行号/SHA](SII2027_RAW_SOURCE_CODE_INDEX_20261021.json)、[聚合数据](SII2027_RAW_SOURCE_AGGREGATES_20261021.csv)。安装左右语义已由采集者确认；实验室轴、固定安装旋转与clinical JCS仍需分别验收。216原始文件/16加工源桥接已建立；17条native重建不沿用旧全记录滤波/旋转，但继承原离线clock/QC，旧2.205°不能转记为新版本成绩。

原患侧表与标记侧有2例待核，11条缺原光学；未用拐时S6也可能被携带，运动不能等同承重。下一步先确认标记事件和native预处理支持，再冻结正式实验；不据网络误差改条件、侧别或lag。旧阶段“安装未闭合”指其当时证据，最新采集者确认与剩余坐标问题以本次更新为准。

## 10/21新增：mocap少于IMU时的顺序/跳段配对（R13–R16）

[完整方法、尝试和结果](SII2027_ORDERED_MATCHING_20261021_ZH.md)、[源码函数/行号/SHA](SII2027_ORDERED_CODE_INDEX_20261021.json)、[聚合数据](SII2027_ORDERED_AGGREGATES_20261021.csv)。156原始光学中只有58属于当前有固定监督步态边界的69目标；另98未自动入组。164是IMU单侧重复动作候选，不是真实行走计数。未匹配IMU可能属于未选光学，不能等同漏采。

旧PDF同尾号绑定已降为历史假设，组内有序、组间另核来自用户确认。前置块决定候选与全局路径，步行仅后验验收且失败不重选。49原始候选仍依赖有限detector候选集和离线光学校时，正式释放false；下一步补候选召回与S6/预处理验收，再冻结新版本重训。旧数据和模型保留，未追逐原文不保真数值。

## 10/21新增：标记漏检的统一修复与回归（R17–R18）

[完整尝试、目的、代码职责和结论](SII2027_MARKER_RECALL_20261021_ZH.md)、[函数/行号/SHA](SII2027_RECALL_CODE_INDEX_20261021.json)、[聚合数据](SII2027_RECALL_AGGREGATES_20261021.csv)。

两条漏检源自标记后的活动并入峰组，导致整组对侧RMS超限。保留0.35rad/s及比值3等原门槛，全部18session统一枚举极大有效子窗；没有按旧时钟补单例。新增14动作提案，最终多4条验收；旧49同步时钟完全不变。真实同号绑定仍被弃用，两个条件各自保序、共享源且允许跳段。

物理身份反事实排除整类别名，10ms实际源区间隔与原始行非复用仍有效；当前311有效边无实际别名重复，因此结果改善来自新子窗。路径先冻结、步行后验收，失败不重选。剩余16/69未验收继续保留原因（11无模板、2侧别/模式、1无路径、2验收失败）。

本轮数据召回工作完成，正式训练就绪仍为false。下一步补53条S6证据及预处理/坐标合同，再冻结并重训；测试mocap用于离线修复，不称完全未接触测试集，不继承原2.205°模型分数。历史49版结果保留供对照。

## 10/21新增：原生53条工程训练版本与固定基线（R19–R22）

[完整目的、尝试、结论与决策树](SII2027_NATIVE_BASELINE_20261021_ZH.md)、[源码函数/行号/SHA](SII2027_NATIVE_CODE_INDEX_20261021.json)、[全部聚合指标](SII2027_NATIVE_AGGREGATES_20261021.csv)。

本轮完成此前计划的S6、输入和坐标合同：26目录有拐/27目录无拐的S6运动模式相容，未改条件或删人；53条原生SI和几何通过，三平面索引没有混淆，原生sensor XYZ与骨盆解剖轴严格区分。训练只用各患者TRAIN唯一帧拟合统计量，不再默认旧gravity加工输入或移植旧模型成绩。

固定24fits（8患者×3seed）全部200epoch，每10epoch在各人VALID择checkpoint，全部验签后统一TEST。原角色31/12/10、TEST6人；两人只有TRAIN/VALID；有一位患者VALID/TEST条件不同。连续源CSV跨角色共享但原生采样支持无重用，不能称文件级独立。

患者内真实IMU基线及TRAIN均值结果见表；旧2.205°是不同输入和分母的历史探索，不作直接增益比较。全部种子和10条TEST保留，212预测/1272角度指标完整审计。数据工程训练就绪不等于临床最终认证；下一步围绕冻结版本补输入/表示/虚拟数据消融，跨患者需另立协议，改临床输出或主队列须先讨论。

## 10/22新增：I_full信息、监督表示与假设虚拟对照（R23–R31）

[实验目的、每次尝试及结论](SII2027_NATIVE_ABLATIONS_20261022_ZH.md)、[函数/行号/SHA](SII2027_ABLATION_CODE_INDEX_20261022.json)、[聚合结果](SII2027_ABLATION_AGGREGATES_20261022.csv)、[患者配对差](SII2027_ABLATION_PAIRED_20261022.csv)。

本批实际是3输入信息组、2个Rot6D监督/损失组，共120新fits；另3个同共同crop/同4视图/同21000步的真实重复与假设虚拟组，共72新fits。简单当前帧Ridge参考8模型/48VALID候选另列，不能称完整Guo框架复现。旧raw12参考24fits只读复用。全数据角色和测试段不变，1537预测记录/9222角度指标与额外1908SO3指标可追溯，N仍为6测试患者。

虚拟完整context首次0/31失败；共同裁剪后31TRAIN/124视图，12665训练目标帧及18865参考context成本分别记账。原论文有sensor-to-segment标定方法，当前没有逐人实际安装数值，不把假设模拟提升为已标定真实IMU。输入轴与原六投影角含义保持不变。

每患者统计先汇总trial/seed再等患者，64种符号翻转与Holm保持原定义；不能为显著性把窗口/种子当患者或更换检验。本轮未完成原E2的外层患者G/A2×2：下一批需source彻底排除目标、两A共用同target真实适配并记VALID参考成本。草案已在本地形成，不冒充已运行结果。
