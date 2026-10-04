# 博士研究计划中文概要

**题目：面向具身康复交互的 UWB 动作捕捉与决策验证型人体神经肌骨数字孪生**

英文题目：**Toward Decision-Validated Human Neuromusculoskeletal Digital Twins: UWB Motion Capture for Embodied Rehabilitation Interaction**

拟开展环境：南方科技大学张明明课题组。证据核查日期：2026-10-04。完整计划、实验细节和统计方案见 [PHD_PROPOSAL.md](PHD_PROPOSAL.md)；逐项 gap verdict、nearest prior work、文献状态与访问深度见 [GAP_VALIDATION_AND_NEAREST_WORK.md](GAP_VALIDATION_AND_NEAREST_WORK.md)。

## 1. 定位与背景

主线是 **人体神经肌骨系统 + 具身智能 + sensing/modeling/control/interaction**。主要动作观测工具为可穿戴 **UWB 标签与锚点**，不是 IMU gait analysis。IMU 仅作为可选补充、消融或对照。

动作捕捉的价值不止是输出看起来合理的姿态，而是为人体状态判断和下一步物理动作提供可靠信息。UWB 测量能够约束空间关系，但人体遮挡、几何退化、异步采样和重新佩戴可能造成系统性误差；距离本身也不能唯一确定全部关节转动，更不能直接给出神经驱动或肌肉力。

因此，计划从 UWB 的任务可观测性出发，以有独立参考的 EMG/力学模型连接神经、肌肉与运动，再验证该人体状态是否有助于物理交互。具身智能体需要预测动作后果、执行有界动作并根据实际响应更新状态。

**工作假设**是使用 ranging/localization 平台，而非无接触 UWB radar。实际硬件能否输出原始 TDoA/TWR、标签间距离及质量诊断，必须先核实。若仅提供位置输出，则采用经验位置误差模型，不承诺原始射频级推断。

## 2. State of the art 与 novelty 边界

已有 UWB 关节角测量 [R01]、上肢 IMU/UWB 融合 [R20]、UI-MoCap 硬件 [R02]、稀疏融合全身重建 [R03], [R05]、不确定性融合 [R04]、显式距离几何 [R06]、纯距离全身运动推断 [R07]，以及 UWB 姿态识别驱动机器人命令 [R08]。

动作到肌骨分析 [R11]、实时 EMG 神经机械控制 [R12]、NMS 不确定性辅助控制 [R13]、模型个体化 [R14]、卒中患者简化手臂模型 [R21] 和个体化上肢柔顺控制 [R18] 也已有先例。因此，不把“换成 UWB”“加入不确定性”“建立患者模型”或“连接机器人”单独写成创新。

## 3. Validated gap

承接原 dossier 已进行文献验证的 **G07/G01、G04、G05**，其相关 verdict 为 **partially-addressed**。本次收窄为三个可检验的剩余问题：

1. UWB 实际约束了哪些任务相关人体状态，重新佩戴与遮挡后该边界是否仍可靠？
2. 空间与校准不确定性是否会改变可独立评估的神经肌骨预测？
3. 这些状态信息是否改善真实物理动作的风险与任务表现，而强基线不能同样做到？

这是有反证边界的研究残余，不是已经证明的新方法，也不是“尚无完整整合系统，所以一定新颖”。旧 G02 多时间尺度论点不直接继承为 UWB 创新。

## 4. Central research question 与 hypothesis

**核心问题：**以 UWB 为中心的观测组合能够可靠恢复哪些人体状态？显式保留它们的不确定性，是否比动作信息、点估计模型和普通故障回退更有利于个体化 NMS 预测及有界康复交互？

**中心假设：**区分测量约束、运动先验、每次佩戴校准和 EMG 力学信息，可提高跨会话预测的可靠性，并在部分条件下改善动作决策。其三个子假设分别由 Aim 1–3 检验；如果简化模型或现有控制器已足够，就缩减模型复杂度并报告负结果。

## 5. Specific Aim 1–3

| Aim | 研究内容 | 独立证据与主指标 | Nearest prior work / 推翻条件 |
|---|---|---|---|
| **Aim 1：UWB 任务可观测性与失效边界** | 先用编码器机械台架检验几何歧义，再在重复佩戴、遮挡、锚点变化中比较解剖状态估计和可信度。全身功能动作是感知基准，坐位上肢任务是后续主端点。 | 光学/编码器参考；留出会话肘角 CRPS，配合误差尾部、区间覆盖/宽度、可用数据比例和延迟。 | [R01], [R04], [R06], [R07], [R20] 已解决相邻问题。若几何无法满足任务要求，收窄状态或明确最低补充观测需求。 |
| **Aim 2：UWB 驱动的人体 NMS 预测** | 在一个躯干—上肢子系统中融合目标 EMG 和已测外力，传播 UWB/佩戴不确定性，区分初次个体化、校准更新与小规模模型更新。 | 光学运动与独立外力形成净关节力矩参考；锁定未来会话/未见负载的净力矩 CRPS，配合偏差、覆盖及参数补偿分析。 | [R11], [R12], [R13], [R14], [R21] 已有模型与预测工具。若校准或黑箱基线同样有效，不能宣称更强的生理解释。 |
| **Aim 3：有界具身交互的决策价值** | 同一 admittance/assist-as-needed 控制器比较动作信息、NMS 点估计和后验信息；先离线/硬件在环，再条件性开展短时人体交互。 | 继续执行的动作中，独立定义的约束违规风险，联合任务表现非劣检验；同时记录回退负担、实际力与响应预测误差。 | [R08], [R12], [R13], [R18] 已有 HRI/自适应辅助。若编码器/力控制或普通回退足够，复杂人体表示不成立为该任务的必要贡献。 |

