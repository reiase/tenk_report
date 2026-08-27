# 万卡国产加速卡训练技术报告

本仓库维护 10,240 张国产加速卡大模型训练项目的技术报告与实验记录。报告覆盖双资源池总体架构、Megatron 并行调优、HCCL/MCCL 通信、健康准入、前向进展、规模扩展和工程资产管理。

## 项目规模

- 华为 Atlas 900 A3：8,192 张加速卡
- 沐曦曦云 C550：2,048 张加速卡
- 协同编排：8 个训练组与 64 个参数服务器
- 总纳管规模：10,240 张加速卡

## 代表结果

| 方向 | 结果 |
| --- | --- |
| Qwen3-200B 弱扩展 | 1,024→4,096 卡效率 94.26% |
| 2,048 die 并行网格 | TP2/PP16/uniform1，MFU 33.4% |
| 4,096 卡 Dense | 124.264 TFLOPS/GPU，CV 1.68% |
| 万卡协同窗口 | 加权 ECP 保留率 92.43% |
| 模型运行 | 200B Dense 800 step，1T MoE 500 step |
| 健康准入 | A3 两批 4,096 卡；C550 2,336 卡与 Final256 |
| 健康检查效率 | 1,706→1,056 秒 |

## 本地预览

```powershell
uv run zensical serve
```

站点默认地址为 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)。

## 构建与校验

```powershell
python scripts/check_markdown.py
uv run zensical build --clean --strict
```

## 仓库结构

- `docs/`：正式报告章节、技术图和站点资源
- `experiments/`：十四组实验摘要与结构化数据
- `references/`：项目材料与引用索引
- `guides/`：写作与实验记录规范
- `scripts/`：Markdown 质量校验
- `zensical.toml`：站点导航与主题配置

报告入口见 [docs/README.md](docs/README.md)，核心结果见 [docs/08-results-and-analysis.md](docs/08-results-and-analysis.md)。
