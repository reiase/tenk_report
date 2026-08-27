---
title: 训练系统与并行策略
---

# 训练系统与并行策略

## 模型与工作负载

项目训练工作负载覆盖 Qwen3-200B Dense 与 Qwen3-1T MoE。Dense 主性能实验采用 sequence length 4096、MBS1，归档代码 commit 为 `54daa56ad07f86e510b8be9027fcdbd9957fc998`；MoE 主线围绕 TP1/PP16/EP16、optimizer CPU offload、重计算和专家通信开展扩展验证。

| 模型 | 参数量 | 代表规模 | 运行结果 | 主要评价指标 |
| --- | ---: | ---: | --- | --- |
| Qwen3-200B Dense | 201.42B（交付值） | 1,024--8,192 卡/die | 1,024 die 完成 800/800 step | TFLOPS/GPU、MFU、弱扩展效率 |
| Qwen3-1T MoE | 1,099.55B（交付值） | 1,024--4,096 卡/die | 2,048 die 完成 500/500 step | TFLOPS/GPU、专家通信、显存与稳定性 |

模型估算值分别为 200.75B 和 1,091.80B，与交付值相差约 0.33% 和 0.71%，验证了参数规模与配置设计的一致性。

## 并行策略

并行组合同时决定计算切分、显存占用、流水线气泡和通信组映射。A3 训练遵循“高频通信就近、跨域通信对称”的原则：TP 组优先位于同一逻辑超节点，PP 相邻 stage 减少跨域跳转，DP 组在超节点和出口网卡间均衡分布，MoE 的 EP 组与 All-to-All 路径按实际 rank order 固化。

| 维度 | 已验证范围 | 主要通信 | 选择因素 |
| --- | ---: | --- | --- |
| TP | 1 / 2 / 4 / 8 | AllReduce、AllGather、ReduceScatter | 算子效率、显存、高频通信距离 |
| PP | 8 / 16 / 32 / 64 | stage 间 Send/Recv | 模型切分、流水线气泡、激活传输 |
| DP | 16--256 | ReduceScatter、AllGather | 全局 batch、跨域带宽、优化器分片 |
| EP | 8 / 16 / 32 | All-to-All / All-to-AllV | 专家容量、负载均衡、显存与拓扑 |
| VPP | 2 / 4 | 虚拟 stage 调度 | 气泡比例、调度复杂度、阶段均衡 |

### 代表配置

