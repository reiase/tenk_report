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

- 标题：DiLoCo: Distributed Low-Communication Training of Language Models
- 作者或机构：Arthur Douillard 等
- 发布日期：2023-11，2024-09 修订
- 访问日期：2026-08-16
- 链接：https://arxiv.org/abs/2311.08105
- 支撑内容：训练岛、较多 inner steps、AdamW inner optimizer、Nesterov momentum outer optimizer、低频参数差聚合，以及资源动态可用实验
- 备注：论文在特定模型、数据与 8-worker 条件下报告约 500 倍通信降低；该数字不是任意模型规模、网络和容错策略下的通用收益

## R019

- 标题：OpenDiLoCo: An Open-Source Framework for Globally Distributed Low-Communication Training
- 作者或机构：Sami Jaghouar、Jack Min Ong、Johannes Hagemann
- 发布日期：2024-07
- 访问日期：2026-08-16
- 链接：https://arxiv.org/abs/2407.07852
- 支撑内容：DiLoCo 复现、十亿参数级实验、跨地域训练、worker 数和 inner step 消融、FP16 outer gradient 通信
- 备注：结果同时展示了通信收益与早期收敛/FLOP efficiency 权衡，适合作为系统评估边界而非生产效果保证

## R020

- 标题：Streaming DiLoCo with overlapping communication: Towards a Distributed Free Lunch
- 作者或机构：Arthur Douillard 等
- 发布日期：2025-01
- 访问日期：2026-08-16
- 链接：https://arxiv.org/abs/2501.18512
- 支撑内容：分片 outer synchronization、通信计算重叠、低精度更新，以及峰值带宽、计算利用率和模型质量的联合评估
- 备注：属于低通信训练的后续研究；模型质量和系统收益依赖同步片段、重叠深度、精度与网络条件

## R021

- 标题：Scaling Distributed Machine Learning with the Parameter Server
- 作者或机构：Mu Li 等，USENIX OSDI 2014
- 发布日期：2014
- 访问日期：2026-08-16
- 链接：https://research.google.com/pubs/pub44634.html
- 支撑内容：Parameter Server 的分片全局状态、异步通信、灵活一致性、弹性扩展和持续容错模型
- 备注：论文覆盖多类分布式机器学习工作负载；用于本文 outer state plane 的设计原型，不表示经典每步参数服务器可直接承载当前稠密大模型

## R022

- 标题：MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs
- 作者或机构：Ziheng Jiang 等，ByteDance / Peking University，USENIX NSDI 2024
- 发布日期：2024-04
- 访问日期：2026-08-16
- 链接：https://www.usenix.org/conference/nsdi24/presentation/jiang-ziheng
- 支撑内容：超过 10,000 GPU 的生产训练、全栈协同优化、CUDA Event 低扰动计时、跨 rank 热力图与分布式时间线、故障自动定位和恢复，以及 12,288 GPU 上的 MFU 结果
- 备注：该工作证明热力图、分布式时间线和深层观测已经是公开的大规模训练系统能力；本文的区别应落在跨后端证据语义、partial/coverage 收据、完成路径案例与触发式取证，而不是宣称这些视图本身首次出现

## R023

- 标题：Holmes: Localizing Irregularities in LLM Training with Mega-scale GPU Clusters
- 作者或机构：Yao 等，USENIX NSDI 2025
- 发布日期：2025-04
- 访问日期：2026-08-16
- 链接：https://www.usenix.org/conference/nsdi25/presentation/yao
- 支撑内容：以通信算子日志、异常算子检测和通信算子图定位异常设备；在生产日志驱动实验中报告定位准确率、规模扩展和端到端定位延迟
- 备注：Holmes 的问题范围比本文窄，但提供了有标签数据和诊断准确率基线；本文若主张诊断有效，需要补充 Top-K 命中、误报、漏报和 time-to-localize，而不能只展示可查询的数据面

## R024

