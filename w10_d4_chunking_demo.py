# ============ W10-D4 练习：文本切块函数 ============
# 目标：把长文本按 chunk_size 和 overlap 切成多个块
# 原理：step = chunk_size - overlap，相邻块之间有 overlap 个字符重叠
#       这样"刚好在切割处的内容"不会丢失

raw_text = """Python是一门易学的编程语言。它广泛应用于数据分析、\
人工智能、Web开发等领域。机器学习是人工智能的核心分支。通过数据训练模型，\
让计算机自动学习规律。深度学习使用神经网络处理复杂任务。ChatGPT等大语言模型\
都基于深度学习技术。RAG系统结合了检索和生成两种能力。"""

chunk_size = 30   # 每块多少字符
overlap = 0      # 相邻块重叠多少字符

# 步长 = 每块长度 - 重叠长度
# chunk_size=30, overlap=10 → step=20
# 含义：每切一块，下一块从当前位置+20个字符开始
# 这样块1(0~30)和块2(20~50)之间有10个字符重叠
step = chunk_size - overlap   # 30 - 10 = 20

chunks = []
i = 0
while i < len(raw_text):
    chunk = raw_text[i : i + chunk_size]   # 切片：[起始位置 : 起始位置+块大小]
    chunks.append(chunk)
    i = i + step                           # 下一起始位置 = 当前 + 步长(不是块大小)

# ============ 输出验证 ============
print(f"原文总字符数: {len(raw_text)}")
print(f"chunk_size={chunk_size}, overlap={overlap}, 步长={step}")
print(f"切成 {len(chunks)} 块\n")
print("=" * 50)

for j, c in enumerate(chunks):
    print(f"块{j+1}: [{c}]")

# ============ 验证重叠是否生效 ============
print("\n" + "=" * 50)
print("块边界检查（看块之间有没有重叠）")
if len(chunks) >= 2:
    # overlap=0 时，显示块1末尾10字和块2开头10字，看是否不同
    check_len = max(overlap, 10)  # 至少显示10个字符对比
    print(f"  块1末尾{check_len}字: [{chunks[0][-check_len:]}]")
    print(f"  块2开头{check_len}字: [{chunks[1][:check_len]}]")
    
    if overlap == 0:
        print(f"  ℹ️ overlap=0，无重叠设计，块1末尾≠块2开头是正常的")
    elif chunks[0][-overlap:] == chunks[1][:overlap]:
        print(f"  ✅ 重叠生效！两端完全一致，内容没丢")
    else:
        print(f"  ⚠️ 重叠内容不一致")

# ============ 延伸实验（看完运行结果后试这里） ============
# 改动 chunk_size 或 overlap，观察：
# 1. 块的数量怎么变？
# 2. 如果 step = chunk_size（overlap=0），块之间还有重叠吗？
# 3. chunk_size 太小（如10）会怎样？语义会被割断
