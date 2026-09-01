# Core Paper Critiques 04 — Wearable Sensing, Rehabilitation, and Assistive Robotics

批判标准见 [`../CRITIQUE_PROTOCOL.md`](../CRITIQUE_PROTOCOL.md)。IMU 在本组只是 wearable sensing 的一种；DT 等级取决于个体模型、状态更新、预测与干预闭环，而非传感器类型。

## WEA001 — Al Borno et al. (2022)

**Citation:** [OpenSense: An open-source toolbox for inertial-measurement-unit-based measurement of lower extremity kinematics over long durations](https://doi.org/10.1186/s12984-022-01001-x), *JNER*.

- **Type / Evidence:** sensing + validation/software；`full_text_checked`。
- **One-Sentence Contribution:** 把 8 枚 IMU、OpenSim 标定和 inverse kinematics 组成开放管线，并量化 20 分钟步行中下肢角度误差与漂移。
- **Problem:** marker-based motion capture 难覆盖长时间/真实环境，商业 IMU 算法又不透明且难与肌骨模型衔接。
- **Method:** sensor-to-segment calibration、orientation estimation 和 OpenSim IK；与 optical motion capture 对照。
- **Data:** 11 名健康成人，每人两段约 10 分钟步行；8 IMUs、光学标记和同步运动数据。
- **Evaluation:** sagittal joint-angle RMS 约 3–6°、相关系数约 0.60–0.87，并评估近似线性 drift（约 −0.14 至 −0.17°/min）。
- **Findings:** 开放 IMU-to-model pipeline 可支持长时 kinematics，但 heading/drift 与非矢状面精度仍限制机械负荷推断。
- **Digital Twin Assessment:** `L2` sensing/digital-shadow enabler。它更新运动学状态，但没有 neural/muscle/tissue state、个体预测或干预闭环；不是以 IMU 为中心的 twin。
- **Limitations:** 健康小样本、实验室步行、短于日常长期监测；光学参考本身有误差；kinematic agreement 不能证明内部 load accuracy。
- **Reproducibility:** 高；OpenSense、示例、数据和代码开放。
- **PhD Relevance:** **Strong sensing baseline**。适合作为低成本 observability layer；课题价值在于多模态校正与状态/不确定性同化，而不是再做一篇纯 IMU angle paper。

## WEA002 — Uhlrich et al. (2023)

**Citation:** [OpenCap: Human movement dynamics from smartphone videos](https://doi.org/10.1371/journal.pcbi.1011462), *PLOS Computational Biology*.

- **Type / Evidence:** sensing + modeling validation/software；`full_text_checked`。
- **One-Sentence Contribution:** 将双智能手机视频、无标记姿态估计和云端 OpenSim 串联，低成本输出运动学与动力学并与实验室测量核验。
- **Problem:** 临床和现场难以获得传统 mocap/force-plate 级别的运动动力学信息。
- **Method:** 多视角视频、深度学习 keypoints、三角化、scaled OpenSim IK 与学习/物理结合的动力学估计。
- **Data:** 多任务健康受试者实验与公共示例；视频同光学 mocap、force plates 对照。
- **Evaluation:** joint kinematics、joint moments 和 task metrics 的误差/相关性，并示范 field/clinical-like use。
- **Findings:** consumer video 可扩展人体动力学采集，但精度受视角、遮挡、动作分布和动力学模型假设影响。
- **Digital Twin Assessment:** `L2` sensing/model-update infrastructure；能生成 episodic digital shadow，不具备 subject-specific tissue/neural state、longitudinal adaptation 或 intervention prediction。
- **Limitations:** 训练分布外动作和病理体态可能退化；无直接内部负荷真值；云处理/视频带来隐私和网络依赖。
- **Reproducibility:** 高；平台、文档和部分代码/数据开放，但完整服务端依赖需考虑长期可用性。
- **PhD Relevance:** **Strong scalable acquisition route**。可用于 cohort/remote follow-up；需与 EMG、wearable force/pressure 或成像融合，避免只从视频反演不可辨识的内部状态。

## WEA004 — Yang et al. (2025)

**Citation:** [Virtual reality interactions via a user-generic ultrasound human-machine interface for wrist and hand tracking](https://www.nature.com/articles/s41467-025-66001-6), *Nature Communications*.

- **Type / Evidence:** sensing + interface validation；`full_text_checked`。
- **One-Sentence Contribution:** 用 forearm ultrasound 和 user-generic learning 解码 wrist/hand motion，减少逐用户标定并在 VR interaction 中验证连续控制。
- **Problem:** EMG 对电极位置和皮肤状态敏感，而 ultrasound 能观测深层肌肉形变，却通常需要用户特异训练和笨重处理。
- **Method:** wearable ultrasound acquisition、spatiotemporal learning 与跨用户/少标定 prediction，驱动 VR wrist/hand tasks。
- **Data:** 多用户实验和 VR 交互数据；包含跨用户训练/测试，但不是临床患者纵向队列。
- **Evaluation:** tracking error、cross-user/generalization、task completion 和对标定负担的比较。
- **Findings:** 肌肉形态变化包含可泛化运动意图信息，ultrasound 可补充表面 EMG/IMU 的可观测性。
- **Digital Twin Assessment:** `L2` sensing/interface paper；它估计动作，不维护 subject-specific NMS mechanics、预测 tissue load 或闭环更新治疗。
- **Limitations:** user-generic accuracy 可能掩盖特定病理/解剖差异；VR success 不是真实 assistive/rehabilitation outcome；探头位置和长期固定仍是挑战。
- **Reproducibility:** 中等；方法和实验充分，硬件、训练数据与完整部署代码的开放度需逐项核验。
- **PhD Relevance:** **Strong multimodal sensing candidate**。适合与 EMG/kinematics 联合估计 muscle state，但博士主线应验证它是否改善模型可辨识性和干预决策。

## ROB001 — Durandau et al. (2019)

**Citation:** [Voluntary control of wearable robotic exoskeletons by patients with paresis via neuromechanical modeling](https://doi.org/10.1186/s12984-019-0559-z), *JNER*.

- **Type / Evidence:** modeling + personalization + closed-loop validation；`full_text_checked`。
- **One-Sentence Contribution:** 在 4 名健康者与 3 名 paresis 患者中把 residual EMG 经 subject-specific neuromechanical model 实时转为多关节 exoskeleton torque，实现患者主动驱动机器人。
- **Problem:** 弱残余 EMG 很难直接稳定映射为多关节 assistance，预设轨迹又削弱用户主动控制。
- **Method:** 在线 EMG-driven NMS estimation、个体 calibration 与 proportional exoskeleton actuation；在 ankle/hand/wrist 等装置任务中闭环测试。
- **Data:** 7 人：4 healthy、1 SCI、2 stroke；实验室单/多关节动作和机器人交互。
- **Evaluation:** joint torque/angle tracking、实时性、不同用户/任务控制可行性与患者操作表现。
- **Findings:** 即使 paresis 患者肌力弱，生理模型仍可放大残余 neural drive 成为连续 voluntary control signal。
- **Digital Twin Assessment:** 接近 `L4` 的早期 closed-loop NMS twin prototype：P3–P4、实时 state estimation 和 intervention coupling 齐备；但没有纵向 adaptation、out-of-calibration prediction、uncertainty 或临床疗效验证。
- **Limitations:** 病例仅 3 且诊断/装置异质；短时 lab proof-of-concept；模型输出与 controller 紧密耦合，缺少独立内部-state ground truth。
- **Reproducibility:** 中等；架构与开放模型基础清楚，患者数据、硬件和完整实时 stack 难以独立复现。
- **PhD Relevance:** **Nearest implemented architecture**。是 neural control→patient model→robot 闭环的核心先例；可从 longitudinal self-calibration、安全约束和临床 endpoint 超越。

## ROB002 — Sartori et al. (2018)

**Citation:** [Robust simultaneous myoelectric control of multiple degrees of freedom in wrist-hand prostheses by real-time neuromusculoskeletal modeling](https://doi.org/10.1088/1741-2552/aae26b), *Journal of Neural Engineering*.

- **Type / Evidence:** modeling + personalization + device validation；`methods_results_checked`。
- **One-Sentence Contribution:** 将实时 NMS model 用作 wrist–hand prosthesis 的连续多自由度 decoder，利用物理约束提升未训练组合动作中的鲁棒性。
- **Problem:** pattern recognition 常输出离散动作，且同时/比例多自由度控制在姿势与组合变化下不稳定。
- **Method:** 多通道 EMG、subject-specific muscle–tendon/joint mapping 与 real-time forward estimation，驱动 wrist–hand prosthesis commands。
- **Data:** 健康和/或肢体缺失参与者的实验室 EMG/运动任务；本轮可核验材料不足以可靠报告精确样本分层。
- **Evaluation:** 多自由度 simultaneous/proportional control、未训练任务、实时误差和与常规 myoelectric mapping 的比较。
- **Findings:** NMS constraints 可把肌肉信号转成协调的连续 joint commands，并改善组合动作泛化。
- **Digital Twin Assessment:** `L3–L4` prototype：有 subject-specific real-time model 与 device coupling；但主要预测控制命令，不是完整身体状态或治疗反事实，也缺 longitudinal update。
- **Limitations:** evidence 对长期日常使用、疲劳、电极重放和患者功能获益不足；模型 calibration 可能在同一任务分布内受益。
- **Reproducibility:** 中低；实时方法描述可重建，但专用 prosthesis、数据和完整软件未作为一键复现包开放。
- **PhD Relevance:** **Nearest control precedent**。适合作为 physics-constrained neural interface 基线；应增加跨日 adaptation 和 independent functional validation。

## ROB003 — Lotti et al. (2020)

**Citation:** [Adaptive Model-Based Myoelectric Control for a Soft Wearable Arm Exosuit: A New Generation of Wearable Robot Control](https://doi.org/10.1109/MRA.2019.2955669), *IEEE Robotics & Automation Magazine*.

- **Type / Evidence:** modeling + adaptive control/device demonstration；`methods_results_checked`。
- **One-Sentence Contribution:** 把 adaptive EMG-driven biomechanical model 嵌入 soft arm exosuit，使 assistance 随用户 voluntary effort 和姿势变化，而非跟随固定轨迹。
- **Problem:** soft exosuits 需要连续估计用户意图与生物关节力矩，静态 EMG mapping 容易受姿态、疲劳和装配变化影响。
- **Method:** 实时 EMG processing、subject-specific musculoskeletal mapping、在线/快速参数适配和 assist-as-needed actuation。
- **Data:** 健康参与者的上肢实验室装置试验；精确样本/任务细节在本轮可访问证据中不完整。
- **Evaluation:** torque/kinematic tracking、adaptation、不同动作和 exosuit assistance demonstration。
- **Findings:** model-based adaptation 可支持更自然的多姿态 voluntary control，并展示 wearable soft actuation 的整合可行性。
- **Digital Twin Assessment:** `L4-like` engineering prototype；具 person model、online adaptation 与 actuator loop，但对 patient-specific physiological state、outcome prediction 和长期共适应验证不足。
- **Limitations:** magazine-format 证据深度与小规模健康试验限制结论；controller performance 不能推出康复疗效；独立 ground truth 不充分。
- **Reproducibility:** 低到中；硬件、实时控制栈和原始数据未形成完整公开包。
- **PhD Relevance:** **Strong systems precedent**。提示 twin 应在线适应传感/个体变化；博士工作需把 adaptation 与安全性、参数可解释性和患者研究结合。

## ROB004 — Pizzolato et al. (2019)

**Citation:** [Neuromusculoskeletal Modeling-Based Prostheses for Recovery After Spinal Cord Injury](https://doi.org/10.3389/fnbot.2019.00097), *Frontiers in Neurorobotics*.

- **Type / Evidence:** framework/perspective on modeling + intervention；`full_text_checked`。
- **One-Sentence Contribution:** 提出 NMS-model-based prosthesis 可同时读取 residual neural drive、估计内部负荷并提供恢复导向 assistance，但主要是路线图而非已完成临床系统。
- **Problem:** SCI 辅具多侧重运动替代，未利用个体神经肌骨状态来促进安全、主动和可塑性的恢复。
- **Method:** 综述现有 EMG-driven modeling、robotics 与 rehabilitation evidence，提出 sensing–model–prosthesis closed-loop 架构。
- **Data:** 二手文献与概念案例，无新患者实验。
- **Evaluation:** 架构和可行性论证，无独立 prospective trial。
- **Findings:** NMS model 可作为 human–robot shared-control layer，并可能用 tissue load 与 voluntary effort 调节 assistance。
- **Digital Twin Assessment:** 目标接近 `L4–L5`，本文自身为 framework，不应与 ROB001 式实证闭环混淆。
- **Limitations:** 未解决长期参数漂移、plasticity timescale、sensory feedback、uncertainty/safety certification 和临床 trial design。
- **Reproducibility:** 概念可复核，无完整系统 artifact。
- **PhD Relevance:** **Strong research agenda**。可把文中未实现模块转为课题假设；优先做 longitudinal co-adaptation 和可验证决策，而非再提同类概念框架。

## ROB005 — Zhang et al. (2017)

**Citation:** [Human-in-the-loop optimization of exoskeleton assistance during walking](https://doi.org/10.1126/science.aal5054), *Science*.

- **Type / Evidence:** personalization + closed-loop validation；`full_text_checked`。
- **One-Sentence Contribution:** 用实时 metabolic-rate estimate 在人机闭环中自动搜索 ankle-exoskeleton torque profile，证明个体辅助可在一次实验内被生理目标优化。
- **Problem:** 最优 assistance 随人变化，人工参数扫描慢且无法处理高维 timing/magnitude design。
- **Method:** breath-by-breath metabolic estimation、Bayesian/evolutionary HIL optimization 与 programmable ankle exoskeleton。
- **Data:** 健康成人 treadmill walking 的多条件、迭代试验。
- **Evaluation:** 相对 zero-torque/control 的 metabolic cost 与 convergence；optimized assistance 平均降低代谢成本约 24.2%（±7.4%）。
- **Findings:** 可从实时人类生理 response 个体化 device controller，而无需完整 NMS internal-state model。
- **Digital Twin Assessment:** `L4` closed-loop personalization，但不是 NMS digital twin：更新的是黑箱 objective/controller，不表示 neural–muscle–skeletal state，也不做 mechanistic counterfactual。
- **Limitations:** healthy treadmill setting；代谢测量延迟且 noisy；优化可过拟合单次条件，未验证跨日、病理或组织安全。
- **Reproducibility:** 中高；算法与部分数据/代码公开，完整硬件复现成本高。
- **PhD Relevance:** **Strong intervention benchmark**。它定义了闭环个体化的实证标准；博士方向可将黑箱 HIL 与 mechanistic NMS twin 和 safety constraints 结合。

## ROB006 — Slade et al. (2022)

**Citation:** [Personalizing exoskeleton assistance while walking in the real world](https://doi.org/10.1038/s41586-022-05191-1), *Nature*.

- **Type / Evidence:** personalization + real-world validation；`full_text_checked`。
- **One-Sentence Contribution:** 用 portable exoskeleton 和 online optimization 在约一小时内个体化户外/真实世界辅助，并显示速度和能耗改善可超越实验室固定 profile。
- **Problem:** treadmill-optimized assistance 未必迁移到坡度、速度和真实环境，传统 metabolic HIL 又依赖实验室设备。
- **Method:** wearable sensing、portable hip/ankle assistance、real-world cost estimation 与 online parameter optimization。
- **Data:** 小规模健康成人多环境行走；包含 treadmill 与 outdoors/real-world conditions。
- **Evaluation:** 一小时内 personalization；真实世界 self-selected speed 提高约 9±4%、cost of transport 降低约 17±5%，treadmill metabolic cost 约降 23±8%。
- **Findings:** 人机系统可在真实环境自适应个体，而不只在预定义 treadmill protocol 优化。
- **Digital Twin Assessment:** `L4` intervention/control personalization；接近 adaptive human–device loop，但缺 mechanistic NMS representation、patient model 和 longitudinal physiological state。
- **Limitations:** 健康小样本、短期优化；cost estimator 与控制器可能把环境/行为变化混为一体；未评价组织负荷、患者安全或长期学习。
- **Reproducibility:** 中等；论文/算法细节充分，商业/定制硬件和完整实时系统限制独立复现。
- **PhD Relevance:** **Strong real-world bar**。博士系统若声称 twin 应至少达到这种在线、现场、个体结果验证，同时补上 mechanism 与 uncertainty。

## ROB007 — Luo et al. (2023)

**Citation:** [Robust walking control of a lower limb rehabilitation exoskeleton coupled with a musculoskeletal model via deep reinforcement learning](https://doi.org/10.1186/s12984-023-01147-2), *JNER*.

- **Type / Evidence:** modeling + control/simulation validation；`full_text_checked`。
- **One-Sentence Contribution:** 在耦合 human musculoskeletal model–exoskeleton simulation 中训练 DRL controller，提高不同步态扰动下的行走鲁棒性。
- **Problem:** rehabilitation exoskeleton 与人体动力学强耦合，固定控制器难适应交互和扰动。
- **Method:** human–exoskeleton co-simulation、深度强化学习、reference tracking 与 disturbance/parameter tests。
- **Data:** 仿真 trajectories；没有患者硬件闭环数据。
- **Evaluation:** tracking、stability、robustness 和 baseline control comparison。
- **Findings:** 显式耦合肌骨模型可让 policy 学习 human-aware assistance，并提高 simulation robustness。
- **Digital Twin Assessment:** `L0` simulation-only modeling/control。尽管有人体模型与机器人闭环，未绑定某位患者、未由实时数据更新，也无实机验证。
- **Limitations:** sim-to-real gap、reward exploitation、简化 human response 与 contact uncertainty；rehabilitation 效果没有任何临床证据。
- **Reproducibility:** 中等；开放全文和算法描述，环境/代码完整开放程度需核验。
- **PhD Relevance:** **Useful virtual testbed**。适合先做 safe policy screening；必须用 patient-conditioned model、HIL/实机和 clinical endpoints 才能进入 twin 贡献。

## ROB008 — Ma, Xie & Zhang (2016)

**Citation:** [A patient-specific EMG-driven neuromuscular model for the potential use of human-inspired gait rehabilitation robots](https://doi.org/10.1016/j.compbiomed.2016.01.001), *Computers in Biology and Medicine*.

- **Type / Evidence:** personalization + modeling validation；`methods_results_checked`。
- **One-Sentence Contribution:** 在 6 名青少年、多速度步行中用少量 EMG 建立 patient-specific gait torque model，为 human-inspired robot control 提供个体参考。
- **Problem:** rehabilitation robots 的预设 normative trajectory 忽略患者残余肌肉驱动和个体动力学。
- **Method:** subject-specific lower-limb model、EMG-driven activation/muscle dynamics 与 inverse-dynamics calibration；使用有限表面 EMG 通道。
- **Data:** 6 名 adolescents，3 种步行速度，约 2 个主要 EMG channels 加运动学/动力学测量。
- **Evaluation:** predicted versus reference joint moments、跨速度表现和个体参数校准。
- **Findings:** sparse EMG + personalized mechanics 可估计 gait joint torque，支持 rehabilitation robot 中保留 voluntary contribution 的概念。
- **Digital Twin Assessment:** `L1` personalization/modeling paper；题目中的 “potential use” 很关键——没有机器人闭环、在线 update 或治疗效果验证。
- **Limitations:** n=6、非明确患者临床队列；稀疏 EMG 导致深层/拮抗肌不可辨识；reference torque 非直接肌力真值。
- **Reproducibility:** 低到中；方法可重建，但数据、代码和设备接口未开放为完整包。
- **PhD Relevance:** **Useful early baseline**。适合说明个体模型在机器人中的必要性；后续必须实际闭环并检验患者功能/安全。

## ROB009 — Cheng et al. (2018)

**Citation:** [On Muscle Activation for Improving Robotic Rehabilitation after Spinal Cord Injury](https://doi.org/10.1109/IROS.2018.8593973), *IROS*.

- **Type / Evidence:** sensing + rehabilitation validation；`methods_results_checked`。
- **One-Sentence Contribution:** 在 SCI 与健康参与者中比较 standing、spinal cord stimulation 和训练相关 EMG，论证肌肉激活应成为机器人康复的实时状态/目标，而不只看关节运动。
- **Problem:** 机器人能把肢体带到正确轨迹，却可能没有诱发所需 voluntary/neuromuscular engagement。
- **Method:** 多肌 EMG 分析，比较 SCI 参与者在 stimulation/训练条件下与健康 standing pattern 的变化。
- **Data:** 2 名 SCI 与 6 名健康参与者的下肢 EMG/standing conditions。
- **Evaluation:** muscle-activation pattern、相似性/变化及训练或 stimulation condition comparison；没有机器人 controller trial。
- **Findings:** 外观相似的姿势可对应不同肌肉募集，康复机器人评价应纳入 neural engagement。
- **Digital Twin Assessment:** `L1–L2` sensing/validation paper，不是 robot-control twin；它提供应被 twin 表示的 neural state，但没有 person-specific mechanics、预测或闭环 intervention。
- **Limitations:** SCI n=2、条件异质、表面 EMG 可比性有限；从 activation pattern 不能直接推出恢复或因果治疗效果。
- **Reproducibility:** 低到中；conference paper 方法可追溯，原始数据/代码未见完整公开。
- **PhD Relevance:** **Strong outcome-design warning**。博士系统不能只优化 kinematics；应把 voluntary neural engagement 与 tissue load 作为多目标状态和验证指标。

## ROB011 — Kang et al. (2025)

**Citation:** [Online Adaptation Framework Enables Personalization of Exoskeleton Assistance During Locomotion in Patients Affected by Stroke](https://doi.org/10.1109/TRO.2025.3595701), *IEEE Transactions on Robotics*.

- **Type / Evidence:** personalization + closed-loop validation；`full_text_checked`（开放作者稿）。
- **One-Sentence Contribution:** 用在线 human–exoskeleton model adaptation 在少于一分钟内估计用户 gait phase/torque 并个体化辅助，且在单例 stroke pilot 中展示功能性改善。
- **Problem:** stroke gait 与装置交互高度个体化且随状态变化，固定模型/控制参数需要耗时手动调节。
- **Method:** 在线参数/状态适配、gait-phase estimation、torque prediction 与 exoskeleton assistance；先健康验证，再 stroke pilot。
- **Data:** 健康实验加 1 名 stroke 参与者的 pilot locomotion 数据。
- **Evaluation:** adaptation time、phase estimation、torque error 和 assistance outcomes；报告 phase accuracy 提高约 40.9%（healthy）/65.9%（stroke）、torque error 降约 32.7%，pilot speed 增约 21.8%、metabolic cost 降约 6.5%。
- **Findings:** 快速在线 adaptation 能把 generic interaction model 调到个体，并改善闭环 controller 的估计与初步功能结果。
- **Digital Twin Assessment:** 当前最接近 `L4` 的系统之一：实时更新、person-specific interaction model、预测与 actuator loop 齐备；仍非 `L5`，因无 longitudinal plasticity/fatigue、uncertainty management 或多患者临床验证。
- **Limitations:** 临床结论来自单例 pilot；模型适配参数未必等于真实生理状态；短时指标不能证明恢复、长期安全或跨日稳定。
- **Reproducibility:** 中等；开放稿方法充分，专用 exoskeleton、患者数据和实时 stack 的完整开放度有限。
- **PhD Relevance:** **Nearest true-twin candidate**。非常适合作为博士系统对照：需要从快速 control adaptation 扩展到 mechanistic NMS state、uncertainty-aware prediction 和 longitudinal patient validation。