- 标题：FLARE: Anomaly Diagnostics for Divergent LLM Training in GPU Clusters of Thousand-Plus Scale
- 作者或机构：Cui 等，USENIX NSDI 2026
- 发布日期：2026-05
- 访问日期：2026-08-16
- 链接：https://www.usenix.org/conference/nsdi26/presentation/cui
- 支撑内容：面向多训练后端的全栈轻量 tracing、后台异步计时、fail-slow 与性能回归诊断、intra-kernel inspection，以及千卡开销和 6,000 GPU 长期部署评测
- 备注：本文的本地事实、联邦查询和触发式证据需要与 FLARE 的运行开销、日志体积、人工标签准确率和部署规模同口径比较；架构成本公式不能替代实测扩展曲线

## R025

- 标题：The Llama 3 Herd of Models
- 作者或机构：Llama Team, Meta
- 发布日期：2024-07
- 访问日期：2026-08-16
- 链接：https://arxiv.org/abs/2407.21783
- 支撑内容：16K GPU 训练的有效训练时间、中断分类、硬件相关故障占比、自动化恢复，以及 PyTorch Flight Recorder 在大规模训练中的使用
- 备注：论文中的中断比例来自特定训练、时间窗口和分类规则，不作为 A3 或 C550 的先验故障率；用于说明同步训练规模化后可靠性和自动诊断的系统影响

## R026

- 标题：Flight Recorder: A New Lens for Understanding NCCL Watchdog Timeouts
- 作者或机构：PyTorch / Meta
- 发布日期：2026
- 访问日期：2026-08-16
- 链接：https://pytorch.org/blog/flight-recorder-a-new-lens-for-understanding-nccl-watchdog-timeouts/
- 支撑内容：collective 的 sequence、调用栈和开始/完成状态记录，超时触发的跨 rank 尽力转储，以及按 process group 对齐离线分析
- 备注：首先触发 watchdog 的 rank 和超时时正在执行的 collective 均不自动等于根因；本文的通信快照应与原生 recorder 互操作，并以变量、角色、内存和跨后端证据补充而非替代其语义

## R027

- 标题：How Meta Keeps Its AI Hardware Reliable
- 作者或机构：Meta Engineering
- 发布日期：2025-07-22
- 访问日期：2026-08-16
- 链接：https://engineering.fb.com/2025/07/22/data-infrastructure/how-meta-keeps-its-ai-hardware-reliable/
- 支撑内容：静态、瞬态和静默故障分类，Fleetscanner、Ripple 与 Hardware Sentinel 的组合检测，周期性 fleet 覆盖，以及 SDC 对训练前向、反向和梯度的影响
- 备注：属于 Meta 生产经验与方法说明；具体故障率和覆盖周期不能直接迁移到本文资源池，但其 factory-to-fleet 和训练期检测思想可用于补充一次性准入的边界

## R028

- 标题：Understanding Silent Data Corruption in LLM Training
- 作者或机构：Jeffrey Ma、Hengzhi Pei、Leonard Lausen、George Karypis
- 发布日期：2025-02
- 访问日期：2026-08-16
- 链接：https://arxiv.org/abs/2502.12340
- 支撑内容：使用生产中识别的健康与 SDC 异常节点，在确定性执行条件下比较子模块、单优化步和训练区间的数值差异及训练影响
- 备注：该工作说明微小局部数值扰动与最终训练质量之间不存在固定映射；本文需要把硬件测试命中、训练状态偏离和模型质量影响作为不同实验层级

## R029

- 标题：PEP 669 — Low Impact Monitoring for CPython
- 作者或机构：Mark Shannon / Python Software Foundation
- 发布日期：2021-12，Python 3.12 接纳
- 访问日期：2026-08-16
- 链接：https://peps.python.org/pep-0669/
- 支撑内容：`sys.monitoring` 的按工具与按 code object 事件控制、低影响监控目标，以及逐行 instrumentation 与统计采样的开销边界
- 备注：即使采用低影响接口，LINE 事件仍可能明显扰动执行；变量 watch 必须限制函数、变量、rank 和时间窗，并与统计采样及无观测基线比较

