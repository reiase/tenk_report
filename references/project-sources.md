# 受控项目材料

以下材料包含内部环境信息或大体积运行证据，不直接提交 Git。仓库保留脱敏标题、内容哈希和结论边界；原件位于受控交付目录 `3rd/`、`ZWS/` 或 `ZCX/`。

## S001

- 标题：A3 单卡前向进展 Stall 分析
- 原件：`3rd/a3 stall.md`
- SHA256：`3a9a2a78c9cec4a79bd4d55414b24769babae214c7c18624c1fb292a4ac994a3`
- 支撑内容：512/1,024 卡事件率、宽度分布、空间集中度、训练传播和对照实验

## S002

- 标题：A3 512 卡节点热点剔除实验
- 原件：`3rd/a3 512.md`
- SHA256：`4082e9d4e610ef4ad418bebbb76fb82587de990ae551d475a3cf1de502cec604`
- 支撑内容：125M、8B Dense 与 MoE 的热点/随机/冷点节点剔除对比

## S003

- 标题：C550 单卡 Stall 与大规模通信尾延迟分析
- 原件：`3rd/c550 stall.md`
- SHA256：`f09b1ab756eca615338b5695a8b0d067807cb92619816167b56fe14a5de11864`
- 支撑内容：64 卡探针事件率、256/512 卡 AllReduce 重复和 QP 消融

## S004

- 标题：A3 异常 Stall 与训练调优汇总
- 原件：`3rd/异常-stall-分析.pdf`
- SHA256：`34aef9c4c840766a656325d6140abf07c892bf41b17be3248a2172528c545457`
- 支撑内容：训练侧 Stall 图表、TaskQueue 与内存分配器消融

## S005

- 标题：A3 NPU 训练 Stall 根因定位报告
- 原件：`3rd/a3-stall-root-cause.docx`
- SHA256：`ba9fe59b45b8e76282b187bdc2acd74a5c973013460df0af74c233a4a56d0cc3`
- 支撑内容：IPVS `estimation_timer`、TIMER_SOFTIRQ、NPU CQ IRQ/tasklet 的 ftrace 因果链
- 备注：完整 ftrace 未入库，按“文档内闭环、原始证据待归档”使用

## S006

- 标题：A3 NPU 训练 Stall 临时优化方案
- 原件：`3rd/a3-stall-mitigation.docx`
- SHA256：`d2611bfa72b2cf0e04cc547cfe8b51b7cd48809631067a30956ea692fe15a005`
- 支撑内容：TaskQueue level 2、jemalloc 与组合消融

## S007

- 标题：C550 Stall 厂商说明
- 原件：`3rd/c550-stall-vendor-note.pdf`
- SHA256：`f7d8ed0d814cb7041677f7b054c0fb85b93171e06b0b719dcdc7850bdfaa99a9`
- 支撑内容：direct/non-direct dispatch 路径、复测说明和 CUDA Graph 建议

## S008

- 标题：200B Dense 与 1T MoE 模型交付记录
- 原件：`ZWS/200b-1t-delivery.pdf`
- SHA256：`7cd148d6508e40d812d9c4a667410de1cf858b7a5ce5ace8fc0d6def69f6cfc1`
- 支撑内容：模型参数量、1,024/2,048 die 功能运行和 loss 曲线截图

## S009

- 标题：八组混训编排与运行材料
- 原件：`ZWS/tenk-mixed-run-material.pdf`
- SHA256：`858d90f35329d3cc9260b9cd95632228ef7debadc7de0166315988da782db5e3`
- 支撑内容：八个训练组、64 个参数服务器、组规模、训练步数与同步周期
- 备注：原件含内部地址和执行路径，不入 Git

## S010

- 标题：200B Dense 与 1T MoE 模型及容量估算
- 原件：`ZWS/model-sizing.pdf`
- SHA256：`258f29c5864fa85fd6ab7ce6ded006efe2ae4d5578a5b55f0fac4cebab6c943a`
- 支撑内容：参数量公式、候选并行度和检查点容量估算

