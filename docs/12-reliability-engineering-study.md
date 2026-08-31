---
title: 万卡训练可靠性工程研究
---

# 万卡训练可靠性工程研究

## 摘要

万卡级大模型训练的交付质量由单步吞吐、资源准入、持续推进、故障恢复和可复核证据共同决定。作业能否从资源准入开始稳定进入训练、在通信和主机运行时扰动下持续推进、在故障后按检查点恢复，并在全流程中保留可复核证据，决定了算力是否真正转化为有效训练产出。本专题基于 10,240 张国产加速卡资源池、Qwen3-200B 与 Qwen3-1T MoE 训练材料、健康检查与 Stall 定位报告、协同训练日志以及工程资产快照，建立面向结项材料的可靠性工程叙事。

本文采用 HPCA 2025 大规模机器学习集群可靠性研究中的 MTTF、ETTR 与 Goodput 方法作为指标框架参考，并将其转化为本项目语境下的健康准入通过率、作业成功率、有效训练时间占比、集群有效产出、恢复时间和证据可追溯性指标。[R019](references.md#r019) 项目结论均以 A3、C550 资源池的实际实验编号、统计窗口和聚合结果为准。

![可靠性指标框架](assets/diagrams/reliability-metrics-framework.svg){ .technical-diagram loading=lazy }

## 评价对象

本项目资源池由 8,192 张华为 Atlas 900 A3 与 2,048 张沐曦曦云 C550 组成。训练组织采用异构分池、分组训练与参数服务器周期同步：A3 侧形成 4 个 2,048 卡训练组，C550 侧形成 4 个 512 卡训练组，控制面汇总资源、健康、任务、日志和指标状态。

可靠性评价围绕四个问题展开：

1. 资源是否经过分层准入，能否形成可解释的训练成员集合。
2. 作业是否完成目标规模初始化，并在有效窗口内持续推进 step。
3. 前向进展、通信尾延迟、ECC/RAS、运行时和控制面扰动是否被纳入同一诊断体系。
4. 训练配置、日志、脚本、统计口径和工程资产是否具备恢复与复核能力。

这四个问题共同构成项目的可靠性工程闭环。单卡、节点、通信组、训练组和资源池不是同一评价层级：单卡测试负责正确性和局部性能，Pairwise 和拓扑测试负责通信可用性，Megatron 短程训练负责作业启动与稳态推进，协同窗口负责异构资源池整体交付效果。

## 指标框架

| 指标族 | 项目内定义 | 对应证据 |
| --- | --- | --- |
| 健康准入 | 静态检查、单卡计算、HBM、Stall-screen、Pairwise、拓扑和训练复现逐级收敛 | [EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) |
| 有效运行 | 有效 iteration、skipped/NaN、稳态吞吐、step 时间和 CV | [EXP-003](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md)、[EXP-012](https://github.com/reiase/tenk_report/blob/master/experiments/exp-012-a3-4096-tp2pp16-dense/README.md) |
| 集群有效产出 | 共同墙钟窗口内按资源池基线加权的 ECP 保留率 | [EXP-004](https://github.com/reiase/tenk_report/blob/master/experiments/exp-004-tenk-weighted-acceptance/README.md) |
| 中断恢复 | 故障注入、心跳检测、参数版本拉取、恢复后首步结果和检查点成本 | [06-reliability-and-observability](06-reliability-and-observability.md) |
| 运行时治理 | 主机软中断、IRQ、tasklet、direct dispatch、Gloo 建组、RDMA retry 和健康检查耗时 | [EXP-005](https://github.com/reiase/tenk_report/blob/master/experiments/exp-005-a3-8192-startup/README.md)、[EXP-007](https://github.com/reiase/tenk_report/blob/master/experiments/exp-007-a3-forward-progress-stall/README.md)、[EXP-008](https://github.com/reiase/tenk_report/blob/master/experiments/exp-008-c550-stall-and-communication-tail/README.md)、[EXP-011](https://github.com/reiase/tenk_report/blob/master/experiments/exp-011-healthcheck-runtime-optimization/README.md) |
| 证据恢复 | tar、Git bundle、SHA256、运行目录、脚本和统计表的快照校验 | [EXP-014](https://github.com/reiase/tenk_report/blob/master/experiments/exp-014-training-assets-backup/README.md) |

MTTF 与 MTBF 用于描述资源池或训练作业中断事件的到达速度；MTTR 与恢复 step 用于描述故障后的恢复速度；ETTR 表示墙钟时间中真正推进有效训练的比例；Goodput 表示资源池单位时间完成的有效训练工作。对于结项报告，最重要的不是把这些指标写成抽象公式，而是把每个指标绑定到可复核实验编号、统计窗口和证据收据。

## 资源准入

A3 资源池完成两个 4,096 卡批次与 96 卡备机筛查。首批 4,096 逻辑设备中 4,093 张为 GOOD、2 张为 GEMM correctness 异常、1 张为计时质量 CONTENDED；第二批 4,096 逻辑设备中 4,093 张为 GOOD、3 张为 CONTENDED；96 张备机静态、单节点、CARD_SCREEN 与 Pairwise 均通过。[EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md)

C550 资源池先覆盖 292 节点、2,336 张卡，再选择 256 节点进入 2,048-rank Final256 训练拓扑。筛查中记录 1 张 correctness BAD、3 张 SDC-SUSPECT、7 张 DEAD、70 张 HBM SLOW，以及两个通信性能候选对象；Final256 完成 2,048-rank 集合通信通过。[EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md)

这组结果体现了可靠性工程中的核心原则：健康状态不是一个简单 PASS/FAIL 字段，而是由正确性、历史 ECC/RAS、HBM 带宽、计时质量、Pairwise 结果、拓扑复验和训练复现共同构成。BAD、DEAD、SDC-SUSPECT、SLOW、CONTENDED 和传输失败分别进入隔离、复测、风险排序或操作处置路径，避免把不同故障域折叠为一个不透明的坏卡率。

## 前向进展与通信尾延迟

A3 前向进展 Stall 由零通信探针发现。1,024 卡 19 分钟轮次记录 7,658 次事件，事件率 0.393 次/卡/min；512 卡 30 分钟轮次记录 6,972 次事件，事件率 0.4539 次/卡/min。事件宽度 P50/P90 为 504/697 ms，最热 10% 卡在 512 卡轮次中贡献 88.9% 的 Stall 总时间。[EXP-007](https://github.com/reiase/tenk_report/blob/master/experiments/exp-007-a3-forward-progress-stall/README.md)

ftrace 材料把该现象定位到 Linux IPVS `estimation_timer` 长时间占用 `TIMER_SOFTIRQ`，同 CPU 上的 NPU CQ tasklet 等待 timer 返回后才执行。这个结论把“设备计算变慢”“集合通信拥塞”“主机同步返回延迟”三类可能性分开，指向 IRQ/CPU 隔离、kube-proxy 模式、TaskQueue 和 jemalloc 的分层治理方案。TaskQueue level 2 与 jemalloc 组合在固定热点节点上将 step 3--500 窗口平均耗时从 234,447.8 ms 降至 172,215.2 ms，缩短 26.54%。[EXP-007](https://github.com/reiase/tenk_report/blob/master/experiments/exp-007-a3-forward-progress-stall/README.md)

C550 单卡探针在 64 卡 1 小时轮次中记录 40 次事件，事件率 0.0104 次/卡/min，P50/max 为 212.6/272.3 ms；20 分钟复测记录 15 次事件，事件率 0.0117 次/卡/min。厂商 direct dispatch 材料提示 CPU/GPU 派发路径会改变 Stall 暴露概率，后续版本能力以实际部署版本复核。[EXP-008](https://github.com/reiase/tenk_report/blob/master/experiments/exp-008-c550-stall-and-communication-tail/README.md)

C550 另一集群的 256/512 卡 AllReduce 扫描显示，QP 增加后带宽下降，512 卡场景 P99 最高达到 1,043 ms。该现象进入通信尾延迟治理项，与单卡前向进展探针分开评价：前者指向网络、MCCL、QP、交换机和多租户状态，后者指向主机派发、运行时和设备完成通知链路。[EXP-008](https://github.com/reiase/tenk_report/blob/master/experiments/exp-008-c550-stall-and-communication-tail/README.md)

## 作业启动与有效训练

Qwen3-200B 在 A3 1,024→4,096 卡同配置弱扩展中，固定模型、软件版本、序列长度、并行组合和单卡 batch，统计共同 iteration 6--12。1,024 卡平均 108.5571 TFLOPS/GPU，4,096 卡平均 102.3286 TFLOPS/GPU，弱扩展效率为 94.2624%，正式报告取 94.26%。两端 skipped 与 NaN 最大计数均为 0。[EXP-003](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md)

在 4,096 卡 Dense 方案复核中，Qwen3-200B 使用 TP2/PP16/DP128/VPP2、GBS 16,384、MBS 1、uniform1 重计算，iteration 6--30 的 25 个稳态样本达到 124.264 TFLOPS/GPU，平均 step 时间 162.398 秒，CV 1.68%，skipped/NaN 为 0/0。相对同会话中的 TP8/PP8/VPP4/block1/no-overlap 候选方案，整套 TP2/PP16 方案吞吐提高 11.18%，平均步时降低 10.09%。[EXP-012](https://github.com/reiase/tenk_report/blob/master/experiments/exp-012-a3-4096-tp2pp16-dense/README.md)

目标规模启动方面，8,192 卡 r1 在默认 Gloo 全互连建组路径中于首个 iteration 前失败；r2 在启动器中加入 `--disable-gloo-group` 后完成建组并进入 iteration 7，skipped/NaN 为 0。这说明大规模作业的“能否建组”应作为性能评价前置 gate 单独记录，初始化后端、rendezvous、训练首步和稳态窗口要分阶段归档。[EXP-005](https://github.com/reiase/tenk_report/blob/master/experiments/exp-005-a3-8192-startup/README.md)

1T MoE 方面，Qwen3-1T MoE 在 1,024/2,048/4,096 卡 last5 吞吐分别为 65.60/61.82/57.66 TFLOPS/GPU，对应单卡保留率 1024→2048 为 94.24%、1024→4096 为 87.90%。该结果说明 MoE 的 CPU offload、路由、All-to-All、DDP bucket 和建组后端需要独立形成优化链路，不宜直接套用 Dense 的最优参数。[EXP-013](https://github.com/reiase/tenk_report/blob/master/experiments/exp-013-a3-qwen3-1t-moe-tuning/README.md)

## 异构协同 Goodput

万卡协同验收采用 8 个训练组在共同墙钟窗口内的加权 ECP。A3 4 组每组 2,048 卡，C550 4 组每组 512 卡；共同窗口为 2026-08-15 21:39:18 至 2026-08-16 10:49:54，共 47,436 秒。窗口内 A3 每组 239 步，C550 每组 120 步，所有组 skipped 和 NaN iteration 均为 0。[EXP-004](https://github.com/reiase/tenk_report/blob/master/experiments/exp-004-tenk-weighted-acceptance/README.md)

A3 混训窗口 ECP 为 101.6508 TFLOPS/卡，独立基线为 108.5571 TFLOPS/卡；C550 混训窗口 ECP 为 51.0364 TFLOPS/卡，独立基线为 60.9000 TFLOPS/卡。按 8192:2048 的资源权重计算，混合窗口加权 ECP 为 91.5279，独立基线加权 ECP 为 99.0257，加权保留率为 92.4284%，正式取 92.43%。[EXP-004](https://github.com/reiase/tenk_report/blob/master/experiments/exp-004-tenk-weighted-acceptance/README.md)

从可靠性角度看，这个结果把“有效训练时间”和“资源池产出”合在同一验收视角中：各训练组在共同窗口内持续推进，参数服务器按周期完成同步，异构资源池相对各自基线保留了主要算力。该指标与单平台弱扩展效率各司其职，前者回答资源池协同交付，后者回答同硬件同模型同配置扩容后的每卡吞吐保持。

## 健康检查运行效率

健康准入本身也是大规模系统的一部分。128 节点 Pairwise 专项实验显示，并发 32 时，64 个 no-op group 约 4 秒完成，真实两节点通信约 74.58--75.71 秒；单组生命周期中位数 34.65 秒，其中 Pod 内动态测试 19.68 秒，外层 driver、连接、进程与结果回收 15.04 秒。[EXP-011](https://github.com/reiase/tenk_report/blob/master/experiments/exp-011-healthcheck-runtime-optimization/README.md)

64 节点、1,024-rank 完整流水线中，旧版历史基线多节点墙钟为 1,706 秒，main 优化版为 1,056 秒，下降 650 秒，对应 38.1%。优化保留在 main 中的机制包括：Pod 内任务后台启动并通过 launch acknowledgement 解耦长连接，高频状态和分块结果先落本地 `/tmp`，阶段结束后发布聚合结果；状态机明确区分准备、激活、运行、结果就绪和回收；结果帧按 32 KiB 分块校验长度、SHA256 和完整 payload。[EXP-011](https://github.com/reiase/tenk_report/blob/master/experiments/exp-011-healthcheck-runtime-optimization/README.md)

这部分工作的价值在于把健康检查从“运行前脚本”升级为可伸缩的控制面流水线。随着节点规模增加，可靠性系统的排队、同步、传输、复测和归档开销会进入 ETTR 与 Goodput 分母；因此健康检查自身也需要明确运行态、等待态、回收态和异常态，避免把控制面长尾误写成设备通信长尾。

## 模型交付与检查点成本

模型功能运行材料显示，201.42B Dense 在 1,024 die 完成 800/800 step，1,099.55B MoE 在 2,048 die 完成 500/500 step，并提供 loss 曲线截图。[EXP-009](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) 这些材料证明模型、训练脚本、数据读取、并行配置和运行环境能够在对应规模下完成指定步数，是进入性能、恢复和长期运行评价的基础。

检查点容量估算按每参数约 14 bytes 计算 FP16/BF16 权重、FP32 master weight 与 Adam 一二阶状态：200B 完整状态约 2.8 TB/次，25 份约 70 TB；1T 完整状态约 14 TB/次，25 份约 350 TB。[EXP-009](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) 这说明恢复能力与存储系统、状态切分、保存周期、加载耗时和对象归档策略强相关，属于可靠性工程的主线指标。

工程资产快照方面，`full_training_project_20260817_232003` 覆盖 Qwen3-200B、Qwen3-1T MoE、DeepSeek-V3 Midtrain 的代码、日志、配置、运行环境、启动脚本、拓扑、TensorBoard 和分析结果。校验结果为 10/10 个 tar 可遍历、6/6 个 Git bundle 完整性通过、75/75 项 SHA256 通过，0 失败，总大小约 2.6 GB。[EXP-014](https://github.com/reiase/tenk_report/blob/master/experiments/exp-014-training-assets-backup/README.md)

该快照保存的是工程资产、脚本、日志摘要和复现索引；约 22 TB checkpoint/模型权重/派生数据和约 84 GB profiler 原始数据按清单管理。正式恢复流程采用主快照、增量包、目标端数量/容量对账、内容校验、归档遍历、Git bundle 验证和抽样恢复收据共同闭环。[EXP-014](https://github.com/reiase/tenk_report/blob/master/experiments/exp-014-training-assets-backup/README.md)

## 工程结论

本项目可靠性工程的第一条结论是：资源准入要面向训练拓扑，而不是只面向单卡。A3 与 C550 的筛查结果表明，正确性异常、历史 ECC、HBM 慢卡、计时质量、Pairwise 失败和拓扑复验应进入同一成员构造流程，最终形成入选、备用、候选复测和隔离集合。

第二条结论是：前向进展异常需要从设备同步语义出发拆解。A3 的 500/650 ms 级 Stall 通过 ftrace 连接到 IPVS timer 与 NPU CQ tasklet 的竞争；C550 的 direct dispatch 与 AllReduce 长尾分别指向主机派发路径和通信尾延迟治理。同步训练会放大最慢 rank 的等待，因此这些事件会直接影响有效训练时间占比。

第三条结论是：规模化训练的性能指标要与可靠性指标联合解释。弱扩展效率 94.26%、4,096 卡 Dense 124.264 TFLOPS/GPU、异构协同 ECP 92.43% 与健康检查 1,706→1,056 秒共同说明，项目不仅完成了单点性能优化，也把资源准入、启动建组、运行态观测和证据恢复纳入了工程体系。

第四条结论是：检查点和工程资产恢复决定长期训练可持续性。200B 与 1T 模型的状态容量达到 TB 到百 TB 量级，任何长周期训练都需要把保存周期、加载耗时、增量归档、跨故障域副本和恢复抽样纳入 run 级记录。没有恢复收据的备份只是一份材料快照；带校验、对账和抽样恢复的快照才是训练系统可靠性的组成部分。

综合来看，项目已经形成面向万卡国产加速卡训练的可靠性工程范式：以分层健康准入构造资源集合，以前向进展和通信观测定位运行时扰动，以短程训练和共同窗口验证有效推进，以检查点和资产快照保障恢复，以实验编号、统计窗口和哈希收据支撑结项复核。
