# BSN启发的稀疏到稠密分阶段运动重建

日期：2026-10-25。用户确认“BCN”指同一篇BSN稿，并授权探索网络；位置监督已明确批准先用关节相对位置作工程代理。新支线沿用当前题目，不覆盖旧ARCH79项、既有基线或答辩结果。

## 1. 输入、中间量和输出

部署输入保持S1左小腿＋S2右小腿真实ACC/GYRO十二维；重力与native sensor轴保持。第一阶段重建S3腰、S4左足、S5右足真实六轴信号共18维，同时重建8个下肢关节/足部关键点相对双髋中点的位置共24维，单位m。第二阶段从**预测**中间量估计既有6个工程运动角。

位置定义：`r_j(t)=(p_j(t)−(p_Lhip(t)+p_Rhip(t))/2)/1000`。原位置为mm，此处变为m；仍保留原工程骨盆轴方向。它不是IMU硬件中心位置，不补造安装杆臂。S6拐杖不纳入身体重建目标。

BSN原思路是从真实足部信号重建真实小腿信号；本支线借鉴稀疏到稠密监督思想，输入仍是当前双小腿，故不称BSN原文整套复现。既有[来源审阅](https://github.com/InchengWang/NMS-GAP/blob/main/Digital%20Twin/halfyeat/SOURCE_AND_GAP_AUDIT.md)保留历史。相对位置作为运动中间表示亦有[TransPose，ACM TOG/SIGGRAPH2021](https://xinyu-yi.github.io/TransPose/)先例；其6IMU姿态/加速度和全身任务不同，本支线不是TransPose复现。

## 2. 数据新增监督

S3/S4全部53条可用。S5存在原文件缺模态：P6缺ACC，P17缺GYRO；TRAIN可用数量分别28/31、29/31。保留全部既有parent，以逐模态/通道mask屏蔽缺失监督，0仅为存储占位，不是零真值。mask只进loss，部署输入不增加mask、其他IMU或mocap。

继承原`input_epoch_ms`与`optic_absolute_time`，不重新找lag/轴/符号。共享raw CSV需要先解析时间，再只解码TRAIN插值括号行；全文件SHA机械读取与动态值解析分别记账。现有时钟/配对来自既往离线修复，仍不是独立硬件精密同步证明。

## 3. 五个受控网络

共同TCN64编码器采用3残差块、两次kernel7卷积/块、dilation1/2/4，RF85；运动解码器是逐帧MLP，不额外扩展时域。GRU可作后续候选，首个真实开发pilot仅跑TCN。

| 模式 | 运动路径 | 研究问题 |
|---|---|---|
| direct | x→encoder→MLP→angles | 同类直接预测参考 |
| auxiliary_only | 同direct，同时监督signal/position heads | 额外监督本身是否有益 |
| latent_bottleneck | x→encoder→无语义42D latent→MLP→angles | 同维度瓶颈控制；latent不叫真实传感器/位置 |
| strict_staged | x→encoder→预测signal18＋position24→MLP→angles | 显式重建监督与严格瓶颈的作用 |
| residual_staged | x→encoder→预测中间量，与观测x合并→MLP→angles | 瓶颈丢失的信息是否需要原观测补充 |

latent与strict网络、参数和初始化完全相同，区别仅中间监督。direct与aux运动路径相同，额外头的参数和监督成本另列；不把所有模式强称完全同参数。所有模式训练/推理都不向运动头喂真实中间量；GT只用于loss。仅有预测中间量的网络不创造新的独立测量，价值来自表示和训练约束。

## 4. 首个开发pilot的预定范围

仅31TRAIN固定共同crop[100:-100]、12665唯一帧；先完成新目标导出和独立复算。首批5个TCN模式，pooled TRAIN覆盖8位患者、单seed20261025、固定50epoch final；batch64、AdamW3e-4/wd1e-4、clip1、120帧窗/stride20＋tail，独立洗牌RNG。x/y与中间目标各用唯一允许TRAIN拟合统计量，signal统计只用有效mask；不从VALID/TEST补缺失通道统计。

角度、信号与位置损失分别均值，权重固定1/.25/.25；无中间监督的direct/latent两项权重为0。信号按6组(sensor×ACC/GYRO)有效元素归一化，再等有效组。该权重是本次工程先验，不是BSN/TransPose论文参数，尚未调优。

此pilot先检验数据和机制能否正常训练，不作为跨患者或临床结论。所有fit完成并经过训练检查后，才按另行冻结的开发分析协议解锁一次12个VALID trial；不据它选择或反复优化网络。TEST保持未新增读取。中间监督的额外sensor-seconds与光学位置参考必须列账，不能把staged与angle-only的差异全部算作网络结构增益。

后续若进行VALID诊断，同时报告六角/双膝/患膝、真实信号和位置误差，以及预测中间量置零/打乱的依赖检查。不能以oracle中间量的运动成绩冒充可部署模型；不能按这批开发结果升级为独立泛化证明。

## 5. 当前状态

本文件是数据producer与模型实现前的设计记录，尚非训练结果。实现、数据验收、训练和开发评价分别出具独立状态与源码SHA。旧论文不保真数字不作为目标。
