# 来源、最近邻与 gap 复核

编制日期：2026-10-05（Asia/Tokyo）。用途：支撑 SII2027 修改、第三篇规划及博士计划。所有“贡献”均为待检验目标，不是已获得的新结果。

## 1. 本次材料及审阅边界

逐页阅读并检查了上传的 `BSN.pdf`（4 页）和 `sii2027_abstract_summary.pdf`（7 页）。后者虽然文件名含 summary，实际包含方法、实验、结果、讨论和参考文献；本报告评价的是这份版本，不假定它等同于全部代码、日志或原始数据。未取得这些实验材料，因而没有复现模型，也没有认定任何数据泄漏已经发生。

| 编号 | 材料 | 能确认的内容 | 尚不能确认 |
|---|---|---|---|
| P1 | BSN 稿件，Personalized Sparse-to-Dense IMU Signal Reconstruction for Gait Event Analysis in Chronic Stroke Patients | 当前作者表中 Yincheng Wang 为第一作者；真实足部信号重建真实小腿信号；同患者留出一次 walking session；事件参考来自实测小腿 IMU | 实际分析患者数、日期是否跨日、投稿/录用/发表状态、原始数据可用范围 |
| P2 | SII2027 稿件，Subject-Adaptive Staged Lower-Limb Kinematic Reconstruction in Chronic Stroke Gait Using Real and Virtual Two-Shank IMUs | 当前作者表中 Shuo Feng 在首位，Yincheng Wang 在第二位；用户确认尚未投稿；原队列 17 人，主要结果 8 人，数据量实验 5 人；训练用 mocap 合成 IMU；测试用真实 IMU | 原始试次配对谱系、测试输入骨盆框架来源、完整拆分清单、汇总指标实现、原始 GRF/EMG 是否存在并可使用 |

本次任务以这两份工作和留组半年为约束；此前 UWB 计划不是本次必须执行的硬件路线。UWB 可作为博士阶段的可选观测，IMU 也是可选 sensing modality。

## 2. 稿件证据定位

| 定位 | 原文证据 | 审阅判断与后续动作 |
|---|---|---|
| P1 p.1–2 | 7 m 平地、自选舒适速度；五个 IMU；100 Hz；225 样本窗口 | 受控直行证据；不支持日常活动、跨日或在线控制的结论。需补患者数、原始采样与同步说明 |
| P1 p.2 | IC/FC 与实测小腿算法结果比较，150 ms 匹配容差 | 属于传感器替代的一致性评估，不是独立足接触准确性；容差敏感性及独立参考待补 |
| P1 p.3 Table I | 双足输入 biRNN 的非患侧/患侧 PCC 0.9573/0.9701；加腰为 0.9542/0.9710 | 加腰收益随侧别和指标变化；不能概括为所有重建指标一致改善 |
| P1 p.4 Table II | F1 0.883–0.957；非患侧 FC 加腰后 F1 从 0.904 降至 0.889 | 减小 MAE 不等于提升全部事件质量。需要传感负担与任务收益的联合分析 |
| P2 p.2 Fig.1、Eq.(1) | 输入和标签共享骨盆框架；虚拟信号使用 mocap 世界中的骨盆姿态 | 训练生成用 mocap合理；测试真实输入若也用逐帧 mocap 骨盆姿态，则含额外参考信息。需追踪来源后选择实验室上界或可部署版本 |
| P2 p.2–3 | 真实/虚拟试次先划分再生成窗口；预训练排除目标患者的两种数据 | 有正确的拆分意图；仍需证明来自同一原始轨迹的真实/合成版本始终属于同一组 |
| P2 p.3 Eq.(12)、p.5 Table IV | 个体适配加入目标患者真实和虚拟训练试次；ratio 描述只涉及真实试次比例 | 若低 ratio 仍使用全部目标虚拟轨迹和标签，不能据此声称减少同等比例标定成本 |
| P2 p.3 Eq.(6)、p.4 Table I | 中心窗口、双向 GRU、120 帧/120 Hz、20 帧 stride、Hann 融合 | 名义上约 0.5 s 未来信息；精确支持范围需由代码确认。处理耗时快不代表端到端实时 |
| P2 p.4–5 | 17 人中 8 人进入主评估；5 人学习率/数据量实验 | 需报告其余 9 人排除理由；“held-out participants”应区分零样本与适配后留出试次 |
| P2 p.5 Tables II–III、V | 逐角度 PCC 0.872–0.986；总体 PCC 0.9974；总体 RMSE 2.968° | 按表中 8 项 PCC 等权均值为 0.923875；RMSE 等权均值 2.562°，这些不是自动更正值，而是提示聚合定义必须解释 |
| P2 p.5–6 | 最优 ratio 0.9；每次试次选择仅 3 次；Table VI 跨研究比较 | 当前“约 8–10 次即可稳定适配”为描述性观察；需分钟数、独立标签预算、区间和固定测试。文献数字不能替代同数据重跑 |
| P2 p.4 Eq.(13)–(14)、p.6 Fig.5 | 从 6D 相对旋转投影到指定平面；示例踝角约 −40 至 −60° | 需说明坐标和零点；投影角不是自动等价于临床 JCS 全部三维关节角。偏置、ROM 和 SO(3) 误差应分开 |

