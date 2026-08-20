# 实验记录

每项实验使用稳定编号，并按照统一实验模板记录。建议结构：

```text
exp-001-scaling/
├── README.md
├── config/       # 脱敏后的运行配置
├── scripts/      # 运行与处理脚本
├── summary/      # 可入库的聚合数据
└── figures/      # 由数据生成的图表
```

大型原始日志通常不直接提交 Git；在实验 README 中记录受控存储位置、哈希和保留期限。

## 索引

| 编号 | 实验 | 状态 | 负责人 | 日期 | 对应章节 |
| --- | --- | --- | --- | --- | --- |
| EXP-001 | [A3 1024 卡并行与通信消融](https://github.com/reiase/tenk_report/blob/master/experiments/exp-001-a3-1024-tuning/README.md) | 已导入，待内容评审 | 待认领 | 2026-08-11 | [训练系统](05-training-and-parallelism.md)、[结果](08-results-and-analysis.md) |
| EXP-002 | [A3 4096 卡数据并行通信消融](https://github.com/reiase/tenk_report/blob/master/experiments/exp-002-a3-4096-dp-communication/README.md) | 已导入，待内容评审 | 待认领 | 2026-08-12 | [训练系统](05-training-and-parallelism.md)、[结果](08-results-and-analysis.md) |
| EXP-003 | [A3 1024 到 4096 卡弱扩展](https://github.com/reiase/tenk_report/blob/master/experiments/exp-003-a3-1024-4096-weak-scaling/README.md) | 已复核，待内容评审 | 待认领 | 2026-08-15 | [评测方法](07-evaluation-methodology.md)、[结果](08-results-and-analysis.md) |
| EXP-004 | [10240 卡异构资源池加权验收](https://github.com/reiase/tenk_report/blob/master/experiments/exp-004-tenk-weighted-acceptance/README.md) | 已复核，基线有限制 | 待认领 | 2026-08-17 | [评测方法](07-evaluation-methodology.md)、[结果](08-results-and-analysis.md) |
| EXP-005 | [A3 8192 卡建组与短程启动](https://github.com/reiase/tenk_report/blob/master/experiments/exp-005-a3-8192-startup/README.md) | 部分通过，长稳待执行 | 待认领 | 2026-08-12 | [训练系统](05-training-and-parallelism.md)、[工程经验](10-lessons-learned.md) |
| EXP-006 | [A3 2048 die 并行策略与 MFU 分析](https://github.com/reiase/tenk_report/blob/master/experiments/exp-006-a3-2048die-parallelism-mfu/README.md) | 已导入，文档级证据；原始数据待补 | 待认领 | 2026-08-17 | [训练系统](05-training-and-parallelism.md)、[结果](08-results-and-analysis.md) |
| EXP-007 | [A3 前向进展 Stall 定位与缓解](https://github.com/reiase/tenk_report/blob/master/experiments/exp-007-a3-forward-progress-stall/README.md) | 根因文档内闭环；原始 ftrace 待归档 | 待认领 | 2026-08-20 | [稳定性](06-reliability-and-observability.md)、[结果](08-results-and-analysis.md) |
| EXP-008 | [C550 Stall 与大规模通信尾延迟](https://github.com/reiase/tenk_report/blob/master/experiments/exp-008-c550-stall-and-communication-tail/README.md) | 已导入，文档级证据；direct dispatch 待独立复核 | 待认领 | 2026-08-20 | [网络](04-cluster-network-storage.md)、[稳定性](06-reliability-and-observability.md) |
| EXP-009 | [200B Dense 与 1T MoE 交付证据](https://github.com/reiase/tenk_report/blob/master/experiments/exp-009-200b-1t-delivery-evidence/README.md) | 功能运行文档级证据；性能与收敛待补 | 待认领 | 2026-08-20 | [训练系统](05-training-and-parallelism.md)、[结果](08-results-and-analysis.md) |
| EXP-010 | [A3 与 C550 资源池健康准入](https://github.com/reiase/tenk_report/blob/master/experiments/exp-010-fleet-health-admission/README.md) | 已导入，文档级准入证据；成员清单与原始结果待补 | 待认领 | 2026-08-20 | [稳定性](06-reliability-and-observability.md)、[结果](08-results-and-analysis.md) |
| EXP-011 | [大规模健康检查耗时与运行时优化](https://github.com/reiase/tenk_report/blob/master/experiments/exp-011-healthcheck-runtime-optimization/README.md) | 已导入，观察性运行时对比；同节点随机化 A/B 待补 | 待认领 | 2026-08-20 | [稳定性](06-reliability-and-observability.md)、[工程经验](10-lessons-learned.md) |
| EXP-012 | [A3 4096 卡 TP2/PP16 Dense 运行复核](https://github.com/reiase/tenk_report/blob/master/experiments/exp-012-a3-4096-tp2pp16-dense/README.md) | 会话日志聚合；原始逐 rank 日志待恢复 | 待认领 | 2026-08-20 | [训练系统](05-training-and-parallelism.md)、[结果](08-results-and-analysis.md) |
| EXP-013 | [A3 Qwen3-1T MoE 1024--4096 卡调优](https://github.com/reiase/tenk_report/blob/master/experiments/exp-013-a3-qwen3-1t-moe-tuning/README.md) | 会话日志聚合；长稳、检查点与重复轮待补 | 待认领 | 2026-08-20 | [训练系统](05-training-and-parallelism.md)、[结果](08-results-and-analysis.md) |
| EXP-014 | [训练实验资产备份与恢复状态](https://github.com/reiase/tenk_report/blob/master/experiments/exp-014-training-assets-backup/README.md) | AFS 主快照已校验；增量与对象存储副本未完成 | 待认领 | 2026-08-20 | [工程经验](10-lessons-learned.md)、[复现](appendix-b-reproducibility.md) |
