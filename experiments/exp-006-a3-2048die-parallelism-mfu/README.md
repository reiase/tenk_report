# EXP-006：A3 2048 die 并行策略与 MFU 分析

## 目的

导入《昇腾 910C 训练集群并行策略对 MFU 影响的技术分析报告》中的 TP/PP 趋势、GBS 与重计算消融、通信根因摘要和 2048 die 配置搜索结果，并明确该材料的证据范围。

## 来源与完整性

- 仓库附件：[ascend-910c-parallelism-mfu-analysis.pdf](../../references/ascend-910c-parallelism-mfu-analysis.pdf)
- PDF 创建时间：2026-08-17 12:53:23（文件元数据）
- PDF 页数：8
- PDF SHA256：`1afd922dfa074143ad093ed78d753be80b563d43686b5e07cd4f5d7c4ca42aaa`
- 结构化摘录：[summary.tsv](summary.tsv)

本记录属于**文档级证据导入**。PDF 提供聚合表、趋势图和 TensorBoard/Profiling 归因摘要；run ID、逐 iteration 数据、完整训练配置、软件版本、rank placement、MFU 公式和原始 profile 文件按来源材料管理。仓库用于核对来源报告内容、表内算术关系和可入库结构化摘录。

## 实验口径

PDF 包含三组不同口径，分别作为独立结果登记：

1. TP/PP 趋势实验：固定 PP=2 扫描 TP=1/2/4/8，或固定 TP=2 扫描 PP=1/2/4/8；进一步在 TP8 或 PP8 下扫描 world size=32/64/128/256。
2. GBS 与重计算归因：GBS A/B 使用 2048 die、TP8/PP8/VPP4；重计算表另含 TP1/PP64，但 PDF 没有单独注明该行 VPP。
3. 并行度网格搜索：2048 die、Qwen3-200B、GBS 8192、MBS 1、VPP2；比较七组 TP/PP/重计算组合。

原文以 `die` 报告硬件规模。本记录保留该单位；与 EXP-003 以“卡”为单位的弱扩展曲线分开管理。

## 主要结果

### TP/PP 与规模趋势

| 对比 | 原文报告的平均 MFU 变化率 |
| --- | ---: |
| PP=2，TP 从 1 扫描到 8 | 19.36% |
| TP=2，PP 从 1 扫描到 8 | 14.99% |
| TP8，world size 从 32 扫描到 256 | 17.17% |
| PP8，world size 从 32 扫描到 256 | 8.08% |

趋势图显示上述变化均以 MFU 下降为主，大 TP 组下降更明显。这里保留来源报告的“平均变化率”口径，统计显著性由后续带误差条和重复次数的实验承担。

### 2048 die 配置搜索

| TP | PP | 重计算 | TP×PP | MFU |
| ---: | ---: | --- | ---: | ---: |
| 1 | 64 | uniform1 | 64 | 26.7% |
| 2 | 32 | uniform1 | 64 | 30.4% |
| 4 | 16 | uniform1 | 64 | 29.8% |
| **2** | **16** | **uniform1** | **32** | **33.4%** |
| 4 | 8 | uniform1 | 32 | 31.3% |
| 8 | 8 | uniform1 | 64 | 24.1% |
| 8 | 8 | block1 | 64 | 28.1% |

在来源报告给定条件内，TP2/PP16/uniform1 的 33.4% 是七组中的最高值。对于 TP×PP=64 且 uniform1 的可比子集，TP2/PP32（30.4%）高于 TP4/PP16（29.8%）和 TP8/PP8（24.1%）；TP1/PP64（26.7%）也低于 TP2/PP32，说明两端过大的 TP 或 PP 都可能损失 MFU。这个排序只适用于该模型、GBS、VPP、显存与拓扑条件，不是通用最优配置。

### GBS 与重计算归因

- 在 TP8/PP8/VPP4、2048 die 下，仅将 GBS 从 1024 增至 8192，MFU 从约 20.7% 升至约 24.1%，增加 3.4 个百分点。
- GBS8192 从 1024 die 扩到 2048 die 后，MFU 从约 26% 降至约 24%，下降约 2 个百分点。
- TP8/PP8 从 uniform1 改为 block1 后，MFU 从 24.1% 升至 28.1%；TP1/PP64 对应从 26.7% 升至 27.0%。
- 原文解释 block1 在 PP8 下重计算 8 层、在 PP64 下重计算 64 层，而 uniform1 均重计算 128 层。因此两组 block1 的“策略名”相同但节省的重计算层数不同，+4.0 个百分点按并行度与实际重计算工作量的联合变化解释。

### 通信根因摘要

PDF 报告 TP8 在 Scaling 后的 forward-compute 耗时增长约 3.1 倍，对照 TP2/PP8 为约 1.83 倍；未重叠通信分别增长 120% 和 54%。其 Profiling 摘要进一步指出：大消息 AllReduce 基本不变，小消息 AllReduce 延迟增加约 4--19 倍；iteration 尾部 ReduceScatter 随 DP 扩大而增加，且 TP8 下增长更明显。

这些数据支持“大 TP 在该环境扩展后暴露更多通信时延”的工作假设。归因链后续与原始 TensorBoard、collective 明细和网络遥测对齐后，可升级为日志级诊断结论。

## 适用范围

- 33.4% 是 2048 die、Qwen3-200B、GBS8192、MBS1、VPP2 网格中的最佳已测点，适用于该模型和该配置族。
- GBS A/B 使用 VPP4，并行度网格使用 VPP2；TP1/PP64 重计算对比的 VPP 信息按来源报告记录。跨口径数字只用于趋势对照。
- MFU 理论峰值、模型 FLOPs 公式、精度口径与重计算计入口径按来源报告管理，与其他实验的 TFLOPS/卡分开解释。
- 点估计后续通过随机化重复、统计窗口、运行顺序和方差收据增强。
- 通信根因通过原始 profile、collective 消息大小、rank/拓扑映射和网络 counter 形成闭环诊断。
