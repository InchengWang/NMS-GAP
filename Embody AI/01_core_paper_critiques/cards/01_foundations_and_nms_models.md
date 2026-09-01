# Core Paper Critiques 01 — Frameworks and NMS Body Models

Each card preserves the previously checked Problem/Method/Data/Evaluation evidence and re-evaluates the paper for human NMS Embodied AI. See [`../ASSESSMENT_PROTOCOL.md`](../ASSESSMENT_PROTOCOL.md).

## DT001 — Saxby, Pizzolato & Diamond (2023)

**Citation:** [A Digital Twin Framework for Precision Neuromusculoskeletal Health Care: Extension Upon Industrial Standards](https://doi.org/10.1123/jab.2023-0114), *Journal of Applied Biomechanics*.

- **Primary Type / Evidence:** `embodied_ai_related_weak`; secondary: framework|human NMS architecture; evidence: `full_text_checked`.
- **One-Sentence Contribution:** 把工业数字孪生的功能关系映射到 NMS 医疗，并以 Achilles tendon 多尺度建模说明“观测—模型—工程资产—临床服务”的目标闭环。
- **Problem:** NMS 医疗缺少可检验的数字孪生边界，仿真、传感和治疗常被分别讨论。
- **Method:** 概念框架与案例映射；区分 observable NMS elements、computational models、engineering assets 与 service interfaces。
- **Data:** 无新受试者或前瞻性临床数据；Achilles tendon 场景是整合既有技术的说明性案例。
- **Evaluation:** 评价的是框架与 ISO 工业标准的对应关系，不是预测精度、在线稳定性或治疗获益。
- **Findings:** 论文最重要的贡献是规定双向关系和临床功能，而非宣称现有系统已经是完整孪生。
- **Embodied AI Assessment:** **Primary: `embodied_ai_related_weak`; secondary: framework|human NMS architecture; embodiment: `E0`.** Human NMS modeling: a conceptual neural–muscle–skeletal and tissue hierarchy. Embodied intelligence / sensorimotor control: the perception–action loop is specified but not implemented. Human–robot interaction: none; assistive control: conceptual only. Rehabilitation relevance: high as a research agenda, untested as rehabilitation technology. Subject-specific validation: none. **Judgment:** It contributes a systems architecture for future embodied agents, not empirical embodied intelligence.
- **Limitations:** 作者没有给出统一的不确定性传播、模型身份辨识、长期组织适应验证或监管/数据治理方案；Achilles 案例可能高估不同时间尺度模型被可靠耦合的成熟度。
- **Reproducibility:** 概念文章无可运行系统；术语和功能映射可复核，但没有端到端代码、数据或测试协议。
- **PhD Relevance:** **Strong foundation**。适合作为博士课题的系统边界与反例判据；真正可发表的空间在于实现并验证其中尚为空白的同步、预测和闭环，而不是重复提出框架。 **Embodied-AI use:** Use mainly to define scope and claim boundaries; it is not a technical embodied-agent baseline.

## DT002 — Diniz et al. (2025)

**Citation:** [Digital twin systems for musculoskeletal applications: A current concepts review](https://doi.org/10.1002/ksa.12627), *Knee Surgery, Sports Traumatology, Arthroscopy*.

- **Primary Type / Evidence:** `embodied_ai_related_weak`; secondary: review|musculoskeletal applications; evidence: `full_text_checked`.
- **One-Sentence Contribution:** 从骨科视角整合多体动力学、有限元、可穿戴监测、AI 与临床应用，但证据主体仍是组成技术而非已验证的端到端 twin。
- **Problem:** MSK 数字孪生概念扩张快、临床应用分散，缺少组件和使用场景的共同叙述。
- **Method:** current-concepts narrative review，按模型、数据采集、实时反馈、手术/康复用途和实施障碍组织证据。
- **Data:** 二手文献；没有新的患者数据或独立复现实验。
- **Evaluation:** 没有 PRISMA 式穷尽性或统一偏倚评分，主要评价技术可行性与潜在应用。
- **Findings:** 个体化多尺度模型与 wearables 已分别成熟到可用组件，但互操作、验证、实时计算和临床工作流仍是瓶颈。
- **Embodied AI Assessment:** **Primary: `embodied_ai_related_weak`; secondary: review|musculoskeletal applications; embodiment: `E0`.** Human NMS modeling: surveys multibody, FE and AI components. Embodied intelligence / sensorimotor control: no implemented policy, action loop or environment interaction. Human–robot interaction: none; assistive control: conceptual only. Rehabilitation relevance: medium, through orthopedic use cases rather than tested rehabilitation. Subject-specific validation: reviewed studies are heterogeneous. **Judgment:** It maps enabling components but does not establish an embodied NMS system.
- **Limitations:** “digital twin”纳入边界偏宽，可能把一次性个体模型、监测系统和 predictive twin 混合；缺少按同步、反事实、干预和纵向更新进行的严格分层。
- **Reproducibility:** 检索和编码透明度弱于系统综述；参考文献可追溯，但无开放提取表。
- **PhD Relevance:** **Useful field review**。用于补充骨科/组织尺度版图；不能据此直接主张 NMS twin 已具临床成熟度。 **Embodied-AI use:** Use mainly to define scope and claim boundaries; it is not a technical embodied-agent baseline.

## DT003 — Barricelli, Cerutti & Morzenti (2026)

**Citation:** [Human digital twins in sports and rehabilitation: a systematic review](https://doi.org/10.1080/0144929X.2026.2660222), *Behaviour & Information Technology*.

- **Primary Type / Evidence:** `embodied_ai_related_weak`; secondary: systematic review|field validation; evidence: `full_text_checked`.
- **One-Sentence Contribution:** 用 PRISMA/HCI 视角量化 32 项 HDT 研究的技术、界面和用户参与，揭示很多所谓 twin 仍是小样本监测系统。
- **Problem:** sports/rehabilitation HDT 的设计、交互、AI 使用和用户评价高度碎片化。
- **Method:** 2025-07-11 检索 Scopus 与 Google Scholar；三位作者筛选，最终纳入 2019–2024 年 32 篇。
- **Data:** 32 篇研究；20 篇康复、11 篇运动、1 篇其他；23/32 使用 AI，多数评价样本少于 20，仅两项报告用户参与设计。
- **Evaluation:** 描述性编码 application、goal、technology、interface、user involvement、AI；没有重新验证模型输出或临床效应。
- **Findings:** monitoring 最普遍，expert dashboard 主导；参与式设计、透明 AI、方法标准化与大样本评价明显不足。
- **Embodied AI Assessment:** **Primary: `embodied_ai_related_weak`; secondary: systematic review|field validation; embodiment: `E0`.** Human NMS modeling: audits heterogeneous human digital-twin representations. Embodied intelligence / sensorimotor control: no implemented sensorimotor agent. Human–robot interaction: none; assistive control: none. Rehabilitation relevance: high at field level, but no system-level rehabilitation test. Subject-specific validation: not applicable. **Judgment:** Its real contribution is an audit showing that monitoring interfaces are often mislabeled as twins; it is contextual evidence, not an embodied-AI method.
- **Limitations:** 检索式围绕显式 `digital twin` 术语，容易漏掉实质上更接近 twin、但不用该词的 NMS/robotics 工作；HCI 编码不能替代生理模型有效性审查。
- **Reproducibility:** 检索日、数据库、筛选过程和排除原因较清楚；逐条筛选数据需向作者索取。
- **PhD Relevance:** **Useful validation benchmark**。为“不要以术语判定 twin”提供证据，也提示博士工作必须把真实用户、界面和临床评价纳入技术路线。 **Embodied-AI use:** Use mainly to define scope and claim boundaries; it is not a technical embodied-agent baseline.

## NMS001 — Lloyd & Besier (2004)

**Citation:** [Neuromusculoskeletal modeling: estimation of muscle forces and joint moments and movements from measurements of neural command](https://doi.org/10.1123/jab.20.4.367), *Journal of Applied Biomechanics*.

- **Primary Type / Evidence:** `modeling`; secondary: neural control|physiological mechanics; evidence: `methods_results_checked_via_full_text_secondary_copy`.
- **One-Sentence Contribution:** 奠定以 EMG 神经指令驱动个体肌肉—肌腱动力学、再估计肌力和关节力矩的经典 NMS 链条。
- **Problem:** 逆动力学只能得到净关节力矩，不能解析冗余肌肉如何产生运动。
- **Method:** EMG 处理、激活动力学、Hill-type muscle–tendon mechanics、关节力矩映射与校准组成的生理模型。
- **Data:** 以既有实验和模型案例说明方法；它不是现代意义上的大队列独立验证研究。
- **Evaluation:** 重点是模型结构和用实验关节力矩校准/核对，而非跨中心、跨病种或前瞻性治疗验证。
- **Findings:** EMG 提供个体神经控制信息，可减少纯优化方法对肌肉募集策略的强假设。
- **Embodied AI Assessment:** **Primary: `modeling`; secondary: neural control|physiological mechanics; embodiment: `E1`.** Human NMS modeling: an EMG-to-activation-to-muscle-force-to-joint-moment body model. Embodied intelligence / sensorimotor control: offline neural-to-mechanical inference with no action or environmental feedback. Human–robot interaction: none; assistive control: none. Rehabilitation relevance: indirect but foundational for rehabilitation and assistance. Subject-specific validation: subject-specific calibration in human movement data. **Judgment:** It provides a physiologically interpretable body model for an embodied agent, but no embodied controller.
- **Limitations:** EMG 覆盖、串扰、归一化和深层肌缺失；肌力缺少直接 ground truth，参数可辨识性弱。
- **Reproducibility:** 公式与流程可重建，但原始代码、数据和统一实现并非本文交付物。
- **PhD Relevance:** **Strong foundation**。你的工作若引入 wearable/学习模型，应保留这条可解释的 neural-to-mechanical 链，而不是只预测表面运动量。 **Embodied-AI use:** Use as a physiological body-model baseline; a PhD contribution must add an evaluated perception–action loop or decision consequence.

## NMS002 — Seth et al. (2018)

**Citation:** [OpenSim: Simulating musculoskeletal dynamics and neuromuscular control to study human and animal movement](https://doi.org/10.1371/journal.pcbi.1006223), *PLOS Computational Biology*.

- **Primary Type / Evidence:** `modeling`; secondary: software infrastructure|biomechanics; evidence: `full_text_checked`.
- **One-Sentence Contribution:** 提供开放、可扩展的肌骨动力学平台，使个体模型、最优控制和可复现实验管线成为可能，但平台本身不是 twin。
- **Problem:** NMS 建模需要统一的模型表示、动力学求解、分析与共享机制。
- **Method:** 多体动力学、肌肉模型、inverse/forward simulation、API 与 GUI；文章以多个科学案例说明能力。
- **Data:** 平台论文汇总多个示例和既有数据，不是单一受试者研究。
- **Evaluation:** 软件验证、已发表应用和社区采用；没有对某个患者 twin 进行端到端评价。
- **Findings:** OpenSim 把模型与分析工具标准化，显著降低重复实现成本，并支持从运动重建到预测仿真。
- **Embodied AI Assessment:** **Primary: `modeling`; secondary: software infrastructure|biomechanics; embodiment: `E1`.** Human NMS modeling: a general musculoskeletal dynamics and simulation platform. Embodied intelligence / sensorimotor control: supports optimal control and simulation, but the paper itself does not implement a learning agent or adaptive loop. Human–robot interaction: none in the platform paper; assistive control: possible but not demonstrated. Rehabilitation relevance: broad enabling relevance. Subject-specific validation: models can be scaled to subjects, but validation is application dependent. **Judgment:** OpenSim is body-model infrastructure; using it alone is not an embodied-AI contribution.
- **Limitations:** 结果质量受模型几何、肌肉参数、接触和目标函数影响；平台可运行不等于模型生理正确。
- **Reproducibility:** 高。核心与 GUI 开源，示例和模型生态完整；具体研究仍需公开其个体化和预处理配置。
- **PhD Relevance:** **Strong foundation**。适合作为物理层和基线，不宜把“用了 OpenSim”写成创新点。 **Embodied-AI use:** Use as a physiological body-model baseline; a PhD contribution must add an evaluated perception–action loop or decision consequence.

## NMS003 — Pizzolato et al. (2015)

**Citation:** [CEINMS: A toolbox to investigate the influence of different neural control solutions...](https://doi.org/10.1016/j.jbiomech.2015.09.021), *Journal of Biomechanics*.

- **Primary Type / Evidence:** `modeling`; secondary: personalization|EMG-informed mechanics; evidence: `full_text_checked`.
- **One-Sentence Contribution:** 将 EMG-driven、EMG-assisted 与 hybrid neural control 统一到可校准工具箱中，形成后续个体化内部负荷研究的重要基础。
- **Problem:** 不同 neural control 假设和缺失 EMG 会显著改变肌力/力矩估计，却缺少统一可比较实现。
- **Method:** OpenSim-derived musculotendon kinematics、EMG preprocessing、activation/contraction dynamics、参数校准和多种 excitation 生成模式。
- **Data:** 动态运动实验用于演示模式差异；论文目标是工具和方法验证而非临床效果研究。
- **Evaluation:** 比较模型关节力矩与逆动力学、不同 neural solution 的拟合与计算表现；肌力本身缺少直接真值。
- **Findings:** calibration 与 hybrid excitation 可改善关节力矩匹配，并允许在 EMG 不完整时估计未测肌肉。
- **Embodied AI Assessment:** **Primary: `modeling`; secondary: personalization|EMG-informed mechanics; embodiment: `E1`.** Human NMS modeling: a calibrated EMG-informed/assisted NMS body model. Embodied intelligence / sensorimotor control: estimates internal state offline; no agent action or environment loop. Human–robot interaction: none; assistive control: none. Rehabilitation relevance: high as a mechanistic rehabilitation substrate. Subject-specific validation: subject-specific calibration is central, while internal-force truth remains indirect. **Judgment:** CEINMS is a strong physiological substrate, not an embodied-intelligence system by itself.
- **Limitations:** 最优参数不唯一；净力矩匹配不能证明单肌力或组织负荷正确；EMG 与缩放误差可能被校准吸收。
- **Reproducibility:** 中高。CEINMS 可获得，模型配置和实验数据的开放程度决定具体结果能否复现。
- **PhD Relevance:** **Potential nearest infrastructure**。你的方向可把其作为 mechanistic backbone，再研究稀疏多模态观测、在线 P6 更新与不确定性。 **Embodied-AI use:** Use as a physiological body-model baseline; a PhD contribution must add an evaluated perception–action loop or decision consequence.

## NMS004 — Sartori, Farina & Lloyd (2014)

**Citation:** [Hybrid neuromusculoskeletal modeling to best track joint moments...](https://doi.org/10.1016/j.jbiomech.2014.10.009), *Journal of Biomechanics*.

- **Primary Type / Evidence:** `modeling`; secondary: neural control|missing-muscle inference; evidence: `methods_results_checked`.
- **One-Sentence Contribution:** 以多目标折中最小调整实测 EMG、补全深层/缺失肌激励并匹配关节力矩，解决纯 EMG-driven 与纯优化各自的盲点。
- **Problem:** 表面 EMG 不完整且含噪，而纯静态优化丢失个体真实募集策略。
- **Method:** EMG-informed NMS 与静态优化混合，沿 EMG 保真—力矩跟踪 Pareto 曲线选取 knee point。
- **Data:** 5 名健康男性，地面 walking 与 running，各 8 次试验。
- **Evaluation:** 省略不同肌群 EMG 的模拟缺失试验；比较预测/调整 excitation 与实测 EMG，并检查多 DOF 力矩跟踪。
- **Findings:** 仅适度调整 EMG 即显著改善力矩匹配，并能推断深层或缺失肌激励。
- **Embodied AI Assessment:** **Primary: `modeling`; secondary: neural control|missing-muscle inference; embodiment: `E1`.** Human NMS modeling: a hybrid EMG-informed NMS representation. Embodied intelligence / sensorimotor control: infers latent excitations and joint moments offline without selecting actions. Human–robot interaction: none; assistive control: none. Rehabilitation relevance: indirect. Subject-specific validation: healthy subject-specific models with limited sample diversity. **Judgment:** It advances neural-state completion for body modeling, not embodied control.
- **Limitations:** 小而单一健康样本；用净力矩约束补全 EMG 存在多解，预测 excitation 的生理真实性不能由同一力矩目标充分证明。
- **Reproducibility:** 中。模型描述充分，但原始数据/完整评估脚本未形成现代端到端开放包。
- **PhD Relevance:** **Strong method foundation**。它提供“缺失肌肉观测”的机制基线，适合与 learned latent neural state 比较。 **Embodied-AI use:** Use as a physiological body-model baseline; a PhD contribution must add an evaluated perception–action loop or decision consequence.

## NMS005 — Durandau, Farina & Sartori (2018)

**Citation:** [Robust Real-Time Musculoskeletal Modeling Driven by Electromyograms](https://doi.org/10.1109/TBME.2017.2704085), *IEEE Transactions on Biomedical Engineering*.

- **Primary Type / Evidence:** `modeling`; secondary: real-time state estimation|personalization; evidence: `methods_results_checked`.
- **One-Sentence Contribution:** 首次把校准后的 EMG-driven 下肢 NMS 模型压到实时运行，并在未见任务及未用于校准的 DOF 上检验外推。
- **Problem:** 传统临床生物力学延迟高，无法作为人机接口的在线内部状态估计器。
- **Method:** 个体校准的 EMG-to-activation-to-muscle-force-to-joint-moment pipeline；13 个 muscle–tendon units、3 个下肢 DOF 实时并行。
- **Data:** 健康参与者完成多种下肢任务；本轮核验到 6 个未见任务与 1 个未见 DOF 的外推设计，但原始队列细节应以正文表格复核。
- **Evaluation:** 与实验净关节力矩比较，报告实时计算延迟和 calibration-to-unseen-task 泛化。
- **Findings:** 在实时约束下仍可估计肌力/多 DOF 力矩，并跨出校准条件。
- **Embodied AI Assessment:** **Primary: `modeling`; secondary: real-time state estimation|personalization; embodiment: `E1`.** Human NMS modeling: a real-time subject-specific EMG-driven lower-limb NMS model. Embodied intelligence / sensorimotor control: continuous sensing updates the body state, but the evaluated paper does not close an action–environment loop. Human–robot interaction: no physical robot in this study; assistive control: potential downstream use. Rehabilitation relevance: high as the state-estimation layer for assistance. Subject-specific validation: subject-specific real-time validation including unseen tasks/DOF. **Judgment:** It is a nearest real-time body-state estimator; embodied intelligence begins only when its estimate changes action and is evaluated in interaction.
- **Limitations:** 健康实验和净力矩 surrogate 不能验证肌力；EMG 电极迁移、疲劳、病理神经控制与长时漂移未覆盖。
- **Reproducibility:** 中。作者稿和算法细节可得，但当时的完整实时软件、硬件同步与原始数据开放有限。
- **PhD Relevance:** **Potential nearest prior work**。这是“实时 mechanistic twin”主线的关键起点；博士创新应放在多模态可观测性、患者状态更新、uncertainty 与闭环安全，而非仅再做实时化。 **Embodied-AI use:** Use as a physiological body-model baseline; a PhD contribution must add an evaluated perception–action loop or decision consequence.

