# === 功能描述：导入依赖模块，并配置模块搜索路径以便导入本地 content_generator ===
# 导入 sys 模块，用于操作模块搜索路径
import sys
# 导入 os 模块，用于获取当前文件所在目录
import os
# 导入 json 模块，用于把结果序列化为 JSON 文本
import json

# 把当前文件所在目录加入模块搜索路径，便于导入同目录下的模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入 Streamlit 网页框架
import streamlit as st
# 从本地 content_generator 模块导入内容类型、生成函数与 Markdown 渲染函数
from content_generator import CONTENT_TYPES, generate, render_markdown

# === 功能描述：设置网页标题、图标与宽屏布局 ===
# 配置页面：标题、emoji 图标、宽屏布局
st.set_page_config(page_title="AI 内容生成器", page_icon="🤖", layout="wide")

# ===== 美化：自定义 CSS =====
# === 功能描述：注入自定义 CSS 样式，隐藏默认元素并美化按钮与结果卡片 ===
# 通过 markdown 注入一段 CSS（允许原生 HTML），用于隐藏菜单/页脚、定制按钮与卡片
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
# === 功能描述：渲染侧边栏，提供温度/长度滑块与一键预设模式按钮 ===
# 以侧边栏容器上下文渲染设置区
with st.sidebar:
    # 侧边栏标题
    st.title("⚙️ 设置")
    # 侧边栏说明文字
    st.caption("调参实时生效")
    # 创意度滑块，默认 1.5，写入 session_state 的 temp 键
    temperature = st.slider("🌡 temperature（创意度）", 0.0, 1.5, 1.5, 0.1, key="temp")
    # 长度上限滑块，范围 100~2000，默认 800
    max_tokens = st.slider("📏 max_tokens（长度上限）", 100, 2000, 800, 50)
    # 分隔线
    st.divider()
    # 显示版本/周次信息
    st.write("W8 · 美化版")
    # 显示预设模式提示
    st.write("预设模式：")
    # 定义把温度写入 session_state 的回调函数
    def set_temp(v):
        # 把传入的温度值写入 session_state.temp
        st.session_state.temp = v
    # 文案模式按钮：点击后把温度设为 0.8
    st.button("✍️ 文案模式 (0.8)", on_click=set_temp, args=[0.8], use_container_width=True)
    # 精确模式按钮：点击后把温度设为 0.0
    st.button("🔢 精确模式 (0.0)", on_click=set_temp, args=[0.0], use_container_width=True)

# ===== Hero 说明 =====
# === 功能描述：渲染顶部标题、说明文案与分隔线 ===
# 页面主标题
st.markdown("# 🤖 AI 内容生成器")
# 页面说明文案（引号内两段字符串自动拼接为一段说明）
st.markdown(
    "> 输入一个话题，选择内容类型，一键生成结构化文案。"
    "支持 **Markdown / JSON 双视图**、历史记录与参考素材上传。"
)
# 分隔线
st.divider()

# session_state 历史
# === 功能描述：初始化会话历史列表，用于记录本次会话的生成记录 ===
# 若 session_state 中尚无 history，则初始化为空列表
if "history" not in st.session_state:
    # 创建空的历史列表
    st.session_state.history = []

# ===== 示例话题（点击填入）=====
# === 功能描述：展示可点击的示例话题，点击后自动填入输入框 ===
# 显示示例话题提示
st.markdown("**💡 试试这些话题：**")
# 定义示例话题列表
EXAMPLES = ["咖啡入门", "减肥食谱", "周末旅游", "护肤心得"]
# 按示例数量创建等宽列，用于横向排布按钮
ex_cols = st.columns(len(EXAMPLES))
# 遍历示例话题，为每个生成按钮
for i, ex in enumerate(EXAMPLES):
    # 若点击该示例按钮，把话题写入 session_state.topic_input
    if ex_cols[i].button(ex, key=f"ex_{i}", use_container_width=True):
        # 更新输入框的值为该示例话题
        st.session_state.topic_input = ex

# === 功能描述：创建两列布局，分别放置话题输入框与内容类型下拉选择 ===
# 创建左右两列（各占一半）
col1, col2 = st.columns(2)
# 在第一列中渲染话题输入框
with col1:
    # 话题文本输入框，默认值“咖啡”，键为 topic_input
    topic = st.text_input("✏️ 输入话题", value="咖啡", key="topic_input")
# 在第二列中渲染内容类型选择
with col2:
    # 取出内容类型的所有编号作为选项
    type_options = list(CONTENT_TYPES.keys())
    # 内容类型下拉框，显示名称为各类型的中文名
    type_key = st.selectbox(
        # 选择框标签
        "📂 内容类型",
        # 选项为内容类型编号列表
        options=type_options,
        # 显示时把编号映射为中文名称
        format_func=lambda k: CONTENT_TYPES[k]["name"],
    )

