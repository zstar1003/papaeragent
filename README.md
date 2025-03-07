# Academicagent

Academicagent is a Python package that integrates downloading papers from arXiv and evaluating them using a local large model (Ollama).

<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">简体中文</a> 
</p>

---

## Features

- **Download arXiv Papers**  
  Search for and download a specified number of PDF papers from arXiv based on the keywords provided by the user.

- **Large Model Q&A**  
  For each downloaded paper, extract the first page from the PDF and use the local large model to generate a Chinese summary along with an evaluation score for the paper.

---

## Installation

1. **Download Ollama and Start the Local Large Model Service**

   Download Ollama from: [https://ollama.com/](https://ollama.com/)

   For example, to download the `deepseek-r1:1.5b` model, run:
   ```bash
   ollama pull deepseek-r1:1.5b
   ```

2. **Install paperagent**

Install using pip:
```bash
pip install paperagent
```

## Usage Example

```python
from academicagent.agent import run_agent

run_agent(paper_keyword="object detection", total_count=1, save_path="papers", model_name="deepseek-r1:1.5b")
```

### Input Parameters
- **paper_keyword** (string):
    The keyword used to search for papers on arXiv.  
    Example: "object detection"

- **total_count** (integer):
The total number of papers to download.  
Example: 5

- **save_path** (string, default "papers"):
The folder path where the downloaded PDFs will be saved. If not provided, it defaults to "papers".  
Example: "papers"

- **question** (string, optional):
The question to provide to the large model. If not specified, the default question is:  
"Please generate a Chinese summary of this paper and evaluate its value based on originality, effectiveness, and scope, on a scale of 0 to 10, then provide your score after the summary is generated."

- **model_name** (string, default "deepseek-r1:1.5b"):  
The name of the local large model to be used for invoking Ollama.

### Output
- **PDF Download**:
The PDFs of the papers are downloaded from arXiv into the specified save_path folder based on the provided keyword and count.

- **Evaluation File**:
The title of each paper and the large model's response are written into a Markdown file.
---

## Version History

- **v0.1.0**  
Initial release, implementing arXiv paper downloading and large model Q&A functionality.


## Contact
If you have any questions or suggestions, please feel free to submit an issue or pull request.  

