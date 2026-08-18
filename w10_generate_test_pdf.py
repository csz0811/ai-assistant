"""
W10-D6 收尾工具｜生成支持中文的测试 PDF
========================================
原来 D3 用的 test_document.pdf 是乱码（reportlab 默认字体不支持中文）。
这次用内置的 STSong-Light CID 字体，无需额外字体文件。

内容主题：直播带货实战知识（朋友公司场景）
长度：5 页，每页 200-300 字，够 D4-D6 切块+检索
"""

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# ============================================================
# 第1步：注册中文字体（reportlab 内置，无需文件）
# ============================================================
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
FONT_NAME = 'STSong-Light'

# ============================================================
# 第2步：定义 5 页内容
# ============================================================
pages_content = [
    "直播带货三大核心环节：引流、转化、复盘。"
    "引流负责把人拉进直播间，靠短视频、投流、自然推荐三种方式；"
    "转化靠主播话术和产品吸引力把人从观众变成买家；"
    "复盘则是事后分析数据、优化下一场。这三个环节环环相扣，缺一不可。",

    "选品五大标准：市场需求、利润空间、复购率、库存深度、季节适配。"
    "市场需求决定天花板，可以从抖音榜单、蝉妈妈数据看趋势；"
    "利润空间至少 30% 以上，否则投流亏损；"
    "复购率高的产品适合做私域沉淀；"
    "库存深度影响发货速度，断货是直播大忌；"
    "季节适配则决定何时上架何时清仓。",

    "主播话术四个关键节点：开场留人、痛点共鸣、产品讲解、逼单促单。"
    "开场 30 秒必须抛出福利或悬念，否则观众秒划走；"
    "痛点共鸣要唤起观众的不便和渴望；"
    "产品讲解要突出三大卖点和一个差异化；"
    "逼单促单则要配合库存紧张感和限时优惠，"
    "比如'只剩 200 单了'、'今天直播间专享价'。",

    "直播复盘六大数据指标：场观人数、平均停留时长、转化率、客单价、GMV、退货率。"
    "场观决定流量层级；停留时长反映内容吸引力；"
    "转化率是带货效率的核心指标；客单价影响整体 GMV；"
    "GMV 是总成绩单但不能只看它；"
    "退货率过高说明产品或话术有问题，需要立刻调整。",

    "常见问题解答：Q1 退货率太高怎么办？"
    "A：先看是产品问题还是主播话术夸大；产品问题立刻下架，话术问题重新培训。"
    "Q2 新主播怎么培训？A：先跟播 3 天看老主播怎么控场，再写逐字稿自己练 5 场，"
    "最后上手助理位带 3 场。Q3 流量下滑如何应对？A：检查短视频引流是否正常、"
    "直播间封面标题是否需要优化、付费投流占比是否健康。"
]

# ============================================================
# 第3步：生成 PDF
# ============================================================
OUTPUT_PATH = "/Users/hechengfajituan/ai-assistant/test_zh.pdf"
c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
WIDTH, HEIGHT = A4

for i, content in enumerate(pages_content, 1):
    c.setFont(FONT_NAME, 12)

    # 标题
    c.setFont(FONT_NAME, 16)
    c.drawString(80, HEIGHT - 80, f"第{i}页 - 直播带货实战知识")

    # 正文（手动换行）
    c.setFont(FONT_NAME, 12)
    y = HEIGHT - 130
    line_height = 22
    char_per_line = 30  # A4 + 12号字 + STSong 大约 30 字一行

    for j in range(0, len(content), char_per_line):
        line = content[j:j + char_per_line]
        c.drawString(80, y, line)
        y -= line_height
        if y < 80:  # 到页底就停
            break

    c.showPage()

c.save()
print(f"✅ 已生成：{OUTPUT_PATH}")
print(f"   共 {len(pages_content)} 页，每页约 200-300 字")
print(f"   主题：直播带货实战知识（适合 D6 语义搜索测试）")