## 6. Methodology、baselines 与 metrics

主力学/交互任务暂选**坐位到达中的躯干—上肢子系统**，以便测量外力并限制控制复杂度；这是与导师讨论的可执行选择，尚非设备或临床资源承诺。全身肌肉辨识、新机器人和新 RL 算法均不作为毕业依赖。

UWB 为部署动作传感输入；需要神经—肌肉论断时加入目标 sEMG，需要动力学论断时加入手柄力、负载或测力装置。光学系统用于实验室参考。可选 IMU 单独标注，不能把融合结果归为 UWB-only。

TDoA 按距离差与时钟项建模，共享参考锚点误差保留相关性；TWR/标签间测距仅在实际接口支持时采用。滤波与模型在运行时保持因果；离线平滑另外标注。简化激活动力学/Hill 型肌肉模型只估计数据支持的少量参数，不用模型自己生成的肌肉力当真值。

强基线包括：经典定位+IK、兼容的 WiP/UIP/UMotion/UDP、可选上肢融合；通用/单次个体化/仅校准更新/小规模模型更新；点输入/不确定性传播/概率黑箱/校准包装；编码器与力反馈、动作控制、点 NMS、后验 NMS、确定性回退。比较时尽量统一传感信息、校准时间、计算与佩戴负担。

主要端点之外，还报告解剖角误差、物理坐标系手部位置误差、覆盖与区间宽度、延迟、空口资源、缺失捕捉、实际响应和任务完成度。NLOS/OOD 标签不是危险真值；不断回退导致的低作用力也不是有用交互。

## 7. Statistical analysis

参与者是主要推断单位，帧/动作/会话为重复测量。采用混合效应模型与参与者聚类 bootstrap；锁定跨人、时间顺序会话和负载测试，所有校准与阈值仅用开发数据。三项主对比在联合确认性声明时采用 Holm 校正，报告效应量与区间。

先导拟 6–8 名健康参与者、2–3 次访问；感知/力学主研究暂按 20–24 名健康参与者规划；卒中 12–16 名及健康交互 12–16 名均为条件性资源范围，**不是已经完成的 power analysis**。正式样本量由先导方差、相关性、脱落与各 Aim 的精度/效能分析确定。

非劣界值、控制约束和动作容差在先导后、独立主测试前锁定。人体辅助顺序随机/平衡，并检查残留适应。捕捉失败与回退也是结果；零事件不能证明临床安全，短时交叉实验不能证明长期康复。

## 8. Expected contributions、risks and alternatives

预期贡献为：任务相关 UWB 信息边界；测量不确定性对独立 NMS 端点的影响证据；人体状态对动作价值的因果/实验检验；可复现的 sensing–model–decision 评估轨迹。贡献均有条件，不把完整 pipeline 的存在本身当科学发现。

若 UWB 精度不足，调整几何、减少自由度或量化可选补充模态的必要性；若参数不可辨识，报告等价类并简化模型；若模型无法改善决策，保留有依据的负结果；若机器人/临床资源不可得，完成重复会话、预测及 HIL 验证，不扩大到患者疗效。

## 9. Timeline 与 fit

按**确认入学日起 36 个月**规划：0–6 月硬件/几何先导；6–12 月 Aim 1；10–25 月 Aim 2 及锁定预测；22–29 月 HIL；27–32 月条件性短时交互；32–36 月综合验证与论文。此时间表不宣称学校已经确认学制。

工程力学、Kalman 滤波与半递归肌骨动力学经验，适合观测模型与力学辨识；现有慢性卒中稀疏传感研究可迁移会话验证、缺失数据与患者异质性处理。博士阶段需要补强 UWB 射频/时序、实际可辨识性、EMG、外力参考和人机控制。

张明明课题组的 UI-MoCap 与上肢柔顺控制提供具体衔接 [R02], [R18], [R19]。Hayashibe 的具身/计算研究背景可形成概念连续性；Durandau/Sartori 与 Pizzolato 的神经机械建模工作可作为方法交流方向 [R12], [R14], [R15]，不表述为已落实合作或资源。计划的关键匹配是从 **UWB sensing 到人体 modeling，再到有证据的 control/interaction**。

[R01]: https://pubmed.ncbi.nlm.nih.gov/24403428/
[R02]: https://pubmed.ncbi.nlm.nih.gov/38408007/
[R03]: https://siplab.org/projects/UltraInertialPoser
[R04]: https://arxiv.org/html/2505.09393v1
[R05]: https://siplab.org/projects/GroupInertialPoser
[R06]: https://siplab.org/projects/UltraDiffusionPoser
[R07]: https://arxiv.org/html/2601.19519v1
[R08]: https://tiers.utu.fi/publications/
[R09]: https://ieeexplore.ieee.org/document/11420874
[R10]: https://www.mdpi.com/1424-8220/26/18/5738
[R11]: https://pubmed.ncbi.nlm.nih.gov/39579665/
[R12]: https://research.utwente.nl/en/publications/ceinms-rt-an-open-source-framework-for-the-continuous-neuro-mecha-2/
[R13]: https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1254088/full
[R14]: https://link.springer.com/article/10.1186/s12984-025-01629-5
[R15]: https://proceedings.mlr.press/v168/caggiano22a.html
[R16]: https://www.nature.com/articles/s41586-024-07382-4
[R17]: https://link.springer.com/article/10.1186/s12984-026-02136-x
[R18]: https://www.sciencedirect.com/science/article/abs/pii/S092188901930898X
[R19]: https://www.sustech.edu.cn/en/faculties/zhangmingming.html
[R20]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10422251/
[R21]: https://pubmed.ncbi.nlm.nih.gov/30056607/

