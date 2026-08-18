# === 功能描述：导入依赖模块，用于读取环境变量、调用 OpenAI 兼容接口、加载 .env 配置 ===
# 导入 os 模块，用于读取系统环境变量（API Key）
import os
# 从 openai 库导入 OpenAI 客户端类，封装对话接口的调用
from openai import OpenAI
# 导入 dotenv 的 load_dotenv，用于把 .env 文件中的变量载入环境变量
from dotenv import load_dotenv

# === 功能描述：读取 .env 中的 API Key 并初始化 DeepSeek 客户端 ===
# 加载项目根目录下的 .env 文件，把其中的键值写入环境变量
load_dotenv()
# 创建 OpenAI 客户端实例，配置 DeepSeek 的 API Key 与接口地址
client = OpenAI(
    # 从环境变量中读取 DeepSeek 的 API Key
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    # 设置 DeepSeek 兼容 OpenAI 协议的接口地址
    base_url="https://api.deepseek.com"
)

# === 功能描述：定义统一的提问内容（本次温度对比实验的共性输入） ===
# 定义要发送给模型的话题提示词
prompt = "用一句话形容夏天的午后"

# === 功能描述：以低温度（0.2）调用模型，观察偏稳定、偏事实的输出 ===
# 打印低温度实验的分组标题
print("=== temperature=0.2（稳，偏事实）===")
# 调用 DeepSeek 对话接口，temperature=0.2 让输出更稳定、更贴近事实
r1 = client.chat.completions.create(
    # 指定使用 deepseek-chat 模型
    model="deepseek-chat",
    # 构造对话消息，role 为 user、content 为话题提示词
    messages=[{"role": "user", "content": prompt}],
    # 设置温度为 0.2（越低越保守、确定）
    temperature=0.2,
    # 限制单次最多生成 50 个 token
    max_tokens=50
)
# 打印模型返回的第一条回复正文
print(r1.choices[0].message.content)

# === 功能描述：以高温度（1.2）调用模型，观察偏跳脱、偏创意的输出 ===
# 打印高温度实验的分组标题（前面加换行做视觉分隔）
print("\n=== temperature=1.2（跳，偏创意）===")
# 调用 DeepSeek 对话接口，temperature=1.2 让输出更随机、更有创意
r2 = client.chat.completions.create(
    # 指定使用 deepseek-chat 模型
    model="deepseek-chat",
    # 构造对话消息，role 为 user、content 为话题提示词
    messages=[{"role": "user", "content": prompt}],
    # 设置温度为 1.2（越高越发散、跳脱）
    temperature=1.2,
    # 限制单次最多生成 50 个 token
    max_tokens=50
)
# 打印模型返回的第一条回复正文
print(r2.choices[0].message.content)
