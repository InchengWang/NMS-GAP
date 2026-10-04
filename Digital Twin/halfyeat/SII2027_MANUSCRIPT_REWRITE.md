# SII2027 改稿工作稿：章节、替换段落与证据槽位

日期：2026-10-05。承接 [修改方案](SII2027_REVISION_PLAN.md)。本文件将建议转成可编辑文稿；方括号为待核验/填写项，不能直接投稿。英语段落是拟议修订协议的写作模板，不表示审计、重跑或新增实验已经完成。R01–R14的书目信息与访问深度见 [证据账本](SOURCE_AND_GAP_AUDIT.md)。

## 1. 本稿只回答一个主问题

**在测试时可获得的输入及相同个体标定预算下，分阶段真实—合成学习是否比最近邻物理约束模型及直接回归更有效地重建个体下肢运动？**

投稿故事围绕输入、监督预算和可解释验证；第三篇的完整拒答/主动补充观测问题另行检验。本稿必要的输入/鲁棒性消融不能为第三篇而省略。

### 标题

首选中性标题：**Subject-Adaptive Lower-Limb Motion Reconstruction with Paired Real–Synthetic Training and Explicit Calibration Budgets**。

确认可部署输入后可加“from Sparse Wearable Measurements”；同成本基线支持后才能加“Calibration-Efficient”；有独立康复输出证据后再强调“Functional Assessment”。标题不以“first”“two IMUs”“6D”作为创新主张。

## 2. Abstract：可填写的英文骨架

> Sparse wearable measurements can support subject-specific movement assessment, but reconstruction accuracy must be interpreted together with the availability of input information and the cost of individual calibration. This study evaluates a staged real–synthetic learning framework for lower-limb motion reconstruction in chronic stroke. Real recordings and synthetic features derived from the same underlying motion trial are kept within a single data partition, and population pretraining excludes the target participant. Adaptation is performed using a predefined calibration pool, while final evaluation uses separate real-sensor trials and motion-capture references. We compare the framework with [same-protocol physics-informed baseline] and [direct-regression baseline] under matched input and supervision budgets. Across [number of eligible participants], the participant-level [primary angle] RMSE is [estimate and interval], with a paired difference of [estimate and interval] relative to [primary baseline]. [One sentence on the independent functional outcome, if available.] Factorial experiments quantify the separate effects of synthetic training and individual adaptation, and the calibration analysis reports both recording time and unique supervised trials. The results characterize the conditions under which the framework supports [the actually validated assessment task], together with its input requirements and failure cases.

摘要填数条件：主指标定义审计完毕、完整表来自同一明细、测试未参与模型选择。原稿总体PCC不在这里自动沿用。若没有独立功能输出，删除对应句子；若试验只包含实验室参考辅助输入，标题与摘要必须明确这一条件。

## 3. Introduction：四段结构和替换文字

### 第一段：为什么需要可验证的个体运动状态

> Quantitative lower-limb motion measurements can describe movement patterns after stroke and provide inputs to rehabilitation assessment. Wearable sensing is attractive when laboratory motion capture is impractical, but sparse measurements do not directly observe every segment or joint. A reconstruction system must therefore establish which outputs can be recovered from the information available during use, rather than treating a small sensor count as sufficient evidence of deployability.

作用：从人体状态与使用问题出发；不把角度预测直接写为肌力、神经控制或治疗有效性。

### 第二段：最近邻明确放在前面

> Guo et al. demonstrated lower-limb kinematic prediction from two IMUs using physics-informed learning in chronic stroke [R01]. Sparse inertial reconstruction also has established precedents for staged position and pose estimation [R02], training with simulated and measured inertial data [R03], and transfer learning with reduced sensor configurations [R04]. Continuous rotation representations provide a further established tool for neural pose estimation [R05]. These studies motivate the present formulation, but the individual components are not claimed as new.

