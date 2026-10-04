# halfyeat：半年工作与博士衔接

日期：2026-10-05。目录名称按用户指定保留为 `halfyeat`。

本套计划结合上传的BSN与SII2027工作。SII2027尚未投稿；对它的建议是先核验部署输入、真实/合成配对隔离、标定预算及指标，再决定Sensors Journal或TNSRE的内容路线。第三篇围绕任务可靠性和补充观测价值开展，不以新网络或重建IMU本身作为创新。

| 文件 | 内容 |
|---|---|
| [PHD_PROPOSAL_ZH.md](PHD_PROPOSAL_ZH.md) | 完整中文博士计划：题目、背景/现状/gap、问题/假设、Aims1–3、方法/基线/指标/统计、贡献/风险、时间及实验室契合 |
| [SII2027_REVISION_PLAN.md](SII2027_REVISION_PLAN.md) | 页码对应问题、投稿定位、P0核验、必要实验、统计与图表、标题/摘要骨架 |
| [THIRD_PAPER_PLAN.md](THIRD_PAPER_PLAN.md) | 与两稿的区别、最近邻、任务/动作/基线/指标、数据门槛、kill tests和替代 |
| [SIX_MONTH_EXECUTION_PLAN.md](SIX_MONTH_EXECUTION_PLAN.md) | 工作包、逐月/逐周安排、依赖、产物、验收与前两周清单 |
| [SOURCE_AND_GAP_AUDIT.md](SOURCE_AND_GAP_AUDIT.md) | 两稿逐页证据、已有verdict继承、最近邻反证、访问深度和claim账本 |
| [SII2027_MANUSCRIPT_REWRITE.md](SII2027_MANUSCRIPT_REWRITE.md) | 可直接编辑的章节重写、英文摘要/引言/方法段落、图表和证据槽位 |
| [THIRD_PAPER_MINIMUM_PROTOCOL.md](THIRD_PAPER_MINIMUM_PROTOCOL.md) | v0.2最小协议：任务、Q/T/C对照、患者等权风险、校准与同预算恢复实验 |
| [FIRST_FOUR_WEEKS_EXECUTION.md](FIRST_FOUR_WEEKS_EXECUTION.md) | 10月5日至11月1日逐工作日任务、记录字段、配置草稿和复盘分支 |

**共同主线：** human neuromusculoskeletal system → 任务导向sensing → 可辨识modeling → 经外部反馈检验的control/interaction。半年工作主要建立运动状态和可靠性组件；NMS参数与物理具身交互在具备独立EMG/机械参考后推进。IMU、UWB、视觉等均为可选观测，本次不自动沿用此前UWB主工具路线。

已复用 [$nms-digital-twin-phd-proposal](https://github.com/InchengWang/nms-digital-twin-skills/blob/main/nms-digital-twin-phd-proposal/SKILL.md) 及其proposal结构/实验清单。已有gap主要为partially-addressed；本次补查到2026-10-05，精确联合条件仍需随实际完成实验复查，不声称“首次”或全球空白。

资料限制：已阅读两份上传PDF，没有源代码/原始数据/模型日志；未复现稿件结果，没有认定已经发生数据泄漏；未确认BSN发表状态或新增设备/伦理/患者资源。所有新性能、控制和临床结果均未开展。SII摘要方括号是待补结果，不能直接投稿。

建议阅读顺序：SII修改方案 → 半年执行 → 第三篇 → 博士计划；所有novelty判断回到来源账本核对。

续编说明（2026-10-05）：新增三个执行文档；第三篇与博士计划同步区分“任务层评分改变风险排序”和“区间校准改善包含率”。统一正数缩放不改变排序；全拒答患者风险不能置0；离线曲线目标80%与实际部署阈值分开。原始数据、模型重跑和新增采集仍未开展，方法模板中的待核验项不能直接投稿。