P1 的“虚拟 IMU”是预测未测物理传感器的信号；P2 的“虚拟 IMU”是由训练参考运动学合成的输入。二者不是同一种数据，也不能直接拼接：P1 输出加速度/角速度，P2 需要加速度/姿态矩阵及坐标对齐。

## 3. 已有 gap verdict 的继承与收窄

上游 [Digital Twin gap report](../03_gap_validation/GAP_VALIDATION_REPORT.md) 截止 2026-09-01；其 [matrix](../03_gap_validation/data/gap_validation_matrix.csv) 与 [Embodied AI matrix](../../Embody%20AI/02_gap_validation/data/embodied_ai_gap_validation_matrix.csv) 为本次起点。[2026-10-01 更新](../../01_literature_mapping/updates/2026-10-01.md) 为增量检索，不是对全部 gap 的重新定案。本次补查到 2026-10-05；不是系统综述。

| 上游方向 | 原 verdict | 本次可推进的残余问题 | 进入哪里 |
|---|---|---|---|
| G07 决策相关的最小观测 | partially-addressed | 稀疏输入在不同佩戴、试次/日期和个体适配预算下，能否保留指定任务输出及可靠度；已有稀疏感知不是空白 | SII 的工程基础；第三篇的任务与观测成本实验；博士 Aim 1 |
| G01 在线个体参数与可辨识性 | partially-addressed | 从可观测运动学推进到少量、外部锚定的 NMS 参数；区分参数多解、传感漂移、个体改变 | 博士 Aim 2；半年内仅做资源与小规模可辨识性预研 |
| G05 / EAI-G04 不确定性到动作 | partially-addressed | 重建链条失效时，拒答/补充观测/再标定能否在相同有效输出率下减少错误反馈；物理辅助另需验证 | 第三篇离线试验；博士 Aim 3 的前置条件 |
| EAI-G01 个体后验条件化控制 | partially-addressed | 已识别的 NMS 个体后验相对固定参数/纯运动学是否增加控制价值 | 博士中后期；不将离线复核称为已完成此 gap |
| G03/G04 患者具身适配及未见条件预测 | partially-addressed | 在固定模型后预测未见机械/交互条件并外部验证；不以不同速度或拐杖组比较代替因果干预证据 | 博士后续验证轴 |
| EAI-G07 稀疏或重建 IMU 本身 | not-a-gap | 更少传感器、换网络、重建 IMU 不构成独立具身智能空白 | 不作为博士 novelty |
| G02 / EAI-G03 长期多时间尺度 | 旧报告 confirmed-open | 本次数据未证明多日期、疲劳及恢复证据同时存在；本轮不进一步认证“全球未解决” | 不作为半年主任务；资源充分后再验证 |

**本次保留的是经过验证后收窄的研究问题，主要 verdict 仍为 partially-addressed。** 临床疗效、首次不确定性步态分析、首次稀疏感知均不在可用 claim 中。

## 4. 最近邻参考与访问深度

