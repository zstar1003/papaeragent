import os
import requests
import re
import math
import time
import warnings

from lxml import html
from bs4 import BeautifulSoup


warnings.filterwarnings("ignore")


def get_total_results(url):
    """获取总结果数"""
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


# 下载文章和代码到相应的文件夹
def download_file(url, folder, filename):
    filepath = os.path.join(folder, filename)
    if os.path.exists(filepath):
        print(f"文件已存在，跳过下载: {filename}")
        return True
    try:
        print(f"开始下载: {url}")  # 增加调试信息
        response = requests.get(url)
        response.raise_for_status()
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"成功下载: {filename}\n")
        return True
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {url}, 错误: {e}\n")
    except IOError as e:
        print(f"文件保存失败: {filename}, 错误: {e}\n")
    return False

def get_paper_info(url, save_path):
    """根据URL爬取一页的论文信息"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    papers = []

    for article in soup.find_all('li', class_='arxiv-result'):
        title = article.find('p', class_='title').text.strip()
        authors_text = article.find('p', class_='authors').text.replace('Authors:', '').strip()
        authors = [author.strip() for author in authors_text.split(',')]
        abstract = article.find('span', class_='abstract-full').text.strip()
        submitted = article.find('p', class_='is-size-7').text.strip()
        submission_date = submitted.split(';')[0].replace('Submitted', '').strip()
        pdf_link_element = article.find('a', text='pdf')
        if pdf_link_element:
            pdf_link = pdf_link_element['href']
        else:
            pdf_link = 'No PDF link found'
        print(title, ":", pdf_link)
        filename = re.sub(r'[\/:*?"<>|]', '_', title) + ".pdf"  # 处理非法文件名
        download_success = download_file(pdf_link, save_path, filename)
        if not download_success:
            print(f"论文 {title} 的 PDF 下载失败，跳过")
            continue
        time.sleep(1)
    return papers


# 主程序
if __name__ == '__main__':
    save_path = "pdfs"
    base_url ="https://arxiv.org/search/?query=object+detect&searchtype=abstract&abstracts=show&order=-announced_date_first&size=50"
    os.makedirs(save_path, exist_ok=True)
    total_results = get_total_results(base_url + "&start=0")
    pages = math.ceil(total_results / 50)
    all_papers = []

    for page in range(pages):
        start = page * 50
        print(f"Crawling page {page + 1}/{pages}, start={start}")
        page_url = base_url + f"&start={start}"
        all_papers.extend(get_paper_info(page_url, save_path=save_path))
        time.sleep(3)  # 等待三秒以避免对服务器造成过大压力

    print(f"完成！总共爬取到 {len(all_papers)} 条数据。")