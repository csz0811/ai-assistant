import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from content_generator import CONTENT_TYPES, generate, render_markdown

st.set_page_config(page_title="AI 内容生成器", page_icon="🤖", layout="wide")

# ===== 美化：自定义 CSS =====
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stApp { font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }
.stButton>button {
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    background-color: #f8f9fa;
    color: #1f2937;
    transition: all .2s;
}
.stButton>button:hover { background-color: #e9ecef; }
/* 品牌蓝主按钮 */
button[data-testid="baseButton-primary"],
button[kind="primary"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 600;
}
button[data-testid="baseButton-primary"]:hover,
button[kind="primary"]:hover {
    background-color: #1d4ed8 !important;
}
/* 结果卡片 */
.result-card {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 18px 22px;
    background: #ffffff;
    margin: 12px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
</style>
""", unsafe_allow_html=True)

# ===== 侧边栏设置 =====
with st.sidebar:
    st.title("⚙️ 设置")
    st.caption("调参实时生效")
    temperature = st.slider("🌡 temperature（创意度）", 0.0, 1.5, 1.5, 0.1, key="temp")
    max_tokens = st.slider("📏 max_tokens（长度上限）", 100, 2000, 800, 50)
    st.divider()
    st.write("W8 · 美化版")
    st.write("预设模式：")
    def set_temp(v):
        st.session_state.temp = v
    st.button("✍️ 文案模式 (0.8)", on_click=set_temp, args=[0.8], use_container_width=True)
    st.button("🔢 精确模式 (0.0)", on_click=set_temp, args=[0.0], use_container_width=True)

# ===== Hero 说明 =====
st.markdown("# 🤖 AI 内容生成器")
st.markdown(
    "> 输入一个话题，选择内容类型，一键生成结构化文案。"
    "支持 **Markdown / JSON 双视图**、历史记录与参考素材上传。"
)
st.divider()

# session_state 历史
if "history" not in st.session_state:
    st.session_state.history = []

# ===== 示例话题（点击填入）=====
st.markdown("**💡 试试这些话题：**")
EXAMPLES = ["咖啡入门", "减肥食谱", "周末旅游", "护肤心得"]
ex_cols = st.columns(len(EXAMPLES))
for i, ex in enumerate(EXAMPLES):
    if ex_cols[i].button(ex, key=f"ex_{i}", use_container_width=True):
        st.session_state.topic_input = ex

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("✏️ 输入话题", value="咖啡", key="topic_input")
with col2:
    type_options = list(CONTENT_TYPES.keys())
    type_key = st.selectbox(
        "📂 内容类型",
        options=type_options,
        format_func=lambda k: CONTENT_TYPES[k]["name"],
    )

uploaded = st.file_uploader("📎 上传参考素材（txt，可选）", type=["txt"])
ref_text = ""
if uploaded is not None:
    if st.session_state.get("uploaded_id") != uploaded.file_id:
        st.session_state.ref_text = uploaded.read().decode("utf-8", errors="ignore")
        st.session_state.uploaded_id = uploaded.file_id
    ref_text = st.session_state.ref_text

view = st.radio("显示方式", ["Markdown", "JSON"], horizontal=True)

if st.button("🚀 生成", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("请先输入话题")
    else:
        t = CONTENT_TYPES[type_key]
        prompt = t["prompt"]
        if ref_text:
            prompt = prompt + f"\n\n参考素材：\n{ref_text}"
        with st.spinner(f"正在生成「{t['name']}」..."):
            data = generate(
                topic, prompt, temperature=temperature, max_tokens=max_tokens
            )
        if data is None:
            st.error("❌ 生成失败，可能是网络或 Key 问题，请稍后重试")
        else:
            st.success("✅ 生成完成！")
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            if view == "Markdown":
                md = render_markdown(t["name"], topic, data)
                st.markdown(md)
                st.download_button(
                    "📥 下载 Markdown", md, file_name=f"{t['name']}_{topic}.md",
                    use_container_width=True,
                )
            else:
                st.json(data)
                st.download_button(
                    "📥 下载 JSON",
                    json.dumps(data, ensure_ascii=False, indent=2),
                    file_name=f"{t['name']}_{topic}.json",
                    use_container_width=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.history.append({"type": t["name"], "topic": topic})

if st.session_state.history:
    st.divider()
    st.subheader("📜 本次会话历史")
    for i, h in enumerate(st.session_state.history):
        st.write(f"{i+1}. 【{h['type']}】{h['topic']}")
    if st.button("🗑 清空历史", use_container_width=True):
        st.session_state.history = []

# ===== 页脚署名 =====
st.divider()
st.caption("© 2026 元帅的 AI 实验室 · 由 DeepSeek + Streamlit 打造")
