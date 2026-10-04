# UWB for motion capture — PhD proposal

本目录按请求命名为 **`UBW for motion capture`**；研究正文采用正确技术缩写 **UWB (ultra-wideband)**。

面向南科大张明明课题组的博士计划，以人体神经肌骨系统与具身智能为主线，使用 UWB 作为主要动作观测工具，并连接 sensing、modeling、control 和 interaction。IMU 是可选补充模态。

| 文件 | 内容 |
|---|---|
| [PHD_PROPOSAL.md](PHD_PROPOSAL.md) | 完整英文计划及中文题目：背景、SOTA、validated gap、核心问题/假设、Aim 1–3、方法、基线、指标、统计、贡献、风险、时间表、个人与实验室匹配。 |
| [GAP_VALIDATION_AND_NEAREST_WORK.md](GAP_VALIDATION_AND_NEAREST_WORK.md) | 继承 gap 的 traceability、UWB 专属 verdict、反证边界、nearest-work 对照、检索范围、21 项来源的完整引用/出版状态/访问深度。 |
| [PROPOSAL_SUMMARY_ZH.md](PROPOSAL_SUMMARY_ZH.md) | 中文讨论概要，便于与导师讨论研究范围、端点和推进条件。 |

**建议阅读顺序：**中文概要 → 完整计划 → nearest-work/gap 证据记录。

## 三项 Aim

1. 验证 UWB 的任务可观测性与重新佩戴/遮挡等条件下的失效边界。
2. 检验该测量不确定性对个体化神经肌骨预测的影响，使用独立 EMG/力学参考。
3. 比较人体状态信息是否改善有界物理交互决策，保留强控制与故障回退基线。

## 证据与范围状态

- 核查日期：**2026-10-04**。
- 使用 [nms-digital-twin-phd-proposal](https://github.com/InchengWang/nms-digital-twin-skills/blob/main/nms-digital-twin-phd-proposal/SKILL.md) 及其结构/实验清单。
- 从原 Digital Twin 的 G07/G01、G04、G05 出发；相关状态为 **partially-addressed**。UWB 专属贡献仍须先导与独立实验验证。
- 不宣称首次 UWB 捕捉、首次不确定性融合、首次 NMS 控制或首次 UWB HRI；各 expected contribution 均给出 nearest prior work 和推翻条件。
- 可穿戴标签/锚点 ranging/localization 是硬件假设；原始数据接口、标签间测距、EMG/测力/机器人及患者访问均须核实。
- 主交互任务暂选坐位躯干—上肢到达；全身功能动作作为感知评估。时间表以确认入学日为起点，样本范围待先导后进行正式统计设计。

原有 gap validation 和旧 proposal 保持为独立历史材料。本目录为新的 UWB 研究方案。

