# 前四周执行清单：SII首投基础与固定学习块

更新：2026-10-06。衔接[半年任务重排](SIX_MONTH_EXECUTION_PLAN.md)。优先级为SII→入组学习→第三篇；W1=10/6–11（4个工作日），W2=10/12–18，W3=10/19–25，W4=10/26–11/1。未核验旧事项不计为已完成；日历仅作任务安排，可按实际在场时间移动，周末不设强制实验。

## 1. 四周最低交付

SII：原始trial/输入来源/split清单、统一参考与指标、一个开发个体的同协议baseline/因素pilot、Introduction/Methods修订v0.1及11月完整实验配置。

学习：UWB测量定义、人体状态/坐标说明、简单几何定位练习和最近邻笔记，准备11月两连杆状态练习。

第三篇：只交一页资源结论（独立ROM参考、完整trial数、额外真实观测是否存在）。Q/T/C/ensemble与恢复实验在SII首投后启动。本阶段没有承诺新增患者采集或全部外层训练；源代码、原始数据和设备尚须实际盘点。

## 2. 每周SII任务块

| 日期/任务块 | 主任务 | 产物 | 验收 |
|---|---|---|---|
| 10/6 | 盘点两稿项目、代码、日志、实际参与者与试次 | trial_inventory、resource_inventory | 资源已存在/未知分列；不用论文队列人数代替有效人数 |
| 10/7 | 追踪orientation、骨盆坐标、标定及时间支持 | input_provenance | 逐帧参考辅助进入test输入时明确标注，确定可获得输入分支 |
| 10/8 | 查采样/同步、加速度定义与虚拟生成；原始trial配对 | signal_convention、group_manifest | 真实/合成/增强共享group；在分组之后切窗 |
| 10/9 | 查LR/早停/ratio使用过哪套数据；汇总G0问题 | selection_history、G0_status | 每问题有代码/日志位置和修复动作；未核验不记pass |
| 10/12 | 共同时间范围与独立角度参考 | prediction_schema、reference_definition | 不用test真值调整时序/offset；投影/JCS名称清晰 |
| 10/13 | 已知姿态检查符号/零点/SO(3)；核对近端/远端输出 | 几何定义检查图 | 中间6D输出与实际已验证角度分开 |
| 10/14 | 逐患者/试次/角度导出RMSE/PCC明细 | metric_aggregation_audit | 查明0.9974/2.968°聚合来源；不直接替换为审阅算数 |
| 10/15 | 计数唯一mocap轨迹、真实分钟数；嵌套适配预算 | supervision_budget | 低real ratio不隐藏额外目标合成监督 |
| 10/16 | 冻结一个开发协议与最终test隔离；定基线实现 | protocol_dev_v0.3、baseline配置 | 所有方法同输入/参考/预算；已使用test的历史记录完整 |
| 10/19 | 开发个体最简direct baseline | 一个可追踪debug结果 | debug不写为最终确认性性能 |
| 10/20 | 相同开发条件跑staged与R01可复核实现 | matched-input pilot | reimplementation与原作者代码复现分清 |
| 10/21 | 开发小规模2×2 real/mixed×adapt/no-adapt | component pilot | 共用测试定义；唯一监督预算和计算量披露 |
| 10/22 | 患者点/误差分布、输入依赖和失败图 | diagnostic figures | 展示开发失败；不选最优轨迹代表全体 |
| 10/23 | 按[改稿工作稿](SII2027_MANUSCRIPT_REWRITE.md)重写Introduction/Methods | SII revision v0.1 | 每项方法陈述符合核验事实，Results保持待跑 |
| 10/26 | 复盘P0，修阻塞；确认可分析名单与排除 | eligible-cohort/split清单 | 不能为保留期望人数放宽质量标准 |
| 10/27 | 设置完整外层E1主对照与计算队列 | 主实验配置 | 输入/监督/输出定义相同；最终test不选超参数 |
| 10/28 | 固定E2因素和E4预算点，计数实际成本 | factorial/budget配置 | 预算点来自可用适配池，不预设任意label优势 |
| 10/29 | 核对claim→nearest-work→实验；规划主文与补充 | claim台账、图表槽位 | R01–R05明确；没有性能处写待跑 |
| 10/30 | 月度G0复盘与11月安排 | 一页进度/阻塞报告 | 审计通过才展开主实验；第三篇资源结论与学习产物另列 |

