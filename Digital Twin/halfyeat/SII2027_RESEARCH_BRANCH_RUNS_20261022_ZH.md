# 两条研究线的启动与代码落实（2026-10-22）

**2026-10-23研究决策更新：** 架构方向已冻结，泛化线继续推进，新开第三线“少量适配＋方向增强”。[三线方案、当前阶段及代码索引](SII2027_THREE_LINES_PLAN_20261023_ZH.md)。90个新神经fit及两线固定clean VALID诊断已独立验收；本批无新TEST。

**10/23网络架构与数据增强支线已验收（20261022批次）：** [六格、坐标敏感性与非线性融合追加实验](SII2027_ARCH_AUG_RESULTS_20261022_ZH.md)。完整报告保留阴性结果、全部seed、独立审计与计算成本；当前结果是患者内跨试次探索性证据。


**10/22泛化等患者损失对照已完成：** [66fit、独立VALID/TEST审计与完整配对结果](SII2027_GEN4_EQUAL_PATIENT_RESULTS_20261022_ZH.md)。保留全部6患者、3seed、one/half/full预算及正负方向；本批TEST为描述性比较。


**10/22泛化机制补查：** [TRAIN/VALID独立诊断完成；偏置不足以解释全部误差](SII2027_GEN3_GENERALIZATION_DIAGNOSIS_20261022_ZH.md)。源窗口权重差异已量化，并固定66fit等患者损失对照；新TEST结果尚未在此页报告。


**10/22泛化线结果验收：** [180次拟合与三批独立审计已完成](SII2027_GENERALIZATION_RESULTS_20261022_ZH.md)；真实源适配患膝2.949°，同标准化从零参考3.174°；低数据量曲线与虚拟源负结果均保留。[代码／合同索引](SII2027_GENERALIZATION_CODE_INDEX_20261022.json)。


[共同分支点与研究设计](SII2027_RESEARCH_FORK_20261022_ZH.md)已发布。随后完成训练入口及数据加载审计，并启动两线训练。本页是本轮启动记录，完成计数是生成此记录时的快照；**尚无新TEST推理或精度结论，训练完成仍须结果独立审计。**

| 研究线 | 当前执行 | 拟合预算 | 此次记录已完成200epoch的新fit |
|---|---|---|---:|
| GEN：泛化 | 先36个G，再36个A | 72新增、228000更新 | 4 |
| ARCH_AUG：架构与增强 | 先共享网络replay24，再其余交叉臂72 | 96新增、84000更新；旧48复用 | 17 |

共同数据仍为53真实试次／31TRAIN、12VALID、10TEST／8建模患者、6TEST患者；输入和六角标签不变。GEN使用4个worker，ARCH_AUG使用8个，每worker2个CPU线程；并行数量属于执行配置，不改变每fit数据、200epoch、窗口和更新量。

## GEN执行入口

`native_generalization_20261022/gen_training.py`实现contract/train/worker/verify；`gen_data.py`把拟合访问限定为当前fold允许的TRAIN和VALID。G完整排除目标患者、source TEST禁用；A只用相同目标真实数据，从对应G权重初始化并冻结其scaler。G按source等患者VALID选点，A按目标等trial VALID选点，均每10epoch检查且平局保留早期checkpoint。

`gen_preflight.py`的10项门槛通过：逐fold动态读白名单、source唯一真实帧scaler独立重算、两域窗口/标签一致、A两域真实视图一致、crop/四槽预算、拒绝A重拟合scaler及拟合上下文TEST。预检只读允许TRAIN动态数组，未读真实VALID/TEST；正式训练按方案读取VALID作选择。

`gen_evaluation.py`在72个完整训练和checkpoint验签后才开放目标真实TEST，计划552预测／3312逐角指标。`gen_analysis_preflight.py`已用空训练完成凭据确认提前评估被拒绝，并以合成四格算例核验域／适配／交互、64种符号翻转、患者bootstrap及Holm。此处没有运行正式TEST。

训练合同SHA256：`4c4b72ee5735e7d3f2a54473735dbd7d70e317c1d8c119ac233b971a2700cf23`。

## ARCH_AUG执行入口

`native_architecture_augmentation_20261022/arch_training.py`实现freeze/train/worker/verify。`train --stage all`先等待stage1的24个共享网络replay拟合全部完成，再执行stage2的72个交叉拟合。入口没有TEST loader；全96新fit及旧48参考验签后，独立分析入口才可评估TEST。

`arch_training_preflight.py`的18项门槛通过：旧48个参考的来源、CFG、200epoch历史与最佳点、严格state加载、best/final权重SHA；真实TRAIN scaler逐位相同、四槽窗口/标签/来源精确一致；同架构三增强的初始参数、shuffle和dropout轨迹一致。旧run未单独保存初始权重，因此验证的是不可变初始化代码和seed重现，不假称找到了旧初始checkpoint。

旧shuffle与dropout共用全局torch RNG，架构变化会改变RNG消耗；本版明确不保证跨架构逐batch顺序相同，但保持窗口清单、批数、步数和同架构增强比较。共享模型参数148422，约少1.78%，卷积MAC约1.959倍，不称计算完全匹配。

`arch_evaluation.py`计划636份新预测＋只读旧318份＝954记录／5724逐角指标。旧NPZ的method保留原值，新manifest明确source_method及imported_reference，CSV使用六格canonical名称，不修改旧结果。`arch_analysis_preflight.py`只用合成数据验证全fit gate与五个患者对比，未进行正式TEST。

训练合同SHA256：`6a8b4b59e0fc49d24aa6f4bff2a60d1cb2ac768988914b7a9075060b37a569cd`。

## 完成流程及尚未完成的工作

`research_fork_20261022/complete_research_branch.py`分别等待各分支完整训练凭据，核对已审阅分析源码SHA后执行verify→evaluate→summarize→statistics，仅写本地结果，不自动发布结论。源、合同或某阶段失败会记录错误并停止后处理，不静默换模型、患者或超参数。

当前未完成训练的完整矩阵、正式TEST评估、逐预测与患者统计的独立结果审计及最终图表。流水线完成也只代表固定分析完成，不能直接记为独立验收通过。所有新增结论继续以6患者、历史已接触TEST的探索性边界报告。

函数／行号／SHA及门槛摘要见[训练与分析代码索引](SII2027_RESEARCH_RUN_CODE_INDEX_20261022.json)；本地逐患者角色、原始数据、权重和完整波形不上传。

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
