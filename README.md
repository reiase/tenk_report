# 万卡国产加速卡训练技术报告

本仓库用于以 Markdown 方式协作撰写“万卡规模国产加速卡训练”技术报告。仓库当前提供的是写作骨架，不预设具体厂商、模型、集群或性能结论；相关内容应由可追溯的配置、实验记录和引用逐步补齐。

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

## 常用命令

```bash
make check       # 检查 Markdown 内部链接、图片替代文本和基本格式
make todo        # 汇总未完成事项
make tree        # 查看报告相关目录
```

本仓库暂不绑定特定发布工具。Markdown 文件可直接在 Git 平台评审；待内容稳定后，可再引入 Pandoc、MkDocs 或其他发布链路。
