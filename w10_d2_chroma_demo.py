import chromadb

# ① 建客户端（内存版，最简单，不依赖外部服务）
client = chromadb.Client()

# ② 建 Collection（类似一张"表"，存一组相关文档）
collection = client.create_collection(name="demo")

# ③ 插入文档：ChromaDB 会自动把文本转成向量（默认 sentence-transformers）
#    documents=文本，ids=唯一标识，metadatas=可过滤的元数据
collection.add(
    documents=[
        "苹果公司发布了新款 iPhone",
        "特斯拉的电动车销量领先",
        "Python 是一门易学的编程语言",
        "篮球是 NBA 最受欢迎的运动",
        "抖音是一个短视频平台",
        "长嘴是利群品牌香烟的其中一款",
    ],
    ids=["d1", "d2", "d3", "d4","d5","d6"],
    metadatas=[
        {"类别": "科技"},
        {"类别": "汽车"},
        {"类别": "编程"},
        {"类别": "体育"},
        {"类别":"平台"},
        {"类别":"香烟"},
    ],
)

# ④ 语义查询：问"哪家公司做手机"，应召回最相关片段
results = collection.query(
    query_texts=["哪家公司做手机？"],
    n_results=1,
    where = {"类别":"科技"},
)

print("召回的文档：")
for doc in results["documents"][0]:
    print(" -", doc)
print("\n相似度距离（越小越相似）：", results["distances"][0])

# 🛠 改造题（手敲）：
#   1) 再用 collection.add 加 2 条自己的文档
#   2) 把 n_results 改成 3，看召回变化
#   3) 加 metadata 过滤：collection.query(..., where={"类别": "科技"})
