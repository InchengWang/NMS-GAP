# 独立公开卒中数据：10月26日有界补查

本次在baseline训练期间补查公开论文、官方数据记录和说明文档，不下载新的动态数组、不联系作者、不训练新队列。目标仍是实测双小腿ACC/GYRO与独立光学参考；未发现本轮可以直接接入该任务的新卒中数据。此结论限于本次检索，不表示不存在其他合适数据。

| 候选 | 本轮一手证据 | 对当前任务的决定 |
|---|---|---|
| REHAB，120名卒中患者 | 2026年数据论文描述患侧前臂/上臂/小腿/大腿/手部传感器，约50Hz；临床评分与动作类别是主要标签，Euler来自惯性姿态估计。 | 患侧单小腿不满足双侧实测输入；当前记录未提供可用于本任务的独立光学运动角。不能把120人写成现有六角外部验证。 |
| Therapist-exoskeleton-patient interaction，8名慢性卒中患者 | 2026年Dryad说明有双腿Delsys测量及外骨骼encoder；公开变量说明的imu.jointAngle由IMU得到。机器人encoder角只适用于相应穿戴条件。 | 不把IMU派生角当独立光学GT。README未列出可直接构造12D输入的raw ACC/GYRO；尚未下载20.82GB MAT，不能断言文件中不存在它们。当前不入组。 |
| Simonetti/Twente | 已有10月24日检查与官方记录均说明4位卒中、5枚IMU，健侧小腿未测。 | 不能用虚拟IMU或复制患侧补出第二枚“真实”小腿输入；维持原排除。 |

一手来源：[REHAB论文](https://www.nature.com/articles/s41597-026-07802-2)、[对应PMC全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC13443191/)、[REHAB数据DOI](https://doi.org/10.57760/sciencedb.37018)；[Dryad数据与完整README](https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvxd)；[Twente当前记录](https://zenodo.org/records/10787523)。官方论文或网页的“IMU”“kinematic dataset”字样不能替代输入列、安装部位与参考生成链核验。

REHAB和Dryad尚可服务各自的动作识别、临床评分或人机交互问题，但改变为这些任务属于新的研究范围。本项目仍使用既有卒中开发队列，加WMCG/Dorschky健康技术复核；不以健康样本补足卒中临床泛化证据，不以IMU自派生标签填补光学参考缺口。既有GAITEX/Kiel/Grouvel接入状态维持10月24日报告；本次未重复下载或升级为data-ready。

状态：新候选正式release 0；新增原始数据下载0；新增患者模型0；新增外部卒中性能结论0。后续若获得满足条件的公开记录，先核对schema、同步、单位、左右映射、标签独立性和角色划分，再另行固定外部协议。