| 实验 | 规模 | TP / PP / DP / VPP | GBS | 重计算 | 结果 |
| --- | ---: | --- | ---: | --- | --- |
| [EXP-001](https://github.com/reiase/tenk_report/blob/master/experiments/exp-001-a3-1024-tuning/README.md) | 1,024 卡 | TP1/PP64 或 TP8/PP8，DP16，VPP2 | 按用例固定 | block / uniform | mapping0 在五组配对中均取得更高吞吐 |
| [EXP-002](https://github.com/reiase/tenk_report/blob/master/experiments/exp-002-a3-4096-dp-communication/README.md) | 4,096 卡 | TP8/PP8/DP64 | 16,384 | 固定 | no-overlap 与 bucket-128m 进入候选配置 |
| [EXP-003](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md) | 1,024 / 4,096 卡 | TP1/PP64/DP16 或 64/VPP2 | 4,096 / 16,384 | block1 | 弱扩展效率 94.26% |
| [EXP-005](https://github.com/reiase/tenk_report/blob/master/experiments/exp-005-a3-8192-startup/README.md) | 8,192 卡 | TP2/PP16/DP256/VPP2 | 32,768 | uniform1 | 完成通信建组并进入 iteration 7 |
| [EXP-006](https://github.com/reiase/tenk_report/blob/master/experiments/exp-006-a3-2048die-parallelism-mfu/README.md) | 2,048 die | TP1--8 / PP8--64 / VPP2 | 8,192 | uniform1 / block1 | TP2/PP16/uniform1 达到 MFU 33.4% |
| [EXP-012](https://github.com/reiase/tenk_report/blob/master/experiments/exp-012-a3-4096-tp2pp16-dense/README.md) | 4,096 卡 | TP2/PP16/DP128/VPP2 | 16,384 | uniform1 | 124.264 TFLOPS/GPU，CV 1.68% |
| [EXP-013](https://github.com/reiase/tenk_report/blob/master/experiments/exp-013-a3-qwen3-1t-moe-tuning/README.md) | 1,024 / 2,048 / 4,096 卡 | TP1/PP16/EP16，DP64/128/256 | 4,096 / 8,192 / 16,384 | block7 | last5 为 65.60/61.82/57.66 TFLOPS/GPU |

## 协同训练编排

万卡协同运行由 4 个 A3 训练组、4 个 C550 训练组和 64 个参数服务器构成。每个 A3 组使用 2,048 张卡，每个 C550 组使用 512 张卡；训练组内部维护独立 Megatron 并行域，参数服务器按配置周期完成跨组模型状态同步。

该组织方式将异构适配限定在资源池内部，并在协同层统一管理作业进度和加权 ECP。容量规划按每参数约 14 bytes 估算完整训练状态：200B 模型约 2.8 TB/份，1T 模型约 14 TB/份；保留 25 份时分别预留约 70 TB 与 350 TB。

## TP、PP、GBS 与重计算联合优化

2,048 die、Qwen3-200B、GBS8192、MBS1、VPP2 的七点网格显示，TP2/PP16/uniform1 取得最高 MFU 33.4%。在 TP×PP=64 的 uniform1 子集中，TP2/PP32 为 30.4%，TP4/PP16 为 29.8%，TP1/PP64 为 26.7%，TP8/PP8 为 24.1%。

结果表明：

- TP 增大后，小消息 AllReduce 固定时延和同步开销更容易暴露。
- PP 过深会增加流水线气泡、虚拟 stage 调度和相邻 stage 激活传输。
- TP×PP 从 64 降至 32 后，DP 副本增加，需要同步评估 DP 通信与全局 batch。
- GBS 从 1,024 增至 8,192 时，TP8/PP8/VPP4 的 MFU 由约 20.7% 提升至约 24.1%。
- block1 在 PP8 与 PP64 下分别重计算 8 层和 64 层，实际重计算层数是解释收益的关键变量。

配置搜索采用“容量可行 → 数值正确 → 稳态性能 → 跨 rank 方差 → 扩展稳定性”的顺序。候选配置同时检查 pipeline bubble、暴露通信、小消息 collective、ReduceScatter 尾部和物理 placement。

## 显存与精度优化

Dense 实验覆盖 block/uniform 激活重计算、DDP bucket 和通信重叠；1T MoE 主线进一步使用 optimizer CPU offload fraction 1.0。

1,024 卡 MoE 消融结果显示：

| 配置变化 | TFLOPS/GPU | 相对变化 |
| --- | ---: | ---: |
| clean baseline | 62.400 | 基线 |
| 关闭 parameter gather overlap | 64.065 | +2.67% |
| 增加 CPU optimizer overlap | 60.455 | -5.63% |
| bucket 1.024B→256M | 在 no-param 基础上 +0.72% | 小幅提升 |

扩展到 4,096 卡后，256M bucket 的 last5 为 57.66 TFLOPS/GPU，128M 为 56.66 TFLOPS/GPU。EP8/recompute6 触发 OOM，FP32 main grad 与当前融合反向路径形成稳定运行组合。上述结果将显存、通信和算子契约纳入同一配置决策。

## 训练坐标与性能诊断

每条训练与通信记录使用 `global_step`、`micro_step`、`rank`、`world_size` 以及 TP/PP/DP/EP/CP 角色建立统一坐标。logical step 从首次 forward 开始，到 optimizer 完成结束；forward、backward 和 optimizer 由单一状态所有者标记。

性能诊断采用渐进式流程：

`step 墙钟与资源趋势 → 异常 step/rank/角色 → module/collective 采样 → op/kernel/stack 短窗口 → 通信库事件与网络计数器`

常驻层用于发现偏离，采样层用于识别计算或通信方向，深度层用于解释具体调用路径。确定性采样通过 step 与 layer 稳定键保持跨 rank 对齐，使少量样本仍能恢复完整阶段关系。

## 作业生命周期

![训练作业调度与控制时序](assets/diagrams/scheduling-control-sequence.svg){ .technical-diagram loading=lazy }

训练作业按以下顺序推进：

1. 资源申请与物理拓扑快照。
2. 静态一致性与单节点动态检查。
3. 单卡计算、HBM 与 SDC 测试。
4. 成对硬件和链路筛查。
5. 精确目标节点准入。
6. 实际 TP/PP/DP/EP 通信组验收。
7. Megatron 短程复现与检查点演练。
8. 目标规模训练、指标归档与故障闭环。

运行器采用准备、统一激活和结果回收三阶段协议。调度映射、rank 分组、运行条件和软件版本随实验固化；节点集合、镜像、驱动或通信库变更后，按影响范围重新执行健康与通信准入。

## 规模扩展路径

| 阶段 | 资源与通信准入 | Megatron 验证 | 输出 |
| --- | --- | --- | --- |
| 单节点 | 静态、设备与节点内互连 | loss、显存与吞吐基线 | 单节点性能包络 |
| 小规模多节点 | 成对通信与并行组正确性 | 检查点恢复与短程训练 | 可运行并行配置 |
| 中等规模 | 训练拓扑与性能候选复测 | 扩展效率、方差与稳定性 | 规模化候选方案 |
| 目标规模 | 全部真实子通信组 | 启动、稳态、长稳与恢复 | 生产运行基线 |

该路径把健康检查、训练拓扑和 Megatron 性能验证依次衔接，使资源质量、通信正确性和模型训练能力在同一配置版本上闭环。
