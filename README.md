# Academicagent

academicagent 是一个集成了从 arXiv 下载论文以及利用本地大模型 (Ollama) 对论文进行下载并评价的 Python 包。

---

## 功能

- **下载 arXiv 论文**  
  根据用户提供的关键词搜索并下载指定数量的论文 PDF 文件。

- **大模型问答**  
  对每篇下载的论文，从 PDF 中提取第一页内容，并利用本地大模型生成中文摘要及论文质量评分。
---

## 安装

1. 下载Ollama 并启动本地大模型服务

Ollama 下载地址：[https://ollama.com/](https://ollama.com/)

以`deepseek-r1:1.5b`为例，下载模型
```bash
ollama pull deepseek-r1:1.5b
```

2. 安装 paperagent

使用 pip 安装：
```bash
pip install paperagent
```

## 使用示例

```python
from academicagent.agent import run_agent

run_agent(paper_keyword="object detection", total_count=1, save_path="papers", model_name="deepseek-r1:1.5b")
```

### 输入参数
- **paper_keyword** (字符串):  
  用于在 arXiv 上搜索论文的关键词。  
  *示例:* `"object detection"`

- **total_count** (整数):  
  指定需要下载的论文总数量。  
  *示例:* `5`

- **save_path** (字符串, 默认 "papers"):  
  指定保存下载 PDF 的文件夹路径。若未传入，将默认使用 "papers"。  
  *示例:* `"papers"`

- **question** (字符串, 可选):  
  提供给大模型的提问内容；若未指定，则使用默认问题：  
  > "帮我生成这篇文章的中文摘要，并从新意度、有效性、问题大小三个维度综合评估这篇文章的价值，满分十分，生成完中文摘要后，打出你认为的评分。"

- **model_name** (字符串, 默认 "deepseek-r1:1.5b"):  
  本地大模型的名称，用于 Ollama 的模型调用。

### 输出
- **PDF 下载**:  
  根据指定关键词和数量，从 arXiv 下载论文 PDF 文件到指定的 `save_path` 文件夹中。


- **评估文件**:  
  所有论文的标题和大模型回答会写入一个 Markdown 文件，文件名格式为 `论文质量评估YYYYMMDD.md`（如 `论文质量评估20250307.md`），用于记录每篇论文的中文摘要和综合评分。

---

## 版本更新信息

- **v0.1.0**  
  初始版本，实现了 arXiv 论文下载和大模型问答功能。


## 联系
如果有任何问题或建议，欢迎提交 issue 或 pull request。  

