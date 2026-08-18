# EXP-005：A3 8192 卡建组与短程启动

## 目的

验证 Qwen3-200B 在 8192 卡、512 个节点上完成分布式建组并进入训练 iteration，识别大规模初始化故障。

## 冻结配置

两个运行均使用训练代码 commit `54daa56ad07f86e510b8be9027fcdbd9957fc998`，核心配置为 TP2/PP16/DP256/VPP2、GBS 32768、MBS 1、128 microbatches、sequence length 4096、uniform1 recompute、`tp-dp-pp` mapping，通信重叠与 offload 关闭。

## 运行结果

| 运行 | 变更 | 结果 | 可下结论范围 |
| --- | --- | --- | --- |
| r1 | 基线 | 首个 iteration 前失败；多 rank 报 `Gloo connectFullMesh failed`，部分伴随 `Transport endpoint is not connected` | 证明默认 Gloo 建组路径在该轮 8192 卡运行中失败 |
| r2 | 启动器增加 `--disable-gloo-group` | 完成建组并在保留的代表日志中到达 iteration 7/30；skipped/NaN 为 0 | 证明修正绕过了 r1 的启动阻塞并进入训练，不构成 30 步性能或长稳结论 |

r2 启动器 `launch_8192_best.sh` 在第 46 行设置 `EXTRA_MEGATRON_ARGS=--disable-gloo-group`，SHA256 为 `4d4527bf8bee8ece878b9c8725e4dd9a8287433a1e1376cdde292b7b2e0fcf24`。

## 原始证据

| 文件 | SHA256 |
| --- | --- |
| r1 `run-config.txt` | `6f8be88e36f388da958198829da88580613d8234a4b7e4b9f0be8a6ccafc19a8` |
| r1 `logs/train_pod_rank491.log` | `a1bd5bcfbd377d89bfe7610ef8dc337a14dcf11807abc257587ef260305b7dc2` |
| r2 `run-config.txt` | `22f3c2a6dd244de2dd2f7faa567d86aebf204e05002baf16a563d2602e1d5395` |
| r2 `logs/train_pod_rank511.log` | `dde8219a26cc30038cb332594dca8f9f5e2a637c2807cfd142f2ea3b1739471d` |

受控存储根为：

```text
/afs-a3-241ceshi-shared/zhongxiaolong/experiments/qwen3_200b_weak_scaling/
```

## 结论边界

- `--disable-gloo-group` 是针对本次分布式优化器建组故障的修正，不证明所有 Gloo 故障都应以同一方式处理。
- r2 代表日志只保留到 iteration 7；不得报告 8192 卡稳态均值、MFU、扩展效率或 30 步完成率。
- 正式 8192 卡验收还需完整成员收据、30 步或更长稳态结果、检查点与恢复测试。
