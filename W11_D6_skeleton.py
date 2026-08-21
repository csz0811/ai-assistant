# === W11-D6 骨架: 答案溯源 (代码级, 拿 retriever metadata) ===
# 用法: PyCharm 打开, 改 TODO, 底部 Terminal:
#   source ~/ai-assistant/venv/bin/activate && python W11_D6_skeleton.py
# 验证: 回答带来源 src; 文档外问题答不知道(来源可能是兜底chunk)
# 注意: 本骨架会调用 DeepSeek API (消耗少量 token)

import os
os.environ["SSL_CERT_FILE"] = "/etc/ssl/cert.pem"
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 里的 DEEPSEEK_API_KEY

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# === 1. bge + 多文档带 src 来源标签 ===
emb = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh")
# TODO(你填): 换成你自己的多文档, metadata 加 src 字段
raw_docs = [
    Document(page_content="猫喜欢抓老鼠是天性，这是猫的本能。", metadata={"src": "动物百科"}),
    Document(page_content="股票投资有风险，需要谨慎评估。", metadata={"src": "理财指南"}),
    Document(page_content="利群是浙江中烟生产的香烟品牌。", metadata={"src": "品牌库"}),
]
# ⚠️ 坑: 同目录重复 from_documents 会追加, 改 raw_docs 删 ./chroma_db_d6 重跑
vs = Chroma.from_documents(documents=raw_docs, embedding=emb, persist_directory="./chroma_db_d6")
retriever = vs.as_retriever(search_kwargs={"k": 1})

# === 2. llm (DeepSeek, OpenAI 格式) ===
# ⚠️ 坑: base_url 不带 /v1; temperature=0 稳定可复现
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
)

# === 3. prompt (约束防幻觉) ===
prompt = ChatPromptTemplate.from_template(
    "只根据上下文回答，上下文没有就回答不知道。\n上下文:\n{context}\n问题: {question}"
)

# === 4. format + 溯源函数 (拆解 D5 管道, 单独拿 retriever metadata) ===
# ⚠️ 坑: D5 的 LCEL 管道 retriever|format_docs|prompt|llm|parser 拿不到 metadata
#       D6 拆成 retriever.invoke 单独拿 chunk, 再 prompt|llm|parser 生成
def format_docs(docs):
    return "\n".join(d.page_content for d in docs)

def ask_with_source(question):
    retrieved = retriever.invoke(question)  # 检索到的 chunk (含 metadata)
    context = format_docs(retrieved)
    answer = (prompt | llm | StrOutputParser()).invoke({"context": context, "question": question})
    sources = [d.metadata.get("src", "?") for d in retrieved]  # 代码级溯源
    return answer, sources

# === 5. 测试 (可加 while 循环连续问) ===
for q in ["利群是什么", "猫喜欢抓什么", "今天天气如何"]:
    ans, src = ask_with_source(q)
    print(f"问题: {q}")
    print(f"回答: {ans}")
    print(f"来源: {src}")
    print("---")
