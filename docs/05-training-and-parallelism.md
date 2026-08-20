---
title: 训练系统与并行策略
status: draft
owner: unassigned
reviewers: []
last_updated: 2026-08-20
---

# 训练系统与并行策略

## 模型与工作负载

当前主性能工作负载包括 Qwen3-200B Dense 与 Qwen3-1T MoE。Dense 使用 sequence length 4096、MBS1；已归档训练代码 commit 为 `54daa56ad07f86e510b8be9027fcdbd9957fc998`。EXP-001 至 EXP-006、EXP-012 和 EXP-013 均以短程性能或聚合 MFU 为主，不用于收敛结论。

[EXP-009](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) 新增两组功能运行证据：交付材料报告 201.42B Dense 在 1,024 die 完成 800/800 step，1,099.55B MoE 在 2,048 die 完成 500/500 step，并提供 loss 曲线截图。模型估算分别为 200.75B 与 1,091.80B，和交付值相差约 0.33% 与 0.71%。这些结果把 MoE/1T 从“没有运行证据”推进到“文档级功能运行”。[EXP-013](https://github.com/reiase/tenk_report/blob/master/experiments/exp-013-a3-qwen3-1t-moe-tuning/README.md) 又补充了 1024/2048/4096 卡短程性能和故障栈，但证据仍来自会话日志聚合，缺少仓库内逐 rank 原始日志、数据身份、检查点校验和收敛评估；它单列为 MoE 性能曲线，不与 Dense MFU 排名。

## 并行策略

并行策略不仅决定计算与显存切分，也决定 HCCL 通信组如何映射到 A3 的节点、逻辑超节点和跨超节点网络。A3 上的完整映射方法见 [A3 HCCL 通信优化与超节点亲和性调度](04a-a3-hccl-communication-optimization.md)：高频张量并行组优先保留在超节点内，跨超节点的数据并行组在各超节点和出口网卡之间对称分配。

| 维度 | 并行度 | 分组方式 | 主要通信 | 选择依据 |
| --- | ---: | --- | --- | --- |
| 数据并行 | 16 / 64 / 256 | 跨超节点时对称分布 | AllReduce / ReduceScatter / AllGather | 对应已导入的 1024 / 4096 / 8192 卡稠密实验 |
| 张量并行 | 1 / 2 / 8 | 优先位于同一逻辑超节点 | AllReduce / AllGather / ReduceScatter | 由显存、算子效率和高频通信距离共同决定 |
| 流水线并行 | 8 / 16 / 64 | 减少相邻 stage 跨域次数 | Send / Recv | 兼顾模型切分、bubble 与边界激活传输 |
| 专家并行 | 16（主线），8/32（消融） | 主线优先保持单节点 EP group，最终以 rank-order/placement 快照复核 | AlltoAll / AlltoAllV | EP8 OOM、EP32 短程回退；只适用于当前 1T MoE 代码与拓扑 |

### 已验证配置

| 实验 | 规模 | TP / PP / DP / VPP | GBS | 重计算 | 主要结论 |
| --- | ---: | --- | ---: | --- | --- |
| [EXP-001](https://github.com/reiase/tenk_report/blob/master/experiments/exp-001-a3-1024-tuning/README.md) | 1,024 | TP1/PP64 或 TP8/PP8，DP16，VPP2 | 按用例冻结 | block / uniform | mapping0 在五组配对中均更高；小于 1% 的差异待重复 |
| [EXP-002](https://github.com/reiase/tenk_report/blob/master/experiments/exp-002-a3-4096-dp-communication/README.md) | 4,096 | TP8/PP8/DP64 | 16,384 | 冻结 | no-overlap 与 bucket-128m 是复测候选 |
| [EXP-003](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md) | 1,024 / 4,096 | TP1/PP64/DP16 或 64/VPP2 | 4,096 / 16,384 | block1 | 7 步弱扩展效率 94.26% |
| [EXP-005](https://github.com/reiase/tenk_report/blob/master/experiments/exp-005-a3-8192-startup/README.md) | 8,192 | TP2/PP16/DP256/VPP2 | 32,768 | uniform1 | 无 Gloo 路径完成建组并进入 iteration 7 |
| [EXP-006](https://github.com/reiase/tenk_report/blob/master/experiments/exp-006-a3-2048die-parallelism-mfu/README.md) | 2,048 die | TP1--8 / PP8--64 / VPP2；另有 VPP4 消融 | 1,024 / 8,192 | uniform1 / block1 | 网格中 TP2/PP16/uniform1 的 MFU 最高，为 33.4%；文档级证据 |
| [EXP-012](https://github.com/reiase/tenk_report/blob/master/experiments/exp-012-a3-4096-tp2pp16-dense/README.md) | 4,096 | TP2/PP16/DP128/VPP2 | 16,384 | uniform1 | iteration 6--30 平均 124.264 TFLOPS/GPU；方案级优于已测 TP8/PP8 11.18% |
| [EXP-013](https://github.com/reiase/tenk_report/blob/master/experiments/exp-013-a3-qwen3-1t-moe-tuning/README.md) | 1,024 / 2,048 / 4,096 | TP1/PP16/EP16，DP64/128/256 | 4,096 / 8,192 / 16,384 | block7 | last5 为 65.60/61.82/57.66 TFLOPS/GPU；会话日志聚合 |

### 模型交付与混训编排

模型估算提出的 TP4/PP8/EP8、DP40 等 10,240 卡候选是容量规划，不是已验证的单一同步并行策略。实际协同运行由 4 个 A3 训练组和 4 个 C550 训练组组成：每个 A3 组 2,048 张卡，每个 C550 组 512 张卡，并通过 64 个参数服务器按不同周期同步。各组内部维护自己的 Megatron 与集合通信域，因此并行效率应按组和资源池分别测量；跨组只报告预注册的参数同步与加权验收指标。

估算文档按每参数 14 bytes 粗算完整训练状态：200B 约 2.8 TB/次、1T 约 14 TB/次，保留 25 份分别约 70 TB 与 350 TB。该口径假设 FP16/BF16 权重和 FP32 master/m/v，未包含文件系统冗余与实现元数据，只用于容量预留。

### 并行度、GBS 与重计算的联合选择

[EXP-006](https://github.com/reiase/tenk_report/blob/master/experiments/exp-006-a3-2048die-parallelism-mfu/README.md) 导入了 2048 die、Qwen3-200B、GBS8192、MBS1、VPP2 下的七组配置搜索。原文使用 `die` 作为规模单位，本文保留该单位，不将其自动换算为卡数。

完整七点结果表见[2048 die 并行度网格](08-results-and-analysis.md#2048-die-并行度网格)。

在该网格内，TP2/PP16/uniform1 是最佳已测点。TP×PP=64 且 uniform1 的子集中，TP2/PP32（30.4%）高于 TP4/PP16（29.8%）和 TP8/PP8（24.1%）；TP1/PP64（26.7%）也低于 TP2/PP32。这说明配置选择需要同时避免过深流水线和过大的张量并行通信域，但不能据此宣布 TP2/PP16 对其他规模、模型或拓扑普遍最优。

同一来源在 TP8/PP8/VPP4、2048 die 下报告，GBS 从 1024 增至 8192 时，MFU 从约 20.7% 升至约 24.1%。另一组重计算对比报告 TP8/PP8 从 24.1% 升至 28.1%、TP1/PP64 从 26.7% 升至 27.0%，但没有单独注明 TP1/PP64 的 VPP。block1 在 PP8 下重计算 8 层，在 PP64 下重计算 64 层，因此同名策略并不代表相同重计算量，+4.0 个百分点不能直接归因于 TP8。

并行配置搜索应先满足显存与数值正确性，再在相同 GBS、MBS、VPP、有效重计算层数、软件版本和 placement 下比较 TP/PP。最终候选还要同时检查 pipeline bubble、暴露通信、小消息 collective、ReduceScatter 尾部拥塞和跨 rank 方差，避免只按单点 MFU 排名。

## 内存与显存优化

已导入实验覆盖 block/uniform 激活重计算、DDP bucket、通信重叠和 optimizer CPU offload。Dense EXP-003/005 的 optimizer/activation offload 关闭；1T MoE 主线则使用 optimizer CPU offload fraction 1.0，不能跨模型把 offload 开关效果混算。

EXP-013 的同窗口 1024 卡消融显示：clean baseline 为 62.400 TFLOPS/GPU，关闭 parameter gather overlap 后为 64.065；再启用 CPU optimizer 传输/更新 overlap 只有 60.455，未形成收益。DDP bucket 从 1.024B 降到 256M 的观察提升仅 0.72%，随后被保留为扩展配置；4096 卡继续降到 128M 后反而比 256M no-Gloo 低 1.73%。EP8 和 recompute6 触及 OOM，BF16 main grad 与当前 MoE 融合反向算子不兼容。这些边界只适用于当前代码、参数切分和显存条件。

## 训练坐标与阶段边界

性能事实只有在训练坐标稳定时才能跨 rank 比较。每条 step、module 和通信记录至少携带 `global_step`、`micro_step`、`rank`、`world_size` 和并行角色；角色由 TP、PP、DP、EP、CP 等维度组成。Megatron 适配层只负责把版本敏感的并行状态转换为这些公共坐标，不应让系统、通信或 profiler 采集器直接依赖 Megatron 内部 getter。[I004](references.md#i004)

梯度累积场景必须区分 micro step 与 logical step。一个训练 step 的边界从本次 logical iteration 的首次 forward 开始，到 optimizer 完成结束；中间的多次 forward/backward 不应制造多个完整 step。forward、backward 和 optimizer 阶段还需要单一状态所有者：若训练代码已经显式标记阶段，自动 hook 只补充 module 事实，不重复创建同名区间。否则同一段时间会被重复计算，通信暴露比例和阶段占用可能超过 100%。

## 渐进式性能诊断

训练性能定位采用由低成本到高密度的递进过程：

```text
持续 step 墙钟与资源趋势
  -> 找到异常 step、rank 和并行角色
  -> module/collective 采样确定计算或通信方向
  -> 对少量 rank 和窄时间窗采集 op、kernel 或调用栈
  -> 用通信库原生事件与 NIC counter 完成链路归因
```

常驻观测只回答“何时、哪些 rank、哪个阶段偏离”；短窗口 profiler 回答“哪些 op/kernel/调用路径构成偏离”；HCCL/NCCL 等原生数据回答“通信库内部如何展开”。三层拥有不同计时边界，不能相互替代。尤其是 Python collective API 耗时不等于设备侧通信完成时间，module duration 的重叠区间也不能直接相加为 step wall time。

确定性采样使用 step 序号和 layer 标识决定命中，使各 rank 在同一批 step 上保留可比较证据。优先采集少量 step 的完整层关系，而不是每个 step 随机留下互不相连的少量层；后者虽然事件数相同，却难以恢复层间关键路径。

## 调度与作业生命周期

训练作业生命周期将健康准入作为显式 gate：

调度器在健康准入通过后执行超节点选择和出口网卡负载均衡。必须保存调度映射、Megatron rank 组、HCCL 通信拓扑及其完整性摘要。故障重调度后若节点或超节点集合变化，应生成新的映射版本并重新运行通信准入，不能沿用原性能基线。

```text
资源申请与拓扑快照
  -> 执行前核对实例数、节点映射、rank 和运行条件
  -> 静态一致性检查
  -> 单节点动态检查
  -> 单卡计算与存储可靠性测试
  -> 成对硬件与链路筛查
  -> 精确目标节点准入
  -> 训练通信组验收
  -> Megatron 短程训练复现
  -> 正式训练
  -> 指标、日志、检查点与故障记录归档
```

多节点健康检查应通过作业控制面编排已有计算实例，运行前排除本轮相关残留进程，并选择不冲突的会合端口。任务采用准备、统一激活和结果回收三阶段协议：先确认所有通信组成员就绪，再统一开始；控制连接断开不等于实例内任务终止。每次调度变更、镜像升级、驱动或通信库变更以及维修后回池，都应触发与影响范围相匹配的复验。

训练异常后，应冻结原作业条件和计算实例到物理节点的映射，在原物理节点上建立受控复现环境。复现实验必须与原训练使用相同的训练系统版本、运行环境、配置和数据版本；如果只复用了节点而改变了其他变量，结论只能用于缩小范围，不能声称复现了原故障。

## 规模扩展路径

规模扩展分为两条互补路径：成对测试负责硬件与链路筛查，训练拓扑检查负责真实通信组的功能准入。不采用将小规模全局集合通信矩阵直接放大的方式，因为它会产生真实训练中不存在的超大全局 All-to-All 和连接资源压力。

达到目标规模后，必须依据实际 Megatron/MindSpeed 版本和并行配置生成训练通信组定义。该定义需要冻结训练系统版本、并行参数、rank 顺序、每节点 rank 数，以及各规模的 TP、dense-DP、expert-DP、EP、PP 分组和真实工作负载形状；运行时再次校验其完整性、目标规模、组内覆盖和不重叠性。

| 阶段 | 健康检查准入 | Megatron 准入 | 失败后的动作 |
| --- | --- | --- | --- |
| 单节点 | 静态与动态检查无硬失败 | 单机短程 loss、显存和吞吐基线通过 | 定位设备、运行时或节点内互连 |
| 小规模多节点 | 基础通信、成对测试和专家并行正确性通过 | 并行组和检查点恢复通过 | 换伙伴定位节点或链路，回退配置 |
| 中等规模 | 成对性能候选完成复测；对应训练拓扑功能通过 | 达到预设扩展效率与稳定性门限 | 剖析通信、数据和负载不均衡 |
| 目标规模 | 全部真实子通信组通过 | 端到端训练、检查点与故障演练通过 | 保留失败覆盖，回退到最近通过规模 |

健康检查通过只允许资源进入下一阶段，不替代 Megatron 的性能与收敛验证。训练拓扑检查只验证通信域初始化、正确性、NaN/Inf、进程、超时和结果完整性；性能准入默认仅放在可比较的成对测试群体。反之，短程训练偶然成功也不能替代系统化静态、单卡、正确性和通信检查。扩展效率公式与变量控制见[评测方法](07-evaluation-methodology.md)。

## 当前证据缺口

A3 已有 1024/4096 卡短程性能、8192 卡启动证据和 2048 die 并行策略文档级分析，但缺少长稳、检查点恢复、完整 placement 与成员质量收据；EXP-006 还缺逐步数据、运行版本和原始 profile，EXP-012 缺仓库内逐 rank 日志与 SuperPod placement。C550 仍缺 2048 卡独立分池训练扩展实验。Qwen3-1T MoE 已形成 2,048 die、500 step 的文档级功能运行，并新增 1024/2048/4096 卡会话聚合性能，但三组都只有约 30 步，2048 卡结果对 last5/last10 窗口敏感，且缺数据身份、检查点、原始日志、重复 placement、长稳和收敛评估。健康检查中的示例专家并行度或非均匀全交换模式也不能反推正式训练并行度。
