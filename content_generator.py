import os
import json
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

CONTENT_TYPES = {
    "1": {
        "name": "小红书文案",
        "prompt": """你是一个资深小红书博主，擅长种草文案。
用户给你一个话题，你必须只返回一个 JSON 对象，不要任何解释或多余文字。
JSON 结构必须严格如下（字段名用中文，不要改）：
{
  "标题": "带1-2个emoji的吸引人标题，不超过20字",
  "正文": "分段式种草正文，合理使用emoji，300字以内，口语化有干货",
  "标签": ["标签1", "标签2", "标签3"],
  "发布时间建议":"早/中/晚，根据话题推荐一个适合发布的时间段"
}"""
    },
    "2": {
        "name": "短视频脚本",
        "prompt": """你是一个资深短视频编导。
用户给你一个话题，你必须只返回一个 JSON 对象，不要任何解释或多余文字。
JSON 结构必须严格如下（字段名用中文，不要改）：
{
  "开场钩子": "前3秒抓住注意力的一句话，不超过30字",
  "台词": ["第1句台词", "第2句台词", "第3句台词"],
  "结尾互动": "引导点赞、关注或评论的一句话",
  "时长建议": "如 30秒 或 1分钟",
  "标签": ["标签1", "标签2"]
}"""
    },
    "3": {
        "name": "朋友圈",
        "prompt": """你是一个朋友圈文案高手，文案自然、有烟火气。
用户给你一个话题，你必须只返回一个 JSON 对象，不要任何解释或多余文字。
JSON 结构必须严格如下（字段名用中文，不要改）：
{
  "文案": "轻松自然的一两句话，可带emoji，不超过50字",
  "配图建议": "建议配什么图，一句话",
  "话题": "#相关话题"
}"""
    },
    "4":{
        "name":"微博",
        "prompt":"""你是一个微博文案高手，文案要结合线下热点热梗，幽默风趣。
用户给你一个话题，你必须只返回一个 JSON 对象，不要任何解释或多余文字。
JSON 结构必须严格如下（字段名用中文，不要改）：
{
  "文案":"幽默风趣的两三句话，内容要根据内容插入合适的网络名词，不超过50字",
  "配图建议":"建议配怎么样的图片，一句话",
  "话题":"#相关话题"  
    }"""
    }
}

def generate(topic, system_prompt, max_retry=3, temperature=1.5, max_tokens=800):
    user_msg = f"请为这个话题生成内容：{topic}"
    for attempt in range(1, max_retry + 1):
        try:
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            return json.loads(resp.choices[0].message.content)
        except json.JSONDecodeError as e:
            print(f"第{attempt}次：返回不是合法JSON，重试... ({e})")
        except Exception as e:
            print(f"第{attempt}次失败：{e}")
    return None

def safe_name(topic):
    return "".join(c for c in topic if (c.isalnum() or c in " _-")).strip() or "未命名"

def save_json(type_name, data, safe):
    out_dir = os.path.join(BASE_DIR, "outputs")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{type_name}_{safe}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def render_markdown(type_name, topic, data):
    lines = [f"# {type_name}：{topic}", ""]
    for key, val in data.items():
        lines.append(f"## {key}")
        if isinstance(val, list):
            if key == "台词":
                for i, item in enumerate(val, 1):
                    lines.append(f"{i}. {item}")
            elif key == "标签":
                lines.append(" ".join(f"#{v}" for v in val))
            elif key == "发布时间建议":
                lines.append(" ".join(f"{v}" for v in val))
            else:
                for item in val:
                    clean = str(item).replace("\\n", "\n").replace("\\r", "")
                    lines.append(f"- {clean}")
        else:
            text = str(val).replace("\\n", "\n").replace("\\r", "")
            lines.append(text)
        lines.append("")
    return "\n".join(lines)

def show_menu():
    print("选择内容类型：")
    for k, v in CONTENT_TYPES.items():
        print(f"  {k}. {v['name']}")

if __name__ == "__main__":
    args = sys.argv[1:]
    topic = args[0] if len(args) >= 1 else input("输入话题：")
    type_key = args[1] if len(args) >= 2 else None

    if type_key not in CONTENT_TYPES:
        show_menu()
        type_key = input("输入编号：").strip()
        while type_key not in CONTENT_TYPES:
            type_key = input("编号不对，重新输入：").strip()

    t = CONTENT_TYPES[type_key]
    print(f"\n🎯 正在生成「{t['name']}」：{topic}")
    data = generate(topic, t["prompt"])
    if data is None:
        print("❌ 生成失败，请稍后重试")
    else:
        safe = safe_name(topic)
        json_path = save_json(t["name"], data, safe)
        md_path = os.path.join(BASE_DIR, "outputs", f"{t['name']}_{safe}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(render_markdown(t["name"], topic, data))
        print("\n✅ 生成完成！")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        print(f"\n📁 JSON:     {json_path}")
        print(f"📄 Markdown: {md_path}")
