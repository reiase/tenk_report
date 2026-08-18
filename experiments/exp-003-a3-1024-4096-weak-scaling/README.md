# EXP-003：A3 1024 到 4096 卡弱扩展

## 目的

在模型、软件版本、序列长度、并行组合和单卡 batch 不变的条件下，将卡数与 GBS 同时扩大 4 倍，计算 Qwen3-200B 从 1024 卡到 4096 卡的弱扩展效率。

## 冻结配置

| 配置 | 1024 卡 | 4096 卡 |
| --- | ---: | ---: |
| Git commit | `54daa56ad07f86e510b8be9027fcdbd9957fc998` | 同左 |
| TP / PP / DP / VPP | 1 / 64 / 16 / 2 | 1 / 64 / 64 / 2 |
| GBS / MBS | 4096 / 1 | 16384 / 1 |
| microbatches | 256 | 256 |
| sequence length | 4096 | 4096 |
| recompute | block1 | block1 |
| mapping | tp-pp-dp | tp-pp-dp |
| grad / param overlap | on / off | on / off |
| HCCL RoCE / PCIe | 1 / 0 | 1 / 0 |

平台任务分别为 `qwen3-200b-tp1pp64-1024-opt-t3` 与 `qwen3-200b-tp1pp64-4096-opt-t3`。RUN_ID、逐步结果与哈希见 [summary.tsv](summary.tsv)。

## 统计窗口与结果

两个任务均完成 12 个 iteration。为排除启动阶段，预注册统计窗口取共同的 iteration 6--12，共 7 个样本；不删除 4096 卡 iteration 9 的低点。

| 指标 | 1024 卡 | 4096 卡 |
| --- | ---: | ---: |
| 平均 TFLOPS/GPU | 108.5571 | 102.3286 |
| 平均 step 时间 | 185.822 s | 197.208 s |
| skipped / NaN 最大计数 | 0 / 0 | 0 / 0 |

由于卡数和 GBS 均扩大 4 倍，单卡工作量保持不变，弱扩展效率可以直接用每卡吞吐之比计算：

\[
E_{1024\rightarrow4096}
=\frac{102.3286}{108.5571}
=94.2624\%.
\]

步时倒数口径得到 94.23%，与每卡吞吐口径一致。正式报告取 **94.26%**。

## 原始证据

受控存储根：

```text
/afs-a3-241ceshi-shared/zhongxiaolong/experiments/qwen3_200b_weak_scaling/
```

| 文件 | SHA256 |
| --- | --- |
| 1024 `run-config.txt` | `95bd671347cee6e7e80e054b7894bacb5da948d97b6a55cba1071cafa66bdce8` |
| 1024 `logs/train_pod_rank63.log` | `17af56dc7dca3a8d1abca2ae42ffa2e9e3b512c5b5c3abbd754b5a3997378eeb` |
| 4096 `run-config.txt` | `4052863c36ff90370895ce4c599968567dce94019f254e2ddd0d003a5a371020` |
| 4096 `logs/train_pod_rank255.log` | `c3a3523dfaf311f5033da53dc0943db13ad942db16d41bc175699dd547f6bc14` |

## 结论边界

- 该结果只有 7 个评分 iteration，适用于短程性能验收，不等同于长稳或端到端训练效率。
- iteration 9 的低点已保留；删除该点会把结果提高到约 95.02%，但没有预注册排除依据。
- 未形成随机化 placement 重复轮，不能量化资源组与时间漂移对 94.26% 的影响。
