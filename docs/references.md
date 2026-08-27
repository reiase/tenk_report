# 参考资料

为外部资料分配稳定编号。删除资料时保留编号并标注原因，避免正文引用漂移。内部实现证据使用 `I` 前缀，并冻结仓库 commit；正文只引用可复核的设计与行为边界，不展开具体代码路径。

## R001

- 标题：Atlas 900 A3 SuperPoD
- 作者或机构：华为
- 发布日期：页面未注明
- 访问日期：2026-08-15
- 链接：https://e.huawei.com/cn/products/computing/ascend/atlas-900-a3-superpod
- 支撑内容：A3 产品形态、最大 384 NPU、FP16 聚合算力、单 NPU 最大 3.2 TB/s 片上内存带宽、D2D 带宽与散热规格
- 备注：厂商公开产品规格，不代表项目实际部署配置

## R002

- 标题：曦云 C550 产品
- 作者或机构：沐曦集成电路（上海）股份有限公司
- 发布日期：页面未注明
- 访问日期：2026-08-15
- 链接：https://www.metax-tech.com/prod.html?cid=107&id=35
- 支撑内容：OAM 形态、64 GB 显存、ECC、MetaXLink 8 卡全互连、最大板卡功耗和 MXMACA 软件栈
- 备注：厂商公开产品规格，不代表项目实际部署配置

## R003

- 标题：常用通信算子支持情况
- 作者或机构：昇腾社区 / 华为
- 发布日期：CANN 社区版 8.5.0 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850/commlib/hcclug/hcclug_000113.html
- 支撑内容：A3 上 AllReduce 等算子的节点内、超节点内和超节点间支持，以及零拷贝、确定性和算子重执行能力
- 备注：具体行为需与项目安装的 CANN/HCCL 版本核对

## R004

- 标题：rank table 文件配置资源信息
- 作者或机构：昇腾社区 / 华为
- 发布日期：CANN 8.3.RC1 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/83RC1/hccl/hcclug/hcclug_000014.html
- 支撑内容：A3 超节点 rank table 1.2、`super_device_id`、`super_pod_list`、Device 网卡和备用网卡配置约束
- 备注：同一超节点的 AI Server 需连续配置，不允许跨超节点交叉排列

## R005

- 标题：MindCluster 6.0.RC3.1 亲和性调度方案说明
- 作者或机构：华为
- 发布日期：2025-02-08
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc3/clusterscheduling/ref/affinityschedulesd/MindCluster%206.0.RC3.1%20%E4%BA%B2%E5%92%8C%E6%80%A7%E8%B0%83%E5%BA%A6%E6%96%B9%E6%A1%88%E8%AF%B4%E6%98%8E.pdf
- 支撑内容：A3 节点/NPU 亲和性、逻辑超节点约束、`sp-block`、故障重调度和 Volcano 调度流程
- 备注：跨超节点均衡是建立在官方亲和性约束之上的项目工程策略

## R006

- 标题：HCCL_ALGO 环境变量参考
- 作者或机构：昇腾社区 / 华为
- 发布日期：CANN 社区版 8.5.0.alpha002 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850alpha002/hccl/hcclug/hcclug_000075.html
- 支撑内容：A3 节点间和超节点间集合通信算法支持与自动回退关系
- 备注：算法支持随版本、算子、数据类型和运行模式变化

## R007

- 标题：HCCL 性能测试工具——工具介绍
- 作者或机构：昇腾社区 / 华为
- 发布日期：CANN 社区版 8.5.0 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850/devaids/hccltool/HCCLpertest_16_0001.html
- 支撑内容：HCCL 算法带宽定义及影响因素
- 备注：单算子测试需要与 Megatron 端到端训练联合解释

## R008

- 标题：Atlas 900 A3 SuperPoD——亲和性规则与总线设备节点网络
- 作者或机构：昇腾社区 / 华为
- 发布日期：MindCluster 7.3.0 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/en/mindcluster/730/clustersched/schedulingug/dl_affinity_0007.html
- 支撑内容：HiAM、SIO、HCCS-L1/HCCS-L2、16 NPU 计算节点，以及逻辑超节点内 HCCS、逻辑超节点间 RoCE 的通信边界
- 备注：应与项目实际安装版本和产品子型号核对

## R009

