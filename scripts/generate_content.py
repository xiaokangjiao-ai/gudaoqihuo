"""
自动热点内容生成器
- 抓取百度热搜/微博热搜
- 用智谱AI(GLM)改写生成SEO文章
- 输出为HTML页面
"""

import os
import re
import json
import time
import random
import hashlib
import requests
from datetime import datetime
from pathlib import Path

try:
    import jwt
except ImportError:
    jwt = None

# ===== 配置 =====
API_KEY = os.environ.get("ZHIPU_API_KEY", "")
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4-flash"  # 免费模型
ARTICLES_PER_RUN = 3  # 每次生成3篇，一天9篇
OUTPUT_DIR = Path("articles")
INDEX_FILE = Path("index.html")
SITEMAP_FILE = Path("sitemap.xml")

# 文章分类及对应的广告关键词
CATEGORIES = {
    "hot": "社会热点",
    "tech": "科技数码",
    "health": "健康养生",
    "life": "生活百科",
    "entertainment": "娱乐八卦",
}

# ===== 热点抓取 =====

def fetch_baidu_hot():
    """抓取百度热搜"""
    try:
        url = "https://top.baidu.com/board?tab=realtime"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        # 从页面中提取热搜词
        pattern = r'"word":"(.*?)"'
        words = re.findall(pattern, resp.text)
        return words[:20] if words else []
    except Exception as e:
        print(f"百度热搜抓取失败: {e}")
        return []


def fetch_weibo_hot():
    """抓取微博热搜"""
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        words = []
        for item in data.get("data", {}).get("realtime", []):
            word = item.get("word", "")
            if word:
                words.append(word)
        return words[:20]
    except Exception as e:
        print(f"微博热搜抓取失败: {e}")
        return []


def fetch_toutiao_hot():
    """抓取头条热榜"""
    try:
        url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        words = []
        for item in data.get("data", []):
            title = item.get("Title", "")
            if title:
                words.append(title)
        return words[:20]
    except Exception as e:
        print(f"头条热榜抓取失败: {e}")
        return []


def get_hot_topics():
    """汇总所有热点，去重后随机选取"""
    all_topics = []
    all_topics.extend(fetch_baidu_hot())
    all_topics.extend(fetch_weibo_hot())
    all_topics.extend(fetch_toutiao_hot())

    # 去重
    seen = set()
    unique = []
    for t in all_topics:
        if t not in seen and len(t) > 2:
            seen.add(t)
            unique.append(t)

    if not unique:
        # 备用话题
        unique = [
            "2025年最值得买的手机推荐",
            "如何快速提升睡眠质量",
            "年轻人副业赚钱方法",
            "ChatGPT最新使用技巧",
            "今日股市行情分析",
        ]

    random.shuffle(unique)
    return unique[:ARTICLES_PER_RUN]


# ===== AI内容生成 =====

def get_zhipu_token():
    """生成智谱API的JWT token"""
    if not jwt:
        # 如果没有pyjwt，直接用API Key作为Bearer token（智谱也支持）
        return API_KEY
    parts = API_KEY.split(".")
    if len(parts) != 2:
        return API_KEY
    kid, secret = parts[0], parts[1]
    payload = {
        "api_key": kid,
        "exp": int(time.time()) + 3600,
        "timestamp": int(time.time()),
    }
    token = jwt.encode(payload, secret, algorithm="HS256",
                       headers={"alg": "HS256", "sign_type": "SIGN"})
    return token


def generate_article(topic):
    """用智谱AI生成一篇SEO优化的文章"""
    prompt = f"""你是一个专业的中文SEO内容写手。请根据以下热门话题写一篇1000-1500字的文章。

话题：{topic}

要求：
1. 标题要吸引点击，包含关键词，30字以内
2. 开头第一段要包含核心关键词，吸引读者继续阅读
3. 文章分3-5个小节，每节有小标题（用##标记）
4. 内容要有信息量，不能是废话连篇
5. 结尾要有总结和引导互动的话
6. 自然插入2-3个相关长尾关键词
7. 语气亲民接地气，像朋友聊天一样

请直接输出，格式：
第一行是标题（不加任何标记）
第二行空行
后面是正文（用markdown格式）"""

    try:
        token = get_zhipu_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.85,
            "max_tokens": 2000,
        }
        resp = requests.post(API_URL, headers=headers, json=data, timeout=60)
        result = resp.json()

        if "choices" not in result:
            print(f"AI返回异常: {result}")
            return None, None

        content = result["choices"][0]["message"]["content"]
        lines = content.strip().split("\n")
        title = lines[0].strip().strip("#").strip()
        body = "\n".join(lines[1:]).strip()
        return title, body
    except Exception as e:
        print(f"AI生成失败: {e}")
        return None, None


