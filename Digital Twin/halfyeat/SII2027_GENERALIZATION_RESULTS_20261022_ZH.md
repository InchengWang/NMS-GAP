# 泛化线：已验收结果、代码落实与决策（2026-10-22）

**2026-10-23研究决策更新：** 架构方向已冻结，泛化线继续推进，新开第三线“少量适配＋方向增强”。[三线方案、当前阶段及代码索引](SII2027_THREE_LINES_PLAN_20261023_ZH.md)。90个新神经fit及两线固定clean VALID诊断已独立验收；本批无新TEST。

**10/23网络架构与数据增强支线已验收（20261022批次）：** [六格、坐标敏感性与非线性融合追加实验](SII2027_ARCH_AUG_RESULTS_20261022_ZH.md)。完整报告保留阴性结果、全部seed、独立审计与计算成本；当前结果是患者内跨试次探索性证据。


**10/22泛化等患者损失对照已完成：** [66fit、独立VALID/TEST审计与完整配对结果](SII2027_GEN4_EQUAL_PATIENT_RESULTS_20261022_ZH.md)。保留全部6患者、3seed、one/half/full预算及正负方向；本批TEST为描述性比较。


**10/22泛化机制补查：** [TRAIN/VALID独立诊断完成；偏置不足以解释全部误差](SII2027_GEN3_GENERALIZATION_DIAGNOSIS_20261022_ZH.md)。源窗口权重差异已量化，并固定66fit等患者损失对照；新TEST结果尚未在此页报告。


本轮在[共同分支点](SII2027_RESEARCH_FORK_20261022_ZH.md)上完成GEN1四格、全量同标准化从零参考及嵌套标定量实验。**180个新增fit、286800更新均完成；三批结果已独立验收。当前证据支持目标患者适配的作用，未支持可靠零标定迁移或虚拟源的稳定收益。** 本文更新[原中期综合规划](MIDTERM_LITERATURE_SYNTHESIS_20261019_ZH.md)中的泛化分支，不据架构线TEST挑选模型。

## 数据、训练与可解释范围

仍为53实测试次，31TRAIN/12VALID/10TEST；8建模患者中6人有TEST，另2人仅作source。每个G完整排除该目标患者，用其余7人的TRAIN拟合梯度与scaler、VALID选择checkpoint，source TEST禁用。A从对应G最佳权重开始，只用目标TRAIN和VALID；两种A均使用真实目标数据。12D输入为左右小腿原生加速度/角速度，SI单位与传感器轴保留；标签为六个legacy pelvis-YZ投影工程角，非临床JCS认证。

架构FrameTCN151110参数、window120/stride20、width64、dropout.15、dilation1/2/4、batch64、200epoch、AdamW lr3e-4/wd1e-4/clip1。source真实TRAIN唯一crop[100:-100]拟合x/y scaler；四槽或窗口不重复计入scaler。真实源为replay4，混合源为真实+3个既有假设random虚拟视图。VALID/TEST保留原完整支持；Hann floor.08融合。G按source等患者、A和从零模型按目标等trial双膝VALID每10epoch选择，严格较小、平局保留早期点。

所有TEST均是历史研究已接触数据，身份与时钟重建曾用mocap作离线QC；试次来自共享连续原文件，支持不交叠不等于文件独立。本轮是探索性跨患者/跨试次重建验证，不能声称未接触TEST、新队列、IMU-only部署或临床标定阈值。安装Q和杠杆臂的实际患者记录仍不确定。

## 尝试、目的、结果与保留决策

|尝试|目的与代码定位|完成与结论|
|---|---|---|
|GEN1：G_real/G_mixed/A_real/A_mixed|gen_data.py: FitData；gen_training.py: worker/valid_metric；gen_evaluation.py: evaluate/statistics|72fit、228000更新；检验source域、目标适配及交互。适配有明显降误差，虚拟源无稳定收益。|
|full I_source_scaler|gen_scratch_reference.py: fresh_model/load_training/worker；gen_scratch_evaluation.py: training_gate/paired_statistics|18fit、16200更新；相同source x/y scaler、目标支持和目标阶段优化下隔离预训练权重收益。真实源适配患膝平均改善0.224781°，6/6同方向，Holm2=0.0625。|
|GEN2嵌套标定量|gen_budget_plan.py；gen_nested_training.py: DynamicAccess/initialize/worker/verify；gen_nested_evaluation.py: tables/evaluate|90新增低预算、42600更新，复用full A36+I18，共144个目标预算模型。低数据量预训练有帮助；半量适配未达到full从零参考的平均误差。|
|候选有拐/无拐覆盖核查|gen_condition_feasibility.py，仅冻结角色元数据|TEST有拐候选3条/2人、无拐7条/5人，仅1人两条件均有。条件分层仅描述，不能称充分配对的同患者条件迁移。|
|独立数值验收与图表|audit_GEN1_results.py、audit_GEN2_full_results.py、audit_GEN2_budget_results.py及plot_gen_*|source VALID、checkpoint推理、GT/time、scaler、逐角指标、分层权重及患者统计均通过；保留不利结果。|

代码索引为本地工作区`experiments/native_generalization_20261022`的文件、函数、行号与SHA追溯信息，见[具体代码索引](SII2027_GENERALIZATION_CODE_INDEX_20261022.json)；索引不表示这些本地脚本已作为可运行源码包上传。

## 已核验的全量结果

