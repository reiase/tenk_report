# 万卡国产加速卡训练技术报告

本仓库用于以 Markdown 方式协作撰写“万卡规模国产加速卡训练”技术报告。报告同时维护方法设计与已核验实验：生产数字必须链接到稳定实验编号、冻结配置、统计窗口和证据哈希；尚未达到该标准的材料继续标为待核验或计划项。

## 从这里开始

- 报告目录与进度：[docs/README.md](docs/README.md)
- 协作与评审：[CONTRIBUTING.md](CONTRIBUTING.md)
- 写作规范：[guides/writing-guide.md](guides/writing-guide.md)
- 数据、图表与引用：[guides/evidence-guide.md](guides/evidence-guide.md)
- 实验记录：[experiments/README.md](experiments/README.md)
- 架构决策：[decisions/README.md](decisions/README.md)

## 推荐工作流

1. 在 [docs/README.md](docs/README.md) 认领章节，并填写负责人和计划时间。
2. 从 [templates/chapter.md](templates/chapter.md) 复制章节模板；实验和技术决策使用对应模板。
3. 将原始数据、生成图表的代码和最终图片分开保存，确保图表可复现。
4. 提交前运行 `make check`，然后发起 Pull Request，请至少一位内容评审者审阅。

当前已登记的实验覆盖 A3 1024 卡调优、4096 卡通信消融、1024 到 4096 卡弱扩展、8192 卡建组修正，以及 10240 卡异构资源池加权验收。权威数字与适用边界见[结果与分析](docs/08-results-and-analysis.md)。

## 常用命令

```bash
make check       # 检查 Markdown 内部链接、图片替代文本和基本格式
make todo        # 汇总未完成事项
make tree        # 查看报告相关目录
```

## 文档站预览

本仓库使用 Zensical 生成技术报告站点。首次运行会由 `uv` 创建隔离环境并安装锁定版本的 Zensical：

```bash
make site-serve    # 本地实时预览
make site-build    # 校验并生成静态站点
```

站点采用系统中文字体、自动明暗配色、全文搜索、章节导航和固定布局的 SVG 技术图。静态输出位于 `site/`，不提交版本库；Markdown 文件仍可直接在 Git 平台评审。
