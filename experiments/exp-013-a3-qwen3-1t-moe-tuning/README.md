# EXP-013：A3 Qwen3-1T MoE 1024--4096 卡调优

## 目的

把 Qwen3-1T MoE 从 1024 卡到 4096 卡的短程性能、扩展趋势、有效优化和失败边界固化为独立证据，避免继续把早期 Qwen3-235B 试跑、1T 功能运行截图和 1T 性能调优混在一起。

## 来源与证据等级

| 来源 | 用途 |
| --- | --- |
| [S017](../../references/project-sources.md#s017) | 实际运行配置、日志聚合、失败栈、代码版本和备份核验 |
| [S008](../../references/project-sources.md#s008) | 1,099.55B 模型身份与 2,048 die、500 step 功能运行交叉检查 |

可入库聚合见 [summary.tsv](summary.tsv)。S017 包含远端日志检查和统计输出，但逐 rank 原始日志不在 Git 中，因此结果标为 `session_log_aggregate`。会话前半段的 Qwen3-235B/A22B 试验不进入本实验数值，只有明确替换为 `Qwen3_1TB_moe` 且参数量核验约 1,099.55B 的运行才计入。

## 主配置

三个规模采用同一方案族：TP1/PP16/EP16、MBS1、每 DP 副本 64 个 microbatch、block 重计算 7 层、gradient overlap 开启、parameter gather overlap 关闭、DDP bucket 256M、FP32 主梯度、optimizer CPU offload fraction 1.0。GBS 与 DP 随规模同比放大：

| 规模 | DP | GBS | 4096 卡建组修正 | last5 TFLOPS/GPU | last10 TFLOPS/GPU |
| ---: | ---: | ---: | --- | ---: | ---: |
| 1,024 卡 | 64 | 4,096 | 不需要 | **65.60** | 65.30 |
| 2,048 卡 | 128 | 8,192 | 不需要 | **61.82** | 57.43 |
| 4,096 卡 | 256 | 16,384 | `--disable-gloo-group` | **57.66** | 57.47 |

按 last5 计算，1024→2048 的单卡保留率为 94.24%，1024→4096 为 **87.90%**，2048→4096 为 93.27%。2048 卡 last5 与 last10 差异较大，说明点估计对窗口敏感；三条曲线都需要更长窗口和重复 placement 后才能升级为正式扩展效率。

MoE 与 Dense 的 TFLOPS/MFU 不直接横向排名。当前 FLOPs 公式按每个 token 实际选择的 Top-8 experts 计入主要计算，却没有把 router、token permutation、padding、All-to-All 和 CPU offload 全部计入分子；这些开销仍进入步时。1T 总参数约 1,099.55B，最重 shard 约 69.267B，也使优化器和主机传输成本显著高于稠密工作负载。

## 1024 卡消融

同区间 iteration 3--22 中，clean baseline 为 62.400 TFLOPS/GPU，关闭 parameter gather overlap 后为 64.065，提升约 2.67%；增加 CPU optimizer D2H/CPU update/H2D overlap 后只有 60.455，相对 no-param 低约 5.63%，且后段波动更大。

在 no-param 基线上将 DDP bucket 从 1.024B 降到 256M，iteration 3--16 从 64.164 提高到 64.629 TFLOPS/GPU，观察提升 0.72%，CV 从 4.51% 降到 3.06%。幅度较小，但 256M 随后被保留为扩展配置。EP32 短程约 57.9 TFLOPS/GPU，低于 EP16 的约 64.1；当前证据不支持扩大 EP 作为默认方向。

早期基础脚本在第 5--6 步固定开启 profiler，导致多组 step 6 同时变慢。后续 clean/no-param/bucket 主比较均删除 profiler 参数；含固定 profiler 的 step 6 不进入性能归因。

## 失败与边界矩阵

| 方向 | 结果 | 归因边界 |
| --- | --- | --- |
| EP8 | 首次 DDP buffer 申请 15.75 GiB 时 OOM | 显存硬边界，不是性能结论 |
| EP32 | 可运行但短程吞吐下降 | 只形成方向性淘汰，缺重复轮 |
| recompute 7→6 | FlashAttention/后续内存申请 OOM | 当前内存条件下不可用 |
| BF16 main grad + BF16 reduce | MoE 融合反向调用 `npu_groupmatmul_add_fp32` 时 dtype 不兼容 | 当前 MindSpeed 实现限制，不外推到其他版本 |
| CPU optimizer overlap | 完成训练但平均性能与稳定性更差 | 该开关不作为当前默认值 |
| 4096 卡 bucket128 首次任务 | Gloo full-mesh 在 iteration 前失败 | 没有产生 128M 性能数据；后以 no-Gloo 重跑 |
| 4096 卡 bucket128 no-Gloo | last5 56.66 TFLOPS/GPU | 比 256M no-Gloo 低 1.73% |
| 4096 卡 bucket256 no-Gloo | last5 57.66 TFLOPS/GPU | 相比旧 256M 的 57.46 只高 0.35%，主要价值是启动稳定性 |
| 4096 卡 recompute4 | master Service DNS/rendezvous 超时，未进入训练 | 配置收益未知，不能记为 recompute4 失败 |

`--disable-gloo-group` 解决的是 4096 卡初始化路径：首个失败位于 Gloo full-mesh，后续 no-Gloo 任务完成 30 步。它没有显示出稳态吞吐收益，不能被描述为训练性能优化。

## 结论边界

- 主结果统一报告会话最终复核的 last5，并同时披露 last10；不同早期答复采用的 iteration 3--N 均值不与主表混用。
- 1024/2048/4096 卡均为 30 步级短程运行，没有检查点恢复、长稳、数据身份或收敛结论。
- 4096 卡 placement 分布跨多个 Pod-IP 网段，缺少 SuperPod ID；EP16 单节点内映射的判断还需用最终 rank-order 与物理拓扑快照复核。
- 当前 MFU 分子没有完整覆盖 MoE 路由、通信和 offload 成本，因此本实验以 TFLOPS/GPU、步时和样本吞吐为主，不把约 17% 的早期 MFU 估算作为主结论。
- 1T 原始日志已进入 AFS 全量备份范围，但对象存储迁移尚未完成；在恢复原始包前，本仓库不能独立重算所有窗口。
