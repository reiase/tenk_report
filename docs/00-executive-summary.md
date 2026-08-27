---
title: 执行摘要
---

# 执行摘要

## 项目概况

本项目建设并验证总规模 **10,240 张国产加速卡**的大模型训练基础设施，其中华为 Atlas 900 A3 资源池 8,192 张、沐曦曦云 C550 资源池 2,048 张。系统采用统一控制面和独立训练数据面：资源、健康状态、实验编号和指标体系统一管理，两类硬件分别完成软件适配、通信优化和性能基线建设。

协同训练采用 4 个 A3 训练组、4 个 C550 训练组和 64 个参数服务器。每个训练组在独立 Megatron 与集合通信域内运行，参数服务器按配置周期完成跨组同步，由此兼顾异构硬件适配效率与万卡资源协同管理。

## 核心结论

- **规模化能力**：Qwen3-200B 在 1,024→4,096 卡弱扩展实验中取得 **94.26%** 扩展效率，4,096 卡每卡吞吐为 102.3286 TFLOPS。
- **并行策略**：2,048 die 的七点网格中，TP2/PP16/uniform1 取得最高 MFU **33.4%**，表明中等张量并行与流水线深度的组合更有利于计算、通信和流水线气泡平衡。
- **Dense 方案复核**：4,096 卡 TP2/PP16/DP128/VPP2/uniform1 在 iteration 6--30 达到 **124.264 TFLOPS/GPU**，变异系数 1.68%，较对照 TP8/PP8 方案提升 11.18%。
- **超大规模启动**：8,192 卡训练通过关闭分布式优化器 Gloo 全互连组完成通信建组并进入 iteration 7，验证了目标规模的启动路径。
- **协同验收**：8 个训练组在 47,436 秒共同窗口内取得 **92.43%** 加权 ECP 保留率，反映两类资源池相对各自基线的协同运行水平。
- **模型承载**：201.42B Dense 在 1,024 die 完成 800/800 step，1,099.55B MoE 在 2,048 die 完成 500/500 step；1T MoE 在 1,024/2,048/4,096 卡的 last5 吞吐为 65.60/61.82/57.66 TFLOPS/GPU。
- **健康准入**：A3 完成两个 4,096 卡批次及 96 张备机筛查；C550 完成 292 节点、2,336 卡全量筛查，并从中形成 256 节点、2,048-rank Final256 训练拓扑。
- **稳定性治理**：A3 前向进展 Stall 定位到 IPVS `estimation_timer` 长时间占用软中断并阻塞 NPU CQ tasklet；C550 前向进展事件集中在 200--272 ms，形成 direct dispatch 优化方向。
- **运行效率**：64 节点、1,024-rank 健康检查完整流水线由 1,706 秒缩短至 1,056 秒，墙钟时间下降 650 秒。
- **资产可恢复性**：工程快照完成 10/10 个 tar、6/6 个 Git bundle 和 75/75 项 SHA256 校验，形成训练配置、脚本与分析资产的完整索引。

![关键训练性能结果](assets/diagrams/training-performance-overview.svg){ .technical-diagram loading=lazy }

## 关键指标

### 资源与健康准入

| 指标 | 结果 | 实验 |
| --- | ---: | --- |
| 纳管加速卡规模 | 10,240 张 | 项目资源基线 |
| A3 资源池 | 8,192 张，占 80% | 项目资源基线 |
| C550 资源池 | 2,048 张，占 20% | 项目资源基线 |
| A3 首批 4,096 卡筛查 | 4,093 GOOD / 2 BAD / 1 CONTENDED | [EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) |
| A3 第二批 4,096 卡筛查 | 4,093 GOOD / 0 BAD / 3 CONTENDED | [EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) |
| C550 候选池筛查 | 2,336 卡，覆盖 292 节点 | [EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) |
| C550 训练拓扑 | Final256，2,048 ranks PASS | [EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) |

### 训练与扩展

| 指标 | 结果 | 统计口径 | 实验 |
| --- | ---: | --- | --- |
| A3 1,024→4,096 卡弱扩展效率 | **94.26%** | Qwen3-200B，iteration 6--12 | [EXP-003](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md) |
| A3 2,048 die 最佳 MFU | **33.4%** | TP2/PP16/GBS8192/VPP2/uniform1 | [EXP-006](https://github.com/reiase/tenk_report/blob/master/experiments/exp-006-a3-2048die-parallelism-mfu/README.md) |
| A3 4,096 卡 Dense | **124.264 TFLOPS/GPU** | iteration 6--30，CV 1.68% | [EXP-012](https://github.com/reiase/tenk_report/blob/master/experiments/exp-012-a3-4096-tp2pp16-dense/README.md) |
| 1T MoE 短程吞吐 | **65.60 / 61.82 / 57.66 TFLOPS/GPU** | 1,024/2,048/4,096 卡 last5 | [EXP-013](https://github.com/reiase/tenk_report/blob/master/experiments/exp-013-a3-qwen3-1t-moe-tuning/README.md) |
| 万卡协同加权 ECP | **92.43%** | 8 组共同 47,436 秒窗口 | [EXP-004](https://github.com/reiase/tenk_report/blob/master/experiments/exp-004-tenk-weighted-acceptance/README.md) |
| A3 最大启动规模 | 8,192 卡 | 完成建组并进入 iteration 7 | [EXP-005](https://github.com/reiase/tenk_report/blob/master/experiments/exp-005-a3-8192-startup/README.md) |

### 稳定性与工程效率

| 指标 | 结果 | 实验 |
| --- | ---: | --- |
| A3 Stall 事件分布 | gap P50/P90 = 504/697 ms | [EXP-007](https://github.com/reiase/tenk_report/blob/master/experiments/exp-007-a3-forward-progress-stall/README.md) |
| C550 Stall 事件分布 | P50/max = 212.6/272.3 ms | [EXP-008](https://github.com/reiase/tenk_report/blob/master/experiments/exp-008-c550-stall-and-communication-tail/README.md) |
| 健康检查墙钟 | 1,706→1,056 秒 | [EXP-011](https://github.com/reiase/tenk_report/blob/master/experiments/exp-011-healthcheck-runtime-optimization/README.md) |
| 200B Dense 功能运行 | 1,024 die，800/800 step | [EXP-009](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) |
| 1T MoE 功能运行 | 2,048 die，500/500 step | [EXP-009](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) |
| 工程快照校验 | 10 tar / 6 bundle / 75 SHA256 全部通过 | [EXP-014](https://github.com/reiase/tenk_report/blob/master/experiments/exp-014-training-assets-backup/README.md) |

## 工程价值

项目形成了从资源准入、拓扑编排、并行配置搜索、短程性能验证到稳定性诊断的完整工程链路。A3 与 C550 按各自硬件特征建立基线，统一控制面负责资源状态、实验元数据和协同指标，既保持了单平台优化的准确性，也支撑了万卡规模的统一交付管理。

全部核心指标按实验规模、模型配置和统计窗口登记。弱扩展、加权 ECP、MFU、功能运行、训练拓扑与启动验证分别服务于不同验收环节，共同构成项目技术能力评价体系。
