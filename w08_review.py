"""
W8｜Streamlit Web应用 · 复习模板
"""

# ============================================================
# 第1部分：本周核心概念
# ============================================================
"""
1. Streamlit 组件：st.title / st.write / st.button / st.text_input / st.selectbox / st.chat_message 等。
2. session_state：页面生命周期内持久化变量，跨组件共享状态，实现"记住"用户输入。
3. sidebar：在 st.sidebar 内放置控件，可折叠、节省主画布，适合设置项与参数面板。
4. columns：st.columns([1,2]) 创建并排列，列内分别放组件，实现左右/多栏布局。
5. download_button & file_uploader：st.download_button 下载文件，st.file_uploader 上传文件；
   深色模式（st.set_page_config theme="dark"）时注意颜色对比度和图表可见性。
"""

# ============================================================
# 第2部分：代码骨架（留3个TODO）
# ============================================================
import streamlit as st

# TODO 1: 页面配置——修改页面标题和图标
st.set_page_config(
    page_title="我的AI助手",  # ← 改成你想要的标题
    page_icon="🤖",
    layout="wide",
)

# TODO 2: 用 st.sidebar 创建侧边栏，在其中加入一个 slider 控制 temperature
st.sidebar.title("⚙️ 设置")
temperature = st.sidebar.slider(
    "Temperature（创意度）",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
)

# 初始化 session_state（用于保存历史对话）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 主区域标题
st.title("💬 AI 对话助手")

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 用户输入
user_input = st.chat_input("请输入问题...")
if user_input:
    # 保存用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # TODO 3: 调用 LLM（这里先用占位，真实调用时替换为 client.chat.completions.create）
    with st.chat_message("assistant"):
        response_text = f"[模拟回复] 你刚才说的是：{user_input}，温度={temperature}"
        st.write(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})

# 下载按钮（导出对话历史）
if st.session_state.messages:
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button(
        label="📥 下载对话历史",
        data=history_text,
        file_name="chat_history.txt",
        mime="text/plain",
    )


# ============================================================
# 第3部分：改造题
# ============================================================
# 【改造题1】将页面标题改为"诗歌生成器"，并在侧边栏加入一个 st.selectbox 选择诗体（绝句/律诗/词）。

# 【改造题2】在主区域加入一个示例按钮，点击后自动填充一段示例问题到输入框：
#   st.button("📌 示例问题", on_click=lambda: st.session_state.update(...))
#   （提示：用 st.session_state 或 JavaScript 方式自动触发 st.chat_input）

# 【改造题3】将布局改为 st.columns([1, 2])，左侧放侧边栏控件，右侧放主聊天区。
#   提示：在 st.columns 外层包裹所有 st.sidebar 调用。


# ============================================================
# 第4部分：复习题（无骨架）
# ============================================================
"""
概念题：
1. session_state 和普通变量有什么区别？为什么在 Streamlit 中需要用它？
2. st.sidebar 和主区域（st.container）的区别是什么？sidebar 有哪些使用限制？
3. 深色模式下 Streamlit 有哪些常见踩坑点？请列举至少2个。

代码题：
4. 以下代码尝试在点击按钮时累加计数，但计数总是不累积，为什么？
   if "count" not in st.session_state:
       st.session_state.count = 0
   if st.button("累加"):
       st.session_state.count += 1
   st.write(st.session_state.count)
   请指出问题并给出正确写法。

5. 请写出用 st.file_uploader 上传 .txt 文件，并在页面显示其内容的完整代码片段。
"""


# ============================================================
# 参考答案（完成后自行对照）
# ============================================================
"""
答案4：Streamlit 每次交互都是全新脚本执行，+=1 只执行一次。正确写法：直接用
       st.session_state.count += 1，Streamlit 会自动触发重新运行（rerun）来更新值。
       关键：累加逻辑写在顶层（if 外），session_state 存的是当前值。

答案5：
uploaded_file = st.file_uploader("上传文本文件", type=["txt"])
if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    st.text_area("文件内容", value=content, height=300)
    st.download_button("下载原文", data=content, file_name=uploaded_file.name, mime="text/plain")
"""
