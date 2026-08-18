# === 功能描述：导入依赖模块，用于读取环境变量、调用 OpenAI 接口、加载 .env 配置 ===
# 导入 os 模块，用于读取系统环境变量（API Key）
import os
# 从 openai 库导入 OpenAI 客户端类
from openai import OpenAI
# 导入 dotenv 的 load_dotenv，用于从 .env 文件加载环境变量
from dotenv import load_dotenv

# === 功能描述：读取 .env 中的 API Key 并初始化 DeepSeek 客户端 ===
# 加载项目根目录下的 .env 文件，把变量写入环境变量
load_dotenv()
# 创建 OpenAI 客户端实例，配置 DeepSeek 的 API Key 与接口地址
client = OpenAI(
    # 从环境变量中读取 DeepSeek 的 API Key
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    # 设置 DeepSeek 兼容 OpenAI 协议的接口地址
    base_url="https://api.deepseek.com"
)

# === 功能描述：尝试用 JSON 模式调用模型，验证 response_format=json_object 是否可用 ===
# 进入异常捕获块，防止接口调用失败导致程序崩溃
try:
    # 调用 DeepSeek 对话接口，要求强制返回 JSON 对象
    r = client.chat.completions.create(
        # 指定使用 deepseek-chat 模型
        model="deepseek-chat",
        # 构造对话消息，提示模型只返回 JSON 对象、不要多余文字
        messages=[{"role": "user", "content": "只返回JSON对象，不要任何其他文字：{\"name\":\"测试\"}"}],
        # 设置响应格式为 JSON 对象，模型会被约束输出合法 JSON
        response_format={"type": "json_object"}
    )
    # 打印成功提示
    print("✅ JSON MODE 成功:")
    # 打印模型返回的 JSON 正文内容
    print(r.choices[0].message.content)
# 捕获所有异常，统一处理 JSON 模式调用失败的情况
except Exception as e:
    # 打印失败提示
    print("❌ JSON MODE 失败:")
    # 打印具体的异常信息
    print(e)
