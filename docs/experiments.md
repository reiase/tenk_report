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
