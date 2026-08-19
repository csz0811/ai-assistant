# === W11-D1: 用 LangChain Document Loader 加载 PDF/Word/Markdown ===
# 注意：教程的 from langchain.document_loaders 已废弃
#       新版统一改成 from langchain_community.document_loaders

from langchain_community.document_loaders import(
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)

# === 1. 加载 PDF ===
# TODO(你填): 换成你自己的 PDF 路径；下面是我生成的测试文件
PDF_PATH = "/Users/hechengfajituan/Desktop/AI学习知识库/W11测试文件/demo.pdf"
pdf_loader = PyPDFLoader(PDF_PATH)
pdf_docs = pdf_loader.load() # 返回List[Document]

# === 2. 打印 PDF 结果 ===
# ⚠️ 坑: 扫描件(图片型)PDF 读出来是空文本，需要 OCR 才能加载
print(f"PDF 文档块数：{len(pdf_docs)}")
print(f"PDF 前200字：{pdf_docs[0].page_content[:200]}")
print(f"PDF 元数据： {pdf_docs[0].metadata}")


# === 3. 加载 Word(.docx) ===
# TODO(你填): 换成你自己的 .docx；注意 .doc 老格式不支持
DOCX_PATH = ("/Users/hechengfajituan/Desktop/AI学习知识库/W11测试文件/demo.docx")
docx_loader = Docx2txtLoader(DOCX_PATH)
docx_docs = docx_loader.load()
print(f"Word 文档块数：{len(docx_docs)}")
print(f"Word 前200字：{docx_docs[0].page_content[:200]}")


# === 4. 加载 Markdown ===
# TODO(你填): 换成你自己的 .md；encoding 必须 utf-8 否则中文乱码
MD_PATH = "/Users/hechengfajituan/Desktop/AI学习知识库/W11测试文件/demo.md"
md_loader = TextLoader(MD_PATH,encoding="utf-8")
md_docs = md_loader.load()
print(f"Markdown 文档块数:{len(md_docs)}")
print(f"Markdown 前200字：{md_docs[0].page_content[:200]}")