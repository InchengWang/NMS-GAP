# 公开外部数据候选核验（2026-10-24）

本批只核验公开论文、官方仓库、两个小样本，不训练模型，不读取既有外层评价预测，不联系作者。已排除 WMCG、Dorschky、已开发的 BLISS 作为“新候选”。当前未发现同时满足**公开卒中＋真实双小腿 ACC/GYRO＋独立光学标签＋真实重戴**的替代集。

| 候选 | 实际输入与光学来源 | 公开范围／下载 | 当前决定 |
|---|---|---|---|
| Grouvel／KINEMAGICS 2023 | Physilog6S 8 个，含 LS、RS；独立 Qualisys marker，未发现现成六角 | 10 健康，CC BY 4.0，公开 ZIP 可匿名 Range；4 个成员 CRC 已核 | 后备；先解决约 0.1 s 同步精度与独立标签定义 |
| Kiel Full-body mobility 2022 | 15–16 Noraxon IMU，含双 shank；独立 Qualisys marker；起始 TTL | 21 健康公开；作者 GitHub 有最初 10 人 MAT，可逐文件下载 | 比 Grouvel 更适合下一轮 schema/同步核验；不是公开卒中，也没有现成六角 |
| GAITEX | 9 Xsens，包含双小腿；光学 marker 独立，但发布的 IK 是 IMU 驱动 | 19 健康、模拟限制步态；Zenodo CC BY 4.0，单个 17.66 GB ZIP | 暂不进入 12D 任务：真实 ACC/GYRO 列未核实，不能用其 IMU-IK 作独立 GT |
| Twente／Simonetti 10787523 | sacrum、双足、患侧 thigh/tibia，共 5 IMU，缺健侧 shank | 4 男性卒中，元数据和文件列表可公开读取 | 不满足双小腿；不能补零、复制患侧或用 mocap 生成第二个“真实”IMU |

## Grouvel：已经到实际列级

