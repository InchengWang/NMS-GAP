# 两条研究线的启动与代码落实（2026-10-22）

**10/22泛化机制补查：** [TRAIN/VALID独立诊断完成；偏置不足以解释全部误差](SII2027_GEN3_GENERALIZATION_DIAGNOSIS_20261022_ZH.md)。源窗口权重差异已量化，并固定66fit等患者损失对照；新TEST结果尚未在此页报告。


**10/22泛化线结果验收：** [180次拟合与三批独立审计已完成](SII2027_GENERALIZATION_RESULTS_20261022_ZH.md)；真实源适配患膝2.949°，同标准化从零参考3.174°；低数据量曲线与虚拟源负结果均保留。[代码／合同索引](SII2027_GENERALIZATION_CODE_INDEX_20261022.json)。


[共同分支点与研究设计](SII2027_RESEARCH_FORK_20261022_ZH.md)已发布。随后完成训练入口及数据加载审计，并启动两线训练。本页是本轮启动记录，完成计数是生成此记录时的快照；**尚无新TEST推理或精度结论，训练完成仍须结果独立审计。**

| 研究线 | 当前执行 | 拟合预算 | 此次记录已完成200epoch的新fit |
|---|---|---|---:|
| GEN：泛化 | 先36个G，再36个A | 72新增、228000更新 | 4 |
| ARCH_AUG：架构与增强 | 先共享网络replay24，再其余交叉臂72 | 96新增、84000更新；旧48复用 | 17 |

共同数据仍为53真实试次／31TRAIN、12VALID、10TEST／8建模患者、6TEST患者；输入和六角标签不变。GEN使用4个worker，ARCH_AUG使用8个，每worker2个CPU线程；并行数量属于执行配置，不改变每fit数据、200epoch、窗口和更新量。

## GEN执行入口

`native_generalization_20261022/gen_training.py`实现contract/train/worker/verify；`gen_data.py`把拟合访问限定为当前fold允许的TRAIN和VALID。G完整排除目标患者、source TEST禁用；A只用相同目标真实数据，从对应G权重初始化并冻结其scaler。G按source等患者VALID选点，A按目标等trial VALID选点，均每10epoch检查且平局保留早期checkpoint。

`gen_preflight.py`的10项门槛通过：逐fold动态读白名单、source唯一真实帧scaler独立重算、两域窗口/标签一致、A两域真实视图一致、crop/四槽预算、拒绝A重拟合scaler及拟合上下文TEST。预检只读允许TRAIN动态数组，未读真实VALID/TEST；正式训练按方案读取VALID作选择。

`gen_evaluation.py`在72个完整训练和checkpoint验签后才开放目标真实TEST，计划552预测／3312逐角指标。`gen_analysis_preflight.py`已用空训练完成凭据确认提前评估被拒绝，并以合成四格算例核验域／适配／交互、64种符号翻转、患者bootstrap及Holm。此处没有运行正式TEST。

训练合同SHA256：`4c4b72ee5735e7d3f2a54473735dbd7d70e317c1d8c119ac233b971a2700cf23`。

## ARCH_AUG执行入口

`native_architecture_augmentation_20261022/arch_training.py`实现freeze/train/worker/verify。`train --stage all`先等待stage1的24个共享网络replay拟合全部完成，再执行stage2的72个交叉拟合。入口没有TEST loader；全96新fit及旧48参考验签后，独立分析入口才可评估TEST。

`arch_training_preflight.py`的18项门槛通过：旧48个参考的来源、CFG、200epoch历史与最佳点、严格state加载、best/final权重SHA；真实TRAIN scaler逐位相同、四槽窗口/标签/来源精确一致；同架构三增强的初始参数、shuffle和dropout轨迹一致。旧run未单独保存初始权重，因此验证的是不可变初始化代码和seed重现，不假称找到了旧初始checkpoint。

旧shuffle与dropout共用全局torch RNG，架构变化会改变RNG消耗；本版明确不保证跨架构逐batch顺序相同，但保持窗口清单、批数、步数和同架构增强比较。共享模型参数148422，约少1.78%，卷积MAC约1.959倍，不称计算完全匹配。

`arch_evaluation.py`计划636份新预测＋只读旧318份＝954记录／5724逐角指标。旧NPZ的method保留原值，新manifest明确source_method及imported_reference，CSV使用六格canonical名称，不修改旧结果。`arch_analysis_preflight.py`只用合成数据验证全fit gate与五个患者对比，未进行正式TEST。

训练合同SHA256：`6a8b4b59e0fc49d24aa6f4bff2a60d1cb2ac768988914b7a9075060b37a569cd`。

## 完成流程及尚未完成的工作

`research_fork_20261022/complete_research_branch.py`分别等待各分支完整训练凭据，核对已审阅分析源码SHA后执行verify→evaluate→summarize→statistics，仅写本地结果，不自动发布结论。源、合同或某阶段失败会记录错误并停止后处理，不静默换模型、患者或超参数。

当前未完成训练的完整矩阵、正式TEST评估、逐预测与患者统计的独立结果审计及最终图表。流水线完成也只代表固定分析完成，不能直接记为独立验收通过。所有新增结论继续以6患者、历史已接触TEST的探索性边界报告。

函数／行号／SHA及门槛摘要见[训练与分析代码索引](SII2027_RESEARCH_RUN_CODE_INDEX_20261022.json)；本地逐患者角色、原始数据、权重和完整波形不上传。

## 泛化结果验收补记

**10/22泛化线结果验收：** [180次拟合与三批独立审计已完成](SII2027_GENERALIZATION_RESULTS_20261022_ZH.md)；真实源适配患膝2.949°，同标准化从零参考3.174°；低数据量曲线与虚拟源负结果均保留。[代码／合同索引](SII2027_GENERALIZATION_CODE_INDEX_20261022.json)。

此前启动计数保留为当时快照；GEN已完成固定分析及独立结果验收，具体边界、标定量账目和后续决策见新结果页。

## TRAIN/VALID机制诊断补记

**10/22泛化机制补查：** [TRAIN/VALID独立诊断完成；偏置不足以解释全部误差](SII2027_GEN3_GENERALIZATION_DIAGNOSIS_20261022_ZH.md)。源窗口权重差异已量化，并固定66fit等患者损失对照；新TEST结果尚未在此页报告。