## S011

- 标题：C550 万卡混训问题记录
- 原件：`ZWS/c550-mixed-training-issues.pdf`
- SHA256：`2e043dda8de4c7d0249bb6cc0336064ba04bf497f5741b25336b9891f7c027d2`
- 支撑内容：object collective 异常长度、RDMA retry exceeded 与临时处置

## S012

- 标题：C550 调参实验与日志索引
- 原件：`ZWS/c550-tuning-log-index.pdf`
- SHA256：`b8ba9bba0fca549aee61dce3cf83c906d0b0d949b266d53eb63aed606dc45804`
- 支撑内容：200B/1T 短程运行环境、脚本和日志索引

## S013

- 标题：A3 8192 卡及备机健康检测报告
- 原件：`ZCX/华为8192卡(含备机)健康检测报告.pdf`
- SHA256：`db3b0e31f0f5608724d63b32aff80657a3808e606213625d8f247cc36cb49153`
- 支撑内容：两个 4,096 卡批次与 96 卡备机的 static、dynamic-suite、CARD_SCREEN、stall-screen、Pairwise 和 topology 汇总
- 备注：原件含内部主机名和结果路径，不入 Git；成员清单与逐卡原始结果待归档

## S014

- 标题：C550 2048 卡及备机健康检测报告
- 原件：`ZCX/沐曦2048卡(含备机) 健康检测报告.pdf`
- SHA256：`a4a83eadbcf8cbf3f77b83fc5267521ef751c17c21fc437bb2874b2a9c8284a0`
- 支撑内容：2,336 卡候选池筛查、设备与通信异常分类、256 节点选择和 2,048-rank topology 验收
- 备注：累计 ECC、性能候选与运行期通信错误保持独立状态，不合并为硬件故障率

## S015

- 标题：大规模健康检查耗时过长原因分析
- 原件：`ZCX/健康检查耗时过长原因分析.pdf`
- SHA256：`00d12222c5a039563352cda9e477d4886b9940f0c95cc8c37762a84f5bbcdc49`
- 支撑内容：Pairwise 执行波次、AFS SQLite 竞争、round barrier、超时/复测和结果回收的耗时分解
- 备注：2,048 节点 Pairwise 约 19 分钟为模型估算，不是生产实测 SLA

## S016

- 标题：健康检查运行时优化效果
- 原件：`ZCX/优化后健康检测效果.pdf`
- SHA256：`75f42a88e34bc7d995b7d9f5f93e7f7fd8be13a6fed7487a62c9c135ef632223`
- 支撑内容：64 节点相同训练拓扑下旧版 1,706 秒与 main 1,056 秒的完整流水线对比，以及短连接、本地热数据、状态机和分块校验机制
- 备注：两轮 Job、物理节点、Pairwise 计划和尾部事件不同；38.1% 仅作为受混杂影响的观察值

## S017

- 标题：Codex 会话“读取开发指引会话”完整记录
- 会话 ID：`019feff2-df01-7732-9b47-a9bf6767960a`
- 原件：本机 Codex 会话 JSONL，不提交 Git
- 记录时间：2026-08-11 至 2026-08-20
- 文件大小：260,986,231 bytes
- SHA256：`7b1a143815a80cae11b84d4ad929e2bef4a6ae1fc06fc151ff871c9151234489`
- 完整性复核：流式读取 9,852 条 JSONL，0 条解析失败；包含 144 条用户消息、134 条最终答复和 24 次上下文压缩
- 支撑内容：Qwen3-200B 4096 卡 TP2/PP16 运行复核、Qwen3-1T MoE 1024/2048/4096 卡调优与故障边界、实验资产备份和对象存储迁移状态
- 备注：会话同时保存命令、工具输出、过程判断和建议脚本。只有能回到关联工具输出、运行目录或校验结果的条目进入结果表；仅有建议或助手推断的内容不作为已执行事实。该来源仍是二级聚合证据，不能替代原始逐 rank 日志、配置快照和存储端校验收据。
