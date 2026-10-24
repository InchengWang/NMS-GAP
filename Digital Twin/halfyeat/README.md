# halfyeat：稀疏IMU运动重建的泛化与个体化

**当前主题更新（2026-10-25）：** 用户确认2026-10-27中期答辩题目为 **Generalizable and Personalized Motion Reconstruction in Stroke Patients Using Sparse IMUs**。近期以真实双小腿IMU、跨患者建模与有限标签个体化为中心；三层目标为现有可组织投稿内容、适当优化、期刊证据包，见[当前主题与路线](MIDTERM_THEME_AND_PUBLICATION_ROADMAP_20261027_ZH.md)及[当前答辩大纲](MASTER_MIDTERM_OUTLINE_ZH.md)。现有证据更支持个体适配，零标定卒中泛化仍待验证；健康外部数据仅作技术复核。架构继续冻结，本次不启动新训练。以下旧日期、标题和未完成状态按各自记录日期保留，当前答辩日期以10月27日为准。

| 当前入口 | 内容 |
|---|---|
| [10月27日主题与三层目标](MIDTERM_THEME_AND_PUBLICATION_ROADMAP_20261027_ZH.md) | 当前可投稿内容、有限优化和期刊证据要求 |
| [中期答辩大纲](MASTER_MIDTERM_OUTLINE_ZH.md) | 13页正文、已有结果及问答边界 |

下文长期入组、交接与其他研究安排保留；近期主题以上述入口为准。

**2026-10-23研究决策更新：** 架构方向已冻结，泛化线继续推进，新开第三线“少量适配＋方向增强”。[三线方案、当前阶段及代码索引](SII2027_THREE_LINES_PLAN_20261023_ZH.md)。90个新神经fit及两线固定clean VALID诊断已独立验收；本批无新TEST。

**10/23网络架构与数据增强支线已验收（20261022批次）：** [六格、坐标敏感性与非线性融合追加实验](SII2027_ARCH_AUG_RESULTS_20261022_ZH.md)。完整报告保留阴性结果、全部seed、独立审计与计算成本；当前结果是患者内跨试次探索性证据。


**10/22泛化等患者损失对照已完成：** [66fit、独立VALID/TEST审计与完整配对结果](SII2027_GEN4_EQUAL_PATIENT_RESULTS_20261022_ZH.md)。保留全部6患者、3seed、one/half/full预算及正负方向；本批TEST为描述性比较。


**10/22泛化机制补查：** [TRAIN/VALID独立诊断完成；偏置不足以解释全部误差](SII2027_GEN3_GENERALIZATION_DIAGNOSIS_20261022_ZH.md)。源窗口权重差异已量化，并固定66fit等患者损失对照；新TEST结果尚未在此页报告。


**10/22泛化线结果验收：** [180次拟合与三批独立审计已完成](SII2027_GENERALIZATION_RESULTS_20261022_ZH.md)；真实源适配患膝2.949°，同标准化从零参考3.174°；低数据量曲线与虚拟源负结果均保留。[代码／合同索引](SII2027_GENERALIZATION_CODE_INDEX_20261022.json)。


**10/22双分支执行更新：** [GEN与ARCH_AUG已完成训练入口预检并启动](SII2027_RESEARCH_BRANCH_RUNS_20261022_ZH.md)；72与96次新增拟合按各自冻结合同推进。尚无新TEST结论，当前计数和验收边界见执行记录；[训练／分析代码索引](SII2027_RESEARCH_RUN_CODE_INDEX_20261022.json)。


