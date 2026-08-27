# 架构决策记录

架构决策用于固化万卡训练中的关键技术取舍，使资源组织、性能评价和故障处置保持一致。

## 决策索引

| 编号 | 决策 | 技术依据 | 应用章节 |
| --- | --- | --- | --- |
| ADR-0001 | A3 与 C550 采用统一控制、异构分池 | 两类硬件互连与软件栈不同 | [总体架构](02-system-architecture.md) |
| ADR-0002 | 单平台性能分别建模，协同层采用加权 ECP | 保持基线可比性并评价万卡协同 | [评测方法](07-evaluation-methodology.md) |
| ADR-0003 | 健康准入先于训练放量 | 同步训练对慢卡与异常链路高度敏感 | [稳定性](06-reliability-and-observability.md) |
| ADR-0004 | 并行组与物理拓扑联合固化 | rank mapping 直接影响通信路径 | [HCCL 优化](04a-a3-hccl-communication-optimization.md) |
| ADR-0005 | 常驻轻量观测与短窗口深度采集分层 | 控制万 rank 观测开销 | [通信观测](06a-training-communication-observability.md) |
| ADR-0006 | 启动、稳态、功能运行和长周期指标分层 | 分阶段评价系统能力 | [结果与分析](08-results-and-analysis.md) |
