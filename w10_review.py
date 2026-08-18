"""
W10｜RAG 检索增强生成 · 复习模板
"""

# ============================================================
# 第1部分：本周核心概念
# ============================================================
"""
1. RAG 概述：Retrieval-Augmented Generation，检索增强生成；通过外部知识库补充 LLM 实时知识短板。
2. Embedding 原理：将文本映射为高维向量，语义相近的文本向量距离近，用于相似度检索。
3. ChromaDB add三件套：ids（唯一标识）、documents（原始文本）、embeddings（向量），缺一不可。
4. PDF 加载：PyMuPDF（fitz）或 pdfplumber 提取文本；文本质量直接影响检索效果。
5. 文本切块 & pipeline：chunk_size 控制块大小（太大丢细节，太小丢上下文）；完整 RAG 流程：
   PDF加载 → 文本切块 → Embedding入库 → 相似度检索 → 组装 Prompt → LLM 生成。
"""

# ============================================================
# 第2部分：代码骨架（留3个TODO）
# ============================================================
import chromadb
from chromadb.config import Settings
import PyMuPDF  # 或 from pdfminer import pdfminer（任选其一）

# ---------- 第1步：加载 PDF ----------
# TODO 1: 填入 PDF 文件路径，提取全部文本内容
pdf_path = "your_document.pdf"  # ← 替换为你的 PDF 路径
# 使用 PyMuPDF 提取文本
import fitz
doc = fitz.open(pdf_path)
full_text = ""
for page in doc:
    full_text += page.get_text()
doc.close()
print(f"提取文本长度：{len(full_text)} 字符")

# ---------- 第2步：文本切块 ----------
# TODO 2: 选择切块策略，填入 chunk_size 和 chunk_overlap
chunk_size = 500     # ← 尝试改为 300、800 观察检索效果差异
chunk_overlap = 50   # ← 相邻块重叠字符数，保留上下文
chunks = []
for i in range(0, len(full_text), chunk_size - chunk_overlap):
    chunks.append(full_text[i:i + chunk_size])
print(f"切块数量：{len(chunks)}")

# ---------- 第3步：存入 ChromaDB ----------
import chromadb
client = chromadb.Client(Settings(anonymized_telemetry=False))
collection = client.create_collection(name="knowledge_base")
# TODO 3: 填写 ids、documents、embeddings（embeddings 用 None 让 ChromaDB 自动生成）
collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],  # 唯一ID列表
    documents=chunks,                                  # 原始文本块
    embeddings=None,                                   # 传 None → ChromaDB 用内置模型生成向量
)
print(f"已存入 {collection.count()} 条记录")

# ---------- 第4步：查询与生成 ----------
query_text = "这份文档的核心观点是什么？"
results = collection.query(
    query_texts=[query_text],
    n_results=3,  # ← 尝试改为 1、5 观察效果
)
print("检索结果：", results["documents"][0])

# （后续：将 results["documents"] 组装进 Prompt → 调用 LLM 生成答案）


# ============================================================
# 第3部分：改造题
# ============================================================
# 【改造题1】将 chunk_size 改为 200，重新运行，对比检索结果与 chunk_size=500 时有何不同。
#   提示：观察检索到的文档片段是否完整、相关性评分是否有变化。

# 【改造题2】将 n_results 改为 10（collection.query 的 n_results 参数），
#   说明：为什么 n_results 太大反而可能降低生成质量？

# 【改造题3】如果有多个 PDF 文件（list_pdf_paths = ["a.pdf", "b.pdf"]），
#   请修改上述代码，将两个 PDF 的文本合并后再切块入库。
#   提示：在 for 循环中累加 full_text，或为每个 PDF 的 chunk 加前缀区分来源。


# ============================================================
# 第4部分：复习题（无骨架）
# ============================================================
"""
概念题：
1. RAG 和微调（Fine-tuning）分别解决什么问题？什么场景下 RAG 更适合？
2. Embedding 和关键词检索（如正则匹配）的本质区别是什么？请举例说明。
3. ChromaDB 的 collection.query 中，n_results 参数过大或过小会带来什么问题？

代码题：
4. 以下代码尝试向 ChromaDB 添加数据，但报错了。请指出错误原因并修正：
   collection.add(
       documents=["文本块A", "文本块B"],
       embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],  # 两组向量
   )
   （提示：ids 参数在哪里？）

5. 请写出完整的 RAG pipeline：从用户提问 → ChromaDB 检索 → 组装带上下文的 Prompt → 调用 LLM。
   只需写出核心逻辑，不需要完整运行代码。
"""

# ============================================================
# 参考答案（完成后自行对照）
# ============================================================
"""
答案4：collection.add() 必须传入 ids 参数，且 ids 数量必须与 documents/embeddings 数量一致。
       修正：
       collection.add(
           ids=["doc_0", "doc_1"],
           documents=["文本块A", "文本块B"],
           embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],
       )

答案5（核心逻辑）：
from openai import OpenAI
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"))

query = "用户的问题是什么？"
results = collection.query(query_texts=[query], n_results=3)
context = "\n".join(results["documents"][0])

prompt = f"""基于以下参考内容回答用户问题。如果内容不相关，请如实说明。
参考内容：
{context}

用户问题：{query}
"""
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,
)
print(response.choices[0].message.content)
"""