**10/22研究分支更新：** 以已验收53条数据和结果为共同起点，分为[GEN：泛化与标定成本](SII2027_RESEARCH_FORK_20261022_ZH.md#gen)和[ARCH_AUG：网络架构与数据增强](SII2027_RESEARCH_FORK_20261022_ZH.md#arch_aug)。两个分支的角色／预算已预检，共享模型与静态旋转完成合成预检；规划冻结时新训练均为0，拟执行预算与旧成绩明确分开。


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

## 10/22分支决策（R32–R35）

用户决定以当前结果为分支点，分别研究泛化和网络架构／数据增强。[完整分支图、目的、控制与计划](SII2027_RESEARCH_FORK_20261022_ZH.md)、[代码函数／行号／SHA](SII2027_RESEARCH_FORK_INDEX_20261022.json)。

GEN固定当前网络，先做排除目标患者的G/A×source真实／混合四格（拟72fits），再研究标定成本和独立跨条件／外部协议。ARCH_AUG固定当前患者内划分，用2架构×3增强解耦效果和交互（144逻辑fits，48旧复用、96拟新增）；首阶段24新fits仅TRAIN/VALID，全矩阵完成后统一新TEST。

规划冻结时两个分支尚无新训练结果。当前6名TEST患者与历史接触边界保留；不以窗口／seed扩大N，不把目录条件或投影角升级为临床真值。架构候选以后迁入GEN需另立交叉协议，避免从同一TEST反复选择后宣称独立确认。

## 10/22执行补记

**10/22双分支执行更新：** [GEN与ARCH_AUG已完成训练入口预检并启动](SII2027_RESEARCH_BRANCH_RUNS_20261022_ZH.md)；72与96次新增拟合按各自冻结合同推进。尚无新TEST结论，当前计数和验收边界见执行记录；[训练／分析代码索引](SII2027_RESEARCH_RUN_CODE_INDEX_20261022.json)。

规划和模块合成预检记录保留为分支冻结时事实；后续训练、正式评估及独立结果验收分别记录，不将拟执行次数或启动状态写成最终精度结论。

## 泛化结果验收补记

**10/22泛化线结果验收：** [180次拟合与三批独立审计已完成](SII2027_GENERALIZATION_RESULTS_20261022_ZH.md)；真实源适配患膝2.949°，同标准化从零参考3.174°；低数据量曲线与虚拟源负结果均保留。[代码／合同索引](SII2027_GENERALIZATION_CODE_INDEX_20261022.json)。

此前启动计数保留为当时快照；GEN已完成固定分析及独立结果验收，具体边界、标定量账目和后续决策见新结果页。

## TRAIN/VALID机制诊断补记

**10/22泛化机制补查：** [TRAIN/VALID独立诊断完成；偏置不足以解释全部误差](SII2027_GEN3_GENERALIZATION_DIAGNOSIS_20261022_ZH.md)。源窗口权重差异已量化，并固定66fit等患者损失对照；新TEST结果尚未在此页报告。

## GEN4等患者source损失结果补记

**10/22泛化等患者损失对照已完成：** [66fit、独立VALID/TEST审计与完整配对结果](SII2027_GEN4_EQUAL_PATIENT_RESULTS_20261022_ZH.md)。保留全部6患者、3seed、one/half/full预算及正负方向；本批TEST为描述性比较。

## ARCH_AUG网络架构与数据增强支线结果补记

**10/23网络架构与数据增强支线已验收（20261022批次）：** [六格、坐标敏感性与非线性融合追加实验](SII2027_ARCH_AUG_RESULTS_20261022_ZH.md)。完整报告保留阴性结果、全部seed、独立审计与计算成本；当前结果是患者内跨试次探索性证据。

## 2026-10-23：架构冻结与第三线立项/验收记录

**2026-10-23研究决策更新：** 架构方向已冻结，泛化线继续推进，新开第三线“少量适配＋方向增强”。[三线方案、当前阶段及代码索引](SII2027_THREE_LINES_PLAN_20261023_ZH.md)。90个新神经fit及两线固定clean VALID诊断已独立验收；本批无新TEST。

用户明确授权该安排；架构旧支线120新fit及48旧参考fit不再扩展。泛化GEN5固定one段六方法，新增18个head神经fit和36个闭式校准；第三线固定源/目标方向增强2×2，固定72新fit。目标网络采用预定200 epoch final，不按目标VALID选点；旧final参考曾看VALID另存best，历史保留。本批完训后仅执行一次目标VALID诊断，没有TEST推理实现。后续独立验证只使用开源数据，不安排重新采集；BLISS已经参与开发，不能称新盲测。

GEN5与COMB1的固定clean目标VALID诊断均已完成并通过独立数值审计；本批没有新TEST或方向压力预测。结果属于历史开发VALID，不能作为新增独立泛化证据。

历史VALID患膝：GEN5源G 11.936504°、仿射6.262902°、head 5.183036°、完整final 3.830770°、同预算scratch final 4.166245°；COMB两阶段replay 3.830770°、两阶段SO3 3.783814°。所有格/终点、患者方向计数、阴性结果、监督成本和函数SHA索引均见新报告；不与旧TEST或不同预算混比。


---

### 2026-10-23 外部输入质量纠错与25fit已验收增量

ARCH保持79项冻结。WMCG完整公开源接入后，物理QC发现P05/P06/P07/P10右小腿ACCY5长期近−16g，源CSV有限前缀确认其已存在于发布值。旧45fit批次停止：12源fit启动、0完成、0target/外层预测、≥7200更新，日志与partial全保留且不复用；旧形式通过回执不能覆盖物理失败。

新训练前固定输入质量规则，保留6名健康人，P01仅开发/源角色，另外5人整人排除外层目标。字节不变release_v4独审通过后，全新完成25fit/26000更新：每人normal6秒适配，在其slow/fast/vfast不同完整parents评价。完整clean双膝RMSE：G_R 8.394743°、G_S 7.967532°、A_R 8.050971°、A_S 8.021340°、I_R 10.365379°；独立20秒10°坐标压力增量A_R 0.322786°、A_S 0.158372°。75完整＋1425压力case、9000逐角及11表/3统计已独立复算。五目标最小双侧exact p=.0625，不作统计优越性、真实重戴或卒中临床泛化结论。

详见[目的—尝试—结论与代码入口](SII2027_OPEN_EXTERNAL_VALIDATION_20261023_ZH.md)、[验收/历史失败机器摘要](SII2027_OPEN_EXTERNAL_READINESS_20261023.json)、[函数行号与SHA](SII2027_OPEN_EXTERNAL_CODE_INDEX_20261023.json)及[完整聚合](SII2027_OPEN_EXTERNAL_AGGREGATES_20261023.json)。本条取代此前外部数据仍仅候选的状态，保留旧历史原文。


---

### 2026-10-25 Dorschky独立双膝任务：数据、代码与结果验收增量（实验ID20261024）

旧ARCH79项继续冻结，WMCG与Stroke旧数值不变。新公开Dorschky实测双tibia12D（SI、作者功能标定segment轴）＋独立光学heading双膝proxy，任务头6→2，不能与旧六角或其他数据源合并RMSE/N。297walking候选经固定QC保留271、26因共同XYZ支持不足2.4秒拒收，10健康男性/P02仅开发、9名外层人全部保留。20ms采用作者经验相关校正，非硬件精确同步；每人trial共用连续原IMU文件、上下文不重叠，不是真实重戴/独立session。

45新fit/34200更新及独立训练/结果验收完成。每目标2秒梯度/2.4秒marker预处理，完整trial/公开QC/作者功能标定另计。cross-speed双膝RMSE G_R 5.384334°、G_S 5.031603°、A_R 4.425045°、A_S 4.520874°、I_R 6.897207°；相同2秒固定10°压力差A_R +0.193454°、A_S +0.082787°。same-speed另报，预定三项统计只用cross-speed；1160模型-parent包/22040case（clean计一次）/44080角行、12表及三统计已独立复算。保留适配未必优于无适配G_S等负结果，不据外层成绩调参数。

目的—尝试—结论与函数入口见[新实验报告](SII2027_DORSCHKY_EXTERNAL_20261024_ZH.md)、[来源/成本/验收摘要](SII2027_DORSCHKY_READINESS_20261024.json)、[函数行号/SHA](SII2027_DORSCHKY_CODE_INDEX_20261024.json)与[完整聚合](SII2027_DORSCHKY_AGGREGATES_20261024.json)；新增Kiel/Grouvel/GAITEX/Twente候选核验见[简报](SII2027_PUBLIC_DATASET_CANDIDATES_20261024_ZH.md)。Kiel公开21健康、不是公开卒中，许可来源差异和标定配对待核；未将任何候选包装为已完成训练或真实重戴证据。
