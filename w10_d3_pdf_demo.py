import fitz  # PyMuPDF

# ① 找一个测试 PDF —— 用系统自带的示例或下载一个
# 先用这个:macOS 自带的 PDF 手册(如果存在)
import os

# 备选路径:用户下载目录找 PDF,或创建一个简单测试文件
pdf_path = "/Users/hechengfajituan/Downloads/test_document.pdf"

# 如果没有 PDF,先创建一个简单测试文件
if not os.path.exists(pdf_path):
    print(f"找不到 {pdf_path}")
    print("正在创建一个测试 PDF...")
    
    # 用 reportlab 创建一个简单 PDF(纯文本,无复杂依赖)
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        
        c = canvas.Canvas(pdf_path, pagesize=A4)
        
        # 第 1 页
        c.drawString(100, 800, "第一章:Python 基础")
        c.drawString(100, 780, "Python 是一门简洁优雅的编程语言。")
        c.drawString(100, 760, "它广泛应用于数据分析、人工智能、Web 开发等领域。")
        c.showPage()
        
        # 第 2 页
        c.drawString(100, 800, "第二章:机器学习入门")
        c.drawString(100, 780, "机器学习是人工智能的核心分支。")
        c.drawString(100, 760, "通过数据训练模型,让计算机自动学习规律。")
        c.showPage()
        
        # 第 3 页
        c.drawString(100, 800, "第三章:深度学习")
        c.drawString(100, 780, "深度学习使用神经网络处理复杂任务。")
        c.drawString(100, 760, "ChatGPT 等大语言模型都基于深度学习技术。")
        c.showPage()
        
        c.save()
        print(f"✅ 测试 PDF 已创建: {pdf_path}")
    except ImportError:
        print("❌ 需要安装 reportlab: pip install reportlab")
        exit(1)

# ② 用 PyMuPDF 读取 PDF
try:
    doc = fitz.open(pdf_path)
    print(f"✅ 成功打开 PDF: {pdf_path}")
    print(f"总页数: {len(doc)}")
    
    all_text = ""  # 用来存所有文本
    
    for i, page in enumerate(doc[:3]):  # 只读前 3 页
        text = page.get_text()
        all_text += text + "\n"
        print(f"\n--- 第 {i+1} 页 (前 200 字符) ---")
        print(text[:200] if text else "[无文本]")
    
    doc.close()
    
    print(f"\n{'='*40}")
    print(f"3 页总字符数: {len(all_text)}")
    print(f"{'='*40}")
    
    # 🛠 改造题提示
    print("\n💡 思考:如果直接把这几万字塞进 ChromaDB 的一个 document...")
    print("   向量会'稀释',检索时找不准。明天学 chunking 解决!")
    
except Exception as e:
    print(f"❌ 报错: {e}")