## R030

- 标题：Oobleck: Resilient Distributed Training of Large Models Using Pipeline Templates
- 作者或机构：Insu Jang 等，ACM SOSP 2023
- 发布日期：2023-10
- 访问日期：2026-08-16
- 链接：https://arxiv.org/abs/2309.08125
- 支撑内容：通过异质 pipeline template 和至少 f+1 个等价副本容忍 f 个同时故障，给出资源覆盖保证与故障恢复吞吐评测
- 备注：Oobleck 代表以执行计划和状态副本获得形式化故障保证的路线；其目标与低通信训练不同，但可作为本文容错语义和故障注入评测的对照

## R031

- 标题：TorchFT: Fault Tolerance for PyTorch
- 作者或机构：PyTorch / Meta
- 发布日期：持续维护
- 访问日期：2026-08-16
- 链接：https://github.com/meta-pytorch/torchft
- 支撑内容：按 step 心跳与成员变化、可重配置 ProcessGroup、同伴 checkpoint 恢复，以及 Fault-Tolerant DDP/HSDP、LocalSGD 和 DiLoCo 的实现原语
- 备注：LocalSGD 与 DiLoCo 路径仍标记为实验能力；本文的 outer state plane 需要把 TorchFT 作为当前实现基线，而不是只与经典 Parameter Server 论文比较

## R032

- 标题：Decoupled DiLoCo for Resilient Distributed Pre-training
- 作者或机构：Douillard 等
- 发布日期：2026-04
- 访问日期：2026-08-16
- 链接：https://arxiv.org/abs/2604.21428
- 支撑内容：异步 learner、参数分片、中央 synchronizer、minimum quorum、自适应 grace window、按 token 加权聚合、事件带确定性重放和混沌实验
- 备注：该工作与本文的训练岛加 outer state plane 位于相同设计空间，并给出了更具体的可用性和优化语义；Parameter Server 因而只能作为候选实现，需要与 quorum synchronizer 和可重配置 ProcessGroup 进行实验选择

## R033

- 标题：Holistic Trace Analysis for Distributed Training
- 作者或机构：PyTorch / Meta
- 发布日期：2023
- 访问日期：2026-08-16
- 链接：https://pytorch.org/blog/trace-analysis-for-masses/
- 支撑内容：基于 Kineto trace 的分布式训练分析、跨 rank 空闲时间与通信计算重叠诊断，以及面向大规模 trace 的分析工作流
- 备注：HTA 提供成熟的离线 trace 分析参照；本文的差异应放在长期低密度事实、按需联邦查询、partial 语义和触发式现场，而不是泛化为“支持分布式 trace 分析”

## I001

- 标题：Probing HCCL 原生 profiling 边缘适配
- 仓库与版本：`probing`，commit `906ce8b33eb2`
- 支撑内容：HCCL profiling 事件解析、本地有界事实、原调用透明转发和按事实类型的失败隔离
- 备注：profiling ABI 与事件字段仍需按生产 CANN/HCCL 版本验证

## I002

- 标题：Probing Torch collective 与加速器能力适配
- 仓库与版本：`probing`，commit `906ce8b33eb2`
- 支撑内容：`torch.distributed` API 边界、API wall-clock 语义、设备能力协商和跨后端覆盖边界
- 备注：当前证据未覆盖 C550/MCCL 通信库内部事件

## I003

- 标题：Probing 公共语义层与原生扩展边界
- 仓库与版本：`probing`，commit `906ce8b33eb2`
- 支撑内容：通信事实 schema 注册、Torch/设备/RDMA 能力组合、运行时发现和无后端降级
- 备注：能力声明必须以实际测量路径为准，预留的平台类型不构成已实现证据

## I004

