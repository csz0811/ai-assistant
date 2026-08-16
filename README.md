# AI 内容生成器（Streamlit）

基于 DeepSeek 的 AI 内容生成 Web 应用，支持多类型文案生成 + Markdown 实时预览与导出。

## 功能
- 多类型内容生成（小红书 / 公众号 / 电商详情页 等）
- Markdown 实时预览 + 一键导出
- 深色适配界面（品牌蓝 #2563eb）

## 本地运行
~~~
pip install -r requirements.txt
cp .env.example .env      # 在 .env 中填入 DEEPSEEK_API_KEY
streamlit run app.py
~~~

## 环境变量
- `DEEPSEEK_API_KEY`：DeepSeek API Key（部署时在平台 Secrets 中配置同名变量）

## 文件结构
- `streamlit_app.py`：Streamlit 界面入口
- `content_generator.py`：内容生成核心逻辑（调用 DeepSeek）
- `requirements.txt`：依赖清单