| ID | 最近邻与原始来源 | 已建立的能力 | 本次证据深度 |
|---|---|---|---|
| R01 | Guo et al. (2025), Physics-Informed Learning Framework for Lower Limb Kinematic Prediction With Sparse Sensors and Its Application in Chronic Stroke. TNSRE 33:2475–2486. [DOI](https://doi.org/10.1109/TNSRE.2025.3581352), [作者摘要](https://pubmed.ncbi.nlm.nih.gov/40536851/), [东北大研究发布](https://www.tohoku.ac.jp/japanese/2025/07/press20250702-01-data.html) | 两 IMU、物理约束 TCN、慢性卒中下肢运动预测；也是两稿的数据来源 | 原始索引摘要及大学发布；IEEE全文打开遇验证页。没有把 P2 Table VI 二次摘录当作全文复核 |
| R02 | Yi, Zhou & Xu (2021), TransPose. ACM TOG. [DOI](https://doi.org/10.1145/3450626.3459786), [作者项目](https://xinyu-yi.github.io/TransPose/) | 六 IMU、位置中间表示和分阶段姿态/位移估计 | 作者项目与原始书目信息；未逐页重读全文 |
| R03 | Mundt et al. (2020), Estimation of Gait Mechanics Based on Simulated and Measured IMU Data Using an Artificial Neural Network. [全文](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2020.00041/full) | mocap 合成惯性数据、真实/合成联合训练、传感位置/姿态增强、运动学和力矩估计 | 读取全文方法中生成、参考、划分及讨论相关部分 |
| R04 | Li et al. (2024), 3D Knee and Hip Angle Estimation With Reduced Wearable IMUs via Transfer Learning During Yoga, Golf, Swimming, Badminton, and Dance. [DOI](https://doi.org/10.1109/TNSRE.2024.3349639), [作者摘要](https://pubmed.ncbi.nlm.nih.gov/38224523/) | 减少 IMU、非平面关节角和迁移学习 | 原始索引摘要；直接页面返回空壳，未复核全文协议 |
| R05 | Zhou et al. (2019), On the Continuity of Rotation Representations in Neural Networks. [CVF全文入口](https://openaccess.thecvf.com/content_CVPR_2019/html/Zhou_On_the_Continuity_of_Rotation_Representations_in_Neural_Networks_CVPR_2019_paper.html) | 连续 6D 旋转表示 | P2 引用的既有表示；CVF入口本次返回403，未重新全文审阅，不支撑剩余 gap 的负结论 |
| R06 | Lin et al. (2025), Open-Environment Evidential Learning for Reliable Myoelectric Locomotion Prediction. TNSRE 33:4477–4486. [DOI](https://doi.org/10.1109/TNSRE.2025.3626316), [作者摘要](https://pubmed.ncbi.nlm.nih.gov/41150224/) | sEMG、开放环境不确定性/OOD增强、失败检测与 risk–coverage 评价 | 读取作者摘要；没有据此声称它未处理任何具体的失效类型 |
| R07 | Donahue et al. (2026), Calibrated Uncertainty for Trustworthy Clinical Gait Analysis Using Probabilistic Multiview Markerless Motion Capture. TBME. [DOI](https://doi.org/10.1109/TBME.2026.3691128), [作者全文 v1](https://arxiv.org/html/2601.22412v1) | 运动学不确定性校准、外部参考、多机构患者、剔除不可靠结果 | 期刊元数据核对；阅读作者 v1 方法与讨论。版本可能不同，不称逐页审阅最终期刊版 |
| R08 | Zhang et al. (2023), Neuromusculoskeletal model-informed machine learning-based control of a knee exoskeleton with uncertainties quantification. [全文](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1254088/full) | NMS-informed BNN/GP、EMG+运动学、力矩置信界到外骨骼辅助 | 读取原文方法与控制评估相关部分；不确定性到控制已存在 |
| R09 | Geifman & El-Yaniv (2019), SelectiveNet. [ICML/PMLR](https://proceedings.mlr.press/v97/geifman19a.html) | 选择性预测和拒答架构 | 原始摘要/方法入口；作为方法来源和基线，不主张新拒答算法 |
| R10 | Xu & Xie (2021), Conformal prediction interval for dynamic time-series. [ICML/PMLR](https://proceedings.mlr.press/v139/xu21h.html) | 时序预测区间 EnbPI | 原始摘要；其假设不能自动迁移到本研究小样本、跨患者/佩戴漂移 |
| R11 | Bueno & Montano (2017), Neuromusculoskeletal model self-calibration for on-line sequential bayesian moment estimation. [DOI](https://doi.org/10.1088/1741-2552/aa58f5), [作者摘要](https://pubmed.ncbi.nlm.nih.gov/28079030/) | NMS 在线自标定与顺序 Bayesian 力矩估计 | 原始索引及既有 gap report；本次未全文复核 |
| R12 | Rabbi et al. (2024), Muscle synergy-informed neuromusculoskeletal modelling to estimate knee contact forces in children with cerebral palsy. [全文](https://link.springer.com/article/10.1007/s10237-024-01825-7) | 少量肌电/协同信息支撑特定 NMS 输出 | 出版社摘要和全文入口；内部接触力仍为模型估计，不据此宣称实测肌力 |
| R13 | The Neuromusculoskeletal Modeling Pipeline (2025). [JNER全文](https://link.springer.com/article/10.1186/s12984-025-01629-5) | OpenSim 个体化、神经协同与治疗优化；卒中假设治疗示例 | 读取个体化与卒中示例相关部分；不将假设治疗认作临床有效性试验 |
| R14 | Caggiano et al. (2022), MyoSuite. [CoRL/PMLR](https://proceedings.mlr.press/v168/caggiano22a.html) | 肌肉驱动、接触丰富的运动控制环境 | 原始摘要；仿真平台不是同步到患者的数字孪生证据 |

## 5. Claim-to-nearest-work 账本

| 本次待检验贡献 | 最接近的反证 | 可使用的表述 | 必须增加的证据 |
|---|---|---|---|
| SII 的低标定成本、分阶段真实/合成个体重建 | R01 两 IMU 卒中；R02 staged；R03 synthetic；R04 transfer；R05 6D | “在配对隔离和可获得输入下，检验分阶段表示与真实/合成适配的联合价值” | 同数据同标签预算基线，完整消融、坐标来源及冻结测试 |
| 第三篇观测成本与任务可靠性联合评估 | P1/P2 已有信号/角度重建；R06 有失败检测；R07 有校准与剔除；R09 有拒答 | “检验个体重建链条在误差传播和佩戴/试次变化下，补充观测是否改善指定反馈可靠性” | 独立任务参考、相同有效输出率、成本匹配、独立失效条件；若同类近邻已完整覆盖则调整题目 |
| 低维 NMS 个体后验及可辨识性 | R11 在线自标定；R12 sparse EMG；R13 个体模型 | “评估外部锚定的少量 NMS 参数在未见条件中的可辨识性和预测价值” | EMG/机械参考、参数多解与预测区间、锁定后验证；不能由角度准确性推导 |
| 个体后验驱动交互/辅助 | R08 不确定性控制；R14 肌肉控制仿真 | “检验患者后验相对固定参数与纯运动学状态，在同等延迟和观测预算下的动作价值” | 控制对照、交互参考、失效处理及用户实验；不直接声称康复疗效 |

这些残余条件并非“已证明无人做过”。R06/R07 已推翻宽泛的“运动预测没有不确定性与失败检测”命题。组合方法只有在独立问题、合理对照和外部结果成立时才有论文价值。

## 6. 期刊与实验室原始来源

- J01：[IEEE Sensors Journal 官方作者指南](https://ieee-sensors.org/ieee-sensors-journal/for-authors/)；读取于 2026-10-05。常规双栏稿件通常不超过 8 页；超页收费；图形摘要为要求；会议扩展需实质新材料。不是“加几页就可投”的承诺。
- J02：[Sensors 官方范围](https://ieee-sensors.org/ieee-sensors-journal/)：包含 sensor data processing、检测和估计。
- J03：[TNSRE 官方 editorial policy](https://www.embs.org/tnsre/for-reviewers/editorial-policy/)：检索到范围信息；[详细投稿页](https://www.embs.org/tnsre/for-authors/submission-guidelines/)直接访问被 robots 拒绝。本次不认证其最新页数/APC/文件规格；真正投稿前从官方入口复核。
- L01：[Hayashibe / 东北大生物机械工程官方介绍](https://www.bme.tohoku.ac.jp/english/labo/field_03.html)：神经机器人、运动建模、神经康复及肌肉建模背景；不等于承诺某设备或患者资源对本项目可用。
- L02：[张明明 / 南科大官方主页](https://sustech.edu.cn/zh/faculties/zhangmingming.html)：康复机器人、人机交互、UWB/IMU感知与肌电运动预测；其 R06 应成为博士规划的内部最近邻，而不是被忽略。

## 7. 本次反证检索记录

执行日期 2026-10-05，重点为原始论文/出版社/作者项目与官方期刊页面。代表查询：`Physics-Informed Learning Framework for Lower Limb Kinematic Prediction`；`3D Knee and Hip Angle Estimation transfer learning`；`stroke sparse IMU kinematics uncertainty conformal prediction sensor selection 2025 2026`；`Calibrated Uncertainty for Trustworthy Clinical Gait Analysis`；`Open-Environment Evidential Learning for Reliable Myoelectric Locomotion Prediction`；`neuromusculoskeletal Bayesian neural network confidence bound exoskeleton`；两期刊官方作者说明；两实验室官方主页。

没有完成 Scopus/Web of Science 导出、全部引文追踪或每篇最终版全文审阅。第三篇的精确 joint-condition novelty 为**有依据的候选贡献**，冻结标题和提交前还需按实际完成条件复查最近邻。这里已经足够规划实验，尚不足以写“首次”或排除所有先行工作。
