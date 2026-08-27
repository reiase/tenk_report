---
title: 术语与缩略语
---

# 术语与缩略语

本表是全篇术语的权威来源。新增缩略语时先在首次出现处展开，再链接或收录到这里。

| 术语 | 英文或缩写 | 本报告定义 | 备注 |
| --- | --- | --- | --- |
| 万卡规模 | 10K-scale | 待定义：物理卡数、分配卡数或有效参与训练卡数 | 必须在摘要中沿用同一口径 |
| 模型 FLOPs 利用率 | MFU | (	ext{模型有效 FLOPs/s}/(N P_{mathrm{peak}})) | 冻结模型 FLOPs、精度峰值、设备单位与重计算口径 |
| 硬件 FLOPs 利用率 | HFU | (	ext{实际执行 FLOPs/s}/(N P_{mathrm{peak}})) | 明确实际执行 FLOPs 与重计算口径 |
| 有效训练时间占比 | 待统一 | 待给出分子、分母和排除项 | 不与集群可用率混用 |
| 扩展效率 | Scaling efficiency | 待定义强扩展和弱扩展公式 | 标明基准规模 |
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
| 慢卡候选 | Slow card candidate | 正确性未见异常，但任一性能项持续低于同硬件 cohort 的预注册门限 | 初始参考线可取中位数的 80%，属于相对判定 |
| 受竞争污染 | Contended | 启动前存在外部负载，或持续计时质量异常，导致性能结果不能作为干净硬件基线 | 需排除竞争后复测 |
| cohort | Cohort | 软硬件版本、测试阶段、物理路径、算子、消息大小、负载模式和通信组规模均可比的一组样本 | 必须预先规定最小样本量 |
| 性能候选 | Performance candidate | 首轮相对同 cohort 明显偏离、需要冻结 case 复测的节点或 group | 不等同于坏卡/坏节点 |
| 可疑 | Suspect | 性能偏离经复测持续存在，或证据不足以定为硬失败 | 进入人工或厂商复核 |
| 失败 | Fail | 正确性、关键状态、建联、超时、进程或结果完整性失败 | 默认阻断准入 |
| 训练通信组定义 | Training communication-group definition | 依据目标训练系统与配置形成的总规模、rank 顺序、TP/DP/EP/PP 分组和工作负载形状 | 必须绑定训练系统与配置的不可变版本 |
| 最终训练拓扑验收 | Final training topology | 在精确目标节点上按真实子通信组完成的功能性准入 | 不做大规模 group 间性能归因 |
| 阻断 | Blocked | 在线成员、硬通过节点或对应拓扑条件不足，无法按目标规模执行 | 不得降级冒充目标规模通过 |
| standby | Standby | 通过硬 gate 但未进入本轮精确训练集合的候选节点 | 与因硬失败被 excluded 区分 |
| 物理超节点 | Physical SuperPod | 由产品物理拓扑确定的超节点边界 | 以资产清单和设备管理面的超节点标识为准 |
| 逻辑超节点 | Logical SuperPod | 在一个物理超节点内为作业划分的连续资源块 | 不跨物理超节点；逻辑块内 rank 连续 |
| 超节点亲和性 | SuperPod affinity | 根据 NPU、节点和超节点拓扑选择资源的调度约束 | 小任务优先局部，大任务跨域后均衡 |
| HCCL rank table | HCCL rank table | 描述通信域内 Server、Device、rank、网卡和超节点关系的配置 | A3 超节点模式使用 1.2 格式 |
| HCCL MSProf shim | HCCL MSProf shim | 位于 HCCL 与真实 CANN `libprofapi.so` 之间、旁路记录 MSProf 事件并转发原调用的原生适配器 | 与 CANN/HCCL ABI 和版本绑定 |
| Torch 通用观测路径 | Torch semantic path | 通过 PyTorch module、tensor、step 和 `torch.distributed` API 采集跨厂商公共语义的路径 | 信息粒度低于通信库原生插件 |
| collective API 耗时 | Collective API wall time | Python 调用进入到返回，或异步 `Work.wait()` 返回之间的主机墙钟时间 | 不能直接等同于设备通信执行时间 |
| 观测质量收据 | Query/data quality receipt | 与查询结果同时返回的成员覆盖、失败分区、丢弃事件、partial、精度和对齐信息 | 结果存在不表示证据完整 |
| shadow step | Shadow step | 与被观测 step 交错、保持训练负载但绕过指定采集器重路径的开销基线 | 只能估计被绕过采集器的增量 |
| partial 结果 | Partial result | 部分节点、rank 或分区失败后仍返回的可用数据 | 可用于诊断；正式 gate 需按覆盖规则阻断 |
