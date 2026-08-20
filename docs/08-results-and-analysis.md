---
title: 结果与分析
status: draft
owner: unassigned
reviewers: []
last_updated: 2026-08-20
---

# 结果与分析

## 当前证据状态

仓库已经导入九组带稳定编号的实验。聚合结果、冻结配置、受控原始证据位置和 SHA256 已登记；结论按“日志级短程结果、文档级功能/根因证据、部分启动验证、待完成生产验收”分层。

| 结论层级 | 当前状态 | 可使用的证据 | 尚缺材料 |
| --- | --- | --- | --- |
| 方法覆盖范围 | 可评审 | 测试对象、指标定义和判定逻辑 | 生产环境闭环验证 |
| [EXP-001](https://github.com/reiase/tenk_report/blob/master/experiments/exp-001-a3-1024-tuning/README.md) A3 1024 卡调优 | 已导入 | 15 个长跑用例聚合与原始汇总哈希 | placement 快照、随机化重复 |
| [EXP-002](https://github.com/reiase/tenk_report/blob/master/experiments/exp-002-a3-4096-dp-communication/README.md) A3 4096 卡通信消融 | 已导入 | 7 个 PASS、1 个 NO_DATA；每个 PASS 有 25 个稳态步 | 交错 A/B 与重复轮 |
| [EXP-003](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md) A3 弱扩展 | 已复核短程结果 | 两侧配置、代表日志与哈希；共同 7 步窗口 | 长稳、重复 placement 与端到端时间 |
| [EXP-004](https://github.com/reiase/tenk_report/blob/master/experiments/exp-004-tenk-weighted-acceptance/README.md) 万卡加权验收 | 可复核点估计 | 8 组共同 13.18 小时窗口、日志包哈希与公式 | C550 稳态独立基线、完整 800 步 |
| [EXP-005](https://github.com/reiase/tenk_report/blob/master/experiments/exp-005-a3-8192-startup/README.md) A3 8192 卡启动 | 部分通过 | r1/r2 配置与日志、修正启动器哈希 | 完整 30 步、长稳与成员质量收据 |
| [EXP-006](https://github.com/reiase/tenk_report/blob/master/experiments/exp-006-a3-2048die-parallelism-mfu/README.md) A3 2048 die 并行策略与 MFU | 文档级证据 | 聚合表、趋势图、PDF 与 SHA256 | run ID、逐步数据、MFU 公式、完整配置与原始 profile |
| [EXP-007](https://github.com/reiase/tenk_report/blob/master/experiments/exp-007-a3-forward-progress-stall/README.md) A3 Stall | 根因文档内闭环 | 512/1,024 卡分布、ftrace 配对摘要、缓解消融与 SHA256 | 完整 ftrace、系统级修复后的随机化回归 |
| [EXP-008](https://github.com/reiase/tenk_report/blob/master/experiments/exp-008-c550-stall-and-communication-tail/README.md) C550 Stall/通信尾延迟 | 文档级证据 | 64 卡探针、256/512 卡通信重复、厂商 direct dispatch 说明 | 原始 gap、复测卡时、交换机 counter 和独立 A/B |
| [EXP-009](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) 200B/1T 交付 | 文档级功能运行 | 模型估算、800/500 step 交付截图、混训编排与 SHA256 | 最终配置、逐步日志、检查点校验、性能与收敛评估 |
| 2,048 卡 C550 分池验收 | 待执行 | 万卡窗口中的 C550 分组结果 | 独立分池准入、扩展曲线与长稳 |
| 10,240 卡单作业结论 | 不适用 | 验收加权指标 92.43% | 不得改写为 10,240 卡单一同步作业效率 |

下列生产数字只引用上述实验；没有实验编号、统计窗口和证据哈希的历史陈述仍作为待核验线索。

## 规模扩展

两个资源池分别绘制规模—吞吐—扩展效率曲线。A3 的首组同口径短程结果来自 EXP-003；C550 尚未形成独立扩展曲线。

| 资源池 | 实验 | 规模（卡） | 基准规模（卡） | 每卡吞吐（TFLOPS） | 总吞吐加速比 | 扩展效率 | 口径 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| A3 | [EXP-003 基线](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md) | 1,024 | 1,024 | 108.5571 | 1.0000x | 100.00% | 弱扩展，iteration 6--12 |
| A3 | [EXP-003 目标](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md) | 4,096 | 1,024 | 102.3286 | 3.7705x | **94.26%** | 弱扩展，iteration 6--12 |
| C550 | 待执行 | 待实测 | 待确定 | 待实测 | 待计算 | 待计算 | 独立分池口径待冻结 |

A3 两侧均为 Qwen3-200B、TP1/PP64/VPP2、MBS1、sequence length 4096 和同一代码 commit；DP 与 GBS 随卡数扩大 4 倍，microbatches 保持 256。统计仅含 7 个稳态步，因此 94.26% 是短程弱扩展结果。

EXP-006 使用 `die` 作为规模单位，且没有提供与 EXP-003 对齐的设备换算、运行版本和逐步吞吐，因此不并入上表的“卡数与 TFLOPS/卡”弱扩展曲线。

### 10240 卡验收加权指标

[EXP-004](https://github.com/reiase/tenk_report/blob/master/experiments/exp-004-tenk-weighted-acceptance/README.md) 按 8192:2048 设备数量加权 A3 与 C550 的每卡 ECP：

| 指标 | A3 | C550 | 加权值 |
| --- | ---: | ---: | ---: |
| 独立基线（TFLOPS/卡） | 108.5571 | 60.9000 | 99.0257 |
| 共同窗口 ECP（TFLOPS/卡） | 101.6508 | 51.0364 | 91.5279 |
| 相对独立基线 | 93.64% | 83.80% | **92.43%** |

92.43% 来自八个训练组共同连续 47,436 秒的窗口。它是资源池加权验收指标，不是 10,240 卡单作业吞吐或跨硬件弱扩展效率。

## 端到端训练性能

稳态吞吐和端到端吞吐分开报告。现有 EXP-001 至 EXP-003 是短程性能实验，禁用了检查点；EXP-004 是共同运行窗口；EXP-006 只有聚合 PDF，不能恢复端到端时间线。EXP-009 虽报告 200B 800/800 step 和 1T MoE 500/500 step，但没有逐步墙钟、检查点和恢复明细。它们均不能替代包含启动、数据等待、检查点和故障恢复的完整端到端测量。

| 资源池 | 实验 | 稳态结果 | 端到端吞吐 | 测量窗口 | 检查点开销 | 数据等待 | 故障恢复 |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: |
| A3 | EXP-003 / 1,024 卡 | 108.5571 TFLOPS/卡 | 未测 | iteration 6--12，7 步 | 禁用 | 未分解 | 未触发 |
| A3 | EXP-003 / 4,096 卡 | 102.3286 TFLOPS/卡 | 未测 | iteration 6--12，7 步 | 禁用 | 未分解 | 未触发 |
| A3+C550 | EXP-004 | 加权 ECP 91.5279 TFLOPS/卡 | 未测 | 47,436 秒共同窗口 | 未分解 | 未分解 | 前段重启已排除并披露 |
| C550 | 独立分池 | 待实测 | 待实测 | 待定义 | 待实测 | 待实测 | 待实测 |

### 模型交付功能运行

| 模型 | 参数量口径 | 规模 | 完成 step | 证据等级 | 不能推出 |
| --- | ---: | ---: | ---: | --- | --- |
| 200B Dense | 交付值 201.42B；估算 200.75B | 1,024 die | 800/800 | 文档级功能运行 | 收敛、长稳、MFU、端到端吞吐 |
| 1T MoE | 交付值 1,099.55B；估算 1,091.80B | 2,048 die | 500/500 | 文档级功能运行 | 收敛、长稳、MFU、端到端吞吐 |

来源截图显示两条 loss 曲线并报告运行无错误。仓库尚不能从原始日志复算曲线，也没有最终参数枚举、数据身份和检查点完整性，因此只确认来源所记录的有限步数训练推进。

## 稳定性结果

### 前向进展 Stall

A3 最小同步探针在 1,024 卡 x 19 min 中记录 7,658 次事件，在 512 卡 x 30 min 中记录 6,972 次事件；gap P50/P90 为 504/697 ms。来源报告把代表事件闭环到 IPVS `estimation_timer` 在软中断上下文占用约 875 ms，阻塞同 CPU 上 NPU CQ tasklet。[EXP-007](https://github.com/reiase/tenk_report/blob/master/experiments/exp-007-a3-forward-progress-stall/README.md)

C550 64 卡 x 1 h 记录 40 次事件，P50/max 为 212.6/272.3 ms；厂商材料报告 direct dispatch 后未复现，但未给观察卡时。C550 的另一组 256/512 卡 AllReduce 尾延迟是独立通信现象。[EXP-008](https://github.com/reiase/tenk_report/blob/master/experiments/exp-008-c550-stall-and-communication-tail/README.md)

两组数字都依赖同步频率、主机、运行时和插桩模式。A3 材料还观察到 profiler/插桩会提高事件率，因此正式回归必须保存无插桩控制组，不能把深度采集轮直接用于事件率验收。

### 健康与训练稳定性

健康检查结果按 run、phase 和节点状态汇总，训练稳定性按资源池与时间窗口汇总。二者不能混用：一次健康检查 PASS 不是长稳训练成功，一次检查 FAIL 也不能在未定位前直接计为硬件故障。

单卡计算与存储可靠性测试应先按资源池和精确可比样本组报告，不能只给一个总通过数：

| 资源池/cohort | 预期卡数 | 实际覆盖 | good | slow | contended | bad/dead | sdc-suspect | 证据 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| A3 / 待冻结 | 待补充 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 | 待导入 |
| C550 / 待冻结 | 待补充 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 | 待导入 |

| 资源池/cohort | 矩阵 TFLOPS P10/P50 | HBM GB/s P10/P50 | 稳态 TFLOPS P10/P50 | 稳态/瞬时比 P10/P50 | 满载功耗 P10/P50/P90 | 热/功率限频卡数 |
| --- | --- | --- | --- | --- | --- | ---: |
| A3 / 待冻结 | 待实测 | 待实测 | 待实测 | 待计算 | 待实测 | 待实测 |
| C550 / 待冻结 | 待实测 | 待实测 | 待实测 | 待计算 | 待实测 | 待实测 |

SDC 结果按目标单元拆开，至少报告实际轮数、命中卡数、异常卡数、功耗遥测覆盖，以及因限频而未达到目标压力的卡数。HBM 数据模式测试还要报告实际覆盖 GiB 和覆盖率分布；固定容量抽样不得汇总成全显存无错误。发生命中时保留首个命中轮、不一致元素数、最大偏差、当时可获得的遥测和复测状态。

| 资源池 | 时间范围 | 候选节点 | selected | standby | excluded | FAIL/SUSPECT | topology 状态 | 证据 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| A3 | 待补充 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 | 待导入 |
| C550 | 待补充 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 | 待导入 |

训练拓扑结果另按 `world_size + family + op + shape + group_size` 报告 case 数、期望/实际 subgroup 数、最慢 subgroup、correctness 和错误分类。`BLOCKED` 与 `NOT_RUN` 必须计入覆盖率，不能从分母中删除。

| 资源池 | 统计窗口 | 有效训练时间占比 | 中断次数 | MTBF | MTTR | 训练成功率 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| A3 | 待补充 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 |
| C550 | 待补充 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 |

## 观测质量与开销

性能数字必须同时给出观测质量，避免“只在正常 rank 上有数据”的幸存者偏差。每个关键实验至少附带以下表格：

| 实验 | 采集模式 | 期望/实际 rank | 有效 step | 丢弃事件 | 失败节点/分区 | partial | P50/P95/Max 开销 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| 待导入 | 常驻/采样/短窗口 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 | 待实测 |

常驻路径、采样重路径、短窗口 profiler 和通信库原生插件分开报告开销。若关闭观测后性能改善，只能先确认观测路径存在增量；还需通过 dispatch、采样、设备时间读取、写表和查询等分层实验定位来源。观测开销超过预算或质量收据不完整时，该轮数据可用于诊断，但不得进入扩展效率主曲线。

跨 rank 分析先展示 step/rank 热力图、行为组和尾部 rank，再对少量对象下钻到精确事件。报告必须保存下钻所使用的 rank 集合、时间窗、对齐方式和过滤条件，使概览结论可以回到原始证据。对 compute、communication 和 idle 占用的计算先合并重叠区间，不直接相加原始 duration。

## 瓶颈分析

每个瓶颈使用下表记录，避免由“时间上同时发生”直接推出因果：

| 观察 | 直接证据 | 原因假设 | 替代解释 | 验证实验 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 4096 卡 iteration 9 降至 97.8 TFLOPS/GPU | EXP-003 原始代表日志 | 瞬时通信或资源竞争 | placement 差异、主机抖动、测量噪声 | 同 placement 复跑并关联 rank/网络遥测 | 未归因，主结果保留该点 |
| 8192 卡 r1 首步前 Gloo 建组失败 | EXP-005 多 rank 错误与日志哈希 | 分布式优化器 Gloo 全互连路径在该规模失效 | 节点故障或其他网络异常 | r2 仅增加 `--disable-gloo-group` 后复跑 | 启动阻塞已修正，底层网络根因未外推 |
| C550 独立基线只有 3 个 iteration | EXP-004 基线日志 | 基线统计不足 | 热身阶段尚未结束 | 补跑 20--30 个稳态步并冻结聚合口径 | 已披露，待补证 |
| TP8 扩展后 forward-compute 与未重叠通信增长 | EXP-006 的 TensorBoard/Profiling 聚合摘要 | 小消息 AllReduce 时延与尾部 ReduceScatter 拥塞 | 配置、placement、外部网络负载或计时口径差异 | 导入原始 profile 与网络 counter，并按相同拓扑随机化复跑 | 来源报告支持，尚未独立闭环 |
| A3 单卡同步 gap 出现 500/650 ms 级两簇 | EXP-007 的事件分布与 S005 ftrace 摘要 | IPVS timer 阻塞同 CPU 的 NPU CQ tasklet | trace 丢失样本、其他主机调度或运行时路径 | 系统级修复、IRQ/CPU 控制组与无插桩随机化回归 | 文档内闭环，原始 trace 待归档 |
| C550 256/512 卡 AllReduce 部分重复出现长尾且增加 QP 退化 | EXP-008 聚合材料 | 规模/QP/网络竞争候选 | 多租户、交换机、NIC、退出路径或测量差异 | 同 cohort 交错复跑并绑定端口/交换机 counter | 未归因 |
| C550 混训出现 `IBV_WC_RETRY_EXC_ERR` | EXP-009 问题记录 | RDMA 重试耗尽 | 节点、链路、路由或外部网络竞争 | 换伙伴、固定路径复现和网络遥测 | 临时筛除，根因未关闭 |

健康检查可优先定位正确性失败、慢 rank、慢 group 和通信路径异常；最终归因仍需结合设备日志、交换机遥测、软件版本差异和训练 trace。一次异常应沿“作业概览 → 节点/行为组 → rank/step → module/collective → 原生 task/kernel/stack”逐级收窄，避免先挑选一段细粒度 trace 再事后构造全局解释。

## 消融与对比

[EXP-001](https://github.com/reiase/tenk_report/blob/master/experiments/exp-001-a3-1024-tuning/README.md) 中 mapping0 在五组直接配对比较中均高于 mapping1，相对差异为 0.64%--3.96%。TP8 + block + mapping0 达到 135.00 TFLOPS/GPU，但它同时包含并行与重计算变化，不能把全部收益归因于 mapping。TP1 基线重复轮相差 0.22%，小于 1% 的差异仍需增加重复。

[EXP-002](https://github.com/reiase/tenk_report/blob/master/experiments/exp-002-a3-4096-dp-communication/README.md) 中 `no-overlap`、`bucket-128m` 相对首个 no-param-overlap 基线分别高 6.89% 和 5.35%；同一 no-param-overlap 的重复轮相差 1.67%，且 `full-overlap-b` 为 NO_DATA。当前结论是选出复测候选，而不是宣布关闭重叠为默认最优。

### 2048 die 并行度网格

[EXP-006](https://github.com/reiase/tenk_report/blob/master/experiments/exp-006-a3-2048die-parallelism-mfu/README.md) 在 Qwen3-200B、2048 die、GBS8192、MBS1、VPP2 条件下汇总了七个配置：

| TP | PP | 重计算 | TP×PP | MFU |
| ---: | ---: | --- | ---: | ---: |
| 1 | 64 | uniform1 | 64 | 26.7% |
| 2 | 32 | uniform1 | 64 | 30.4% |
| 4 | 16 | uniform1 | 64 | 29.8% |
| **2** | **16** | **uniform1** | **32** | **33.4%** |
| 4 | 8 | uniform1 | 32 | 31.3% |
| 8 | 8 | uniform1 | 64 | 24.1% |
| 8 | 8 | block1 | 64 | 28.1% |

本轮最高点是 TP2/PP16/uniform1 的 33.4%。在 TP×PP=64、uniform1 子集中，TP2/PP32（30.4%）高于 TP4/PP16（29.8%）和 TP8/PP8（24.1%）；TP1/PP64（26.7%）也低于 TP2/PP32。结果支持“TP 与 PP 都存在过大损失、需要联合搜索”，但缺少重复次数和误差范围，排序仍应复跑确认。

### GBS 与重计算归因

同一来源在 TP8/PP8/VPP4、2048 die 下报告，仅将 GBS 从 1024 增至 8192 时，MFU 从约 20.7% 升至约 24.1%，增加 3.4 个百分点。GBS8192 从 1024 die 扩到 2048 die 后，MFU 从约 26% 降至约 24%，下降约 2 个百分点。PDF 没有为随后 TP1/PP64 的重计算对比单独注明 VPP，因此该行 VPP 在结构化摘要中保留为 `NA`。

uniform1 改为 block1 后，TP8/PP8 从 24.1% 升至 28.1%，TP1/PP64 从 26.7% 升至 27.0%。原文同时指出 block1 在 PP8 下重计算 8 层、在 PP64 下重计算 64 层，而 uniform1 均为 128 层。因此 +4.0 与 +0.3 个百分点的差异首先反映“减少的重计算层数不同”，不能解释为 TP8 本身带来更高收益。

### 大 TP 的通信归因

| 观察量 | TP8 | TP2/PP8 | 当前解释 |
| --- | ---: | ---: | --- |
| Scaling 后 forward-compute 耗时增长 | 约 3.1x | 约 1.83x | 增量集中在 forward 阶段 |
| 未重叠通信增长 | 120% | 54% | 大 TP 暴露更多通信时延 |
| 小消息 AllReduce 时延增长 | 约 4--19x | 未报告 | 固定开销与网络时延更难被短计算窗口掩盖 |
| ReduceScatter 增长相对幅度 | 基准 | 约为 TP8 的 1/4 | 浅流水线使 backward 结束与 DP 通信发射更集中 |

这条链路与网格中 TP8/PP8 的较低 MFU 方向一致，但证据目前只存在于来源 PDF 的聚合叙述中。没有原始 collective 明细、消息大小分布、rank placement 和网络 counter 时，应把它保留为高优先级根因假设，而不是完成的因果闭环。

Megatron 优化仍按单变量或已声明的组合做 A/B，保存完整配置差异，并同时检查吞吐、显存、数值一致性和稳定性。健康检查自身也需要量化漏检、误报和筛查时长，而不是只证明工具能输出 PASS。

## 结果边界

- EXP-003 的 94.26% 只有 7 个评分步，是短程弱扩展结果，不外推为长稳或端到端效率。
- EXP-004 的 92.43% 是异构资源池加权验收点估计；C550 基线只有 3 步，补跑稳态基线前不能升级为最终生产结论。
- EXP-005 只证明 8192 卡 r2 完成建组并进入 iteration 7，不报告稳态 MFU、扩展效率或 30 步完成。
- EXP-006 的 33.4% 是 2048 die、Qwen3-200B、GBS8192、MBS1、VPP2 网格中的文档级最佳已测点；缺少逐步数据、MFU 公式和重复轮，不与日志级实验做跨口径排名。
- EXP-007 的 A3 Stall 根因在来源文档中闭环到 IPVS timer 与 CQ tasklet 竞争；完整 ftrace 未归档前不升级为仓库内原始证据闭环，热点节点也不按永久坏卡处理。
- EXP-008 的 C550 direct dispatch 与通信尾延迟均为文档级证据；缺少观察卡时和网络 counter 时，不报告修复后的事件率或网络根因。
- EXP-009 的 800/800 与 500/500 step 只证明来源记录的功能运行；不报告收敛、MFU、端到端吞吐或检查点恢复成功率。
- 合成 BusBW 不外推为 Megatron 吞吐或 MFU；某消息大小、collective 或 EP pattern 不外推到未测试 workload。
- A3 与 C550 的单平台结果分别报告；加权 ECP 单列，不改写为单一异构同步训练吞吐。
- 历史运行记录缺少原始测量、完整运行条件、版本和完整性摘要时，只能列为待导入线索。

## 证据导入顺序

1. 按[复现实验清单](appendix-b-reproducibility.md)冻结测量方法、运行条件、软件环境与拓扑。
2. 导入最终实验条件、训练拓扑定义、超节点与节点选择依据及其完整性摘要。
3. 为每次实验建立稳定编号，保存可评审的聚合结果，并登记受限原始证据的位置和完整性摘要。
4. 先生成“候选—硬通过—selected—standby—excluded”准入漏斗、失败类型、物理路径候选和 topology coverage，再关联训练作业与维修工单。
5. 数据评审通过后，将“待实测”替换为数字，并同步更新[执行摘要](00-executive-summary.md)。
