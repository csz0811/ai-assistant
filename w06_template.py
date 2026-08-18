"""
W6｜结构化输出 · 代码练习模板
==============================
本周目标：Markdown 分模块 / JSON Schema / response_format
"""

# ============================================================
# 第1部分：本周核心概念（5行讲清）
# ============================================================
"""
1. 给人看 → Markdown（用 --- 分隔线）；程序读 → JSON Schema
2. JSON Schema 五要素：type / enum / required / additionalProperties:false / 字段=输出
3. response_format 两层：type="json_schema" + json_schema={name, schema}
4. JSON 不允许注释（// 和 /* */ 都不行），字段名不能有中文
5. Schema 字段描述的是"模型输出"，不是用户输入
"""

# ============================================================
# 第2部分：代码骨架（逐行注释，TODO你来填）
# ============================================================

# 【练习1】Markdown 分模块 Prompt

product = "咖啡"
user = "上班族"

# TODO(你填)：写一个 Markdown 分模块 Prompt
# 模块：## 产品名称 / ## 核心卖点（3条）/ ## 适用人群
# 注意：分隔线用 --- 不是 #
markdown_prompt = ""  # ← 用 f-string 拼接

print(markdown_prompt)


# 【练习2】JSON Schema 定义

# TODO(你填)：定义一个"情感分析"输出的 Schema
# 字段：
#   - sentiment: 字符串，枚举 positive/negative/neutral
#   - reason: 字符串，解释理由
#   - required: sentiment 和 reason 都必须有
#   - additionalProperties: false

schema = {
    "type": "object",
    "properties": {
        "sentiment": {
            "type": "" ,         # ← 填 "string"
            "enum": []           # ← 填枚举值列表
        },
        "reason": {
            "type": ""           # ← 填 "string"
        }
    },
    "required": [],             # ← 填必填字段列表
    "additionalProperties": ""  # ← 填 False
}

print(schema)


# 【练习3】response_format 拼接

# TODO(你填)：把练习2的 schema 拼成 response_format（两层结构）
response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "",              # ← 填 "sentiment_analysis"
        "schema": ""            # ← 填 schema 变量
    }
}
print(response_format)


# ============================================================
# 第3部分：改造题（改1个参数观察输出）
# ============================================================

# 【改造题A】Schema 加一个 confidence 字段（0-1的小数），表示置信度
# 改动：在 properties 加新字段 + 把它加入 required

# 【改造题B】Markdown Prompt 改成"小红书种草文格式"，加一个 ## 推荐理由 模块
# 改动：在字符串里加一个模块


# ============================================================
# 第4部分：复习题（无骨架，复查时自己写）
# ============================================================
"""
复习目标：

【概念题】
1. JSON Schema 的 required 数组表示什么意思？
2. 什么时候用 Markdown，什么时候用 JSON Schema？
3. 为什么 Schema 字段名不能写成用户输入的内容（如 comment、input）？

【代码题】
1. 定义一个"商品信息"的 Schema：name(string)、price(number)、in_stock(boolean)，required 只要求 name
2. 写一个 Markdown Prompt，格式：## 标题 / ## 正文（100字内）/ ## 标签（3个用逗号分隔），主题是"推荐一本书"
"""