- 标题：分布式场景亲和性策略
- 作者或机构：昇腾社区 / 华为
- 发布日期：MindCluster 7.3.0 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/zh/mindcluster/730/clustersched/dlug/dl_affinity_0026.html
- 支撑内容：A3 逻辑超节点亲和任务的单 Pod NPU 申请约束和非 16 卡分布式调度边界
- 备注：不同 MindCluster 版本的支持范围存在变化，必须冻结版本

## R010

- 标题：HCCL_INTER_HCCS_DISABLE 环境变量参考
- 作者或机构：昇腾社区 / 华为
- 发布日期：CANN 社区版 8.5.0 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850/commlib/hcclug/hcclug_000079.html
- 支撑内容：A3 超节点内使用 HCCS/SDMA 或 RoCE/RDMA 的链路选择，默认值为 HCCS
- 备注：不应仅为提高网卡使用率而改变超节点内默认链路

## R011

- 标题：HCCL_BUFFSIZE 环境变量参考
- 作者或机构：昇腾社区 / 华为
- 发布日期：CANN 社区版 8.5.0.alpha002 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850alpha002/maintenref/envvar/envref_07_0080.html
- 支撑内容：HCCL 通信缓存大小、默认值、显存占用关系和大语言模型估算建议
- 备注：需要按通信域数量、消息大小和显存余量联合调优

## R012

- 标题：CANN 8.5.0 通信库更新说明
- 作者或机构：昇腾社区 / 华为
- 发布日期：CANN 社区版 8.5.0 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850/releasenote/releasenote_0009.html
- 支撑内容：A3 的 AI CPU 小数据优化，以及 ReduceScatter/AllGather pipeline 算法对跨超节点大数据通信的支持
- 备注：发布说明只表示版本能力，性能收益需要在项目工作负载中验证

## R013

- 标题：MindCluster 7.3.0 YAML 参数说明
- 作者或机构：昇腾社区 / 华为
- 发布日期：MindCluster 7.3.0 文档
- 访问日期：2026-08-15
- 链接：https://www.hiascend.com/document/detail/zh/mindcluster/730/clustersched/dlug/dl_resume_054.html
- 支撑内容：AscendJob 的 `sp-block` 位置、取值约束，以及与 `tor-affinity` 的关系
- 备注：YAML 字段位置和 CRD schema 应以集群实际安装版本为准

## R014

- 标题：Removing Obstacles before Breaking Through the Memory Wall: A Close Look at HBM Errors in the Field
- 作者或机构：Ronglong Wu 等，USENIX ATC 2024
- 发布日期：2024-07
- 访问日期：2026-08-16
- 链接：https://www.usenix.org/conference/atc24/presentation/wu-ronglong
- 支撑内容：超过 6 万颗 HBM2、19 个数据中心、两年窗口中的 CE/UE 分布，HBM 的空间与时间相关性、列/TSV/堆叠结构特征，以及传统 DRAM 预测规则不能直接迁移到 HBM
- 备注：公开数据用于说明方法和分布形态，不作为 A3 或 C550 的错误率基线

## R015

- 标题：DRAM Errors in the Wild: A Large-Scale Field Study
- 作者或机构：Bianca Schroeder、Eduardo Pinheiro、Wolf-Dietrich Weber
- 发布日期：2009-06
- 访问日期：2026-08-16
- 链接：https://research.google.com/pubs/archive/35162.pdf
- 支撑内容：大规模服务器 DRAM 的 CE/UE 发生率、错误聚集、CE 与 UE 相关性、年龄效应和维修替换造成的幸存者偏差
- 备注：研究对象为早期 DDR/FBDIMM，不能把其概率和月份阈值直接移植到 HBM

## R016

- 标题：NIST/SEMATECH e-Handbook of Statistical Methods — Bathtub Curve
- 作者或机构：美国国家标准与技术研究院（NIST）
- 发布日期：页面持续维护
- 访问日期：2026-08-16
- 链接：https://itl.nist.gov/div898/handbook/apr/section1/apr124.htm
- 支撑内容：条件失效率及早期失效、稳定使用、磨损失效三阶段的概念模型
- 备注：浴盆曲线是可靠性分析框架，不是特定加速卡的实测寿命曲线

## R017

- 标题：OCP GPU & Accelerator RAS Requirements, Version 1.0
- 作者或机构：Open Compute Project
- 发布日期：2024
- 访问日期：2026-08-16
- 链接：https://www.opencompute.org/documents/ocp-gpu-and-accelerators-ras-requirements-1-0-final-pdf
- 支撑内容：加速器内存 ECC、scrubbing、page offlining、row remapping、spare repair、data poison、错误 containment、总线/链路保护和错误报告要求
- 备注：这是面向超大规模加速器系统的通用 RAS 要求；具体能力仍以 A3、C550 的产品和固件版本为准

