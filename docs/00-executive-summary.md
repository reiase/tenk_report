---
title: 执行摘要
status: draft
owner: unassigned
reviewers: []
last_updated: 2026-08-20
---

# 执行摘要

## 核心问题

本项目建设并验证一套总规模为 **10,240 张国产加速卡**的大模型训练基础设施，其中华为 Atlas 900 A3 SuperPoD 资源池包含 8,192 张加速卡，沐曦曦云 C550 资源池包含 2,048 张加速卡。两套资源池具有不同的卡内架构、互连层级和软件栈，因此分别完成健康准入、Megatron 适配调优和扩展效率验证，再在统一的作业与指标体系下管理。

这里的“万卡规模”指两个资源池可纳管的加速卡总数，不表示 10,240 张异构卡共同运行同一个同步训练作业。卡数是项目提供的部署基线；可分配卡数、健康卡数和单作业实际参训卡数将在结果章节分别披露。

## 核心结论

- 已确定的工作范围包括两类国产硬件资源池，共计 10,240 张加速卡。
- A3 Qwen3-200B 在严格对齐的 1024 与 4096 卡短程实验中得到 **94.26%** 弱扩展效率；两侧共同统计 iteration 6--12。
- EXP-006 的 2048 die 并行度网格中，Qwen3-200B 的 TP2/PP16/uniform1 达到最高 MFU **33.4%**；该结果来自聚合 PDF，属于文档级证据，仍需原始运行和重复轮复核。
- EXP-012 进一步复核 4096 卡 TP2/PP16/uniform1：iteration 6--30 平均 **124.264 TFLOPS/GPU**、CV 1.68%、0 skipped/NaN；相对已测 TP8/PP8 r6 方案高 11.18%，但这是 PP、VPP、DP、microbatch 与重计算同时变化的方案级比较。
- 8192 卡 r1 在首步前发生 Gloo 全互连建组失败；r2 使用 `--disable-gloo-group` 后完成建组并进入 iteration 7，证明启动阻塞已绕过，但尚未形成长稳与最终性能结论。
- 8192 张 A3 与 2048 张 C550 的八组日志在 13.18 小时共同窗口内得到 **92.43%** 加权验收指标；补充材料确认它由 8 个训练组和 64 个参数服务器协同运行，不是 10,240 卡单一同步训练作业的扩展效率。
- A3 单卡同步 Stall 已在来源报告中闭环到 IPVS `estimation_timer` 长时间占用软中断、阻塞同 CPU 的 NPU CQ tasklet；系统级修复回归和完整 ftrace 归档仍待完成。
- 交付材料报告 200B Dense 在 1,024 die 完成 800/800 step，1T MoE 在 2,048 die 完成 500/500 step。它们是文档级功能运行证据，不是性能、收敛或长稳结论。
- EXP-013 补充 1T MoE 的短程性能：1024/2048/4096 卡 last5 分别为 **65.60/61.82/57.66 TFLOPS/GPU**，4096 卡保留 1024 卡约 **87.90%** 的单卡性能；结果来自会话日志聚合，且 MoE FLOPs 不完整覆盖路由、All-to-All 与 offload 开销，不与 Dense MFU 直接排名。
- C550 64 卡前向进展探针的事件宽度集中在 200--272 ms；direct dispatch 是厂商缓解方向，独立观察卡时和通信网络根因仍待补。
- 健康检查材料记录 A3 两个 4,096 卡批次和 96 卡备机筛查；首批发现 2 张 correctness BAD，第二批 0 BAD，两个 256 节点 Job 均完成过 Final256 集合通信。
- C550 对 292 节点、2,336 张卡完成全量筛查，记录 1 BAD、3 SDC-SUSPECT、7 DEAD 和 70 HBM SLOW；筛选出的 256 节点完成 Final256 的 2,048-rank 集合通信。
- 64 节点、1,024 ranks 的健康检查完整流水线从 1,706 秒降到 1,056 秒，观察下降 38.1%；两轮 Job 与节点不同且旧轮含未复现的 Final64 长尾，该值不是纯软件收益。
- EXP-014 记录 AFS 全项目快照约 2.6 GB，10/10 个 tar、6/6 个 Git bundle 和 75/75 项 SHA256 校验通过；约 22 TB 大对象与 84 GB profiler 原件只保存清单，备份后新增 MoE 日志的增量和对象存储副本仍未完成。
- 规模化工作的第一道门槛仍是筛卡和健康检查；所有性能结论必须同时披露配置、统计窗口、证据哈希与未完成项。

## 关键指标

