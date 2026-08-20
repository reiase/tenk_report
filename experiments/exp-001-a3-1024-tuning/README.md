# EXP-001：A3 1024 卡并行与通信消融

## 目的

在 Qwen3-200B、1024 卡和固定训练版本下，比较 rank mapping、重计算、梯度/参数通信重叠、TaskQueue 与 HCCL 链路开关对稳态吞吐的影响。

## 证据与口径

- 原始汇总：`_sweeps/qwen3-200b-1024-long-r2/summary.tsv`
- 受控存储根：`/afs-a3-241ceshi-shared/zhongxiaolong/experiments/qwen3_200b_weak_scaling/`
- 原始汇总 SHA256：`0ffedff5990efee1f9c4df30f2264588a1737bb872097c8a2665535165ebfac6`
- 长跑用例均配置 20 个 iteration，评分窗口为末 5 个有效 iteration。
- `failed_pods=0`、有效样本完整且 `status=PASS` 的用例才进入性能比较。

可入库聚合见 [summary.tsv](summary.tsv)。原始逐 rank 日志不提交 Git。

## 结果

| 对比 | mapping0（TFLOPS/GPU） | mapping1（TFLOPS/GPU） | mapping0 相对优势 |
| --- | ---: | ---: | ---: |
| TP1 + block | 109.68 | 108.98 | 0.64% |
| TP8 + uniform | 109.62 | 108.78 | 0.77% |
| TP1 + uniform | 109.86 | 107.60 | 2.10% |
| TP8 + block | 135.00 | 129.86 | 3.96% |
| TP1 + HCCL PCIe | 109.88 | 107.58 | 2.14% |

在本轮中，`mapping0` 在五组直接配对对比中均更高。TP8 + block + mapping0 达到 135.00 TFLOPS/GPU，是本轮最高值；该结果同时改变了并行与重计算条件，不能把全部收益单独归因给 mapping。

TP1 基线复测为 109.92 TFLOPS/GPU，相对首次 109.68 高 0.22%。因此 0.64% 和 0.77% 的小差异需要更多重复轮确认；2.10% 至 3.96% 的 mapping 差异更值得进入拓扑 A/B 复测。

`tp1-no-grad-overlap` 的 64 个 pod 全部失败，不能据此判断关闭梯度重叠的性能。`full-overlap`、`no-param-overlap`、`no-overlap` 与 TaskQueue 变体在 TP1 组的末 5 步均值差异很小，仍需随机化顺序和重复运行排除时间漂移。

S017 的完整会话复核还发现命名边界：运行器中的 `mapping0/1` 对应 `USE_TP_PP_DP_MAPPING=0/1` 开关，但历史日志另有 `MAPPING=tp-dp-pp` 等人类可读标签，二者未归档成一一对应的 resolved command 与代码路径。因此本实验保留 `mapping0/1` 作为用例名，不将 `mapping0` 直接定义为某个 rank-order 字符串。

## 结论边界

- 这是短窗口性能消融，不是长稳训练、收敛或端到端吞吐结论。
- 汇总没有冻结硬件批次、物理 placement 和外部网络负载，不能把小于约 1% 的差异直接写成稳定收益。
- `mapping0` 的优势需要与实际超节点和 rank placement 快照关联后才能完成因果归因。
