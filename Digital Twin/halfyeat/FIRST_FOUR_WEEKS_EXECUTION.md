# 前四周执行清单：先建立可信实验，再扩大研究

日期：2026-10-05。按Asia/Tokyo规划：W1为10月5–11日、W2为10月12–18日、W3为10月19–25日、W4为10月26日–11月1日。日期是排期，不表示任务已经完成；周末不设置强制实验。衔接 [半年工作包](SIX_MONTH_EXECUTION_PLAN.md)。

## 1. 四周结束时的最小交付

一份可追踪的原始trial清单；一份测试输入来源表；一个配对group不跨split的协议；统一指标明细；至少一个开发个体的同协议baseline/因素pilot；SII引言和方法修订稿；第三篇主任务与是否有恢复动作的数据判断。

本阶段不承诺完成全部外层模型、新增患者试验或期刊投稿。模型训练需要源代码和原始数据；当前已交付的是文稿和协议，没有运行结果。

## 2. 每周五个任务

| 周/工作日 | 任务 | 当日产物 | 验收条件 |
|---|---|---|---|
| W1 周一 | 汇总两稿原始项目、患者与日期、共享trial、代码/日志和可用参考 | `trial_inventory`初版，资源标已存在/未确认/不可用 | 不能以论文队列人数代替实际可分析人数 |
| W1 周二 | 追踪真实输入中的orientation、骨盆框架与sensor-to-segment校准 | `input_provenance`，逐字段来源 | 测试动态mocap若进入输入，明确标reference-assisted并开部署分支 |
| W1 周三 | 查100/120Hz、时间戳/同步、加速度定义与虚拟生成 | `signal_convention`，含物理量/单位/框架/时间支持 | raw specific force与linear acceleration不混用；重采样有记录 |
| W1 周四 | 以原始trial组织真实、合成、增强和标签；查旧LR/早停用过哪些split | `group_manifest`、`selection_history` | 同轨迹派生数据不跨split；已使用test的历史不可抹掉 |
| W1 周五 | 汇总G0：输入、group和参考是否可信；决定先修哪个分支 | 一页`G0_status` | 每问题有证据位置与下一动作；只有验证通过才写pass |
| W2 周一 | 导出共同时间范围内角度预测/参考；确认有效片段规则 | `prediction_schema`和一个开发trial样例 | 同步独立；不借真值调整时间或挑低误差区间 |
| W2 周二 | 查符号、零点、投影/JCS与SO(3)；用已知姿态/运动核验 | `reference_definition`与检查图 | “6D中间输出”和“已验证角度”分开 |
| W2 周三 | 从逐角度/逐trial明细复核总体RMSE和PCC来源 | `metric_aggregation_audit` | 清楚0.9974/2.968°是何种聚合；不直接替换为审阅算数 |
| W2 周四 | 计数唯一mocap轨迹、real trial和分钟；设置嵌套标定子集 | `supervision_budget` | 低real ratio不得隐藏全量目标合成监督 |
| W2 周五 | 冻结一个开发协议与外层测试隔离，完成同协议基线配置 | `protocol_dev_v0.1`和baseline配置 | 开发集/最终test分工明确；所有方法共用输入和标签定义 |
| W3 周一 | 在开发个体跑最简direct baseline，查数据/数值/单位错误 | 一条可复现开发结果链 | 这是debug，不计入确认性结果 |
| W3 周二 | 在相同开发条件跑当前staged模型与可复核R01实现 | matched-input pilot表 | R01若仅重实现，标明实现差异；不能冒充原作者代码复现 |
| W3 周三 | 小规模2×2 real/mixed×adapt/no-adapt | component pilot表 | 测试集合一致；差别仅为预定因素及其成本 |
| W3 周四 | 生成患者点/误差分布、成本曲线雏形与输入图 | diagnostic figures | 不选择最优轨迹代替全体；无结果处标待跑 |
| W3 周五 | 对照[改稿工作稿](SII2027_MANUSCRIPT_REWRITE.md)修Introduction/Methods | revision draft v0.1 | 所有方法陈述与实际核验状态一致；结果槽位留空 |
| W4 周一 | 独立ROM参考、有效时间范围和ε依据；检查测试trial密度 | task feasibility note | 参考不循环；ε不是事后挑最显著的值 |
| W4 周二 | 同ensemble计算角度层Q、任务层T和校准区间C | score/interval定义表 | 相同point estimate；统一缩放前后排序一致 |
| W4 周三 | 用开发数据生成患者等权的risk曲线与逐患者coverage | risk evaluation pilot | 全拒答患者不记0 risk；trial多者不在选择前占更大权重 |
| W4 周四 | 核对额外真实腰/足通道、丰富输入模型与重戴资源 | recovery feasibility table | 不含动态测试参考；回放获取与真实在线获取分开 |
| W4 周五 | G1：SII主实验扩展、第三篇可行性与资源路线 | four-week review | 只冻结有证据的数据/方法；没做的实验保持未开始 |

