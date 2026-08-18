"""
W3｜函数与模块 · 代码练习模板
==============================
本周目标：掌握 def / return / try-except / import
"""

# ============================================================
# 第1部分：本周核心概念（5行讲清）
# ============================================================
"""
1. 函数先定义后调用；import 后用模块名.函数名() 调用
2. return 把结果返回给调用者，同时结束函数；无 return 返回 None
3. except 只捕获 try 块里的异常；except 块里也要 return，否则"穿过去"
4. 常见异常：ValueError（值错误）、TypeError（类型错误）、KeyError（字典key不存在）
5. float("abc") 抛 ValueError，不是 TypeError
"""

# ============================================================
# 第2部分：代码骨架（逐行注释，TODO你来填）
# ============================================================

# 【练习1】计算器函数（def + return）

# TODO(你填)：定义一个函数 calculate(a, b, op)
# op 是 "+" 或 "-" 或 "*" 或 "/"
# 返回计算结果，除法除以0返回 None
def calculate(a, b, op):
    if op == "+":
        return ""      # ← 填 a + b
    elif op == "-":
        return ""      # ← 填 a - b
    elif op == "*":
        return ""      # ← 填 a * b
    elif op == "/":
        if b == 0:
            return ""  # ← 填 None
        return ""      # ← 填 a / b
    else:
        return None

result = calculate(10, 3, "/")
print(f"10 / 3 = {result}")


# 【练习2】安全数字转换（try/except）

# TODO(你填)：写一个 safe_to_int(s) 函数
# 尝试转整数，成功返回整数，失败返回 None
def safe_to_int(s):
    try:
        return ""      # ← 填 int(s)
    except "" :        # ← 填要捕获的异常类型
        return None

print(safe_to_int("42"))    # → 42
print(safe_to_int("abc"))   # → None


# ============================================================
# 第3部分：改造题（改1个参数观察输出）
# ============================================================

# 【改造题A】给 calculate 加一个 "%" 取模运算
# 改动：加一个 elif 分支

# 【改造题B】safe_to_int 失败时返回 0 而不是 None
# 改动：只改 return None 那一行


# ============================================================
# 第4部分：复习题（无骨架，复查时自己写）
# ============================================================
"""
复习目标：

【概念题】
1. except 块里只有 print 没有 return，会发生什么？
2. import math 后，为什么必须写 math.sqrt() 而不是 sqrt()？
3. float("hello") 和 "hello" + 1 分别会报什么错？

【代码题】
1. 定义一个函数 is_prime(n)，判断 n 是否为质数（返回 True/False）
2. 用 try/except 包装文件读取：如果文件不存在捕获异常并打印"文件不存在"
"""
