"""
W10-D5｜PDF读取 → 切块 → 存入 ChromaDB 完整 pipeline
=======================================================
本文件 = RAG 的 Retrieval 全流程：
  PDF读取 → 切块 → 向量化 → 存入向量库

每一步都有 TODO(你填)，手敲完成后运行验证。
"""

import fitz  # PyMuPDF，W10-D3 学过
import chromadb
from chromadb.config import Settings
import os

# ============================================================
# 第1步：读取 PDF
# ============================================================
# 默认指向我们刚生成的支持中文的测试 PDF（直播带货主题）
PDF_PATH = "/Users/hechengfajituan/ai-assistant/test_zh.pdf"

def read_pdf(path, max_pages=3):
    """读取 PDF 前 max_pages 页，返回拼接后的纯文本"""
    doc = fitz.open(path)
    texts = []
    for page in doc[:max_pages]:
        text = page.get_text()
        texts.append(text)
    doc.close()
    # 用两个换行拼接各页
    return "\n\n".join(texts)

raw_text = read_pdf(PDF_PATH)
print(f"[Step1] PDF读取完成，字符数：{len(raw_text)}")

# ============================================================
# 第2步：切块
# ============================================================
# 调整后：每块更大、保留更多上下文重叠
CHUNK_SIZE = 200   # 块大小
OVERLAP    = 30    # 相邻块重叠字符数

def chunk_text(text, chunk_size, overlap):
    """把长文本切成重叠的小块"""
    step = chunk_size - overlap
    chunks = []
    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        if chunk:  # 空块不要
            chunks.append(chunk)
        # 切到末尾了就停
        if i + chunk_size >= len(text):
            break
    return chunks

chunks = chunk_text(raw_text, CHUNK_SIZE, OVERLAP)
print(f"[Step2] 切块完成，共 {len(chunks)} 块，每块最大 {CHUNK_SIZE} 字符")

# ============================================================
# 第3步：存入 ChromaDB（持久化版）
# ============================================================
# 独立变量：向量库目录路径（和 PDF 路径分开）
DB_PATH = "/Users/hechengfajituan/ai-assistant/chroma_db"
PDF_NAME = os.path.basename(PDF_PATH)  # 自动从路径取文件名，做 metadata 用

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="pdf_knowledge")

# 构造 ids 和 metadatas（id 唯一，metadata 存来源信息）
ids = [f"chunk_{i}" for i in range(len(chunks))]
metadatas = [{"来源": PDF_NAME, "块编号": i} for i in range(len(chunks))]

# add 三件套：documents / ids / metadatas 必须等长
collection.add(
    documents=chunks,
    ids=ids,
    metadatas=metadatas
)
print(f"[Step3] 存入 ChromaDB 完成，共 {collection.count()} 条记录")

# ============================================================
# 第4步：查询验证（语义搜索）
# ============================================================
# TODO(你填)：把查询问题改成你想测试的内容
QUERY = "python"  # ← 改这个

results = collection.query(
    query_texts=[QUERY],
    n_results=2
)

print(f"\n[Step4] 查询「{QUERY}」，召回 {len(results['documents'][0])} 条：")
for i, doc in enumerate(results['documents'][0]):
    dist = results['distances'][0][i]
    print(f"  第{i+1}条（距离={dist:.3f}）：{doc[:60]}...")

# ============================================================
# 改造题（手敲完成后再做）
# ============================================================
# ① 把 CHUNK_SIZE 改成 200，OVERLAP 改成 30，对比块数量变化
# ② 把 DB_PATH 改成 "./chroma_db_v2"，第二次运行看 collection.count() 是否累加
# ③ 把 QUERY 改成其他问题，看召回的文档是否和"人工智能"相关