预算建议：每周15–20小时，主要为审计/协议与开发pilot；原有学位任务另排。若W1–2发现严重输入/谱系问题，W3–4优先修复SII，第三篇可行性工作顺延，不并行扩大错误基础。

## 3. 五份最小数据记录的字段

以下是字段设计，不是已填写的患者数据表，也不是要求公开原始数据。

| 记录 | 最少字段 | 作用 |
|---|---|---|
| `trial_inventory` | participant_id、date/visit_known、raw_trial_id、recording_seconds、real_channels、reference_available、quality_status、exclusion_reason | 人数/试次/日期和资源可核验；不知道的日期用unknown |
| `group_manifest` | group_id、participant_id、raw_trial_id、derived_record_id、modality/domain、split_role、outer_fold、generation_parent | 真实/合成/增强派生谱系与split隔离 |
| `input_provenance` | feature_name、physical_quantity、unit、frame、source_stream、calibration_source、uses_dynamic_reference、future_support_seconds | 每项测试输入可获得性与延迟 |
| `supervision_budget` | method、fold、adaptation_trial_ids、unique_reference_trial_count、real_seconds、virtual_parent_ids、validation/calibration_ids、optimization_steps | 真实和合成的监督成本不重计/不隐藏 |
| `prediction_record` | model_version、participant_id、group_id、time、joint、side、angle_convention、prediction、reference、valid_mask、input_config、budget_id、analysis_version | 一条结果能追踪回输入、模型和评分 |

额外建立一页claim台账：claim、nearest-work ID、验证实验、完成状态、可用措辞。没有通过的claim写“拟检验”，不写“证明”。

## 4. 协议配置草稿

下列YAML用于说明冻结字段；`null`表示未知，`frozen: false`表示尚未冻结。它不能替代真实manifest或日志。

```yaml
protocol_version: halfyeat-dev-0.2
frozen: false
freeze_date: null
group_key: [participant_id, original_trial_id]
date_or_visit_available: null
test_inputs_use_dynamic_mocap: null
angle_convention: null
independent_reference_pipeline: null
sampling_and_sync_audited: false
final_test_used_for_selection: null
adaptation_budget_minutes: null
unique_supervised_trial_count: null
roles:
  population_train: null
  target_adaptation: null
  model_validation: null
  interval_calibration: null
  final_test: null
third_paper:
  task: paretic_knee_rom_per_trial
  point_estimate: mean_of_member_roms
  primary_score_comparison: task_rom_spread_vs_mean_angle_spread
  epsilon_degrees: null
  curve_target_coverage: 0.8
  curve_weighting: equal_participant_mass_before_selection
  actual_deployment_threshold: null
  additional_real_channels_available: null
  acquisition_fraction: 0.2
  real_reattachment_data_available: null
```

改变输入、任务、ε或split会产生新协议版本；若看过原test再修改，应明确探索性或取得新的未使用数据，不能只更新版本号恢复“无偏”。

## 5. 四周复盘的决策表

| 观测结果 | 下一步 |
|---|---|
| 输入独立、谱系通过、同协议baseline可运行 | 扩到完整SII外层评估与标定成本实验 |
| 仍依赖动态mocap骨盆 | 保留上界，修deployment输入；暂停仅两传感器可部署的表述 |
| 只缺少原实现但有清晰方法/数据 | 做明确标注的matched reimplementation；说明复现深度，不用跨论文数字冒充实测对照 |
| ROM参考可用但test trial极少 | 先报告个体/离散覆盖率与开发pilot；第三篇规模和独立成篇再评估 |
| T/Q风险排序无差别，但C改善区间包含率 | 分别报告两个结果；不能说校准改善排序；再看恢复动作是否有价值 |
| 有额外真实观测且能形成同预算回放 | 按[最小协议](THIRD_PAPER_MINIMUM_PROTOCOL.md)冻结恢复实验 |
| 只有常规uncertainty补图，没有独立任务或恢复证据 | 合并SII；第三篇转为NMS可辨识性/外部验证预研，保持博士主线 |

四周优先建立的是“实验中每个信息来源、每个监督单位、每个结果和每个claim都能被追踪”的基础。EMG、UWB或机器人下一阶段是否加入，应由其对目标NMS状态和交互任务的信息价值决定。
