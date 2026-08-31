# EXP-002：A3 4096 卡数据并行通信消融

## 目的

在 Qwen3-200B、TP8/PP8、4096 卡和固定 GBS 16,384 下，比较梯度/参数通信重叠和 DDP bucket 配置对稳态吞吐的影响。

## 证据与口径

- 原始汇总：`_sweeps/qwen3-200b-tp8pp8-4096-dpcomm-r1/summary.tsv`
- 受控存储根：`/afs-a3-241ceshi-shared/zhongxiaolong/experiments/qwen3_200b_weak_scaling/`
- 原始汇总 SHA256：`5065051e86e1a5b153cf5ca17fed7d2aca6fb4babd431d60dca2e86caa50ab88`
- 每个有效用例覆盖 256 个日志文件，取 iteration 6--30，共 25 个稳态样本。
- 所有 PASS 用例的 skipped 与 NaN 最大计数均为 0。

可入库聚合见 [summary.tsv](summary.tsv)。

## 结果

| 用例 | 平均 TFLOPS/GPU | 中位 TFLOPS/GPU | CV | 相对 no-param-overlap-a |
| --- | ---: | ---: | ---: | ---: |
| full-overlap-a | 104.148 | 103.5 | 2.11% | -0.39% |
| no-param-overlap-a | 104.556 | 104.3 | 2.67% | 基线 |
| bucket-32m | 102.984 | 103.0 | 2.99% | -1.50% |
| bucket-128m | 110.152 | 110.6 | 2.18% | +5.35% |
| no-align-grad-64m | 108.608 | 108.0 | 1.89% | +3.88% |
| no-overlap | 111.764 | 112.1 | 2.51% | +6.89% |
| no-param-overlap-b | 106.304 | 105.3 | 2.38% | +1.67% |

本轮最高均值来自 `no-overlap`，比首个 `no-param-overlap-a` 高 6.89%；`bucket-128m` 高 5.35%。同一 `no-param-overlap` 的重复轮次相差 1.67%，且计划中的 `full-overlap-b` 没有数据，因此实验顺序和资源组差异作为复测因子保留。

## 适用范围

- 当前结果支持把 `no-overlap` 和 `bucket-128m` 送入随机化复测，通信重叠的默认策略由复测后的同条件比较确定。
- `full-overlap-b=NO_DATA` 保留在实验分母中，与完成用例共同构成实验矩阵。
- 正式默认值应由相同 placement 下的交错 A/B 和至少一轮重复确认。
