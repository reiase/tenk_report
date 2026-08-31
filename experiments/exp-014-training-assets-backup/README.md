# EXP-014：训练实验资产备份与恢复状态

## 目的

记录 Qwen3-200B、Qwen3-1T MoE 与 DeepSeek-V3 Midtrain 的代码、日志和复现材料在资源回收前的备份范围、校验结果、未纳入对象以及对象存储迁移阻塞，避免把“AFS 内已备份”误写成“跨故障域归档完成”。

## 来源与证据等级

- 聚合来源：[S017](../../references/project-sources.md#s017)
- 主快照：`full_training_project_20260817_232003`
- 主快照受控位置：`/afs-a3-241ceshi-shared/zhongxiaolong/backups/`
- 可入库状态表：[summary.tsv](summary.tsv)

会话中保存了远端 `tar`、Git bundle 和 SHA256 校验输出，但归档本体不在 Git 中。本记录证明“来源会话观察到哪些校验通过”，不等同于当前机器已重新下载并逐文件复验。

## 全量快照

主快照覆盖：

- Qwen3-200B 的 1024/4096/8192 卡探索、消融、offload、拓扑与 ECP 日志；
- Qwen3-1T MoE 与早期 Qwen3-235B MoE 日志、配置和 repro；
- DeepSeek-V3 smoke、2048 卡探索和 Midtrain 代码/日志；
- `zhongxiaolong/workspace` 中的 Git 元数据、未提交修改、未跟踪代码和运行环境；
- 实际使用的 Megatron、MindSpeed、MindSpeed-LLM 代码、工具源码、数据清单和历史日志；
- 启动脚本、resolved 配置、拓扑、TensorBoard 和分析结果。

校验结果：10/10 个 tar 归档可遍历，6/6 个 Git bundle 通过完整性检查，75/75 项 SHA256 通过，0 失败，总大小约 2.6 GB。Qwen3-200B 覆盖核查识别 10,202 个 1024 路径项、19,357 个 4096 路径项、2,061 个 8192 路径项、12,112 个训练日志和 3 份 `summary.tsv`。

代码版本记录为：

```text
Megatron  54daa56ad07f86e510b8be9027fcdbd9957fc998
MindSpeed 2b38a9e99dd91b1fd99be0ac89589b4166797947
```

备份目录还生成了 `docs/backup_and_repro_guide.md`，来源会话核验为 414 行、约 15 KB、UTF-8 无 BOM，包含校验、恢复、关键实验启动模板、统计口径和常见故障判断。

此前的 `qwen3_1tb_moe_20260817_230336` 快照为约 1.6 GB，44/44 项 SHA256 通过；它被后续全项目快照覆盖，不再作为唯一恢复入口。

## 大对象清单

为避免在同一 AFS 内重复占用容量，主快照对约 22 TB 的 checkpoint、模型权重、派生训练数据和约 84 GB 原始 profiler 数据保存文件清单。清单证明当时已识别对象；跨存储保全和逐文件内容哈希由对象存储迁移阶段完成。

全量快照时间为 2026-08-17 23:20:03。之后完成的 1T MoE 4096 卡 no-Gloo/bucket 结果通过 `incremental_after_20260817_232003_*` 增量包补齐。S017 保存了增量命令和迁移计划，增量包校验收据随迁移闭环归档。

## 对象存储迁移状态

AFS 主快照与原始资料位于同一存储故障域，可防止 Pod、任务或代码目录被回收。跨故障域对象存储迁移登记为独立交付项：训练资源已回收，旧 SSH 入口失效，AIS 开发机创建缺少 `ais.aiSpace.create` 权限，需要一台同时挂载 AFS 与对象存储的临时 CPU 节点执行迁移。

恢复迁移后依次完成：

1. 在单副本 CPU 节点同时挂载 AFS 与对象存储；
2. 生成并校验 2026-08-17 23:20:03 之后的增量包；
3. 上传主快照与增量，不在命令、日志或仓库中保存 AK/SK；
4. 在目标端执行对象数量/容量对账、SHA256、tar 遍历、Git bundle 和抽样恢复；
5. 只有取得目标端完整收据后，才能释放 AFS 或把状态改为 COMPLETE。

## 适用范围

- 2.6 GB 是归档后的工程资产规模，不包含约 22 TB 大对象和 84 GB profiler 原件。
- 75/75 SHA256 是主快照校验项，不代表 22 TB 清单对象都做了内容校验。
- 全量快照晚于多数 Dense/MoE 实验，但早于最后几组 1T MoE 4096 卡结果；增量状态独立跟踪。
- 本仓库不记录访问凭证、内部 Endpoint 或密钥截图内容；凭证暴露与轮换属于独立安全事项。