# === 功能描述：提供可选的参考素材上传（txt），读取后存入 session_state ===
# 创建仅接受 txt 的文件上传组件
uploaded = st.file_uploader("📎 上传参考素材（txt，可选）", type=["txt"])
# 初始化参考文本为空字符串
ref_text = ""
# 当用户上传了文件时
if uploaded is not None:
    # 若本次上传的文件与上次不同，则重新读取内容
    if st.session_state.get("uploaded_id") != uploaded.file_id:
        # 读取文件内容并解码为 UTF-8 文本（忽略解码错误）
        st.session_state.ref_text = uploaded.read().decode("utf-8", errors="ignore")
        # 记录本次文件 id，避免重复读取
        st.session_state.uploaded_id = uploaded.file_id
    # 取出已读取的参考文本
    ref_text = st.session_state.ref_text

# === 功能描述：提供结果展示方式（Markdown / JSON）的单选 ===
# 创建水平排列的单选框，选择结果展示方式
view = st.radio("显示方式", ["Markdown", "JSON"], horizontal=True)

# === 功能描述：生成按钮逻辑——组装提示词、调用生成、按所选方式展示与下载 ===
# 创建主生成按钮（品牌蓝主按钮，占满宽度）
if st.button("🚀 生成", type="primary", use_container_width=True):
    # 若话题为空，给出警告并中止本次生成
    if not topic.strip():
        # 提示用户先输入话题
        st.warning("请先输入话题")
    # 话题有效时，进入生成流程
    else:
        # 取出所选内容类型的配置
        t = CONTENT_TYPES[type_key]
        # 取出对应的系统提示词
        prompt = t["prompt"]
        # 若上传了参考素材，则把素材追加进提示词
        if ref_text:
            # 把参考素材拼接在提示词末尾
            prompt = prompt + f"\n\n参考素材：\n{ref_text}"
        # 在加载动画中调用生成函数
        with st.spinner(f"正在生成「{t['name']}」..."):
            # 调用生成函数拿到 JSON 数据（传入当前温度与长度上限）
            data = generate(
                topic, prompt, temperature=temperature, max_tokens=max_tokens
            )
        # 若生成返回 None，表示失败
        if data is None:
            # 显示生成失败的错误提示
            st.error("❌ 生成失败，可能是网络或 Key 问题，请稍后重试")
        # 生成成功时展示结果
        else:
            # 显示成功提示
            st.success("✅ 生成完成！")
            # 渲染结果卡片的开启标签（自定义样式）
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            # 若选择 Markdown 视图
            if view == "Markdown":
                # 调用渲染函数得到 Markdown 文本
                md = render_markdown(t["name"], topic, data)
                # 在页面上展示 Markdown
                st.markdown(md)
                # 提供 Markdown 文件下载按钮
                st.download_button(
                    # 按钮文案
                    "📥 下载 Markdown", md, file_name=f"{t['name']}_{topic}.md",
                    # 占满宽度
                    use_container_width=True,
                )
            # 若选择 JSON 视图
            else:
                # 以 JSON 形式展示数据
                st.json(data)
                # 提供 JSON 文件下载按钮（序列化为可读文本）
                st.download_button(
                    # 按钮文案
                    "📥 下载 JSON",
                    # 把数据序列化为缩进、保留中文的 JSON 字符串
                    json.dumps(data, ensure_ascii=False, indent=2),
                    # 下载文件名
                    file_name=f"{t['name']}_{topic}.json",
                    # 占满宽度
                    use_container_width=True,
                )
            # 渲染结果卡片的闭合标签
            st.markdown('</div>', unsafe_allow_html=True)
            # 把本次生成记录追加到会话历史
            st.session_state.history.append({"type": t["name"], "topic": topic})

# === 功能描述：若本会话已有历史，则展示历史列表并提供清空按钮 ===
# 当历史列表非空时
if st.session_state.history:
    # 分隔线
    st.divider()
    # 历史区小标题
    st.subheader("📜 本次会话历史")
    # 遍历历史记录
    for i, h in enumerate(st.session_state.history):
        # 逐条展示历史（序号、类型、话题）
        st.write(f"{i+1}. 【{h['type']}】{h['topic']}")
    # 清空历史按钮
    if st.button("🗑 清空历史", use_container_width=True):
        # 把历史列表重置为空
        st.session_state.history = []

# ===== 页脚署名 =====
# === 功能描述：渲染页脚署名信息 ===
# 分隔线
st.divider()
# 页脚署名说明
st.caption("© 2026 元帅的 AI 实验室 · 由 DeepSeek + Streamlit 打造")