## R018

- 标题：昇腾 910C 训练集群并行策略对 MFU 影响的技术分析报告
- 作者或机构：未署名
- 创建日期：2026-08-17（PDF 元数据）
- 导入日期：2026-08-19
- 链接：[仓库附件](https://github.com/reiase/tenk_report/blob/master/references/ascend-910c-parallelism-mfu-analysis.pdf)
- SHA256：`1afd922dfa074143ad093ed78d753be80b563d43686b5e07cd4f5d7c4ca42aaa`
- 支撑内容：TP/PP 与 world size 的 MFU 趋势、GBS 和重计算消融、TensorBoard/Profiling 通信归因摘要，以及 2048 die 下七组并行配置搜索
- 统计口径：采用来源报告中的聚合表、趋势图和 Profiling 摘要，规模单位保持为 die

## I001

- 标题：Probing HCCL MSProf shim 实现
- 仓库与版本：`probing`，commit `906ce8b33eb2`
- 支撑内容：`libprofapi.so` shim、MSProf 事件解析、`hccl.*` mmap 表、真实 CANN 库转发、独立表失败隔离与部署入口
- 备注：MSProf 结构体布局仍需按生产 CANN/HCCL 版本验证

## I002

- 标题：Probing Torch collective 与加速器 backend 实现
- 仓库与版本：`probing`，commit `906ce8b33eb2`
- 支撑内容：`torch.distributed` API hook、API wall-clock 语义、NPU/CUDA/CPU 能力探测、TorchProbe 当前 backend 覆盖边界
- 备注：代码快照中未发现 C550、MetaX 或 MCCL 专用原生采集器

## I003

- 标题：Probing extension composition 与 GPU backend 抽象
- 仓库与版本：`probing`，commit `906ce8b33eb2`
- 支撑内容：HCCL/NCCL schema 注册、Torch/GPU/RDMA extension 组装、`GpuBackend` trait、运行时发现与无后端降级
- 备注：`GpuBackendKind::Rocm` 当前为预留枚举；代码快照实际发现路径为 CUDA 和 macOS Metal，不能表述成 ROCm 已实现

## I004

- 标题：Probing 性能采集、联邦查询与开销控制设计
- 仓库与版本：`probing`，commit `906ce8b33eb2`
- 支撑内容：本地采集与按需分层 fan-out、聚合下推与联邦 scan、step/rank/role 稳定坐标、确定性采样、shadow 开销估计、有界资源、CPU/GPU/框架显存事实、partial 质量语义、step 矩阵，以及跨 rank folded stack/module 火焰图
- 备注：基础联邦查询、step 矩阵和跨 rank 路径合并已有实现；角色化多指标 Tile、稳定 Path Hash、Rank Set Token 与完整差分/方差火焰图仍主要是架构设计

## I005

- 标题：训练前健康检查的 ECC 策略与精确节点准入设计
- 仓库与版本：`pretrain_healthcheck`，commit `40ee919f7d9e`
- 证据范围：ECC/RAS 事实完整性校验、告警与严格策略、设备/芯片级告警、单卡与长稳判定、跨阶段覆盖校验、风险排序和精确目标节点选择
- 支撑内容：查询覆盖状态、告警到训练资源状态的映射、硬失败约束、风险向量、目标规模准入，以及复测状态的资源选择语义
- 备注：正文只讨论证据语义、故障域和训练节点集合构造，不展开具体命令、脚本、代码路径或平台维修流程

## I006

- 标题：训练前健康检查的计时、异步完成与前向进展设计
- 仓库与版本：`pretrain_healthcheck`，commit `40ee919f7d9e`；所含单卡计时与长稳筛查组件分别固定于 commit `db38011` 与 `e149eae`
- 支撑内容：后端相关的 device event 与 synchronize、预热和预分配后的稳态批次计时、同步主机诊断计时、设备 stream 门控、异步 collective 的逐 work 完成、训练并行组覆盖、固定长度结果交换，以及零通信反复等待的逐 gap 稳定性观测与事件率摘要
- 备注：当前实现中的静态事实深度与设备适配覆盖并不完全对称；正文将其作为软硬件一致性要求和待验证边界，不展开具体命令、代码路径或运维步骤