官方 [数据仓库](https://yareta.unige.ch/archives/e72b9ec2-d097-45ac-8126-d04035407f51) 标为 PUBLIC、CC BY 4.0、774 研究文件。公开下载实际为 2,760,098,341 字节 ZIP，中央目录有 775 个 entry。仅通过有界 Range 读取目录以及两个 Excel、P01 的静态与常速 CSV；四个成员长度及 ZIP CRC 全部通过。未声称整包 SHA/完整性已验证。

P01 `Gait_01.csv` 为 405×279，`Static_01.csv` 为 50×279。279 列是 231 个 optical 坐标列与 48 个实测 IMU 列，没有 timestamp 或关节角列。与论文 100 Hz 说明对应，常速示例约 4.05 s，不能直接套用 WMCG 的单段 6 s 适配预算。左小腿输入列为 `P6_LS_acc_{x,y,z}`、`P6_LS_gyro_{x,y,z}`，右小腿为 `P6_RS_*`，不能按其他数据集的数字传感器编号猜测。

Excel 明确 LS=left shank、RS=right shank，原生 ACC 为 g、GYRO 为 deg/s、均 256 Hz；SYNC CSV 已重采样至 100 Hz。P01 小样本双侧均有限，无近 ±16 g 固定轴；静态 ACC 范数中位数左 1.0001 g、右 1.0058 g。这里只说明选定样本量级合理，不能推广为全队列质控通过。

独立 [原始论文](https://doi.org/10.1038/s41597-023-02077-3) 的重要限制是：无硬件同步，使用前后冲击及人工检测，作者估计精度约 0.1 s，并建议应用者从 raw 数据重同步。每人只采一场 session，不能作为真实重戴证据。P05 缺的是 LT（左大腿），并非 LS；不能因此无条件剔除其双小腿输入，但若标签依赖该 IMU 又会产生不同任务。

可执行路线：先从同一开发者的 RAW bin 与 optical 冲击记录复核时间偏移／漂移，再依据独立 optical markers 建立并冻结标签。若选择 marker 几何代理或自行做 optical IK，须明确这是新标签任务，不能沿用 Stroke 的工程角或 WMCG 六角名称。不得逐试次用目标关节角优化 lag，再将该结果称作未见评价。

## Kiel：真实双侧输入已确认，公开病人范围常被误读

[论文](https://doi.org/10.3390/data7100136) 的总队列是 167 人，包含 23 stroke；公开 [Figshare v2](https://doi.org/10.6084/m9.figshare.20238006.v2) 只包含 21 健康者。病人需联系作者并签协议，本项目不走该路线。作者的 [早期 GitHub](https://github.com/neurogeriatricskiel/Validation-dataset) 提供前 10 名健康者，一些大文件缺失。

已匿名下载 pp001 的 preferred 步态一对文件：IMU 899,638 字节、optical 2,515,028 字节。二者均 1,789 帧、200 Hz；实测 ACC/GYRO 为 1,789×3×16，左右 shank 的 `imu_location` 索引（0 起）为 8／11。光学为 1,789×4×51，含双侧 shank/thigh rigid clusters，与 IMU 来源分开；并无现成关节角数组。双侧 ACC 范数中位数约 1.015／1.024 g。全部 marker XYZ 有限比例约 94.97%，后续需逐必要 marker 核验，不能把 missing 标记填零。

作者说明两系统以起始 TTL 同步；仍需检查采样频率、support、marker 缺失和长段漂移。静态标定文件决定 cluster 到解剖轴的映射，当前仅有一个动态样本，尚不能冻结解剖六角任务。没有健康者重新佩戴记录的证据。

协议 Figure 1 给出器件安装朝向；静态 neutral-pose calibration 可建立技术坐标到解剖坐标的关系。本次下载的是发布的 `acc`、`gyro` 分量，没有实施 segment 注册／功能校准。不能把姿态图当成每位受试者精确的 sensor-to-segment 矩阵。输入若转 SI，仅 g×9.80665、deg/s×π/180；光学坐标 mm×0.001。传感器三个分量名不等于三个解剖平面。

补取 pp001 的 `omc_calibration_4.mat`（4,944,137 字节，Git blob SHA1 与目录一致），确认静态有双侧 `st_fem`／`st_fel`（膝内／外髁）、`st_mm`／`ank`（踝内／外踝）及 `th1–4`、`sk1–4`。可在静态定义膝轴／膝中心并注册到大腿、小腿 cluster，再在动态刚体追踪，构建独立 optical 双膝 proxy。仍须冻结角度定义、零点、符号、轴和平面，检查至少三点非共线及刚体残差。这个静态文件仅用来核验可用 marker；动态 `calibration_file` 是 MATLAB MCOS string，本次 scipy 尚未成功解析，故**没有认定 calibration_4 就是 preferred 的对应标定**。

动态样本的右大腿 marker 缺失不可忽略。双侧每个 cluster 至少三点同时有限的帧占 78.87%，最长连续 3.22 s；左侧单独为 8.945 s。此处还未检查几何残差，因此不能当作标签合格率。不能插值跨缺失段以凑 6 s 适配或 20 s 评价。

早期 GitHub 文件树核到 pp001–pp010 各 **1 对 `walk_preferred`**；另外 `gait1`／`gait2` 是 SPPB 两次 4 m，`chairrise_preferred` 是起坐，不是相同的常速步态重复。Figshare 21 人的逐人试次数仍未核实（当前是七个大 RAR，未下载整包）。协议中“位移后重复静态标定”不能自动视为真实重戴标签。

许可存在来源差异：当前 Figshare v2 API 是 CC BY 4.0，论文写 Dataset License CC BY-NC-SA，旧 GitHub 是 GPL-3.0。现阶段保留各来源证据，不替数据发布者消解冲突；后续最好使用 Figshare 原文件并保留其许可、记录和引用。当前 sample 来自旧 GitHub，只作为本地 schema 开发证据，不向 GitHub 项目重发原始数据。

后续路线是固定 [Figshare v2 API](https://api.figshare.com/v2/articles/20238006/versions/2) 的文件、MD5、许可快照，在本地按该 release 声明准备 intake，明确许可来源差异尚待释义，不联系作者、不混并旧 GitHub 文件到正式 release。这是 Dorschky 双膝探索之后的独立第三源候选，本轮不切换数据源或开始训练。

## GAITEX 与卒中候选：避免输入／标签来源混淆

[GAITEX 官方数据](https://zenodo.org/records/15729056) 为 19 名健康成年人，所谓 impaired gait 来自限制／模拟，不是卒中。官方 [处理代码](https://github.com/ai-for-sensor-data-analytics-ulm/aisd_ortho_ki_dataset/blob/main/processing/imu_inverse_kinematics.py) 实际加载 `xsens_imu_data_*.csv` 的 quaternion，随后调用 `IMUInverseKinematicsTool`。因此其发布 IK 不能当作与实测 IMU 独立的 optical 标签。论文还指出右小腿 heading 参照异常，processed orientation 才做补偿。本次 API 元数据成功，匿名有界 ZIP Range 两个官方 URL 均返回 HTTP 403；没有取得 raw CSV 头，故 ACC/GYRO 的存在标为**未确认**，不写成已经证实不存在。

[Twente 官方记录](https://zenodo.org/records/10787523) 与 [机构传感器说明](https://research.utwente.nl/en/datasets/kinematics-kinetic-and-emg-dataset-of-overground-locomotion-with-/) 明确只有患侧 tibia IMU。已有 reference optical IK 也不能补足缺失的健侧实测输入。当前 Zenodo API 未给出显式 `metadata.license`，复用许可也尚未确认。

本批证据目录包含本地论文和小样本，不是可整体发布物。适宜发布的是本简报、候选 JSON、校验摘要与代码；不上传论文全文、原始 IMU/marker 数据。候选状态全部是 intake/development，不等于 data-ready。

本简报只描述候选接入状态；本轮Dorschky独立任务见[实验报告](SII2027_DORSCHKY_EXTERNAL_20261024_ZH.md)。
