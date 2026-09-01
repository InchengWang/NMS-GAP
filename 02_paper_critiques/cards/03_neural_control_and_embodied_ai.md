# Core Paper Critiques 03 — Neural Control and Embodied AI

批判标准见 [`../CRITIQUE_PROTOCOL.md`](../CRITIQUE_PROTOCOL.md)。本组区分“解释或生成控制策略”与“持续绑定真实个体的数字孪生”；在通用肌骨仿真器中训练策略，默认仍为 `L0`。

## NEU001 — Sartori, Yavuz & Farina (2017)

**Citation:** [In Vivo Neuromechanics: Decoding Causal Motor Neuron Behavior with Resulting Musculoskeletal Function](https://doi.org/10.1038/s41598-017-13766-6), *Scientific Reports*.

- **Type / Evidence:** modeling + validation；`full_text_checked`。
- **One-Sentence Contribution:** 首次把分解得到的 motor-unit discharge trains 直接送入个体化肌骨模型，建立 spinal motor neuron activity 到肌力与关节力矩的因果计算链。
- **Problem:** 表面 EMG 幅值与神经驱动、肌力和运动之间隔着多层非线性，难以解释神经控制如何形成整体机械功能。
- **Method:** HD-EMG decomposition、motor-unit-to-whole-muscle neural drive、Hill-type muscle–tendon dynamics 与 subject-specific joint mechanics 串联，并与常规 EMG-driven 模型比较。
- **Data:** 人体收缩实验中的 HD-EMG、关节运动/力矩和个体模型；研究规模适合机制证明，不是临床队列。
- **Evaluation:** 比较预测与参考 joint moments，并检验从 motor neuron discharge 到 whole-muscle force 的一致性和跨任务表现。
- **Findings:** motor-unit discharge 能形成可解释的 neural-to-mechanical mapping，减少 amplitude EMG 对传导与归一化的依赖。
- **Digital Twin Assessment:** `L1–L2` twin-enabling modeling/validation；代表 NMS twin 的“神经状态观测器”，但无长期同步、未见干预反事实或闭环控制。
- **Limitations:** HD-EMG decomposition 对信噪比和可分解肌肉敏感；深层/未测肌仍靠假设；关节力矩一致不等于内部肌力唯一正确。
- **Reproducibility:** 中等；全文、公式和补充材料开放，但完整原始数据与端到端运行包并非本文交付物。
- **PhD Relevance:** **Strong foundation**。适合构建 neural-control layer；博士工作需处理 sparse wearable sensing 下的可观测性、参数不确定性和跨日稳定性。

## NEU002 — Farina et al. (2017)

**Citation:** [Man/machine interface based on the discharge timings of spinal motor neurons after targeted muscle reinnervation](https://doi.org/10.1038/s41551-016-0025), *Nature Biomedical Engineering*.

- **Type / Evidence:** sensing/neural interface + validation；`methods_results_checked`。
- **One-Sentence Contribution:** 在 6 名高位上肢截肢者中证明 targeted muscle reinnervation 后可解码 spinal motor neuron discharge，并离线映射为多自由度假肢命令。
- **Problem:** 常规 myoelectric control 难以提供直观、并行、连续的多自由度控制。
- **Method:** reinnervated muscle EMG decomposition，比较 proportional control、pattern recognition 与 musculoskeletal mapping 三条离线解码路径。
- **Data:** 6 名 shoulder/humeral-level amputation 患者；重定向肌肉 EMG、phantom-limb task labels 与个体几何/运动信息。
- **Evaluation:** 对比 conventional global-EMG control 的分类或连续 kinematic estimation；包含并发多自由度任务，但主要为离线实验。
- **Findings:** motor-neuron timing 提供比 global EMG 更具生理结构的控制信号，支持多自由度意图解码。
- **Digital Twin Assessment:** `L2` sensing/interface paper，不是完整 twin；有实时 twin 所需的 neural state observation，却没有持续机械状态校正、反事实预测或 device-in-the-loop 临床评价。
- **Limitations:** 小样本、手术人群特殊；离线性能不能推出长期假肢使用获益；神经解码的跨日鲁棒性与 recalibration burden 未解决。
- **Reproducibility:** 中低；方法与图示充分，但患者数据、手术条件和专用解码管线难以独立复现。
- **PhD Relevance:** **Strong sensing benchmark**。说明“更接近神经源头”可提升可解释性，但博士课题应把它接到实时 NMS state estimation 与功能性 device outcomes。

## NEU003 — Kapelner et al. (2020)

**Citation:** [Neuro-Musculoskeletal Mapping for Man-Machine Interfacing](https://doi.org/10.1038/s41598-020-62773-7), *Scientific Reports*.

- **Type / Evidence:** modeling + neural-interface validation；`full_text_checked`。
- **One-Sentence Contribution:** 用 inverse biomechanical calibration 和 motor-unit regression 建立 HD-EMG neural drive 到 wrist kinematics 的闭合映射，并在 intact 与 amputee 数据中验证。
- **Problem:** purely data-driven myoelectric mapping 缺少机械约束，跨组合动作的泛化和可解释性有限。
- **Method:** 校准阶段由个体肌骨模型反求 muscle excitation，再训练 motor-unit discharge regression；测试阶段以前向动力学输出 wrist movement。
- **Data:** 6 名 intact-bodied 参与者和 2 名 transradial amputees；256-channel HD-EMG 与 wrist kinematics。
- **Evaluation:** 未见组合/多自由度动作上的 kinematic prediction 和不同映射方案比较；验证仍以实验室离线数据为主。
- **Findings:** 生理模型可把 neural decoding 转成连续运动命令，并在数据稀疏的动作组合上提供结构性先验。
- **Digital Twin Assessment:** `L1–L2` modeling/interface paper；person-specific calibration 存在，但模型没有在真实装置/日常环境中被连续更新。
- **Limitations:** n=8 且 amputee 仅 2；对高密度阵列、decomposition quality 和对侧 kinematic proxy 依赖强；无长期 functional outcome。
- **Reproducibility:** 中等；开放全文、OpenSim 基础与方法细节可用，完整患者数据和训练管线开放程度有限。
- **PhD Relevance:** **Potential architecture component**。它展示 neural observation 与 mechanics 如何耦合；可延伸为 uncertainty-aware online mapping，而不是仅优化离线 angle error。

## NEU004 — Jung et al. (2022)

**Citation:** [Intramuscular EMG-Driven Musculoskeletal Modelling: Towards Implanted Muscle Interfacing in Spinal Cord Injury Patients](https://doi.org/10.1109/TBME.2021.3087137), *IEEE TBME*.

- **Type / Evidence:** sensing + modeling validation；`methods_results_checked`。
- **One-Sentence Contribution:** 在 4 名健康者和 3 名 incomplete SCI 患者中证明 sparse intramuscular EMG 可经个体 NMS 模型估计步行辅助力矩，性能与 surface EMG 相近。
- **Problem:** implanted EMG 更稳定且可长期使用，但局部采样是否足以驱动多肌肉 NMS estimator 不清楚。
- **Method:** 同步 intramuscular/surface EMG、mocap、GRF，建立 subject-specific models 并分别估计所需 assistive joint torques。
- **Data:** 7 人，多速度步行；其中 3 名 incomplete SCI。
- **Evaluation:** predicted versus inverse-dynamics joint torques 的 correlation/error，并比较两种 EMG 输入与人群差异。
- **Findings:** intramuscular EMG 的局部性没有显著降低 torque estimation，可作为 implanted control interface 的可行输入。
- **Digital Twin Assessment:** `L2` sensing/modeling validation；是长期 twin sensing 的候选，但本文没有植入式长期采集、装置闭环或 patient-state adaptation。
- **Limitations:** 小样本；reference torque 来自同一运动学/动力学链而非独立内部真值；短期线缆式 intramuscular acquisition 不能代表 chronic implant reliability。
- **Reproducibility:** 中等；设计与模型清楚，患者级原始数据和完整控制代码未形成公开复现包。
- **PhD Relevance:** **Strong wearable/implant bridge**。适合研究最小传感集、长期漂移和在线校准；不要把 sensor equivalence 直接表述为 twin validation。

## NEU006 — De Groote & Falisse (2021)

**Citation:** [Perspective on musculoskeletal modelling and predictive simulations of human movement to assess the neuromechanics of gait](https://doi.org/10.1098/rspb.2020.2432), *Proceedings of the Royal Society B*.

- **Type / Evidence:** review/predictive-modeling framework；`full_text_checked`。
- **One-Sentence Contribution:** 系统梳理从 tracking simulations 到 optimal-control predictive simulations 的假设、验证与临床用途，明确“生成合理运动”不等于预测某个患者会怎样改变。
- **Problem:** gait simulations 常被用于解释病理与设计治疗，但 neural objectives、muscle models 和 validation 的不确定性会支配结论。
- **Method:** perspective review，比较 inverse、forward、tracking 与 prediction；讨论 model personalization、motor-control cost 和实验验证。
- **Data:** 二手研究和示例，无新队列。
- **Evaluation:** 评价框架强调 kinematic/kinetic realism、muscle activity、代谢与对未见条件的预测，不提供统一 benchmark。
- **Findings:** predictive simulation 能问反事实问题，但控制目标和个体参数的选择必须被实验约束，尤其在病理步态中。
- **Digital Twin Assessment:** 本文不是 twin；它规定 `L3` predictive twin 必须通过的反事实和外部验证门槛。
- **Limitations:** 观点性综述未系统量化各方法偏倚；对在线同化、传感丢失、实时预算和监管落地讨论有限。
- **Reproducibility:** 作为综述可追溯；无统一代码或数据产物。
- **PhD Relevance:** **Strong methodological foundation**。可直接转化为博士验证计划：校准任务与预测任务分离，并报告 cost-function/parameter uncertainty。

## NEU007 — Song et al. (2021)

**Citation:** [Deep reinforcement learning for modeling human locomotion control in neuromechanical simulation](https://doi.org/10.1186/s12984-021-00919-y), *JNER*.

- **Type / Evidence:** validation-of-methods/review；`full_text_checked`。
- **One-Sentence Contribution:** 通过 NeurIPS 2019 Learn to Move challenge 的大规模算法经验，展示 DRL 能控制复杂肌骨模型，也暴露 reward engineering 与生物真实性之间的鸿沟。
- **Problem:** 高维、冗余、接触丰富的 neuromusculoskeletal locomotion 难以由传统优化稳定求解。
- **Method:** 对竞赛环境、获胜策略、reward shaping、state/action representations 与训练技巧进行回顾和分析。
- **Data:** 竞赛模拟轨迹与约 1,300 支团队的开发经验，不是真实患者数据。
- **Evaluation:** task reward、速度/方向跟踪和仿真稳定性；没有 subject-specific physiology 或 clinical endpoint。
- **Findings:** ensemble、curriculum 和丰富状态反馈可得到稳健 locomotion，但成功高度依赖 simulator/reward 设定。
- **Digital Twin Assessment:** `L0` simulation-only。它是控制算法 substrate，不是 digital twin，也未验证策略能转移到某个人。
- **Limitations:** benchmark reward 可能鼓励非生理动作；sim-to-real、个体损伤、传感噪声和安全约束没有被充分检验。
- **Reproducibility:** 中高；挑战环境和方法公开程度较好，但完整 winning pipelines/compute 并非全部统一提供。
- **PhD Relevance:** **Useful control baseline**。适合开发 control prior；必须叠加 patient binding、partial observability 和真实闭环评价才进入 twin 主线。

## NEU008 — Codol et al. (2024)

**Citation:** [MotorNet, a Python toolbox for controlling differentiable biomechanical effectors with artificial neural networks](https://doi.org/10.7554/eLife.88591), *eLife*.

- **Type / Evidence:** modeling/software infrastructure；`full_text_checked`。
- **One-Sentence Contribution:** 提供可微 biomechanical effectors 与神经网络控制器的开放工具箱，使运动控制假设可在统一、可训练环境中快速检验。
- **Problem:** neuroscience 的神经控制模型与 biomechanical simulators 之间缺少易用、可微、可复现的接口。
- **Method:** Python/TensorFlow 组件化肌肉、骨架、environment 与 controller，并用 reaching 等任务示范训练。
- **Data:** 合成训练轨迹和示例模型，无 patient-specific 数据。
- **Evaluation:** 数值稳定性、训练可行性、任务表现与示例行为；不是人体预测验证。
- **Findings:** differentiable dynamics 降低构建 embodied motor-control experiments 的成本，并支持可控扰动分析。
- **Digital Twin Assessment:** `L0` generic simulator。可作 twin 的 learning/control sandbox，但没有个体绑定、状态同步、临床预测或 intervention loop。
- **Limitations:** 简化的肌肉/骨架与任务可能无法保持临床相关生理约束；可微近似的准确性不代表跨个体有效性。
- **Reproducibility:** 高；代码、文档、示例和版本化仓库公开。
- **PhD Relevance:** **Strong reproducible sandbox**。适合原型化 differentiable state estimator/control policy；最终验证必须回到 OpenSim/CEINMS 等高保真模型与真实数据。

## NEU009 — Chiappa et al. (2024)

**Citation:** [Acquiring musculoskeletal skills with curriculum-based reinforcement learning](https://doi.org/10.1016/j.neuron.2024.09.002), *Neuron*.

- **Type / Evidence:** modeling/control；`full_text_checked`。
- **One-Sentence Contribution:** 以 static-to-dynamic curriculum 训练 39-muscle hand 完成 Baoding-ball manipulation，并用干预分析区分表面低维 synergy 与真实控制维度。
- **Problem:** 接触丰富的肌骨手控制难训练，且传统 synergy 分析可能把观察到的低维运动误作低维神经控制。
- **Method:** recurrent policy、curriculum RL 与 MyoSuite hand；对 latent/control components 做选择性失活，并与人类 kinematic patterns 比较。
- **Data:** 仿真训练数据与人类行为对照，不是同一人的持续数字副本。
- **Evaluation:** task success、ball rotation、kinematic/kinetic dimensionality、ablation 和泛化测试。
- **Findings:** curriculum 可学得复杂技能；观测空间低维并不意味着所有高维控制分量都不重要，synergies 高度 task-specific。
- **Digital Twin Assessment:** `L0` modeling/control paper。它研究 generic embodied motor control，不做 subject-specific calibration 或实时同步。
- **Limitations:** 仿真肌肉、接触和 reward 决定策略；与人类相似性主要是统计形态，不是 neural ground truth；跨任务泛化有限。
- **Reproducibility:** 中高；环境公开且方法描述充分，精确复现需要较大计算和训练细节/权重。
- **PhD Relevance:** **Strong conceptual caution**。适合质疑固定低维 synergy prior；可将 learned control prior 与患者特异状态估计分开建模。

## NEU010 — Chiappa et al. (2023)

**Citation:** [Latent exploration for Reinforcement Learning](https://proceedings.neurips.cc/paper_files/paper/2023/hash/b0ca717599b7ba84d5e4f4c8b1ef6657-Abstract-Conference.html), *NeurIPS*.

- **Type / Evidence:** control/algorithm paper；`full_text_checked`。
- **One-Sentence Contribution:** 在学习到的低维 latent action space 中探索，提高高维肌骨控制的样本效率，但主要贡献是 RL optimization 而非人体模型个体化。
- **Problem:** 对大量 muscle actuators 逐维加噪导致 exploration 无效，难以发现协调动作。
- **Method:** 学习 action representation，并在 latent space 施加结构化 exploration；与标准 RL baselines 在多种连续控制任务比较。
- **Data:** 模拟 benchmark 轨迹，无人类/患者数据。
- **Evaluation:** return、learning speed、stability 与 ablation；生理真实性不是主要 endpoint。
- **Findings:** latent exploration 在 overactuated tasks 中更有效，支持“结构化动作空间”作为控制先验。
- **Digital Twin Assessment:** `L0` simulation-only control。没有 subject-specific NMS model、在线 person-to-model update 或临床 intervention validation。
- **Limitations:** latent structure 可能编码 simulator/reward 偏差；较高回报不代表肌肉募集、组织负荷或患者适配正确。
- **Reproducibility:** 中高；论文与补充材料公开，代码/seed/compute 依仓库版本核验。
- **PhD Relevance:** **Useful algorithmic prior**。可用于 twin 内部 policy search，但应受 physiological constraints 与 uncertainty bounds 约束。

## NEU011 — He et al. (2024)

**Citation:** [DynSyn: Dynamical Synergistic Representation for Efficient Learning and Control in Overactuated Embodied Systems](https://proceedings.mlr.press/v235/he24o.html), *ICML*.

- **Type / Evidence:** control/modeling；`full_text_checked`。
- **One-Sentence Contribution:** 用状态依赖的动态 synergy 代替固定线性肌肉协同，在高维 embodied systems 中压缩动作空间并保留任务适应性。
- **Problem:** 固定 synergy 或直接高维控制难兼顾效率、表达力和跨状态协调。
- **Method:** learned dynamical synergy module 与 RL 联合训练，在 overactuated musculoskeletal/robotic tasks 上比较 fixed-synergy 和 direct-control baselines。
- **Data:** 多个仿真环境和合成 rollout，无 subject-specific human data。
- **Evaluation:** reward、sample efficiency、robustness、representation/ablation；不评价人体肌力或临床结果。
- **Findings:** 动态 synergy 可提高训练与控制效率，并比静态降维更能适应状态变化。
- **Digital Twin Assessment:** `L0` Embodied AI/control；不是 digital twin。“self representation”或生物启发不构成真实人的同步副本。
- **Limitations:** synergy 的生理对应没有直接 neural/EMG 验证；性能受任务 reward 与 simulator fidelity 限制。
- **Reproducibility:** 中高；PMLR 全文与方法开放，具体环境版本和训练成本仍影响复现。
- **PhD Relevance:** **Potential control module**。可研究 patient-specific synergy adaptation，但需用真实 longitudinal EMG/functional outcomes 约束，而不是只看仿真回报。

## NEU012 — Codol, Pruszynski & Gribble (2026)

**Citation:** [Embodied Sensorimotor Control: Computational Modeling of the Neural Control of Movement](https://doi.org/10.1146/annurev-bioeng-102723-020454), *Annual Review of Biomedical Engineering*.

- **Type / Evidence:** review/framework；`full_text_checked`。
- **One-Sentence Contribution:** 将神经控制模型置于身体力学、感觉反馈和环境动力学的闭环中，为判断 AI controller 是否具有生物解释力提供框架。
- **Problem:** 只建模 brain 或只建模 body 都会错过 sensorimotor behavior 的闭环因果结构。
- **Method:** 综述 optimal feedback control、neural networks、differentiable biomechanics、RL 与 embodied modeling。
- **Data:** 二手文献，无新实验。
- **Evaluation:** 按解释层级、行为预测和扰动响应比较建模范式，非系统性 meta-analysis。
- **Findings:** 身体与环境是控制系统的一部分；可解释模型应在 perturbation 与 generalization 中接受检验。
- **Digital Twin Assessment:** 不是 twin 实现；为 `L3–L4` 模型定义正确的 closed-loop scientific questions，但不提供 person-specific synchronization。
- **Limitations:** 神经科学视角强于临床实施；对 patient-specific anatomy、组织载荷、不确定性与监管讨论较少。
- **Reproducibility:** 综述可追溯，无统一 artifact。
- **PhD Relevance:** **Strong conceptual foundation**。可帮助把 digital twin 从“人体数据 dashboard”提升为可受扰动检验的 embodied causal model。

## EMB001 — Wang et al. (2022)

**Citation:** [MyoSim: Fast and physiologically realistic MuJoCo models for musculoskeletal and exoskeletal studies](https://doi.org/10.1109/ICRA46639.2022.9811684), *ICRA*.

- **Type / Evidence:** modeling/software infrastructure；`full_text_checked`（开放作者稿/代码说明）。
- **One-Sentence Contribution:** 将肌骨和外骨骼系统高效实现于 MuJoCo，在保留主要生理 actuator 特性的同时把大规模控制训练变得可行。
- **Problem:** 高保真 NMS simulation 计算昂贵，难支持 RL、控制器搜索和 human–exoskeleton co-simulation。
- **Method:** MuJoCo 肌肉执行器、肌骨模型与 exoskeleton coupling；以速度、动力学和控制任务同既有实现比较。
- **Data:** 模型/仿真 benchmarks，无新患者数据。
- **Evaluation:** simulation throughput、numerical/physiological behavior 与示例控制；不含 subject-specific external validation。
- **Findings:** 运行速度显著提升，使 fatigue、sarcopenia 和 exoskeleton 场景的批量仿真成为可能。
- **Digital Twin Assessment:** `L0` generic simulator/twin substrate。可容纳个体参数，但本文没有 person binding、在线 update 或 device trial。
- **Limitations:** 更快的 simplified physiology 可能牺牲组织尺度与个体参数真实性；示例疾病参数是设定而非患者辨识。
- **Reproducibility:** 高；开放模型/代码与示例，但版本和数值差异需锁定。
- **PhD Relevance:** **Strong rapid-prototyping tool**。适合策略预训练和敏感性分析；临床结论必须在个体高保真模型/真实 HIL 中复核。

## EMB002 — Caggiano et al. (2022)

**Citation:** [MyoSuite: A Contact-rich Simulation Suite for Musculoskeletal Motor Control](https://proceedings.mlr.press/v168/caggiano22a.html), *L4DC*.

- **Type / Evidence:** modeling/benchmark；`full_text_checked`。
- **One-Sentence Contribution:** 提供一组 contact-rich muscle-actuated hand/arm/leg tasks 和 physiology perturbations，使 Embodied AI 可系统研究高维肌肉控制。
- **Problem:** 机器人 benchmarks 多由 torque motors 驱动，不能代表延迟、冗余和状态依赖的肌肉控制。
- **Method:** MuJoCo musculoskeletal environments、标准任务/API、baseline RL 与 weakness/fatigue/tendon-transfer 等参数扰动。
- **Data:** 合成环境与策略 rollouts，无真实个体持续数据。
- **Evaluation:** baseline task performance、计算效率和 perturbation response。
- **Findings:** 肌肉驱动显著增加控制难度；平台允许比较健康、损伤和辅助场景的算法行为。
- **Digital Twin Assessment:** `L0` modeling/benchmark。参数化 pathology 不是 patient-specific twin，除非参数从个体数据辨识并持续更新。
- **Limitations:** pathology 是简化 knob；benchmark success 与人体生理/临床转移未被证明；contact/muscle model bias 可被 policy 利用。
- **Reproducibility:** 高；环境、任务和基线代码开放。
- **PhD Relevance:** **Strong Embodied AI baseline**。适合训练通用 control prior 和设计消融；不要把 benchmark transfer 当作 patient validation。

## EMB003 — Caggiano et al. (2023)

**Citation:** [MyoDex: A Generalizable Prior for Dexterous Manipulation](https://proceedings.mlr.press/v202/caggiano23a.html), *ICML*.

- **Type / Evidence:** control/Embodied AI；`full_text_checked`。
- **One-Sentence Contribution:** 从多任务肌骨手策略学得 reusable motor prior，减少新 manipulation task 的探索负担并提升泛化。
- **Problem:** 单任务 muscle-actuated hand policies 难训练且难迁移到新物体/动作。
- **Method:** 多任务 demonstration/teacher learning 形成 generalizable prior，再对下游任务 finetune，并与 distillation/从头训练比较。
- **Data:** MyoSuite 模拟轨迹，无真实手部或患者数据。
- **Evaluation:** task success、学习速度、任务覆盖和 ablation；主要报告约三倍任务覆盖与更快学习。
- **Findings:** 多样动作经验可形成可迁移的肌骨控制先验，但 transfer 仍发生在同一 simulator family。
- **Digital Twin Assessment:** `L0` control paper。它提升 generic policy，不估计真实人的 NMS 状态或预测患者干预。
- **Limitations:** sim-only；task set、demonstrations 和 simulator bias 决定 prior；没有 biomechanical internal-load validation。
- **Reproducibility:** 高；PMLR 论文与项目代码/环境可用，训练成本较高。
- **PhD Relevance:** **Useful prior-learning route**。可用于 cohort-level prior，再由少量 patient data 个体化；关键研究问题是何时/如何安全偏离 generic prior。

## EMB004 — Zuo et al. (2024)

**Citation:** [Self Model for Embodied Intelligence: Modeling Full-Body Human Musculoskeletal System and Locomotion Control with Hierarchical Low-Dimensional Representation](https://doi.org/10.1109/ICRA57147.2024.10610081), *ICRA*.

- **Type / Evidence:** modeling + control；`full_text_checked`（论文/项目材料）。
- **One-Sentence Contribution:** 构建约 90 segments、206 joints、700 musculotendon units 的 full-body MS-Human-700，并用分层低维表示实现 locomotion control。
- **Problem:** 全身肌骨模型的自由度与执行器规模使直接学习控制几乎不可行，既有 benchmarks 多局限于局部身体。
- **Method:** 高维全身模型、hierarchical low-dimensional representation 与 RL locomotion controller；用运动数据和仿真行为核验。
- **Data:** 公开人体运动轨迹和生成的 simulation rollouts，不是单个 subject 的解剖/神经纵向数据。
- **Evaluation:** locomotion task performance、运动相似性、训练效率与 representation ablation。
- **Findings:** 分层控制可驯服极高维全身肌肉系统，并为 embodiment-aware learning 提供规模化平台。
- **Digital Twin Assessment:** `L0` generic self-model。名称中的“self model”指 agent representation，不是 human digital twin；无 patient binding 或临床反事实。
- **Limitations:** 700-MTU 复杂度不等于个体解剖真实性；验证偏运动外观/任务表现，内部肌力和组织负荷真值不足。
- **Reproducibility:** 高；项目代码/模型公开，重训练需要较大计算资源。
- **PhD Relevance:** **Strong whole-body control substrate**。可探索 learned reduction，但应与 patient-specific biomechanics 和可解释 load estimates 分层耦合。

## EMB005 — Wang et al. (2025)

**Citation:** [MyoChallenge 2024: A New Benchmark for Physiological Dexterity and Agility in Bionic Humans](https://papers.neurips.cc/paper_files/paper/2025/hash/5a8f69523f9511a5706568c552de0ebb-Abstract-Datasets_and_Benchmarks_Track.html), *NeurIPS Datasets and Benchmarks*.

- **Type / Evidence:** benchmark/validation-of-algorithms；`full_text_checked`。
- **One-Sentence Contribution:** 用 biological and bionic limbs 的复杂 dexterity/agility tasks 建立社区 benchmark，量化当前控制算法在 physiological actuation 下的能力边界。
- **Problem:** 肌骨与假肢控制缺少共同环境、任务和比较协议，算法结果难横向复核。
- **Method:** standardized MyoSuite tasks、competition infrastructure、baseline 与参赛方法分析；约 50 支团队、290 次 submissions。
- **Data:** 仿真 trajectories 和 submission logs，无真实患者 cohort。
- **Evaluation:** task-specific score、robustness 和排名；优胜方法显著超过 baseline，但指标仍由仿真 reward 定义。
- **Findings:** curriculum、representation learning 和强 priors 可大幅提升复杂肌骨控制，同时暴露不同任务间迁移不足。
- **Digital Twin Assessment:** `L0` benchmark。即便题目使用 “bionic humans”，也没有真实人—模型同步、个体化或 intervention outcome。
- **Limitations:** competition incentives 可能过拟合 benchmark；生理有效性、hardware transfer、患者安全和长期 adaptation 未纳入主要评分。
- **Reproducibility:** 高；环境、任务和 leaderboard 公开，部分参赛解法/权重开放度不一。
- **PhD Relevance:** **Strong benchmarking resource**。可用于算法筛选与公开基线；博士贡献应新增 patient-conditioned、uncertainty-aware、hardware/clinical validation track。