每个工作日任务块可跨日；首投前每周14h给SII、5h学习、最多1h第三篇。W1较短，按实际可用日同比缩减，缺项并入W2；不要把19个任务块理解为每天必须完整跑完模型。

## 3. 四周的固定学习块

| 周 | 学习块A（约2h） | 学习块B（约2h） | 整理（约1h） | 验收 |
|---|---|---|---|---|
| W1 | ToF/TWR/TDoA、tag/anchor | 人体段/关节坐标；UWB量到什么 | 观测—状态图 | 不把距离/位置直接当段姿态或肌力 |
| W2 | 两维测距最小二乘与anchor几何 | 分析同一位置的多解/退化 | 配置与失败例 | 合成真值、相同噪声配置可重复 |
| W3 | R06组内可靠运动预测；记录输入/参考/条件 | R01稀疏重建与同预算问题 | 两篇最近邻笔记 | 摘要访问深度不足时不作负结论 |
| W4 | 两连杆q到tag位置的正运动学 | 测距Jacobian与局部秩 | D1设计草稿 | 明确基座、段长、安装哪些已知 |

第三篇资源检查只复用SII的清单：ROM能否由独立参考得到；完整test trial多少；额外真实通道和成本是否可用。不将W4改成uncertainty全实验周。

## 4. 最小记录字段

| 记录 | 最少字段 | 用途 |
|---|---|---|
| trial_inventory | participant_id、date/visit_known、raw_trial_id、recording_seconds、real_channels、reference_available、quality_status、exclusion_reason | 人数/试次/资源；未知日期保留unknown |
| group_manifest | group_id、participant_id、raw_trial_id、derived_record_id、modality/domain、split_role、outer_fold、generation_parent | 派生谱系与隔离 |
| input_provenance | feature_name、physical_quantity、unit、frame、source_stream、calibration_source、uses_dynamic_reference、future_support_seconds | 输入可获得性与延迟 |
| supervision_budget | method、fold、adaptation_trial_ids、unique_reference_trial_count、real_seconds、virtual_parent_ids、validation/calibration_ids、optimization_steps | 监督成本 |
| prediction_record | model_version、participant_id、group_id、time、joint、side、angle_convention、prediction、reference、valid_mask、input_config、budget_id、analysis_version | 结果追踪 |

额外claim台账字段：claim、nearest-work ID、验证实验、完成状态、可用措辞。没有通过的claim写“拟检验”。

## 5. 开发协议配置草稿

这是待填写配置，不是已经冻结的manifest或结果；null表示未知。

```yaml
protocol_version: halfyeat-dev-0.3
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
execution:
  primary_venue: IEEE_Sensors_Journal
  target_first_submission: 2027-01-15
  last_onsite_planning_boundary: 2027-02-28
  march_requires_onsite_devices: false
  april_group_arrival: true
third_paper:
  experiments_on_hold_until_sii_first_submission: true
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

改输入/任务/ε/split要记录版本；看过原test后改方案保持探索性或使用新未用数据，不能靠更新版本号恢复无偏。

## 6. 四周复盘

P0通过且baseline可运行：扩展11月完整E1/E2/E4；仍有动态参考或配对问题：先修SII，第三篇保持暂停。ROM/额外通道缺乏：记第三篇资源阻塞，不扩大采集。

学习完成观测定义和基础几何练习：进入11月D1；时间不足时减少阅读数量，保留一个具体练习。完整第三篇启动条件及2月交接见[半年计划](SIX_MONTH_EXECUTION_PLAN.md)，入组内容见[学习计划](ZHANG_LAB_PREPARATION_PLAN.md)。
