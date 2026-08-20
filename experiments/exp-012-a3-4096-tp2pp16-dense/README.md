# EXP-012：A3 4096 卡 TP2/PP16 Dense 运行复核

## 目的

补齐 Qwen3-200B 在 4096 卡上采用 TP2/PP16/uniform1 的日志级运行摘要，并把它与 EXP-006 的 2048 die 聚合结果、EXP-002 的 TP8/PP8 通信消融分开管理。

## 来源与证据等级

- 聚合来源：[S017](../../references/project-sources.md#s017)
- 受控运行目录：`qwen3_200b_weak_scaling/qwen3-200b-4096-pargrid-r1-01-tp2pp16-uniform1`
- 可入库聚合：[summary.tsv](summary.tsv)

S017 中保存了远端目录核验、逐 iteration 聚合和最终统计，但本仓库没有复制 513 个运行文件或逐 rank 日志。本记录因此标为 `session_log_aggregate`：高于只有截图/表格的文档级摘录，低于仓库可直接重算的原始日志证据。

## 冻结配置

| 项目 | 值 |
| --- | --- |
| 模型 | Qwen3-200B Dense |
| 规模 | 4,096 卡，256 Worker x 16 卡 |
| 并行 | TP2 / PP16 / DP128 / VPP2 |
| 批次 | MBS1 / GBS16384 / 每 DP 副本 128 microbatches |
| 重计算 | uniform，`recompute-num-layers=1` |
| 通信开关 | gradient overlap 关闭、parameter gather overlap 关闭 |
| 运行时 | TaskQueue=2、HCCL RoCE 开启、HCCL PCIe 关闭 |
| 训练步数 | 30；iteration 6--30 进入稳态统计 |

运行脚本记录 `USE_TP_PP_DP_MAPPING=0`。该值只证明开关状态，不足以单独恢复当时代码中最终 rank-order 字符串；`mapping0`、`mapping1` 和日志中的人类可读别名在归档 resolved command 与对应代码前不能互换使用。

## 主要结果

| 指标 | 结果 |
| --- | ---: |
| 完成情况 | 30/30，PASS |
| 稳态样本 | 25 个 iteration |
| TFLOPS/GPU 算术均值 | **124.264** |
| TFLOPS/GPU 时间加权均值 | 124.230 |
| TFLOPS/GPU 中位数 | 124.2 |
| TFLOPS/GPU 最小 / 最大 | 120.8 / 127.4 |
| 稳态 CV | 1.68% |
| 平均 iteration 时间 | 162.398 秒 |
| P95 iteration 时间 | 166.961 秒 |
| skipped / NaN | 0 / 0 |
| 峰值 allocated / reserved | 49.78 / 50.80 GB |

按来源会话沿用的约 372 TFLOPS 理论峰值口径，124.264 TFLOPS/GPU 对应约 33.4% MFU。由于 MFU 公式和理论峰值没有随原始运行一并归档，本记录以 TFLOPS/GPU 为主指标，MFU 只保留为口径化近似值。

## 与 TP8/PP8 的方案级比较

同一会话中的 r6 候选为 TP8/PP8/VPP4/block1/no-overlap，iteration 6--30 平均 111.764 TFLOPS/GPU、180.625 秒/步、CV 2.51%。TP2/PP16 方案相对提高 11.18%，平均步时降低 10.09%，波动也更低。

这不是单变量 TP 消融：PP、DP、VPP、microbatch 数和重计算方法同时变化。因此可支持的结论是“本轮 TP2/PP16 整套方案优于已测 TP8/PP8 方案”，不能把 11.18% 全部归因于降低 TP。

EXP-006 在 2048 die、GBS8192、MBS1、VPP2 下也报告 TP2/PP16/uniform1 为 33.4% MFU。两边在一位小数上相同，支持继续复测其弱扩展方向；但 EXP-006 使用 `die`、只有聚合 PDF，且两边 MFU 公式与逐步窗口未共同冻结，当前不报告精确的 2048→4096 弱扩展效率。

## 结论边界

- 这是 25 个稳态步的短程结果，不证明长稳、检查点恢复、端到端吞吐或收敛。
- `host_ip` 与 `superpod` 在当时 topology 摘要中为 `unknown`，不能排除 placement 对结果的贡献。
- MFU 约 33.4% 依赖来源会话中的理论峰值口径；正式复跑需归档 FLOPs 公式、理论峰值和是否计入重计算。
- 运行目录在共享 AFS 中被现场核验，后续又进入全量备份清单；本仓库仍缺原始逐 rank 日志，不能独立重算 25 个点。
