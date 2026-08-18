# === 功能描述：导入依赖模块，用于路径处理、JSON 解析、命令行参数、调用接口与加载配置 ===
# 导入 os 模块，用于拼接路径、读写文件等操作
import os
# 导入 json 模块，用于解析模型返回的 JSON 字符串与序列化输出
import json
# 导入 sys 模块，用于读取命令行参数
import sys
# 从 openai 库导入 OpenAI 客户端类
from openai import OpenAI
# 导入 dotenv 的 load_dotenv，用于从 .env 文件加载环境变量
from dotenv import load_dotenv

# === 功能描述：加载环境变量、确定项目根目录并初始化 DeepSeek 客户端 ===
# 加载项目根目录下的 .env 文件，把变量写入环境变量
load_dotenv()
# 计算当前脚本所在目录，确定项目根路径（用于后续输出目录拼接）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 创建 OpenAI 客户端实例，配置 DeepSeek 的 API Key 与接口地址
client = OpenAI(
    # 从环境变量中读取 DeepSeek 的 API Key
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    # 设置 DeepSeek 兼容 OpenAI 协议的接口地址
    base_url="https://api.deepseek.com"
)

# === 功能描述：定义内容类型字典，每种类型含中文名称与对应的系统提示词（要求返回 JSON） ===
# 定义内容类型字典，键为编号、值为名称与系统提示词
CONTENT_TYPES = {
    # 第 1 种内容类型：小红书文案
    "1": {
        # 该类型的显示名称
        "name": "小红书文案",
        # 该类型对应的系统提示词（要求模型只返回规范 JSON 对象）
        "prompt": """你是一个资深小红书博主，擅长种草文案。
用户给你一个话题，你必须只返回一个 JSON 对象，不要任何解释或多余文字。
JSON 结构必须严格如下（字段名用中文，不要改）：
{
  "标题": "带1-2个emoji的吸引人标题，不超过20字",
  "正文": "分段式种草正文，合理使用emoji，300字以内，口语化有干货",
  "标签": ["标签1", "标签2", "标签3"],
  "发布时间建议":"早/中/晚，根据话题推荐一个适合发布的时间段"
}"""
    },
    # 第 2 种内容类型：短视频脚本
    "2": {
        # 该类型的显示名称
        "name": "短视频脚本",
        # 该类型对应的系统提示词（要求模型只返回规范 JSON 对象）
        "prompt": """你是一个资深短视频编导。
用户给你一个话题，你必须只返回一个 JSON 对象，不要任何解释或多余文字。
JSON 结构必须严格如下（字段名用中文，不要改）：
{
  "开场钩子": "前3秒抓住注意力的一句话，不超过30字",
  "台词": ["第1句台词", "第2句台词", "第3句台词"],
  "结尾互动": "引导点赞、关注或评论的一句话",
  "时长建议": "如 30秒 或 1分钟",
  "标签": ["标签1", "标签2"]
}"""
    },
    # 第 3 种内容类型：朋友圈
    "3": {
        # 该类型的显示名称
        "name": "朋友圈",
        # 该类型对应的系统提示词（要求模型只返回规范 JSON 对象）
        "prompt": """你是一个朋友圈文案高手，文案自然、有烟火气。
用户给你一个话题，你必须只返回一个 JSON 对象，不要任何解释或多余文字。
JSON 结构必须严格如下（字段名用中文，不要改）：
{
  "文案": "轻松自然的一两句话，可带emoji，不超过50字",
  "配图建议": "建议配什么图，一句话",
  "话题": "#相关话题"
}"""
    },
    # 第 4 种内容类型：微博
    "4":{
        # 该类型的显示名称
        "name":"微博",
        # 该类型对应的系统提示词（要求模型只返回规范 JSON 对象）
        "prompt"""你是一个微博文案高手，文案要结合线下热点热梗，幽默风趣。
用户给你一个话题，你必须只返回一个 JSON 对象，不要任何解释或多余文字。
JSON 结构必须严格如下（字段名用中文，不要改）：
{
  "文案":"幽默风趣的两三句话，内容要根据内容插入合适的网络名词，不超过50字",
  "配图建议":"建议配怎么样的图片，一句话",
  "话题":"#相关话题"  
    }"""
    }
}

# === 功能描述：generate 函数——带重试地调用模型，生成并解析为 JSON 的文案内容 ===
# 定义生成函数：接收话题与系统提示词，支持重试次数、温度与长度上限
def generate(topic, system_prompt, max_retry=3, temperature=1.5, max_tokens=800):
    # 构造发给模型的用户消息，把话题拼接到固定模板里
    user_msg = f"请为这个话题生成内容：{topic}"
    # 循环进行最多 max_retry 次调用（attempt 从 1 开始计数）
    for attempt in range(1, max_retry + 1):
        # 捕获单次调用过程中可能出现的异常，以便重试
        try:
            # 调用 DeepSeek 对话接口，要求返回标准 JSON 对象
            resp = client.chat.completions.create(
                # 指定使用 deepseek-chat 模型
                model="deepseek-chat",
                # 构造消息列表：system 为系统提示词、user 为话题消息
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                # 设置创意度温度（默认 1.5，偏创意）
                temperature=temperature,
                # 设置单次生成的最大 token 数
                max_tokens=max_tokens,
                # 约束模型响应格式为 JSON 对象
                response_format={"type": "json_object"}
            )
            # 解析模型返回的 JSON 字符串为 Python 字典并返回
            return json.loads(resp.choices[0].message.content)
        # 若返回内容不是合法 JSON，打印提示并进入下一次重试
        except json.JSONDecodeError as e:
            print(f"第{attempt}次：返回不是合法JSON，重试... ({e})")
        # 捕获其他异常（如网络错误），打印失败信息并继续重试
        except Exception as e:
            print(f"第{attempt}次失败：{e}")
    # 所有重试均失败则返回 None，表示本次生成未成功
    return None

# === 功能描述：safe_name 函数——把话题清洗为合法文件名（仅保留字母数字、空格、下划线、连字符） ===
# 定义文件名清洗函数，接收话题字符串
def safe_name(topic):
    # 过滤出字母数字或空格/下划线/连字符，拼接后去除首尾空白；为空则用“未命名”
    return "".join(c for c in topic if (c.isalnum() or c in " _-")).strip() or "未命名"

# === 功能描述：save_json 函数——把生成结果写入 outputs 目录下的 JSON 文件 ===
# 定义保存 JSON 函数：接收类型名、数据与清洗后的文件名
def save_json(type_name, data, safe):
    # 拼接输出目录路径（项目根目录下的 outputs 文件夹）
    out_dir = os.path.join(BASE_DIR, "outputs")
    # 若输出目录不存在则创建（exist_ok 避免已存在时报错）
    os.makedirs(out_dir, exist_ok=True)
    # 拼接最终 JSON 文件路径（类型名_文件名.json）
    path = os.path.join(out_dir, f"{type_name}_{safe}.json")
    # 以 UTF-8 编码打开文件准备写入
    with open(path, "w", encoding="utf-8") as f:
        # 把数据以缩进 2、保留中文的方式写入 JSON 文件
        json.dump(data, f, ensure_ascii=False, indent=2)
    # 返回写好的文件路径，便于后续展示与下载
    return path

# === 功能描述：render_markdown 函数——把 JSON 数据渲染为可读的 Markdown 文本 ===
# 定义 Markdown 渲染函数：接收类型名、话题与数据字典
def render_markdown(type_name, topic, data):
    # 初始化行列表，先放入一级标题与空行
    lines = [f"# {type_name}：{topic}", ""]
    # 遍历数据字典的每一个字段
    for key, val in data.items():
        # 把当前字段名作为二级标题加入
        lines.append(f"## {key}")
        # 判断字段值是否为列表（用于不同字段的特殊排版）
        if isinstance(val, list):
            # 若为“台词”字段，按序号逐条列出
            if key == "台词":
                # 遍历台词列表，用序号编号输出
                for i, item in enumerate(val, 1):
                    # 追加第 i 条台词（带序号）
                    lines.append(f"{i}. {item}")
            # 若为“标签”字段，把标签拼成带 # 的话题串
            elif key == "标签":
                # 把每个标签前加 # 并用空格连接
                lines.append(" ".join(f"#{v}" for v in val))
            # 若为“发布时间建议”字段，直接拼接各选项
            elif key == "发布时间建议":
                # 用空格连接各时间建议
                lines.append(" ".join(f"{v}" for v in val))
            # 其他列表字段，逐条以无序列表展示
            else:
                # 遍历列表每一项
                for item in val:
                    # 还原转义换行符，并清理回车符
                    clean = str(item).replace("\\n", "\n").replace("\\r", "")
                    # 以无序列表项追加
                    lines.append(f"- {clean}")
        # 字段值不是列表时，作为普通文本处理
        else:
            # 还原转义换行符并清理回车符
            text = str(val).replace("\\n", "\n").replace("\\r", "")
            # 追加纯文本行
            lines.append(text)
        # 每个字段后追加一个空行做分隔
        lines.append("")
    # 把全部行用换行符连接成完整 Markdown 文本并返回
    return "\n".join(lines)

# === 功能描述：show_menu 函数——在控制台打印可选的内容类型菜单 ===
# 定义菜单展示函数
def show_menu():
    # 打印选择提示
    print("选择内容类型：")
    # 遍历内容类型字典，逐项打印编号与名称
    for k, v in CONTENT_TYPES.items():
        # 打印形如“  1. 小红书文案”的菜单项
        print(f"  {k}. {v['name']}")

# === 功能描述：主程序入口——解析参数、选择类型、调用生成并保存 JSON 与 Markdown ===
# 仅在作为脚本直接运行时执行以下逻辑
if __name__ == "__main__":
    # 读取命令行参数（去掉脚本名后的所有参数）
    args = sys.argv[1:]
    # 若存在第 1 个参数则作为话题，否则交互式输入
    topic = args[0] if len(args) >= 1 else input("输入话题：")
    # 若存在第 2 个参数则作为类型编号，否则暂置为 None 待交互选择
    type_key = args[1] if len(args) >= 2 else None

    # 当未指定或指定的编号不在字典中时，进入交互选择流程
    if type_key not in CONTENT_TYPES:
        # 展示内容类型菜单
        show_menu()
        # 读取用户输入的编号并去除首尾空白
        type_key = input("输入编号：").strip()
        # 当编号非法时循环提示重新输入
        while type_key not in CONTENT_TYPES:
            # 提示编号不对并重新读取
            type_key = input("编号不对，重新输入：").strip()

    # 取出所选类型对应的名称与提示词配置
    t = CONTENT_TYPES[type_key]
    # 打印开始生成的提示（含类型名与话题）
    print(f"\n🎯 正在生成「{t['name']}」：{topic}")
    # 调用生成函数拿到 JSON 数据
    data = generate(topic, t["prompt"])
    # 若生成返回 None，表示本次失败
    if data is None:
        # 打印失败提示
        print("❌ 生成失败，请稍后重试")
    # 生成成功时，进行保存与展示
    else:
        # 把话题清洗为安全的文件名片段
        safe = safe_name(topic)
        # 保存 JSON 文件并拿到路径
        json_path = save_json(t["name"], data, safe)
        # 拼接 Markdown 输出文件路径
        md_path = os.path.join(BASE_DIR, "outputs", f"{t['name']}_{safe}.md")
        # 以 UTF-8 编码打开 Markdown 文件准备写入
        with open(md_path, "w", encoding="utf-8") as f:
            # 写入渲染好的 Markdown 文本
            f.write(render_markdown(t["name"], topic, data))
        # 打印生成成功提示
        print("\n✅ 生成完成！")
        # 以可读格式打印 JSON 数据（保留中文）
        print(json.dumps(data, ensure_ascii=False, indent=2))
        # 打印 JSON 文件路径
        print(f"\n📁 JSON:     {json_path}")
        # 打印 Markdown 文件路径
        print(f"📄 Markdown: {md_path}")