作用：R01是同队列最近邻，应在核心问题之前讲清，而不是只出现在跨论文性能表。R02–R05的部件先例逐项对应方法。不可据摘要访问深度宣称其没有做过某项详细实验。

### 第三段：提出协议层的可检验问题

> The question addressed here is whether staged reconstruction and paired real–synthetic training provide additional value under explicit subject-adaptation budgets. This question requires separating three factors: the information used to construct the test inputs, the amount of unique subject-specific supervision, and the contribution of each learning stage. In particular, synthetic features derived from a held-out motion trajectory must not enter training, and reference-derived coordinate information must be distinguished from information obtainable from wearable measurements.

作用：这是本稿拟检验的条件，不是“整个领域没有这些协议”的断言。坐标来源和配对谱系若已经正确，就展示证据，不使用问题暗示作者已犯错。

### 第四段：贡献表述

> We evaluate the framework through three analyses: (1) a comparison with physics-informed and direct-regression baselines using matched inputs and subject-specific supervision; (2) a factorial analysis of synthetic training and adaptation, together with a focused stage ablation; and (3) calibration-cost and output-validity analyses using participant-level errors and [a predefined functional measure, if available]. The study aims to identify both the benefit and the limitations of the reconstruction strategy within the tested movement and sensing conditions.

作用：贡献写为“完成了什么检验”，待结果成立后再写“提高了什么”。这里没有新的有效性结论。

## 4. Methods：六个需要替换/新增的模块

| 模块 | 最少必须写清 | 应放的证据 |
|---|---|---|
| A. Participants and recording | 原队列和本分析人数、排除原因、原始trial数、日期/visit、通道、采样/同步、伦理和共享数据来源 | 参与者流图；每人trial与缺失表 |
| B. Input availability | device orientation来源、局部/世界/骨盆框架、sensor-to-segment校准、测试是否借助动态mocap | 每个输入字段的来源和时间支持表 |
| C. Synthetic feature generation | raw specific force或linear acceleration、位置偏移、重力、旋转方向、滤波、生成时使用哪些轨迹 | 与真实信号同单位/框架的公式；静态/已知运动检查 |
| D. Partition and adaptation | 同轨迹真实/合成分组；population排除目标人；adapt/model validation/calibration/test职责 | group manifest；监督预算表 |
| E. Staged model | 各阶段输入输出、预测/真值中间状态使用、loss、6D正交化与SO(3)稳定实现 | 端到端推理图；参数和计算量 |
| F. Reference and evaluation | 投影角/JCS区别、符号零点、共同时间范围、患者级聚合、ROM定义和总延迟 | 统一指标明细；已知姿态算例 |

### D 模块的英文替换模板

> Each original motion trial defines a grouping unit containing its measured sensor streams, motion-capture data, synthetic features, labels, and augmented derivatives. Group assignment precedes window generation. For each outer evaluation participant, population pretraining excludes all records from that participant. The remaining target-participant records are assigned to adaptation, model-selection, [uncertainty-calibration, if used], and final-test roles using [the audited rule]. Only the predefined adaptation pool supplies target-specific supervision. The reported budget counts unique underlying motion trials and recording duration; synthetic copies do not reduce this supervision cost. Final-test labels are used only for scoring.

### B 模块的两种互斥表述

**可部署协议核验通过后：**

> Test inputs are generated exclusively from [the measured wearable signals] and [the predefined calibration procedure]. Dynamic motion-capture measurements are not used to transform or normalize test inputs. Motion capture is used to generate training features and evaluation references within their assigned roles.

**只有参考辅助条件时：**

> The present evaluation uses motion-capture-derived pelvis-frame information to construct the sensor features. Results therefore describe a reference-assisted reconstruction condition. A separate wearable-only experiment is required before interpreting this pipeline as deployable from the stated sensor set.

二者不能混写为一个“只有两IMU”的结果。若有实测腰部/额外观测，单列配置与成本。

### F 模块的英文替换模板

