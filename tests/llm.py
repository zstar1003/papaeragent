from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyMuPDFLoader

# 连接本地 Ollama
llm = OllamaLLM(model="deepseek-r1:1.5b")

def ask_ollama(query, context):
    """将 PDF 内容作为上下文，并向 Ollama 提问"""
    prompt = f"以下是文档内容的一部分:\n\n{context}\n\n基于此内容，请回答：{query}"
    response = llm.invoke(prompt)
    return response

def load_pdf(file_path):
    """使用 LangChain 解析 PDF 文件"""
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    return documents

pdf_path = "pdfs/DEAL-YOLO_ Drone-based Efficient Animal Localization using YOLO.pdf"
docs = load_pdf(pdf_path)

# 读取PDF前几页的文本
pdf_text = "\n".join([doc.page_content for doc in docs[:1]])  # 只取前3页

# 提问 Ollama
question = "这篇论文的主要结论是什么？"
answer = ask_ollama(question, pdf_text)

print("Ollama 的回答：", answer)