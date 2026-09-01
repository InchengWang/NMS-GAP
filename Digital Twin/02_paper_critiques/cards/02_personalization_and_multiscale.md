# Core Paper Critiques 02 — Personalization, Multiscale Modeling, and Intervention Planning

## NMS007 — Akhundov et al. (2022)

**Citation:** [Is subject-specific musculoskeletal modelling worth the extra effort or is generic modelling worth the shortcut?](https://doi.org/10.1371/journal.pone.0262936), *PLOS ONE*.

- **Type / Evidence:** validation + personalization；`full_text_checked`。
- **One-Sentence Contribution:** 用 MRI-derived 几何与生理参数直接检验 generic scaling 的后果，证明个体化会改变肌纤维状态、肌力和侧间差异，而不只是改善表面运动拟合。
- **Problem:** 线性缩放忽略真实解剖差异，但高成本个体模型的增益缺少系统量化。
- **Method:** 为 9 名健康运动员建立 MRI-derived 与 generic-scaled 下肢模型，使用 CEINMS 比较 sprint 和 sidestep cut。
- **Data:** 9 人；每人 10 次 15 m sprint 与 10 次非预期切步；MRI、3D mocap、GRF、EMG。
- **Evaluation:** 1D statistical parametric mapping；比较 kinematics、kinetics、torque matching、activation、fiber length/velocity 和 force。
- **Findings:** generic 模型系统性误估 segment mass、inertia 和最大肌力；subject-specific 模型改善 torque matching 与生理合理性，并揭示 generic 模型漏掉的侧间差异。
- **Digital Twin Assessment:** `L1`, P2–P3；是强 personalization/validation paper，不是同步 twin。它验证“个体绑定为何必要”，未验证模型随人更新或预测干预结果。
- **Limitations:** 小样本、健康运动员、高成本 MRI；更好的生理合理性仍主要依赖间接指标，未直接测肌力。
- **Reproducibility:** 中高；汇总数据与代码仓库公开，但完整 MRI/个体模型受数据共享限制。
- **PhD Relevance:** **Strong validation foundation**。可作为你决定哪些参数值得个体化的依据；博士工作应量化低成本 wearable/learning personalization 与 MRI 标准之间的 trade-off。

## NMS008 — Ao et al. (2023)

**Citation:** [EMG-Driven Musculoskeletal Model Calibration With Wrapping Surface Personalization](https://doi.org/10.1109/TNSRE.2023.3323516), *TNSRE*.

- **Type / Evidence:** personalization paper；`full_text_checked`（PMC 作者稿）。
- **One-Sentence Contribution:** 把 muscle wrapping geometry 纳入 EMG-driven calibration，并用双层 polynomial surrogates 避免反复 OpenSim 分析。
- **Problem:** 肌腱路径和 moment arm 对肌力/关节负荷很敏感，却通常沿用 scaled generic wrapping surfaces。
- **Method:** 比较无几何校准、全 surrogate coefficient 校准、局部 surrogate 校准与真实 cylindrical wrapping-parameter personalization 四种方案。
- **Data:** 2 名 post-stroke 个体的步行 EMG、运动学和动力学。
- **Evaluation:** joint moment matching、计算可行性、hip contact force 与文献中体内范围的一致性。
- **Findings:** 三种几何调整均降低 moment error；物理 wrapping personalization 的误差降幅不是最大，却得到更可解释几何，并使 peak hip contact force 更接近文献范围。
- **Digital Twin Assessment:** `L1`, P2–P4；真实贡献是“可解释的几何个体化”，不是 twin 同步。没有直接 hip-contact-force ground truth 或闭环使用。
- **Limitations:** n=2；校准目标与评价共享关节力矩信息；以文献范围而非受试者内植入测量验证内部负荷。
- **Reproducibility:** 中高；全文方法和 surrogate 结构充分，数据/代码开放度需逐项确认。
- **PhD Relevance:** **Potential nearest personalization method**。提示 learned surrogate 应服务于物理参数辨识，并区分“拟合更好”与“结构更可信”。

## NMS009 — Savage et al. (2023)

**Citation:** [Neuromusculoskeletal model calibration accounts for differences in electromechanical delay and maximum isometric muscle force](https://doi.org/10.1016/j.jbiomech.2023.111503), *Journal of Biomechanics*.

- **Type / Evidence:** validation + personalization；`methods_results_checked`。
- **One-Sentence Contribution:** 通过 28 人敏感性实验说明 calibration 会吸收部分 EMD/Fmax 初始差异，但并不能让任意初值都等价。
- **Problem:** EMD 与最大等长肌力因人和任务而变，会影响 joint contact force，实践中却常用固定或通用值。
- **Method:** 为同一批数据建立不同 EMD（15–110 ms）及 generic/personalized Fmax 初始化的多个 EMG-informed 模型，再统一校准。
- **Data:** 28 名参与者，步态及髋/膝/踝 contact-force 预测。
- **Evaluation:** stance 前后半段 contact-force peaks、时序和 muscle-specific tension；repeated-measures ANOVA。
- **Findings:** EMD 35–70 ms 的校准模型产生相近 peak；personalized Fmax 初始化改善 muscle tension plausibility，但 knee/ankle force 仍不同。
- **Digital Twin Assessment:** `L1` validation paper。它审查个体参数可辨识性，不进行状态同步、反事实干预或在线更新。
- **Limitations:** contact force 多为模型输出而非参与者直接真值；“校准后相似”可能反映 compensating parameters，而非真实参数恢复。
- **Reproducibility:** 中；设计和统计清楚，完整数据/执行配置未形成开箱即用包。
- **PhD Relevance:** **Strong methodological warning**。博士计划必须报告 parameter identifiability 与 uncertainty，不能只以 joint-moment fit 证明模型参数正确。

## NMS010 — Berman et al. (2024)

**Citation:** [An Efficient Framework for Personalizing EMG-Driven Musculoskeletal Models Based on Reinforcement Learning](https://doi.org/10.1109/TNSRE.2024.3483150), *TNSRE*.

- **Type / Evidence:** personalization + neural-interface paper；`full_text_checked`（PMC 作者稿）。
- **One-Sentence Contribution:** 用预训练 RL policy 快速调节上肢 NMS 参数，减少每名新用户的优化时间，并在线控制虚拟手。
- **Problem:** 传统 simulated annealing personalization 太慢，不适合作为假肢接口的日常校准。
- **Method:** generic upper-limb model + ANN policy；RL 学习如何调整参数以减小 EMG-to-joint-motion error，并与 generic 和 simulated annealing 比较。
- **Data:** 10 名 non-disabled 用于 policy 预训练；另 6 名 non-disabled 与 1 名 transradial amputee 做未参与预训练的在线姿态匹配。
- **Evaluation:** personalization time、offline/online kinematic error 和 virtual posture-matching performance。
- **Findings:** individualized models 优于 generic；RL personalization 比逐人全局搜索更快，并可迁移到未见使用者，包括单名截肢者。
- **Digital Twin Assessment:** `L1–L2`, P3–P4；是快速个体绑定和实时 state mapping，不是 patient twin：缺少真实 prosthesis、长期 electrode shift、治疗预测和多尺度生理状态。
- **Limitations:** clinical evidence 几乎由单名 amputee 支撑；优化目标是 kinematics，参数未必生理解剖可辨识；policy 依赖预训练人群覆盖。
- **Reproducibility:** 中；作者稿与流程可得，实时硬件、数据和训练细节的完整可复运行性低于开源 benchmark。
- **PhD Relevance:** **Useful hybrid-physics personalization method**。与你的 learned personalization 很相关，但要加入 parameter plausibility、OOD 与患者 longitudinal test。

## NMS011 — Hammond et al. (2025)

**Citation:** [The Neuromusculoskeletal Modeling Pipeline: MATLAB-based model personalization and treatment optimization functionality for OpenSim](https://doi.org/10.1186/s12984-025-01629-5), *JNER*.

- **Type / Evidence:** modeling + personalization + treatment-planning；`full_text_checked`。
- **One-Sentence Contribution:** 将 joint、muscle–tendon、neural control、foot–ground personalization 与 direct-collocation treatment optimization 集成到公开软件中。
- **Problem:** OpenSim/Moco 能仿真但缺少统一的患者模型个体化和临床治疗设计工作流。
- **Method:** 7 个 MATLAB tools；从视频/mocap、GRF、EMG 建模，经 tracking/verification/design optimization 预测 intervention。
- **Data:** 端到端 use case 为 1 名 post-stroke 个体；使用其 self-selected walking 数据。
- **Evaluation:** 软件功能与内部 verification；示例预测改变 synergy recruitment 可使步速提高 60% 且不增加单位时间代谢成本。
- **Findings:** 证明端到端 personalized-model-to-counterfactual-treatment 可以在统一软件中运行；60% 是模型内预测，不是治疗后观察结果。
- **Digital Twin Assessment:** 接近 `L3` predictive twin substrate：P2–P5 和 counterfactual intervention 明确；缺少 prospective treatment execution、online sync 和 L4 clinical loop。
- **Limitations:** 单例 hypothetical treatment；结果受实验数据质量、局部极小、muscle activation/excitation 区分、MATLAB/OpenSim API 速度与无 fatigue model 限制。
- **Reproducibility:** 高；软件、模型、数据、设置、文档均公开（Apache 2.0），但 MATLAB 与 GPOPS-II 为商业依赖。
- **PhD Relevance:** **Potential nearest prior work**。这是 patient-specific predictive layer 的重要基线；你的可区分创新是 wearable online updating、uncertainty 和真实 intervention outcome。

## NMS012 — Rabbi et al. (2024)

**Citation:** [Muscle synergy-informed neuromusculoskeletal modelling to estimate knee contact forces in children with cerebral palsy](https://doi.org/10.1007/s10237-024-01825-7), *Biomechanics and Modeling in Mechanobiology*.

- **Type / Evidence:** modeling + sensing-burden reduction；`full_text_checked`。
- **One-Sentence Contribution:** 用 TD walking EMG database 的 synergies，从每腿仅 3–4 个 EMG 重建未测肌肉，以接近 13-channel EMG-assisted 模型的 knee-force 输出。
- **Problem:** 大量 EMG 传感器阻碍 NMS 模型进入儿童 CP 临床步态实验室。
- **Method:** synergy-informed excitation reconstruction，与 EMG-assisted 和 static optimization 三路线比较。
- **Data:** 3 名 CP、3 名 typically developing；TD 三人的数据还用于 synergy database。
- **Evaluation:** excitation/joint-moment RMSE、R²、KS test、AIC/BIC；knee contact force 以 full-EMG model 为参考。
- **Findings:** sparse-EMG synergy 估计的 total knee force 接近 full EMG（CP R² 约 0.95；TD 约 0.93），但 hip moment 明显较弱。
- **Digital Twin Assessment:** `L1` modeling/sensing paper；减少可观测负担有利于 L2，但没有在线同步或直接 contact-force ground truth。
- **Limitations:** n=6 且 database 与 TD evaluation 极小；以另一个模型而非植入测量作 force 真值；GMFCS 和病理异质性不足。
- **Reproducibility:** 中高；开放全文、方法和补充材料较完整，需确认个体原始 EMG/模型是否全部可下载。
- **PhD Relevance:** **Strong sensor-to-model bridge**。适合你的博士路线：问题不是“少放 IMU”，而是最小多模态 sensing 是否保持可行动的 NMS latent state。

## NMS013 — Esrafilian et al. (2022)

**Citation:** [Toward Tailored Rehabilitation by Implementation of a Novel Musculoskeletal Finite Element Analysis Pipeline](https://doi.org/10.1109/TNSRE.2022.3159685), *TNSRE*.

- **Type / Evidence:** personalization + multiscale modeling；`methods_results_checked`（开放作者稿）。
- **One-Sentence Contribution:** 把 EMG-assisted whole-body loads 连接到 poro(visco)elastic knee FE，比较不同康复动作的个体组织 stress/strain。
- **Problem:** 外部运动指标不能直接说明 cartilage/meniscus 是否处于有利机械环境。
- **Method:** 个体 EMG-assisted MSK + fibril-reinforced cartilage/meniscus FE 的快速 pipeline。
- **Data:** 15 名 knee osteoarthritis 患者，多种日常活动与康复练习。
- **Evaluation:** 比较跨活动、跨参与者的 cartilage/meniscus mechanics 及退变相关机械指标。
- **Findings:** 康复练习的 inter-subject tissue-load 差异大于日常活动，支持按组织负荷定制动作。
- **Digital Twin Assessment:** `L1–L3`：有患者多尺度模型和 alternative-activity counterfactual，但没有 prospective prescription/outcome、连续更新或闭环机器人控制。
- **Limitations:** 组织材料和边界条件难以个体测量；内部机械量缺少直接 in-vivo truth；“可用于定制”尚未等同于临床获益。
- **Reproducibility:** 中；方法和模型链清楚，完整自动化代码/患者影像共享受限。
- **PhD Relevance:** **Strong multiscale foundation**。揭示 NMS twin 的临床价值可能在 tissue endpoint，而不是仅提高关节角预测。

## NMS014 — Pizzolato et al. (2020)

**Citation:** [Targeted Achilles Tendon Training and Rehabilitation Using Personalized and Real-Time Multiscale Models...](https://doi.org/10.3389/fbioe.2020.00878), *Frontiers in Bioengineering and Biotechnology*.

- **Type / Evidence:** near-digital-twin prototype；`full_text_checked`。
- **One-Sentence Contribution:** 将个体 NMS 与 tendon FE surrogate 实时耦合，在 smartphone 显示局部 Achilles strain，是本图谱最接近 tissue-aware digital shadow 的原型之一。
- **Problem:** 康复以外部动作/负荷处方，无法实时知道局部 tendon 是否落在适应性 strain 范围。
- **Method:** 3D imaging、个体 muscle/tendon geometry、EMG-informed NMS、FE surrogate 与实时可视化；250 Hz 处理。
- **Data:** 单名健康受试者完成 walking、single-leg hopping、eccentric heel drop。
- **Evaluation:** 实时运行、surrogate 对 FE 的 RMSE（最佳约 0.0017 strain）及任务间局部 strain 分布。
- **Findings:** 局部 strain 在 tendon 内高度不均一；不同任务约覆盖 2–15% 范围，外部任务名称不足以确定内部剂量。
- **Digital Twin Assessment:** `L2` 且接近 `L4` 的原型；真实人连续更新个体多尺度模型并反馈，但尚未进行 human-in-the-loop 改变训练的实验，所以不能称已验证 closed-loop twin。
- **Limitations:** n=1、20-camera lab、offline initial calibration、FE surrogate 与 tendon strain 缺少体内验证；无纵向 remodeling outcome。
- **Reproducibility:** 中；全文与模型细节开放，原始数据仅 upon request，端到端实时栈未开箱发布。
- **PhD Relevance:** **Potential nearest prior work**。它最清楚展示你的长期方向：wearable observability → personalized NMS → tissue state → actionable feedback；空白在低负担 sensing、验证和 longitudinal adaptation。

## NMS015 — Hambly et al. (2025)

**Citation:** [Real-Time Continuous Calibration of an EMG-Informed Neuromusculoskeletal Model for Assistive Exoskeleton Control](https://doi.org/10.1109/ICORR66766.2025.11062981), *ICORR*.

- **Type / Evidence:** near-digital-twin/control paper；`abstract_and_methods_summary_checked`（全文访问受限）。
- **One-Sentence Contribution:** 用 autodifferentiable NMS + sliding-window optimization 在运动过程中连续校准，约 15 个 movement cycles（110 s）达到 offline calibration 水平。
- **Problem:** 预会话校准妨碍 NMS 模型用于自适应闭环神经康复。
- **Method:** 上肢 EMG-informed model、在线滑窗校准、ArmeoPower reaching control；另探索 synergy-driven missing-excitation reconstruction。
- **Data:** functional reaching 人体实验；可访问来源未给出足以可靠记录的样本规模和病理构成，因此不推断。
- **Evaluation:** uncalibrated、offline calibrated、continuous calibrated 的 moment accuracy 和 exoskeleton control performance。
- **Findings:** continuous calibration 在 110 s 内达到类似 offline 精度，并产生可用于控制的 plausible joint moments。
- **Digital Twin Assessment:** `L4`-like short-session prototype：在线 P6 更新和 action loop 同时存在；但未证明 fatigue 等生理变化真的被辨识，也没有 longitudinal/clinical outcome，因此不是 L5。
- **Limitations:** 全文证据受限；短时 reaching、可能健康队列、净力矩 surrogate、滑窗更新稳定性和 catastrophic drift 尚需严格验证。
- **Reproducibility:** 低至中；论文/摘要可核验，代码、数据与在线系统配置未在本轮发现完整开放包。
- **PhD Relevance:** **Closest technical prior work**。你的课题必须在其基础上加入多模态 state observability、uncertainty-aware safe update 和病人跨日验证。

## NMS017 — Diaz et al. (2026)

**Citation:** [Benchmarking Neural Network Personalized Musculoskeletal Hand Models...](https://doi.org/10.1109/TNSRE.2026.3711799), *TNSRE*.

- **Type / Evidence:** validation + personalization；`full_text_checked`（开放作者稿）。
- **One-Sentence Contribution:** 用 MRI 和 fine-wire EMG 作为较强实验参照，比较五类手部模型个体化，发现预测最好的 NN 参数未必最解剖真实。
- **Problem:** hand model personalization 方法繁多，但缺少对 anatomy 和 muscle-activation prediction 的同一基准测试。
- **Method:** scaling、NMSM joint-moment optimization、MRI segmentation、MRI+optimization 和只需 lateral-pinch force 的 NN personalization。
- **Data:** 30 名采集 biomechanics，15 名 MRI；最终 13 名用于 14 种 personalized models/person，7 个 ROM + 8 个 isometric tasks，含 surface/fine-wire EMG。
- **Evaluation:** held-out trials 的 predicted activation 对 EMG、参数对 MRI anatomy；共 8,190 次 OpenSim simulation。
- **Findings:** 无方法恢复完全准确 anatomy；NN 在 muscle-activation error 上最佳/相当，但参数值可能离 MRI 更远。
- **Digital Twin Assessment:** `L1` validation paper。它证明 output accuracy 与 parameter truth 可分离；无在线同步、患者干预或纵向更新。
- **Limitations:** 健康样本；neural control 未个体化；static optimization 和 EMG ground truth 仍有误差；高 participant variance。
- **Reproducibility:** 中高；作者稿、详细协议与 BHaM 数据资源较强，计算成本很高。
- **PhD Relevance:** **Strong validation benchmark**。博士论文必须同时报告 predictive validity 与 parameter/anatomical validity，避免“黑箱校准成 twin”。

## NMS018 — Wang et al. (2026)

**Citation:** [Personalized Robotic Lumbar Rehabilitation Based on Medical-Imaging-Assisted Musculoskeletal Biomechanical Modeling](https://doi.org/10.1109/TNSRE.2026.3663395), *TNSRE*.

- **Type / Evidence:** personalization + intervention/control；`full_text_checked`（CC BY 作者稿）。
- **One-Sentence Contribution:** 从 sparse MRI 推断个体 paraspinal geometry，生成 muscle-targeted robot trajectory/force，并在人体验证 EMG activation 是否达到目标。
- **Problem:** 固定 lumbar robot strategy 无法适应不同 muscle fat infiltration 和形态。
- **Method:** Bayesian sparse-slice shape fusion、fat infiltration/PCSA-derived biomechanical model、motion/interaction-force optimization 和 robot execution。
- **Data:** 4 名具有不同肌肉脂肪浸润水平的志愿者；并使用公共/临床影像数据验证分割重建。
- **Evaluation:** geometry reconstruction、target/non-target EMG、经验策略与 personalized strategy 比较。
- **Findings:** personalized strategy 将目标 activation 控制在约 50% MVC，MAE 3.79±1.02%；activation variance 相对经验策略下降 60.49%。
- **Digital Twin Assessment:** `L3–L4` prototype：P2–P5、counterfactual strategy 和机器人执行均存在；但模型不是连续同步，研究验证的是急性 EMG target 而非患者恢复。
- **Limitations:** n=4、志愿者而非临床患者；EMG activation 不是功能/疼痛结局；MRI 参数和模型简化的不确定性未贯穿策略安全边界。
- **Reproducibility:** 中；开放全文和算法细节，完整代码、影像、机器人控制栈开放程度有限。
- **PhD Relevance:** **Strong intervention exemplar**。说明“twin”的价值应由 individualized action + measured response 证明；可借鉴其 sensor-to-model-to-robot 闭环，但要增加临床和纵向验证。

## NMS019 — Paz et al. (2026)

**Citation:** [Personalized musculoskeletal models show that gait biofeedback alters knee cartilage contact mechanics in ACL-reconstructed subjects](https://doi.org/10.1016/j.jbiomech.2026.113376), *Journal of Biomechanics*.

- **Type / Evidence:** validation + personalization；`full_text_checked`（PMC 作者稿）。
- **One-Sentence Contribution:** 直接比较 generic 与 MRI-personalized knee model 对同一 gait-biofeedback intervention 的敏感性，发现 limb-level 结论不一定需要昂贵个体几何。
- **Problem:** 个体 cartilage surfaces/ligament insertions 是否真正改变 gait-retraining 结论不清楚。
- **Method:** 8 名 ACLR；habitual 与一周后 biofeedback walking，各约 3,000 steps；generic 12-DOF knee 对比 MRI-personalized geometry。
- **Data:** 3D mocap、GRF、pre-walking MRI；视觉反馈目标为第一 vGRF peak 提高 12%。
- **Evaluation:** 1D SPM、peak/effect size；比较 joint moments/forces 与 compartment contact-pressure metrics。
- **Findings:** 两种模型都捕捉到 biofeedback effect；personalization 对 compartment cumulative pressure 更敏感，但 generic 对 limb-level 分析可能足够。
- **Digital Twin Assessment:** `L1–L3` validation paper。它评估 intervention 的模型响应，却没有让模型选择反馈目标，也未验证预测 tissue mechanics 与后续组织结局。
- **Limitations:** pilot n=8；无直接 cartilage pressure truth；研究为横断/短期，不证明个体化能改善 ACLR outcome。
- **Reproducibility:** 中高；开放作者稿和详细方法，影像及模型数据的完整共享需进一步确认。
- **PhD Relevance:** **Critical design benchmark**。它提醒博士项目按输出层级决定 personalization 成本：运动/关节级可能 generic 足够，组织级才需要 P2。
