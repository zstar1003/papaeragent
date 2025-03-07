import os
import requests
import re
import math
import time
import warnings
import datetime
from urllib.parse import quote
from lxml import html
from bs4 import BeautifulSoup
from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyMuPDFLoader

warnings.filterwarnings("ignore")

def get_total_results(url):
    """获取搜索结果中的论文总数"""
    response = requests.get(url)
    tree = html.fromstring(response.content)
    result_string = ''.join(tree.xpath('//*[@id="main-container"]/div[1]/div[1]/h1/text()')).strip()
    match = re.search(r'of ([\d,]+) results', result_string)
    if match:
        total_results = int(match.group(1).replace(',', ''))
        return total_results
    else:
        print("没有找到匹配的数字。")
        return 0


def download_file(url, folder, filename):
    """
    下载文件到指定文件夹，若文件已存在则跳过下载
    返回下载后的文件路径；下载失败返回 None
    """
    filepath = os.path.join(folder, filename)
    if os.path.exists(filepath):
        print(f"文件已存在，跳过下载: {filename}")
        return filepath
    try:
        print(f"论文标题: {filename}")
        print(f"开始下载: {url}")
        response = requests.get(url)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"下载成功\n")
        return filepath
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {url}, 错误: {e}\n")
    except IOError as e:
        print(f"文件保存失败: {filename}, 错误: {e}\n")
    return None


def get_paper_info(url, save_path, max_papers=None):
    """
    根据给定 URL 爬取一页的论文信息并下载 PDF
    返回 [(论文标题, PDF 路径), ...] 的列表
    若 max_papers 不为 None，则最多下载该数量的论文
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    papers = []
    articles = soup.find_all('li', class_='arxiv-result')
    for article in articles:
        if max_papers is not None and len(papers) >= max_papers:
            break
        title_element = article.find('p', class_='title')
        if not title_element:
            continue
        title = title_element.text.strip()
        pdf_link_element = article.find('a', text='pdf')
        if pdf_link_element:
            pdf_link = pdf_link_element['href']
            if not pdf_link.startswith("http"):
                pdf_link = "https://arxiv.org" + pdf_link
        else:
            print(f"论文 {title} 没有找到 PDF 链接，跳过")
            continue
        # 处理标题中的非法字符生成合法文件名
        filename = re.sub(r'[\/:*?"<>|]', '_', title) + ".pdf"
        filepath = download_file(pdf_link, save_path, filename)
        if filepath:
            papers.append((title, filepath))
        time.sleep(1)
    return papers


def ask_ollama(query, context, llm):
    """
    将 PDF 内容作为上下文，并向大模型提问
    返回模型回答的字符串，并过滤掉 <think>...</think> 部分
    """
    prompt = f"以下是文档内容的一部分:\n\n{context}\n\n基于此内容，请回答：{query}"
    response = llm.invoke(prompt)
    # 如果返回内容中包含 <think> 标签，则将其过滤掉
    filtered_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    return filtered_response.strip()


def load_pdf(file_path):
    """
    使用 LangChain 解析 PDF 文件，返回文档对象列表
    """
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    return documents


def run_agent(paper_keyword, total_count, save_path="papers", question=None, model_name="deepseek-r1:1.5b"):
    """
    运行 agent，实现以下功能：
      - 根据传入的论文关键词搜索 arXiv，并下载总数不超过 total_count 的论文 PDF，
      - 对每篇论文调用大模型，传入指定问题进行问答，
      - 将每篇论文的回答写入一个名为 "论文质量评估YYYYMMDD.txt" 的文件中，

    参数：
      - paper_keyword: 搜索关键词（字符串）
      - total_count: 论文下载数量（整数）
      - save_path: 保存 PDF 的路径（默认 "papers"）
      - question: 大模型提问的问题；若未指定，则默认：
          "帮我生成这篇文章的中文摘要，并从新意度、有效性、问题大小三个维度综合评估这篇文章的价值，
           满分十分，生成完中文摘要后，打出你认为的评分。"
    """
    # 初始化本地大模型
    llm = OllamaLLM(model=model_name)

    if question is None:
        question = ("帮我生成这篇文章的中文摘要，并从新意度、有效性、问题大小三个维度综合评估这篇文章的价值，"
                    "满分十分，生成完中文摘要后，打出你认为的评分。")

    os.makedirs(save_path, exist_ok=True)

    # 对关键词进行 URL 编码
    encoded_keyword = quote(paper_keyword)
    base_url = (f"https://arxiv.org/search/?query={encoded_keyword}&searchtype=abstract"
                "&abstracts=show&order=-announced_date_first&size=50")

    papers_downloaded = []
    pages = math.ceil(total_count / 50)
    for page in range(pages):
        if len(papers_downloaded) >= total_count:
            break
        start = page * 50
        page_url = base_url + f"&start={start}"
        print(f"页面: {page + 1}")
        remaining = total_count - len(papers_downloaded)
        papers = get_paper_info(page_url, save_path, max_papers=remaining)
        papers_downloaded.extend(papers)
        time.sleep(3)

    if not papers_downloaded:
        print("未下载到任何论文。")
        return

    # 创建保存大模型回答的输出文件，文件名包含今日日期
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    output_filename = f"论文质量评估{today_str}.md"

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for title, pdf_path in papers_downloaded:
            print(f"正在处理论文: {title}")
            try:
                docs = load_pdf(pdf_path)
                if not docs:
                    print(f"无法解析 PDF 文件: {pdf_path}")
                    continue
                # 这里取 PDF 的第一页内容作为上下文
                context = docs[0].page_content
                answer = ask_ollama(question, context, llm)
                output_text = f"论文标题: {title}\n回答:\n{answer}\n{'-' * 50}\n"
                outfile.write(output_text)
                print(f"论文处理完成\n")
            except Exception as e:
                print(f"处理论文 {title} 时发生错误: {e}")

    print(f"所有论文处理完毕，评估结果保存在 {output_filename}")


if __name__ == '__main__':
    run_agent(paper_keyword="object detection", total_count=5, save_path="papers")