| 指标 | 结果 | 统计口径 | 证据位置 |
| --- | ---: | --- | --- |
| 纳管加速卡总数 | 10,240 张 | A3 8,192 + C550 2,048 | 项目部署基线 |
| A3 资源池占比 | 80% | 8,192 / 10,240 | 项目部署基线 |
| C550 资源池占比 | 20% | 2,048 / 10,240 | 项目部署基线 |
| A3 CARD_SCREEN | r1：4,093 GOOD / 2 BAD / 1 CONTENDED；r2：4,093 GOOD / 0 BAD / 3 CONTENDED | 两个独立 4,096 卡批次；文档级证据 | [EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) |
| C550 候选池筛查 | 1 BAD / 3 SDC-SUSPECT / 7 DEAD / 70 HBM SLOW | 292 节点、2,336 卡；状态不合并为坏卡率 | [EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) |
| C550 训练拓扑验收 | Final256 PASS | 筛选后 256 节点、2,048 ranks；只证明集合通信验收 | [EXP-010](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) |
| 健康检查墙钟观察 | 1,706→1,056 秒（-38.1%） | 64 节点同拓扑、不同 Job；受 Final64 长尾等混杂 | [EXP-011](https://github.com/reiase/tenk_report/blob/master/experiments/exp-011-healthcheck-runtime-optimization/README.md) |
| A3 最大已进入训练规模 | 8,192 张 | r2 完成建组并观测到 iteration 7；非完整验收 | [EXP-005](https://github.com/reiase/tenk_report/blob/master/experiments/exp-005-a3-8192-startup/README.md) |
| A3 1024→4096 弱扩展效率 | **94.26%** | 同代码/模型/序列长度/并行组合，7 个共同稳态步 | [EXP-003](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md) |
| A3 2048 die 配置搜索最佳 MFU | **33.4%** | Qwen3-200B、GBS8192、MBS1、VPP2、TP2/PP16/uniform1；文档级证据 | [EXP-006](https://github.com/reiase/tenk_report/blob/master/experiments/exp-006-a3-2048die-parallelism-mfu/README.md) |
| A3 4096 卡 Dense TP2/PP16 | **124.264 TFLOPS/GPU** | iteration 6--30，25 步，CV 1.68%；会话日志聚合 | [EXP-012](https://github.com/reiase/tenk_report/blob/master/experiments/exp-012-a3-4096-tp2pp16-dense/README.md) |
| A3 1T MoE 短程扩展 | **65.60 / 61.82 / 57.66 TFLOPS/GPU** | 1024/2048/4096 卡 last5；4096/1024 单卡保留率 87.90% | [EXP-013](https://github.com/reiase/tenk_report/blob/master/experiments/exp-013-a3-qwen3-1t-moe-tuning/README.md) |
| 工程资产 AFS 主快照 | 10/10 tar、6/6 bundle、75/75 SHA256 | 约 2.6 GB；同故障域，增量与对象存储副本未完成 | [EXP-014](https://github.com/reiase/tenk_report/blob/master/experiments/exp-014-training-assets-backup/README.md) |
| 10240 卡加权验收指标 | **92.43%** | 8192:2048 加权 ECP，8 组共同 47,436 秒 | [EXP-004](https://github.com/reiase/tenk_report/blob/master/experiments/exp-004-tenk-weighted-acceptance/README.md) |
| A3 前向进展 Stall 根因 | IPVS timer / CQ tasklet 竞争 | 5 次来源事件中 3 次直接 ftrace 配对、2 次按周期推断；文档内闭环 | [EXP-007](https://github.com/reiase/tenk_report/blob/master/experiments/exp-007-a3-forward-progress-stall/README.md) |
| 200B Dense 功能运行 | 800 / 800 step | 1,024 die，201.42B；文档级证据 | [EXP-009](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) |
| 1T MoE 功能运行 | 500 / 500 step | 2,048 die，1,099.55B；文档级证据 | [EXP-009](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) |
| 单作业最终验收规模 | 待完成 | 完整训练、成员收据、检查点与恢复均通过 | [结果边界](08-results-and-analysis.md#结果边界) |
| 端到端吞吐 | 待补充 | 包含启动、数据、检查点和恢复的墙钟口径 | [结果](08-results-and-analysis.md#端到端训练性能) |
| 有效训练时间占比 | 待补充 | 统一定义、分池统计 | [稳定性](06-reliability-and-observability.md) |

## 主要贡献

- 面向两种国产加速器构建统一控制、分池优化的万卡训练架构。
- 建立覆盖准入、巡检、隔离、维修和复验的筛卡与健康检查闭环。
- 形成 Megatron 在不同硬件栈上的分层调优路径与可复现实验记录。
- 建立以扩展效率门限驱动的逐级放量方法，控制大规模训练中的非线性损失。
- 建立低成本常驻观测、异常窗口深挖和质量收据相结合的证据链，使万卡分析不依赖集中上传全部原始事件。

## 限制与适用范围

当前已写入部分训练配置、短程实测、健康准入汇总和文档级交付/根因证据，但硬件成员清单、完整 placement、维修闭环、端到端时间分解和长稳结果仍不完整。94.26% 只有 7 个评分步；92.43% 依赖仅 3 个有效 iteration 的 C550 独立基线；EXP-006 的 33.4% 来自缺少逐步数据、MFU 公式和重复轮的聚合 PDF。EXP-012/013 虽包含运行统计和失败栈，仍是缺少仓库内逐 rank 原始日志的会话聚合证据；MoE last5 还存在窗口敏感性，不能升级为长稳扩展曲线。C550 的 2,048-rank Final256 PASS 是集合通信验收，不是训练扩展或长稳；健康检查的 38.1% 墙钟下降来自不同 Job 的观察性对比。A3 Stall 的完整 ftrace、系统级修复回归，以及 200B/1T 的检查点与收敛评估尚未入库。AFS 主快照与原件处于同一故障域，约 22 TB 大对象、后续增量和对象存储端恢复收据尚未闭环。A3 与 C550 的单平台结果继续分别报告，加权 ECP 仅作为验收指标，不用于跨硬件性能排名。
