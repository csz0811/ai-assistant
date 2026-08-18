"""
W4｜API 调用入门 · 代码练习模板
================================
本周目标：requests 调接口 / JSON 解析 / 防御性编程
"""

# ============================================================
# 第1部分：本周核心概念（5行讲清）
# ============================================================
"""
1. requests.get() 结果必须先赋值给变量，再 .json() 解析
2. status_code 200=成功，401=认证失败，429=限速，500=服务器错误
3. 防御性：用 if response.status_code == 200 隔离成功逻辑
4. int()/json.loads() 必须在 try 块里，因为会抛异常
5. response.raise_for_status() 可以把 4xx/5xx 状态码转成异常
"""

# ============================================================
# 第2部分：代码骨架（逐行注释，TODO你来填）
# ============================================================

# 【练习1】模拟 API 调用（用本地 JSON 数据演示）

import json

# 模拟一个 API 返回的 JSON 字符串
fake_response = '{"code": 200, "data": {"name": "咖啡", "price": 30}}'

# TODO(你填)：用 json.loads() 解析字符串，取出 name 和 price
# 用 try/except 捕获解析错误
try:
    result = ""        # ← 填 json.loads(fake_response)
    name = result["data"]["name"]
    price = result["data"]["price"]
    print(f"{name} 价格：{price}元")
except "" :            # ← 填异常类型
    print("JSON解析失败")


# 【练习2】防御性 API 调用模式

# TODO(你填)：补全这个函数
# 功能：传入 URL，调用 API，成功返回数据，失败返回 None
def call_api(url):
    import requests
    try:
        response = requests.get(url)
        # TODO(你填)：判断状态码是否为 200
        if "" :         # ← 填判断条件
            return ""   # ← 填 response.json()
        else:
            print(f"请求失败：状态码{response.status_code}")
            return None
    except requests.ConnectionError:
        print("网络连接失败")
        return None


# ============================================================
# 第3部分：改造题（改1个参数观察输出）
# ============================================================

# 【改造题A】call_api 增加超时参数：requests.get(url, timeout=5)
# 改动：改 requests.get() 那一行

# 【改造题B】解析失败时返回空字典 {} 而不是 None
# 改动：只改 return None 为 return {}


# ============================================================
# 第4部分：复习题（无骨架，复查时自己写）
# ============================================================
"""
复习目标：

【概念题】
1. response.status_code 为 429 是什么意思？第一步怎么处理？
2. 为什么 int() 必须放在 try 块里？
3. response.json() 和 response.text 有什么区别？

【代码题】
1. 写一个函数 parse_user(data_dict)，传入字典，返回用户名；如果缺少 "name" 键返回 "匿名用户"
2. 模拟一个"带重试的API调用"：失败后等1秒再试，最多重试3次
"""