> Predictions and references are compared within a predefined common time range using the same angle convention and units. Errors are first calculated for each trial and output, then aggregated within participant; group summaries give equal weight to participants. Correlations are computed separately for each output and are not obtained by concatenating distinct joint-angle channels. Participant-level paired effects are reported for the prespecified primary comparison. [The functional measure] is computed using the same predefined rule for predictions and the independent reference pipeline. Bias correction, if used, is fitted only on the calibration data and is not estimated from final-test labels.

## 5. Experiments：保留四个主实验

1. **主对照：** staged vs R01可复核实现 vs matched direct regression；同输入、同标定池、同输出定义。不能用旧Table VI跨论文数字替代。
2. **因素归因：** real-only/mixed × no-adapt/adapt，保持共同测试和唯一监督轨迹计数；另报训练steps/参数量。
3. **标定成本：** 从同一适配池构建嵌套预算，固定验证/测试；同时记录分钟、trial、唯一mocap轨迹和更新时间。
4. **输入与输出有效性：** deployment/reference-assisted分列；主要角度与ROM/偏置/失败例。中心窗口为离线时明确标注；若没有因果重跑，不把低计算耗时称实时。

学习率扫描移到补充材料。分阶段消融至少保留一个能检验科学解释的直接对照，不把全部TCN/GRU/attention组合穷举作为主结果。

## 6. Results：五张图、四张表的槽位

| 项目 | 内容 | 必须避免 |
|---|---|---|
| Fig.1 | 观测来源、配对group、外层评估及模型流程 | mocap训练生成箭头和测试输入箭头混在一起 |
| Fig.2 | 每患者主终点和配对差 | 只有一条代表轨迹或均值柱状图 |
| Fig.3 | RMSE–标定分钟数/唯一trial曲线 | ratio变化时隐藏全量目标合成标签 |
| Fig.4 | 关键失败例与角度零点/ROM误差 | 用最优个体代表总体有效性 |
| Fig.5 | 指定功能输出或误差–延迟结果，按实际完成选择 | 未验证的临床/控制图 |
| Table1 | 人数、原始trial、split、排除与数据资源 | 17人队列被写成17人均完成主验证 |
| Table2 | 同协议主基线，逐输出及患者级汇总 | 不同角度flatten后的PCC成为主指标 |
| Table3 | 2×2因素与阶段消融 | 不同输入/标签预算导致的收益被归因网络 |
| Table4 | deployment/upper-bound、成本和适用范围 | 上界与部署版本合成一列 |

所有结果先填“待重跑”，不是填0，也不是自动抄原摘要数值。每行应能追踪到 `group_id`、模型版本、输入配置、标定预算和评估版本。

## 7. Discussion：先解释边界，再解释潜在价值

建议分四段：同预算主对比解释；synthetic与adapt收益是否独立；近端/远端、非矢状与功能误差差异；实际输入、标定、样本/任务和时间范围的局限。

可用的限制段落：

> This evaluation is limited to [the audited cohort and movement conditions]. Subject adaptation uses supervised calibration data, and performance should therefore not be interpreted as zero-shot generalization. The validated outputs are [the actually tested projected angles or joint-coordinate measures]; use of a 6D representation does not itself validate every anatomical rotation component. [The actual temporal formulation] limits the interpretation of online use. Finally, motion-reconstruction accuracy does not establish the identifiability of neural or muscle states, nor the effectiveness of an assistive intervention.

结尾写本稿经验证的运动状态贡献；可以提出下一步“任务可靠性、外部锚定NMS模型与交互验证”，但不能把博士计划目标写作本稿已实现的能力。

## 8. 改稿完成表

每条置为“未核验/核验通过/已按结果修改”；必须附证据位置：输入与坐标；配对split；LR/早停数据角色；指标聚合；参考定义；标定预算；最近邻同协议实现；作者/affiliation；共享工作说明；结果及limitations一致。投稿稿中不得残留任何方括号。
