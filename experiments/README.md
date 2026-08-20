# 实验记录

实验索引统一维护在 [技术报告实验记录](../docs/experiments.md)。具体实验数据和受控摘要按实验编号保存在本目录：

- [EXP-001：A3 1024 卡并行与通信消融](exp-001-a3-1024-tuning/README.md)
- [EXP-002：A3 4096 卡数据并行通信消融](exp-002-a3-4096-dp-communication/README.md)
- [EXP-003：A3 1024 到 4096 卡弱扩展](exp-003-a3-1024-4096-weak-scaling/README.md)
- [EXP-004：10240 卡异构资源池加权验收](exp-004-tenk-weighted-acceptance/README.md)
- [EXP-005：A3 8192 卡建组与短程启动](exp-005-a3-8192-startup/README.md)
- [EXP-006：A3 2048 die 并行策略与 MFU 分析](exp-006-a3-2048die-parallelism-mfu/README.md)
- [EXP-007：A3 前向进展 Stall 定位与缓解](exp-007-a3-forward-progress-stall/README.md)
- [EXP-008：C550 Stall 与大规模通信尾延迟](exp-008-c550-stall-and-communication-tail/README.md)
- [EXP-009：200B Dense 与 1T MoE 交付证据](exp-009-200b-1t-delivery-evidence/README.md)
- [EXP-010：A3 与 C550 资源池健康准入](exp-010-fleet-health-admission/README.md)
- [EXP-011：大规模健康检查耗时与运行时优化](exp-011-healthcheck-runtime-optimization/README.md)

原始大日志不提交 Git。每项记录必须给出受控位置、内容哈希、统计窗口和结论边界，使仓库内聚合可回到原始证据。