def classify_topic(topic):
    """简单分类"""
    tech_keywords = ["手机", "AI", "芯片", "科技", "数码", "电脑", "苹果", "华为", "小米", "ChatGPT", "人工智能"]
    health_keywords = ["健康", "养生", "睡眠", "减肥", "医", "病", "食物", "营养", "锻炼"]
    life_keywords = ["生活", "省钱", "副业", "赚钱", "工作", "职场", "房", "车"]
    ent_keywords = ["明星", "综艺", "电影", "电视剧", "演员", "导演", "票房", "恋情"]

    for kw in tech_keywords:
        if kw in topic:
            return "tech"
    for kw in health_keywords:
        if kw in topic:
            return "health"
    for kw in life_keywords:
        if kw in topic:
            return "life"
    for kw in ent_keywords:
        if kw in topic:
            return "entertainment"
    return "hot"


# ===== HTML生成 =====

def topic_to_slug(topic):
    """生成URL友好的文件名"""
    h = hashlib.md5(topic.encode()).hexdigest()[:8]
    # 取前10个中文字符
    clean = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', topic)[:10]
    return f"{clean}-{h}"


def generate_html(title, body, category, slug):
    """生成完整的HTML页面"""
    cat_name = CATEGORIES.get(category, "热点")
    date_str = datetime.now().strftime("%Y-%m-%d")

    # 将markdown转成简单HTML
    html_body = body
    html_body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_body, flags=re.MULTILINE)
    html_body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_body, flags=re.MULTILINE)
    html_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_body)
    # 段落处理
    paragraphs = html_body.split("\n\n")
    html_body = ""
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<h"):
            html_body += p + "\n"
        else:
            html_body += f"<p>{p}</p>\n"

    # CPS广告区块（根据分类不同展示不同推广）
    ad_blocks = {
        "tech": '<div class="ad-box"><p>📱 <a href="#tech-rec">2025热门数码好物推荐</a> | <a href="#tech-rec">AI工具合集</a></p></div>',
        "health": '<div class="ad-box"><p>🏥 <a href="#health-rec">健康好物推荐</a> | <a href="#health-rec">养生食谱大全</a></p></div>',
        "life": '<div class="ad-box"><p>💰 <a href="#life-rec">副业赚钱指南</a> | <a href="#life-rec">省钱攻略</a></p></div>',
        "entertainment": '<div class="ad-box"><p>🎬 <a href="#ent-rec">热门影视推荐</a> | <a href="#ent-rec">明星周边</a></p></div>',
        "hot": '<div class="ad-box"><p>🔥 <a href="#hot-rec">今日热门推荐</a> | <a href="#hot-rec">热点深度解读</a></p></div>',
    }
    ad_html = ad_blocks.get(category, ad_blocks["hot"])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 热点资讯</title>
