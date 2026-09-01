# Core Paper Critiques 01 — Frameworks and Modeling Foundations

批判标准见 [`../CRITIQUE_PROTOCOL.md`](../CRITIQUE_PROTOCOL.md)。`L0–L5` 与 `P0–P6` 沿用文献地图的操作性定义。证据等级表示本轮实际核验深度，不等于论文质量。

## DT001 — Saxby, Pizzolato & Diamond (2023)

**Citation:** [A Digital Twin Framework for Precision Neuromusculoskeletal Health Care: Extension Upon Industrial Standards](https://doi.org/10.1123/jab.2023-0114), *Journal of Applied Biomechanics*.

- **Type / Evidence:** framework/modeling；`full_text_checked`。
- **One-Sentence Contribution:** 把工业数字孪生的功能关系映射到 NMS 医疗，并以 Achilles tendon 多尺度建模说明“观测—模型—工程资产—临床服务”的目标闭环。
- **Problem:** NMS 医疗缺少可检验的数字孪生边界，仿真、传感和治疗常被分别讨论。
- **Method:** 概念框架与案例映射；区分 observable NMS elements、computational models、engineering assets 与 service interfaces。
- **Data:** 无新受试者或前瞻性临床数据；Achilles tendon 场景是整合既有技术的说明性案例。
- **Evaluation:** 评价的是框架与 ISO 工业标准的对应关系，不是预测精度、在线稳定性或治疗获益。
- **Findings:** 论文最重要的贡献是规定双向关系和临床功能，而非宣称现有系统已经是完整孪生。
- **Digital Twin Assessment:** 目标架构接近 `L4–L5`，但本文自身是未实现的框架；个体化、状态更新、组织负荷预测和干预均被定义而非共同验证。不能把它作为完整 twin 的实证先例。
- **Limitations:** 作者没有给出统一的不确定性传播、模型身份辨识、长期组织适应验证或监管/数据治理方案；Achilles 案例可能高估不同时间尺度模型被可靠耦合的成熟度。
- **Reproducibility:** 概念文章无可运行系统；术语和功能映射可复核，但没有端到端代码、数据或测试协议。
- **PhD Relevance:** **Strong foundation**。适合作为博士课题的系统边界与反例判据；真正可发表的空间在于实现并验证其中尚为空白的同步、预测和闭环，而不是重复提出框架。

## DT002 — Diniz et al. (2025)

**Citation:** [Digital twin systems for musculoskeletal applications: A current concepts review](https://doi.org/10.1002/ksa.12627), *Knee Surgery, Sports Traumatology, Arthroscopy*.

- **Type / Evidence:** review/framework；`full_text_checked`（作者开放稿）。
- **One-Sentence Contribution:** 从骨科视角整合多体动力学、有限元、可穿戴监测、AI 与临床应用，但证据主体仍是组成技术而非已验证的端到端 twin。
- **Problem:** MSK 数字孪生概念扩张快、临床应用分散，缺少组件和使用场景的共同叙述。
- **Method:** current-concepts narrative review，按模型、数据采集、实时反馈、手术/康复用途和实施障碍组织证据。
- **Data:** 二手文献；没有新的患者数据或独立复现实验。
- **Evaluation:** 没有 PRISMA 式穷尽性或统一偏倚评分，主要评价技术可行性与潜在应用。
- **Findings:** 个体化多尺度模型与 wearables 已分别成熟到可用组件，但互操作、验证、实时计算和临床工作流仍是瓶颈。
- **Digital Twin Assessment:** 文章描述的理想系统为 `L3–L5`；所综述的大多数工作实际停留在 `L1–L2`。它是领域导航，不是接近真正 twin 的实证工作。
- **Limitations:** “digital twin”纳入边界偏宽，可能把一次性个体模型、监测系统和 predictive twin 混合；缺少按同步、反事实、干预和纵向更新进行的严格分层。
- **Reproducibility:** 检索和编码透明度弱于系统综述；参考文献可追溯，但无开放提取表。
- **PhD Relevance:** **Useful field review**。用于补充骨科/组织尺度版图；不能据此直接主张 NMS twin 已具临床成熟度。

## DT003 — Barricelli, Cerutti & Morzenti (2026)

**Citation:** [Human digital twins in sports and rehabilitation: a systematic review](https://doi.org/10.1080/0144929X.2026.2660222), *Behaviour & Information Technology*.

- **Type / Evidence:** systematic review/validation-of-field；`full_text_checked`。
- **One-Sentence Contribution:** 用 PRISMA/HCI 视角量化 32 项 HDT 研究的技术、界面和用户参与，揭示很多所谓 twin 仍是小样本监测系统。
- **Problem:** sports/rehabilitation HDT 的设计、交互、AI 使用和用户评价高度碎片化。
- **Method:** 2025-07-11 检索 Scopus 与 Google Scholar；三位作者筛选，最终纳入 2019–2024 年 32 篇。
- **Data:** 32 篇研究；20 篇康复、11 篇运动、1 篇其他；23/32 使用 AI，多数评价样本少于 20，仅两项报告用户参与设计。
- **Evaluation:** 描述性编码 application、goal、technology、interface、user involvement、AI；没有重新验证模型输出或临床效应。
- **Findings:** monitoring 最普遍，expert dashboard 主导；参与式设计、透明 AI、方法标准化与大样本评价明显不足。
- **Digital Twin Assessment:** 这是领域成熟度审计，不是 twin 实现。其结果反而支持“多数 HDT 只是 sensing/monitoring + dashboard”的判断。
- **Limitations:** 检索式围绕显式 `digital twin` 术语，容易漏掉实质上更接近 twin、但不用该词的 NMS/robotics 工作；HCI 编码不能替代生理模型有效性审查。
- **Reproducibility:** 检索日、数据库、筛选过程和排除原因较清楚；逐条筛选数据需向作者索取。
- **PhD Relevance:** **Useful validation benchmark**。为“不要以术语判定 twin”提供证据，也提示博士工作必须把真实用户、界面和临床评价纳入技术路线。

## NMS001 — Lloyd & Besier (2004)

**Citation:** [Neuromusculoskeletal modeling: estimation of muscle forces and joint moments and movements from measurements of neural command](https://doi.org/10.1123/jab.20.4.367), *Journal of Applied Biomechanics*.

- **Type / Evidence:** modeling foundation；`methods_results_checked_via_full_text_secondary_copy`。
- **One-Sentence Contribution:** 奠定以 EMG 神经指令驱动个体肌肉—肌腱动力学、再估计肌力和关节力矩的经典 NMS 链条。
- **Problem:** 逆动力学只能得到净关节力矩，不能解析冗余肌肉如何产生运动。
- **Method:** EMG 处理、激活动力学、Hill-type muscle–tendon mechanics、关节力矩映射与校准组成的生理模型。
- **Data:** 以既有实验和模型案例说明方法；它不是现代意义上的大队列独立验证研究。
- **Evaluation:** 重点是模型结构和用实验关节力矩校准/核对，而非跨中心、跨病种或前瞻性治疗验证。
- **Findings:** EMG 提供个体神经控制信息，可减少纯优化方法对肌肉募集策略的强假设。
- **Digital Twin Assessment:** `L1` twin-enabling modeling；有 P3–P4 个体化潜力，但没有在线同步、反事实临床预测或干预闭环。
- **Limitations:** EMG 覆盖、串扰、归一化和深层肌缺失；肌力缺少直接 ground truth，参数可辨识性弱。
- **Reproducibility:** 公式与流程可重建，但原始代码、数据和统一实现并非本文交付物。
- **PhD Relevance:** **Strong foundation**。你的工作若引入 wearable/学习模型，应保留这条可解释的 neural-to-mechanical 链，而不是只预测表面运动量。

## NMS002 — Seth et al. (2018)

**Citation:** [OpenSim: Simulating musculoskeletal dynamics and neuromuscular control to study human and animal movement](https://doi.org/10.1371/journal.pcbi.1006223), *PLOS Computational Biology*.

- **Type / Evidence:** modeling/software infrastructure；`full_text_checked`。
- **One-Sentence Contribution:** 提供开放、可扩展的肌骨动力学平台，使个体模型、最优控制和可复现实验管线成为可能，但平台本身不是 twin。
- **Problem:** NMS 建模需要统一的模型表示、动力学求解、分析与共享机制。
- **Method:** 多体动力学、肌肉模型、inverse/forward simulation、API 与 GUI；文章以多个科学案例说明能力。
- **Data:** 平台论文汇总多个示例和既有数据，不是单一受试者研究。
- **Evaluation:** 软件验证、已发表应用和社区采用；没有对某个患者 twin 进行端到端评价。
- **Findings:** OpenSim 把模型与分析工具标准化，显著降低重复实现成本，并支持从运动重建到预测仿真。
- **Digital Twin Assessment:** `L0` generic simulator / twin substrate。只有绑定个体、持续更新并经未见条件验证后才可能进入 `L1–L3`。
- **Limitations:** 结果质量受模型几何、肌肉参数、接触和目标函数影响；平台可运行不等于模型生理正确。
- **Reproducibility:** 高。核心与 GUI 开源，示例和模型生态完整；具体研究仍需公开其个体化和预处理配置。
- **PhD Relevance:** **Strong foundation**。适合作为物理层和基线，不宜把“用了 OpenSim”写成创新点。

## NMS003 — Pizzolato et al. (2015)

**Citation:** [CEINMS: A toolbox to investigate the influence of different neural control solutions...](https://doi.org/10.1016/j.jbiomech.2015.09.021), *Journal of Biomechanics*.

- **Type / Evidence:** modeling + personalization infrastructure；`full_text_checked`。
- **One-Sentence Contribution:** 将 EMG-driven、EMG-assisted 与 hybrid neural control 统一到可校准工具箱中，形成后续个体化内部负荷研究的重要基础。
- **Problem:** 不同 neural control 假设和缺失 EMG 会显著改变肌力/力矩估计，却缺少统一可比较实现。
- **Method:** OpenSim-derived musculotendon kinematics、EMG preprocessing、activation/contraction dynamics、参数校准和多种 excitation 生成模式。
- **Data:** 动态运动实验用于演示模式差异；论文目标是工具和方法验证而非临床效果研究。
- **Evaluation:** 比较模型关节力矩与逆动力学、不同 neural solution 的拟合与计算表现；肌力本身缺少直接真值。
- **Findings:** calibration 与 hybrid excitation 可改善关节力矩匹配，并允许在 EMG 不完整时估计未测肌肉。
- **Digital Twin Assessment:** `L1` personalization/modeling substrate；可构成 `L2–L4` 系统的机制核心，但本文没有持续物理同步或行动闭环。
- **Limitations:** 最优参数不唯一；净力矩匹配不能证明单肌力或组织负荷正确；EMG 与缩放误差可能被校准吸收。
- **Reproducibility:** 中高。CEINMS 可获得，模型配置和实验数据的开放程度决定具体结果能否复现。
- **PhD Relevance:** **Potential nearest infrastructure**。你的方向可把其作为 mechanistic backbone，再研究稀疏多模态观测、在线 P6 更新与不确定性。

## NMS004 — Sartori, Farina & Lloyd (2014)

**Citation:** [Hybrid neuromusculoskeletal modeling to best track joint moments...](https://doi.org/10.1016/j.jbiomech.2014.10.009), *Journal of Biomechanics*.

- **Type / Evidence:** modeling paper；`methods_results_checked`。
- **One-Sentence Contribution:** 以多目标折中最小调整实测 EMG、补全深层/缺失肌激励并匹配关节力矩，解决纯 EMG-driven 与纯优化各自的盲点。
- **Problem:** 表面 EMG 不完整且含噪，而纯静态优化丢失个体真实募集策略。
- **Method:** EMG-informed NMS 与静态优化混合，沿 EMG 保真—力矩跟踪 Pareto 曲线选取 knee point。
- **Data:** 5 名健康男性，地面 walking 与 running，各 8 次试验。
- **Evaluation:** 省略不同肌群 EMG 的模拟缺失试验；比较预测/调整 excitation 与实测 EMG，并检查多 DOF 力矩跟踪。
- **Findings:** 仅适度调整 EMG 即显著改善力矩匹配，并能推断深层或缺失肌激励。
- **Digital Twin Assessment:** `L1` modeling；有个体 neural-control 表征，但主要是离线重建，不具实时更新、反事实验证或干预。
- **Limitations:** 小而单一健康样本；用净力矩约束补全 EMG 存在多解，预测 excitation 的生理真实性不能由同一力矩目标充分证明。
- **Reproducibility:** 中。模型描述充分，但原始数据/完整评估脚本未形成现代端到端开放包。
- **PhD Relevance:** **Strong method foundation**。它提供“缺失肌肉观测”的机制基线，适合与 learned latent neural state 比较。

## NMS005 — Durandau, Farina & Sartori (2018)

**Citation:** [Robust Real-Time Musculoskeletal Modeling Driven by Electromyograms](https://doi.org/10.1109/TBME.2017.2704085), *IEEE Transactions on Biomedical Engineering*.

- **Type / Evidence:** modeling + real-time personalization；`methods_results_checked`（开放作者稿）。
- **One-Sentence Contribution:** 首次把校准后的 EMG-driven 下肢 NMS 模型压到实时运行，并在未见任务及未用于校准的 DOF 上检验外推。
- **Problem:** 传统临床生物力学延迟高，无法作为人机接口的在线内部状态估计器。
- **Method:** 个体校准的 EMG-to-activation-to-muscle-force-to-joint-moment pipeline；13 个 muscle–tendon units、3 个下肢 DOF 实时并行。
- **Data:** 健康参与者完成多种下肢任务；本轮核验到 6 个未见任务与 1 个未见 DOF 的外推设计，但原始队列细节应以正文表格复核。
- **Evaluation:** 与实验净关节力矩比较，报告实时计算延迟和 calibration-to-unseen-task 泛化。
- **Findings:** 在实时约束下仍可估计肌力/多 DOF 力矩，并跨出校准条件。
- **Digital Twin Assessment:** 接近 `L2` digital shadow：个体模型与连续 EMG 更新真实存在；尚无由模型输出改变治疗/机器人并验证获益的 `L4` 闭环，也无纵向 P6。
- **Limitations:** 健康实验和净力矩 surrogate 不能验证肌力；EMG 电极迁移、疲劳、病理神经控制与长时漂移未覆盖。
- **Reproducibility:** 中。作者稿和算法细节可得，但当时的完整实时软件、硬件同步与原始数据开放有限。
- **PhD Relevance:** **Potential nearest prior work**。这是“实时 mechanistic twin”主线的关键起点；博士创新应放在多模态可观测性、患者状态更新、uncertainty 与闭环安全，而非仅再做实时化。
