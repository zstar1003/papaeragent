from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(file_path):
    """使用 LangChain 解析 PDF 文件"""
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    return documents

pdf_path = "pdfs/DEAL-YOLO_ Drone-based Efficient Animal Localization using YOLO.pdf"
docs = load_pdf(pdf_path)

# 仅显示前500个字符，确保成功加载
print(docs[1].page_content[:10000])