<meta name="description" content="{title}，最新热点资讯深度解读，了解更多请阅读全文。">
<meta name="keywords" content="{title},{cat_name},热点资讯,最新消息">
<link rel="canonical" href="https://gudaoqihuo.com/articles/{slug}.html">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.8;color:#333;max-width:800px;margin:0 auto;padding:20px;background:#f9f9f9}}
h1{{font-size:1.6em;margin-bottom:10px;color:#1a1a1a}}
h2{{font-size:1.3em;margin:25px 0 10px;color:#2c2c2c;border-left:4px solid #ff6b35;padding-left:10px}}
h3{{font-size:1.1em;margin:20px 0 8px;color:#444}}
p{{margin-bottom:15px;text-align:justify}}
.meta{{color:#888;font-size:0.9em;margin-bottom:20px;padding-bottom:15px;border-bottom:1px solid #eee}}
.ad-box{{background:#fff8f0;border:1px solid #ffe0c0;border-radius:8px;padding:15px;margin:25px 0;text-align:center}}
.ad-box a{{color:#ff6b35;text-decoration:none;font-weight:bold}}
.footer{{margin-top:40px;padding-top:20px;border-top:1px solid #eee;text-align:center;color:#888;font-size:0.85em}}
.nav{{margin-bottom:20px;padding:10px 0;border-bottom:1px solid #eee}}
.nav a{{color:#ff6b35;text-decoration:none;margin-right:15px}}
</style>
</head>
<body>
<nav class="nav">
<a href="/">首页</a>
<a href="/articles/">全部文章</a>
</nav>
<article>
<h1>{title}</h1>
<div class="meta">发布时间：{date_str} | 分类：{cat_name} | 阅读约3分钟</div>
{ad_html}
{html_body}
{ad_html}
</article>
<div class="footer">
<p>© 2025 热点资讯站 | 内容仅供参考</p>
</div>
<!-- 广告位预留 -->
<div id="ad-placeholder"></div>
</body>
</html>"""
    return html


# ===== 首页生成 =====

def rebuild_index():
    """重建首页，列出所有文章"""
    articles_dir = OUTPUT_DIR
    if not articles_dir.exists():
        return

    # 收集所有文章
    articles = []
    for f in sorted(articles_dir.glob("*.html"), key=os.path.getmtime, reverse=True):
        if f.name == "index.html":
            continue
        # 从文件中提取标题
        content = f.read_text(encoding="utf-8")
        title_match = re.search(r"<h1>(.*?)</h1>", content)
        date_match = re.search(r"发布时间：(\d{4}-\d{2}-\d{2})", content)
        cat_match = re.search(r"分类：(.+?) \|", content)
        if title_match:
            articles.append({
                "title": title_match.group(1),
                "url": f"/articles/{f.name}",
                "date": date_match.group(1) if date_match else "",
                "category": cat_match.group(1) if cat_match else "热点",
            })

    # 只保留最新100篇在首页
    articles = articles[:100]

    # 生成文章列表HTML
    article_list = ""
    for a in articles:
        article_list += f'<li><span class="date">{a["date"]}</span><span class="cat">[{a["category"]}]</span><a href="{a["url"]}">{a["title"]}</a></li>\n'

    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>每日热点资讯 - 今日头条热搜汇总</title>
<meta name="description" content="每日更新最新热点资讯、社会新闻、科技动态、健康养生、生活百科，一站了解天下事。">
<meta name="keywords" content="今日热点,热搜,最新消息,社会新闻,科技资讯,健康养生">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.8;color:#333;max-width:900px;margin:0 auto;padding:20px;background:#f9f9f9}}
h1{{text-align:center;margin:20px 0;color:#1a1a1a}}
.subtitle{{text-align:center;color:#666;margin-bottom:30px}}
ul{{list-style:none}}
li{{padding:12px 15px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:10px}}
li:hover{{background:#fff}}
.date{{color:#999;font-size:0.85em;white-space:nowrap}}
.cat{{color:#ff6b35;font-size:0.8em;white-space:nowrap}}
a{{color:#333;text-decoration:none}}
a:hover{{color:#ff6b35}}
.footer{{margin-top:40px;text-align:center;color:#888;font-size:0.85em}}
.ad-banner{{background:#fff8f0;border:1px solid #ffe0c0;border-radius:8px;padding:20px;margin:20px 0;text-align:center}}
.ad-banner a{{color:#ff6b35;font-weight:bold;text-decoration:none}}
</style>
</head>
<body>
<h1>📰 每日热点资讯</h1>
<p class="subtitle">AI智能聚合，每日三更，一站了解天下事</p>
<div class="ad-banner">
<p>🔥 <a href="#">热门推荐</a> | <a href="#">今日必读</a> | <a href="#">深度好文</a></p>
</div>
<ul>
{article_list}
</ul>
<div class="footer">
<p>© 2025 每日热点资讯 | 内容由AI智能生成，仅供参考</p>
<p>更新频率：每日三次自动更新</p>
</div>
<!-- 广告位 -->
<div id="ad-placeholder"></div>
</body>
</html>"""

    INDEX_FILE.write_text(index_html, encoding="utf-8")
    print(f"首页已更新，共 {len(articles)} 篇文章")


def rebuild_sitemap():
    """重建sitemap"""
    articles_dir = OUTPUT_DIR
    if not articles_dir.exists():
        return

    urls = ['<url><loc>https://gudaoqihuo.com/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>']
    for f in sorted(articles_dir.glob("*.html"), key=os.path.getmtime, reverse=True):
        if f.name == "index.html":
            continue
        urls.append(f'<url><loc>https://gudaoqihuo.com/articles/{f.name}</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>')

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>"""

    SITEMAP_FILE.write_text(sitemap, encoding="utf-8")
    print("Sitemap已更新")


# ===== 主流程 =====

def main():
    if not API_KEY:
        print("错误：未设置 ZHIPU_API_KEY 环境变量")
        return

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 获取热点话题
    print("正在抓取热点话题...")
    topics = get_hot_topics()
    print(f"获取到 {len(topics)} 个话题: {topics}")

    # 检查已有文章，避免重复
    existing = set()
    for f in OUTPUT_DIR.glob("*.html"):
        existing.add(f.stem)

    generated = 0
    for topic in topics:
        slug = topic_to_slug(topic)
        if slug in existing:
            print(f"跳过已存在: {topic}")
            continue

        print(f"正在生成: {topic}")
        category = classify_topic(topic)
        title, body = generate_article(topic)

        if not title or not body:
            continue

        html = generate_html(title, body, category, slug)
        output_path = OUTPUT_DIR / f"{slug}.html"
        output_path.write_text(html, encoding="utf-8")
        print(f"已生成: {output_path}")
        generated += 1

    if generated > 0:
        print(f"\n本次共生成 {generated} 篇文章")
        rebuild_index()
        rebuild_sitemap()
    else:
        print("本次无新文章生成")


if __name__ == "__main__":
    main()
