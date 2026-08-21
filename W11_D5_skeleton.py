# === W11-D5 骨架: 完整 RAG 闭环 (retriever + DeepSeek + LCEL) ===
# 用法: PyCharm 打开, 改 TODO, 底部 Terminal:
#   source ~/ai-assistant/venv/bin/activate && python W11_D5_skeleton.py
# 验证: 问文档内问题 → 基于文档答; 问文档外问题 → "不知道"
# 注意: 本骨架会调用 DeepSeek API (消耗少量 token)

import os
os.environ["SSL_CERT_FILE"] = "/etc/ssl/cert.pem"
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 里的 DEEPSEEK_API_KEY (不硬编码 key)

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI  # DeepSeek 用 OpenAI 格式
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# === 1. bge + 建库 (D2+D3 成果) ===
emb = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh")
# TODO(你填): 换成你自己的文档
raw_docs = [
    Document(page_content="猫喜欢抓老鼠是天性，这是猫的本能。", metadata={"src": "a"}),
    Document(page_content="股票投资有风险，需要谨慎评估。", metadata={"src": "b"}),
    Document(page_content="利群是一个香烟品牌。",metadata={"src": "c"}),
    Document(page_content="iPhone是苹果手机", metadata={"src": "j"}),
]
# ⚠️ 坑: 同目录重复 from_documents 会追加, 改 raw_docs 删 ./chroma_db_d5 重跑
vs = Chroma.from_documents(documents=raw_docs, embedding=emb, persist_directory="./chroma_db_d5")

# === 2. retriever (把库转检索器) ===
# TODO(你填): k 改成 2 看效果
retriever = vs.as_retriever(search_kwargs={"k": 2})

# === 3. llm (DeepSeek, OpenAI 格式) ===
# ⚠️ 坑: base_url 不带 /v1 (DeepSeek = https://api.deepseek.com)
# ⚠️ 坑: temperature=0 保证稳定可复现, RAG 场景不要创意生成
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
)

# === 4. prompt (约束: 不知道就说不知道, 防幻觉) ===
# TODO(你填): 想清楚为什么必须加"上下文没有就回答不知道"
prompt = ChatPromptTemplate.from_template(
    "只根据上下文回答，上下文没有就回答不知道。\n上下文:\n{context}\n问题: {question}"
)

# === 5. format + LCEL 管道 (替代已删的 RetrievalQA) ===
def format_docs(docs):
    return "\n".join(d.page_content for d in docs)

# ⚠️ 坑: 1.x 用 LCEL 管道, 已删的 RetrievalQA 不可用
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# === 6. 测试 ===
user_q = input("请输入你的问题： ")
print(rag_chain.invoke(user_q))
