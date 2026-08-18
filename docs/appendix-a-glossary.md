---
title: 术语与缩略语
status: draft
owner: unassigned
reviewers: []
last_updated: 2026-08-16
---

# 术语与缩略语

本表是全篇术语的权威来源。新增缩略语时先在首次出现处展开，再链接或收录到这里。

| 术语 | 英文或缩写 | 本报告定义 | 备注 |
| --- | --- | --- | --- |
| 万卡规模 | 10K-scale | 两个独立资源池可纳管的设备总数 | 不表示异构设备共同执行一个同步作业 |
| 模型 FLOPs 利用率 | MFU | 单位时间完成的模型有效 FLOPs 除以声明精度下的设备聚合理论峰值 | 通常不把重计算视为模型有效 FLOPs |
| 硬件 FLOPs 利用率 | HFU | 单位时间实际执行的 FLOPs 除以声明精度下的设备聚合理论峰值 | 需说明是否计入重计算和辅助算子 |
| 有效训练时间占比 | Effective training time ratio | 形成可保留训练进度的设备时间除以已分配设备时间 | 不与集群可用率混用 |
| 扩展效率 | Scaling efficiency | 相对基准规模的吞吐加速比除以设备数量倍率 | 强扩展与弱扩展分别报告 |
| 健康证据向量 | Health evidence vector | 在冻结条件下分别表示正确性、可持续能力与前向进展的证据集合 | 不压缩为跨故障域通用的单一分数 |
| 性能包络 | Performance envelope | 由计算吞吐、算术强度、有效 HBM 带宽及功率热状态共同限定的可持续性能范围 | 厂商峰值仅是包络上界之一 |
| 算术强度 | Arithmetic intensity | 单位数据搬运字节对应的浮点运算量，通常记为 FLOPs/Byte | 用于区分计算受限与带宽受限负载 |
| 达质时间/能耗 | TTQ / ETQ | 达到预注册模型质量门限所需的墙钟时间与累计能量 | 比较训练方案时须保持质量门限一致 |
| 算法带宽 | AlgBW | collective 有效 payload 除以执行时间 | payload 解释随 collective 变化 |
| 总线带宽 | BusBW | 由 AlgBW 按 collective 和 group size 换算的链路负载指标 | 不是物理链路逐端口实测值 |
| 单卡测试 HBM 有效带宽 | Effective HBM bandwidth | 流式读取、简单变换和写回的名义总字节数除以设备执行时间 | 不是厂商原始 HBM 峰值，也不是 scale-up 互连带宽 |
| 静默数据损坏 | SDC, Silent Data Corruption | 设备或算子未显式报错，但输出数值相对独立参考、确定性参考或已知显存数据模式发生异常 | 探针命中先记为可疑，再做复测与硬件归因 |
| 错误纠正码 | ECC, Error-Correcting Code | 为数据增加冗余校验信息，使受保护域内的部分位错误能够被检测或纠正 | 纠错能力、码字组织和覆盖路径由具体设备实现决定 |
| 单错纠正、双错检测 | SEC-DED | 能纠正一个受保护位错误并检测两个受保护位错误的一类编码能力 | 超出设计距离的多位错误不具备统一检测或纠正保证 |
| 可纠正错误 | CE, Correctable Error | 错误仍处于当前 ECC 的纠正能力内，硬件能够恢复码字 | 不等于根因已消失；重复位置或 CE storm 仍需处置 |
| 不可纠正错误 | UE/UCE, Uncorrectable Error | 错误超出当前 ECC 的纠正能力，系统无法由 syndrome 唯一恢复原值 | 是否影响作业还取决于 containment、poison、scrub 和访问时机 |
| 单比特/双比特错误 | SBE/DBE | SEC-DED 语境下常见的 syndrome 分类 | DBE 不必然证明两个独立 HBM cell 同时损坏 |
| 内存巡检与修正 | Memory scrubbing | 周期读取内存、检查 ECC，并将可纠正结果写回以缩短错误累积窗口 | scrub 发现错误与应用访问触发错误应分开统计 |
| 十亿设备小时事件率 | FIT, Failures In Time | 每十亿设备小时内某类已定义事件的期望数量 | 必须注明事件是 CE、UE、设备失效还是作业中断 |
| 持续性能离群候选 | Persistent performance outlier candidate | 正确性未见异常，但任一性能项持续低于同硬件 cohort 的预注册门限 | 初始参考线可取中位数的 80%，属于相对判定 |
| 受竞争污染 | Contended | 启动前存在外部负载，或持续计时质量异常，导致性能结果不能作为干净硬件基线 | 需排除竞争后复测 |
| cohort | Cohort | 软硬件版本、测试阶段、物理路径、算子、消息大小、负载模式和通信组规模均可比的一组样本 | 必须预先规定最小样本量 |
| 性能候选 | Performance candidate | 首轮相对同 cohort 明显偏离、需要冻结 case 复测的节点或 group | 不等同于功能异常设备或节点 |
| 可疑 | Suspect | 性能偏离经复测持续存在，或证据不足以定为硬失败 | 进入人工或厂商复核 |
| 失败 | Fail | 正确性、关键状态、建联、超时、进程或结果完整性失败 | 默认阻断准入 |
| 同步完成路径固定时延 | Fixed-latency synchronization completion-path fault | 用户任务提交后，Host 调度、runtime dispatch、内核驱动或完成等待路径偶发引入近似固定的额外时延；操作最终完成但 forward progress 暂时不可见 | 属于缓慢失效故障族；平台具体机制分别验证，与峰值算力、HBM、ECC 和通信带宽检查正交 |
| 训练通信组定义 | Training communication-group definition | 依据目标训练系统与配置形成的总规模、rank 顺序、TP/DP/EP/PP 分组和工作负载形状 | 必须绑定训练系统与配置的不可变版本 |
| 训练岛 | Training island | 内部使用高带宽互连和频繁同步、对外只进行低频状态交换的一组训练资源 | island 可以包含多节点和多个并行维度，不等同于单机 |
| DiLoCo | Distributed Low-Communication training | 多个训练 island 执行较多 inner steps，再以参数差进行低频 outer optimization 的训练方法 | 低通信不自动等于完整容错；质量依赖 inner/outer 优化和成员策略 |
| Inner/outer optimizer | Inner/outer optimizer | inner optimizer 在各 island 内连续更新本地模型；outer optimizer 在全局同步轮次合并 island 参数差 | 两层优化器状态都属于恢复语义 |
| Parameter Server | PS | 分片保存全局共享参数或状态，并提供通信、一致性、版本和弹性成员能力的服务 | 本文设计中只作为低频 outer state plane，不承载每个 micro-batch 的稠密梯度 |
| 版本栅栏 | Epoch fencing | 使用单调 round/epoch 拒绝旧版本、重复或失效成员提交的更新 | 防止网络恢复或迟到 worker 污染已发布版本 |
| 最终训练拓扑验收 | Final training topology | 在精确目标节点上按真实子通信组完成的功能性准入 | 不做大规模 group 间性能归因 |
| 阻断 | Blocked | 在线成员、硬通过节点或对应拓扑条件不足，无法按目标规模执行 | 不得以较小规模结果替代目标规模验收 |
| standby | Standby | 通过硬 gate 但未进入本轮精确训练集合的候选节点 | 与因硬失败被 excluded 区分 |
| 物理超节点 | Physical SuperPod | 由产品物理拓扑确定的超节点边界 | 以资产清单和设备管理面的超节点标识为准 |
| 逻辑超节点 | Logical SuperPod | 在一个物理超节点内为作业划分的连续资源块 | 不跨物理超节点；逻辑块内 rank 连续 |
| 超节点亲和性 | SuperPod affinity | 根据 NPU、节点和超节点拓扑选择资源的调度约束 | 小任务优先局部，大任务跨域后均衡 |
| HCCL rank table | HCCL rank table | 描述通信域内 Server、Device、rank、网卡和超节点关系的配置 | A3 超节点模式使用 1.2 格式 |
| 原生 profiling 边缘适配器 | Native profiling edge adapter | 在通信库既有 profiling 边界旁路记录事件，并保持原调用参数、返回值和错误语义 | 与通信库 ABI 和版本绑定 |
| Torch 通用观测路径 | Torch semantic path | 通过 PyTorch module、tensor、step 和 `torch.distributed` API 采集跨厂商公共语义的路径 | 信息粒度低于通信库原生插件 |
| collective API 耗时 | Collective API wall time | Python 调用进入到返回，或异步 `Work.wait()` 返回之间的主机墙钟时间 | 不能直接等同于设备通信执行时间 |
| 观测质量收据 | Query/data quality receipt | 与查询结果同时返回的成员覆盖、失败分区、丢弃事件、partial、精度和对齐信息 | 结果存在不表示证据完整 |
| 分布式火焰图 | Distributed flamegraph | 各 rank 先折叠调用路径，再按稳定路径身份归并权重分布、贡献 rank 和覆盖率的跨进程调用路径视图 | 总宽度不能替代每 rank 分布；采样权重不等于精确墙钟 |
| 触发式运行时取证 | Triggered runtime forensics | 由异常条件、watchdog、Python 异常、fatal signal 或受控请求触发，在限定 rank 和窗口内保存深度运行时证据 | 不为取证插入训练全局同步；触发率和单次成本均需受控 |
| Python 变量 watch | Python variable watch | 在指定函数作用域内观察少量命名变量的变化，并记录类型、位置、摘要、时间及可用的训练坐标 | 逐行 tracing、字符串化或张量取值可能产生扰动；缺少 step 坐标时不得按最近时间强行归属 |
| 崩溃指纹 | Crash fingerprint | 由异常类型、顶层帧和规范化消息等稳定字段生成的故障聚类键 | 相同指纹表示现场相似，不等于底层根因相同 |
| 交错基线 step | Interleaved baseline step | 与被观测 step 交错、保持训练负载但绕过指定采集器重路径的开销基线 | 只能估计被绕过采集器的增量 |
| partial 结果 | Partial result | 部分节点、rank 或分区失败后仍返回的可用数据 | 可用于诊断；正式 gate 需按覆盖规则阻断 |
