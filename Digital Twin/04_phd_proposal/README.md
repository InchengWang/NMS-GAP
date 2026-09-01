# 04 — PhD Proposal

本目录把前一阶段通过反证检索的 research gaps 收敛为一项可证伪、分阶段推进的人体神经肌骨数字孪生博士计划。

## Proposal positioning

**主题：** 纵向、带不确定性的人体 neuromusculoskeletal digital twin，用于患者特异状态估计、双时间尺度适应和安全康复决策。

**不是：** 以 IMU 信号重建为中心的 gait-analysis proposal。IMU 仅作为候选运动学观测；EMG、足底压力、实验室动力学参考和必要时的超声/影像由目标状态的可观测性决定。

**Gap selection：**

- 核心科学 gap：G02 `confirmed-open`，但缩窄为可执行的“快速疲劳 + 慢速跨周适应”两时间尺度问题。
- 近期方法入口：G07、G01、G05，均为 `partially-addressed`，因此只研究其尚未解决的联合条件。
- 转化扩展：G03、G04，采用分阶段、带停止条件的验证路线。
- 不作为 novelty：G06（`not-a-gap`）、G10（`out-of-scope`）；G09 作为预先规定的有效性审计维度。

## Files

- [`PHD_PROPOSAL.md`](PHD_PROPOSAL.md): 完整英文博士研究计划，可作为导师讨论稿。
- [`NOVELTY_AND_NEAREST_WORK.md`](NOVELTY_AND_NEAREST_WORK.md): 每项 novelty boundary、最近已有工作、差异与禁止使用的过度表述。
- [`data/aim_design_matrix.csv`](data/aim_design_matrix.csv): Aim—data—baseline—metric—statistics—risk—kill test 的结构化矩阵。

## One-sentence thesis

> Develop and test a patient-bound hybrid NMS model that remains calibrated across sessions, separates fast fatigue from slower adaptation, and uses uncertainty to preserve or safely withhold rehabilitation decisions under sensing and model failure.

## Evidence status

这是由 literature map、49 篇核心论文 critique 和 10 个 gap-validation dossier 推导出的 **proposal-level plan**，不是已取得的研究结果。所有贡献均写为待检验目标；没有使用 “first” 或 “unexplored” 声明。

