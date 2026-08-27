# 实验记录

实验编号用于关联训练配置、统计窗口、聚合结果和工程材料。十四组实验共同构成资源准入、训练性能、规模扩展、稳定性与资产管理的结果体系。

## 实验索引

| 编号 | 实验 | 规模/对象 | 核心结果 | 日期 |
| --- | --- | --- | --- | --- |
| EXP-001 | [A3 并行与通信消融](https://github.com/reiase/tenk_report/blob/master/experiments/exp-001-a3-1024-tuning/README.md) | 1,024 卡 | mapping0 五组配对均高于 mapping1，最高 135.00 TFLOPS/GPU | 2026-08-11 |
| EXP-002 | [A3 数据并行通信消融](https://github.com/reiase/tenk_report/blob/master/experiments/exp-002-a3-4096-dp-communication/README.md) | 4,096 卡 | no-overlap 与 bucket-128m 形成候选 | 2026-08-12 |
| EXP-003 | [A3 弱扩展](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md) | 1,024→4,096 卡 | 弱扩展效率 94.26% | 2026-08-15 |
| EXP-004 | [异构资源池加权验收](https://github.com/reiase/tenk_report/blob/master/experiments/exp-004-tenk-weighted-acceptance/README.md) | 10,240 卡纳管规模 | 共同窗口加权 ECP 92.43% | 2026-08-17 |
| EXP-005 | [A3 目标规模启动](https://github.com/reiase/tenk_report/blob/master/experiments/exp-005-a3-8192-startup/README.md) | 8,192 卡 | 完成通信建组并进入 iteration 7 | 2026-08-12 |
| EXP-006 | [A3 并行策略与 MFU](https://github.com/reiase/tenk_report/blob/master/experiments/exp-006-a3-2048die-parallelism-mfu/README.md) | 2,048 die | TP2/PP16/uniform1 达到 MFU 33.4% | 2026-08-17 |
| EXP-007 | [A3 前向进展 Stall](https://github.com/reiase/tenk_report/blob/master/experiments/exp-007-a3-forward-progress-stall/README.md) | 512/1,024 卡探针 | 定位 IPVS timer 与 NPU CQ tasklet 竞争 | 2026-08-20 |
| EXP-008 | [C550 Stall 与通信尾延迟](https://github.com/reiase/tenk_report/blob/master/experiments/exp-008-c550-stall-and-communication-tail/README.md) | 64/256/512 卡 | Stall P50 212.6 ms，形成 direct dispatch 优化方向 | 2026-08-20 |
| EXP-009 | [200B Dense 与 1T MoE 运行](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) | 1,024/2,048 die | 完成 800/800 与 500/500 step | 2026-08-20 |
| EXP-010 | [双资源池健康准入](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) | A3 8,192 卡、C550 2,336 卡 | 完成分层筛查与 C550 Final256 | 2026-08-20 |
| EXP-011 | [健康检查运行时优化](https://github.com/reiase/tenk_report/blob/master/experiments/exp-011-healthcheck-runtime-optimization/README.md) | 64--292 节点 | 64 节点流水线 1,706→1,056 秒 | 2026-08-20 |
| EXP-012 | [A3 4,096 卡 Dense 复核](https://github.com/reiase/tenk_report/blob/master/experiments/exp-012-a3-4096-tp2pp16-dense/README.md) | 4,096 卡 | 124.264 TFLOPS/GPU，CV 1.68% | 2026-08-20 |
| EXP-013 | [A3 Qwen3-1T MoE 调优](https://github.com/reiase/tenk_report/blob/master/experiments/exp-013-a3-qwen3-1t-moe-tuning/README.md) | 1,024--4,096 卡 | last5 为 65.60/61.82/57.66 TFLOPS/GPU | 2026-08-20 |
| EXP-014 | [训练资产快照与校验](https://github.com/reiase/tenk_report/blob/master/experiments/exp-014-training-assets-backup/README.md) | 工程资产 | 10 tar、6 bundle、75 SHA256 全部通过 | 2026-08-20 |

实验结论在[结果与分析](08-results-and-analysis.md)中按统一指标口径汇总。