- 标题：Probing 性能采集、联邦查询与开销控制设计
- 仓库与版本：`probing`，commit `906ce8b33eb2`
- 支撑内容：本地采集与按需分层 fan-out、聚合下推与联邦 scan、step/rank/role 稳定坐标、确定性采样、交错开销估计、有界资源、分层内存事实、partial 质量语义、step 矩阵和跨 rank 调用路径合并
- 备注：基础联邦查询、step 矩阵和跨 rank 路径合并已有实现；角色化多指标 tile、稳定路径身份、压缩 rank 集合与完整差分/方差火焰图仍主要是架构设计

## I005

- 标题：训练前健康检查的 ECC 策略与精确节点准入设计
- 仓库与版本：`pretrain_healthcheck`，commit `40ee919f7d9e`
- 证据范围：ECC/RAS 事实完整性校验、告警与严格策略、设备/芯片级告警、单卡与长稳判定、跨阶段覆盖校验、风险排序和精确目标节点选择
- 支撑内容：查询失败与覆盖缺失的证据边界，告警到训练资源状态的映射，硬失败约束、风险向量、目标规模不足时阻断，以及当前复测状态尚未成为独立选择约束的实现边界
- 备注：正文只讨论证据语义、故障域和训练节点集合构造，不展开具体命令、脚本、代码路径或平台维修流程

## I006

- 标题：训练前健康检查的计时、异步完成与前向进展设计
- 仓库与版本：`pretrain_healthcheck`，commit `40ee919f7d9e`；所含单卡计时与长稳筛查组件分别固定于 commit `db38011` 与 `e149eae`
- 支撑内容：后端相关的 device event 与 synchronize、预热和预分配后的稳态批次计时、同步主机诊断计时、设备 stream 门控、异步 collective 的逐 work 完成、训练并行组覆盖、固定长度结果交换，以及零通信反复等待的逐 gap 稳定性观测与事件率摘要
- 备注：当前实现中的静态事实深度与设备适配覆盖并不完全对称；正文将其作为软硬件一致性要求和待验证边界，不展开具体命令、代码路径或运维步骤

## I007

- 标题：昇腾 A3 单卡概率性定长暂停内部测量汇总
- 来源与日期：用户侧内部技术材料，2026-08-02
- 支撑内容：零通信单卡 gap 定义、两个卡池的长窗事件率、约 500 ms 与 640–690 ms 宽度分布、卡/节点异质性、Host 与设备分层计时、观测者效应、同步节奏消融、NVIDIA 窄口径对照，以及 256/512/1,024 卡 BSP 训练影响摘要
- 证据边界：当前只审阅了汇总材料；其声明的逐事件时间线、训练逐 step 数据、逐卡身份、完整配置、软件版本和完整性摘要尚未导入本报告。数字用于定义复验问题与模型，不作为 A3 全池验收结论

## I008

- 标题：沐曦 C550 单卡概率性软停顿内部测量汇总
- 来源与日期：用户侧内部技术材料，2026-08-02
- 支撑内容：64 卡一小时单卡长窗与 20 分钟复测、墙钟率与完成机会率、200.7–272.3 ms 条件宽度、节点/卡异质性、时间聚集、NVIDIA 窄口径对照、简化 BSP 放大，以及另一集群 256/512 卡 AllReduce 尾部、QP A/B 和退出阶段崩溃线索
- 证据边界：单卡逐事件/窗口数据、物理卡—槽位映射和完整版本尚未导入；大规模通信来自不同集群，缺少隔离网络、背景流量与 RNIC/交换机 counter。两类现象分别登记，均不作为 C550 平台或 MCCL 根因结论

## I009