均为同6名患者等trial→等seed→等患者平均RMSE，单位°。双膝及六角均为各角RMSE的算术平均。

|方法|双膝|患侧膝（主终点）|六角|
|---|---:|---:|---:|
|G_real|9.138240|11.076073|10.417331|
|G_mixed|9.425187|11.322245|10.474993|
|I_source_scaler|2.705857|3.173843|2.441341|
|A_real|2.450731|2.949062|2.304418|
|A_mixed|2.534602|2.966957|2.331119|

G为未使用该目标患者标签的跨患者直接预测；A为目标患者适配。I_source_scaler是随机权重目标训练参考，含source x/y统计及source标签信息，不能称无群体信息。A−I才用于本轮预训练权重收益解释；A另有source预训练算力，source+target总计算未配平。旧patient-only I及原完整TRAIN基线的scaler/支持不同，不混入本轮配对效应。

![GEN1患者级结果与因素对比](assets/GEN1_generalization_patient_results_20261022.svg)

GEN1预定患膝因素对比：source域+0.132033°，患者bootstrap95%区间[-0.457959,0.777779]、Holm3=1；适配−8.241149°，区间[-10.695212,-6.059855]、6/6降误差、Holm3=0.09375；交互−0.228276°，区间[-1.454824,0.858954]、Holm3=1。6患者只有64种符号组合，最小原始双侧p=0.03125，Holm3最低0.09375；不把seed或窗口当患者追求显著性。

full同标准化辅助对比：A_real−I=−0.224781°，区间[-0.367026,-0.105136]；A_mixed−I=−0.206885°，区间[-0.336252,-0.112246]；两项均6/6降误差、原始p=0.03125、Holm2=0.0625。bootstrap区间不能替代多重校正检验；当前不宣称p<0.05的确认性优势。

![全量配平初始化对照](assets/GEN2_full_matched_initialization_20261022.svg)

## 嵌套标定量：已核验的描述性曲线

每seed依`SHA256(GEN2_nested_budget_v1|seed|parent_id)`排序取1、ceil(n/2)、n嵌套前缀，不按信号或分数选段。重复k合并；只有1条TRAIN的目标只有1个真实预算，图中只画1点。各A_k均从对应source G最佳权重开始，绝不从见过全量target的A_full初始化。

|目标标定预算|I_source_scaler患膝RMSE|A_real患膝RMSE|A_mixed患膝RMSE|
|---|---:|---:|---:|
|1条TRAIN|4.315726|3.922012|3.987889|
|ceil(n/2)条|3.584422|3.385850|3.398776|
|全部n条|3.173843|2.949062|2.966957|

真实源预训练在1条、半量、全量的平均差分别为−0.393714°、−0.198571°、−0.224781°；患者改善方向分别6/6、5/6、6/6。曲线不新增显著性检验。半量A_real的3.385850°仍高于full I的3.173843°，目前不能宣称半量标定保持全量个体训练精度。

![患者标定成本曲线](assets/GEN2_patient_calibration_curves_20261022.svg)

图中TRAIN监督crop的患者/seed平均长度约3.779、9.851、17.002秒；对应所选完整参考段约5.779、14.851、25.668秒，还另需固定目标VALID平均9.805秒、source TRAIN/VALID与离线QC。它们是已有裁剪数据的账目，不能解释为临床采集只需数秒。不同k的优化更新、运动/条件覆盖和parent顺序均会改变；full复用保留原manifest序，低k取SHA前缀序；只在同k三方法内匹配数据/更新/RNG，不称跨k计算匹配或纯标签量因果效应。

## 验收证据与决策树

GEN1在72fit验签后生成552新预测/3312逐角指标；独立审计另重跑36个G最佳模型的source VALID（372个trial-model组合），核对等7患者选择分数与history最低值。full参考新增138预测/828指标，另外只读导入276个A预测；138份scratch预测重新从checkpoint独立前向，最大预测差0，目标VALID分数也一致。

预算分析先验签144目标模型+36源G及900个checkpoint/receipt/access/history摘要，再新增162个低预算TEST预测，只读导入90个full TEST预测，共252唯一预测/1512指标。独立审计重跑162个低预算TEST及90模型的完整目标VALID，预测最大差0；唯一TRAIN scaler、嵌套支持、别名处理、成本端点和等trial/seed/患者汇总均通过。总新增预测为552+138+162=852、逐角指标5112；导入记录不重复计数。

```mermaid
flowchart TD
  F[冻结实测分支点] --> G[GEN1：真实/混合源 × 直接预测/适配]
  G --> Z[直接跨患者患膝约11度：零标定仍弱]
  G --> A[适配约2.95度：继续核对预训练价值]
  A --> I[同source scaler从零参考3.17度]
  I --> W[真实源权重收益约0.225度：探索性]
  W --> K[嵌套1条/半量/全量标定]
  K --> C[低数据量有帮助：尚未证明减半保精度]
  G --> V[混合虚拟源无稳定收益：保留负结果]
  C --> N[下一步：训练侧误差机制与独立采集验证]
```

下一步优先基于TRAIN/VALID分解跨患者直接预测的偏差来源、检查source患者训练贡献不均及输入统计变化，再规划独立患者/独立采集验证。任何新增坐标标定、队列或标签定义须另立方案；不据当前TEST重排试次、患者或更改坐标来美化结果。ARCH_AUG继续保留独立分支，本页不使用其成绩决定GEN模型。

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
