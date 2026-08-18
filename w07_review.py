"""
W7｜LLM API调用 · 复习模板
"""

# ============================================================
# 第1部分：本周核心概念
# ============================================================
"""
1. LLM API调用：通过 openai 兼容接口向云端 LLM 发送请求，获取文本补全。
2. DeepSeek 切换三处：model 名 / base_url（API地址）/ api_key（密钥）。
3. temperature：控制输出随机性。0~0.3 偏确定，0.7~1.0 偏创意，默认常取 0.7。
4. 多轮对话 messages：role（system/user/assistant）+ content，传入历史实现上下文记忆。
5. JSON mode & 错误码：response_format={"type":"json_object"} 强制结构化；
   429=速率超限 / 401=鉴权失败 / 400=请求格式错误。
"""

# ============================================================
# 第2部分：代码骨架（留3个TODO）
# ============================================================
import os
from openai import OpenAI

# TODO 1: 填入你的 DeepSeek API Key（可从环境变量读取）
api_key = os.getenv("DEEPSEEK_API_KEY") or "YOUR_KEY_HERE"

# TODO 2: 初始化客户端，填入正确的 base_url
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",  # ← 替换这里
)

# 构造多轮对话 messages
messages = [
    {"role": "system", "content": "你是一个乐于助人的助手。"},
    # TODO 3: 添加一条 user 消息，内容为"用一句话介绍你自己"
    {"role": "user", "content": "用一句话介绍你自己"},
]

# 调用 LLM
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    temperature=0.7,  # ← 可尝试改为 0.2 或 1.0 对比效果
    response_format={"type": "json_object"},  # 开启 JSON mode
)

# 解析输出
result = response.choices[0].message.content
print(result)


# ============================================================
# 第3部分：改造题
# ============================================================
# 【改造题1】将 temperature 改为 0.2，观察输出稳定性变化。

# 【改造题2】将 model 改为 "deepseek-coder"，体验不同模型的回复差异。

# 【改造题3】在 messages 中添加一条 assistant 回复，让模型接着说：
messages.append({"role": "assistant", "content": result})
messages.append({"role": "user", "content": "再详细说说刚才的内容"})


# ============================================================
# 第4部分：复习题（无骨架）
# ============================================================
"""
概念题：
1. 调用 DeepSeek API 需要修改哪三处配置？请分别说明。
2. temperature=0 和 temperature=1 时，模型输出有什么本质区别？
3. messages 列表中 system/user/assistant 三种 role 分别代表什么角色？

代码题：
4. 以下代码中，429 错误通常由什么原因引起？应如何处理？
   try:
       response = client.chat.completions.create(model="deepseek-chat", messages=messages)
   except Exception as e:
       print(e)

5. 请补全代码，使模型返回 JSON 格式的自我介绍（包含 name、age、city 三个字段）。
"""


# ============================================================
# 参考答案（完成后自行对照）
# ============================================================
"""
答案4：429 = Rate limit exceeded，短时间内请求次数过多。处理方式：加 time.sleep 降频，
       或在代码中捕获429后等待若干秒再重试（指数退避）。
答案5：
messages = [
    {"role": "system", "content": "你是一个JSON生成器，必须返回有效的JSON对象，包含name、age、city三个字段，不要包含其他文字。"},
    {"role": "user", "content": "用JSON格式介绍你自己"}
]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    temperature=0,
    response_format={"type": "json_object"}
)
print(response.choices[0].message.content)
"""