- 标题：昇腾 A3 固定 512 卡资源池的停顿与训练影响内部测量汇总
- 来源与日期：用户侧内部技术材料，2026-08-05
- 支撑内容：固定 32 节点及停顿排序，按节点构造高事件移除、低事件移除和 3 个随机移除的 448 卡集合，并在小模型纯 DP、Dense TP×PP 与 MoE EP 三类训练中比较稳态 step 中位数
- 证据边界：当前只审阅了汇总材料；节点身份与排序快照、完整训练日志、rank/拓扑映射和 step 分布尚未导入。高/低事件集合各只有 1 组、随机集合只有 3 组，Dense/MoE 因共同 NaN 仅分析第 5–25 步；结果用于说明样本内关联和工作负载依赖，不作为通用资源选择收益

## I010

- 标题：昇腾 A3 同步完成路径固定时延内部定位描述
- 来源与日期：用户提供的内部定位描述，2026-08-16
- 支撑内容：同步操作进入内核驱动后，在完成等待路径上遇到近似固定的额外时延；该定位用于将 A3 概率性亚秒停顿归类为独立的同步完成路径缓慢失效
- 证据边界：内核时间线、符号或状态、触发条件和受影响驱动版本尚未导入；华为追加材料给出 host-bound 与软件消融证据，因此该描述作为同步完成链中的一个定位边界，不能独立升级为唯一底层根因

## I011

- 标题：浦江集群 C550 Stall 问题说明
- 来源与日期：沐曦技术说明，用户于 2026-08-16 提供
- 支撑内容：cudaDeviceSynchronize wait-signal 暴露点、direct/non-direct dispatch 的线程和队列差异、短 kernel 高频 launch/synchronize 对 CPU 负载的影响、direct dispatch 短窗复现及厂商机制结论
- 证据边界：direct 模式报告约 10 分钟未复现且厂商明确说明理论上不能完全避免；未提供与 64 卡一小时主测严格匹配的随机长窗 A/B、有效卡时和事件率区间

## I012

- 标题：昇腾 A3 Stall 问题首轮联合排查结论
- 来源与日期：华为侧排查摘要，用户于 2026-08-16 提供
- 支撑内容：Qwen3-0.6B 纯 DP 热/冷节点 512-step 影响约 7%–10%、内部单矩阵未复现、硬件压力与 SNR/CRC 正常、TP broadcast 同步点 profiling、周期任务排查、热点卡覆盖不足、中断绑核和共享周期源候选
- 证据边界：属于阶段性联合排查摘要；完整训练日志、profiling 时间线、硬件日志和反向实验结果尚未归档，已排除方向均限于当前观测覆盖

## I013

- 标题：【PJ】异常 Stall 问题第二轮说明
- 来源与日期：华为技术说明，用户于 2026-08-16 提供
- 支撑内容：512-rank 纯 DP 节点 step 曲线、热点节点 512/640-step 总时间、卡上计算一致性、通信/同步暴露与 host-bound 结论，以及任务下发流水、内存分配器和组合消融
- 证据边界：第 3–500 步消融中基线报告 2 个轮次，其他条件报告 3 个轮次；总时间未分解为稳态基线、spike 频率和条件宽度，透明大页没有独立量化结果，原始日志与完整配置尚未导入

## I014

- 标题：Probing 触发式运行时取证与 Python 内省设计
- 仓库与版本：`probing`，commit `906ce8b33eb2`
- 支撑内容：Python/native 调用栈的本地折叠与跨 rank 合并、函数作用域变量变化观测、主线程与后台线程异常捕获、原生 fatal signal 最小转储、训练 step/phase/活动 span/最近通信上下文、主机与设备内存摘要、崩溃 fingerprint、本地持久化与 grace 取证窗口，以及 watchdog 触发的通信 Flight Recorder 快照
- 证据边界：基础跨 rank 路径合并、变量变化记录和崩溃捕获已有实现；稳定路径身份、完整差分/方差火焰图和变量状态矩阵仍需目标规模验证。逐行 Python tracing、对象字符串化与实时 eval 可能扰动训练或改变进程状态，必须限定作用域、时间窗、权限和数据脱敏；fatal signal 上下文只能尽力保全，缺失记录不表示未发生故障
