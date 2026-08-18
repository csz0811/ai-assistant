"""
W10-D6｜深化语义搜索：多 query 测试 + 距离分析 + metadata 过滤
===============================================================
本文件接 D5 建好的向量库，专门练「检索质量」：
  连库 → 多问题测试 → 看距离判断是否相关 → metadata 过滤

每一步都有 TODO(你填)，填完运行验证。
"""

import chromadb

# ============================================================
# 第1步：连接 D5 已建好的向量库
# ============================================================
# DB_PATH 指向 D5 持久化目录（独立于 PDF 路径）
DB_PATH = "/Users/hechengfajituan/ai-assistant/chroma_db"

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="pdf_knowledge")
print(f"[连接] 向量库已打开，当前共 {collection.count()} 条记录")

# ============================================================
# 第2步：单个问题测试 + 距离判断
# ============================================================
def test_query(question, n_results=3):
    """查一个问题，打印每块的 distances，自动标是否相关"""
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    print(f"\n🔍 查询：「{question}」")
    for i, (doc, dist) in enumerate(
        zip(results['documents'][0], results['distances'][0])
    ):
        # 距离 < 1.0 算真相关，否则只是"最不烂"的块
        tag = "✅相关" if dist < 1.0 else "❌不相关"
        print(f"  第{i+1}条 距离={dist:.3f} {tag}")
        print(f"    内容：{doc[:50]}...")

# ============================================================
# 第3步：多 query 批量测试
# ============================================================
# 和 test_zh.pdf（直播带货 5 页）相关的问题
query_list = [
    "直播带货",          # 预期相关：第1页核心环节
    "选品标准",          # 预期相关：第2页选品
    "主播话术开场",      # 预期相关：第3页话术
    "复盘指标",          # 预期相关：第4页复盘
    "退货率高怎么办",     # 预期相关：第5页 Q&A
    "人工智能",          # 对照组：库里没有这个主题
]

for q in query_list:
    test_query(q, n_results=1)

# ============================================================
# 第4步：metadata 过滤（缩小检索范围）
# ============================================================
# 过滤演示：用 $and 嵌套实现多条件（ChromaDB 0.4.24 不支持并列字段）
filtered = collection.query(
    query_texts=["复盘"],
    n_results=2,
    where={
        "$and": [
            {"来源": "test_zh.pdf"},
            {"块编号": {"$gte": 2}}
        ]
    }
)
print(f"\n📌 加 metadata 过滤后召回 {len(filtered['documents'][0])} 条")
print(collection.get(ids=["chunk_0"])["metadatas"])

# ============================================================
# 改造题（填完跑通再做）
# ============================================================
# ① 把 query_list 换成 3 个和 PDF 真相关的问题，看距离是否都 < 1.0
# ② 把 test_query 的 n_results 改成 1，看 top-1 是否就是最相关块
# ③ 改 where 条件（如 {"块编号": 0}），观察过滤前后召回变化
#
# ⚠️ 如果召回质量整体很差：是因为 D5 用的是测试 PDF（中文乱码）。
#    可以回头把 D5 的 PDF_PATH 换成一个真实 PDF 重跑建库，
#    再回来做 D6，距离会明显变好。
