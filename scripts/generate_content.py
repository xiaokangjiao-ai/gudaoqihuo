# -*- coding: utf-8 -*-
"""
全自动双语热点流量站内容生成器 v3.0
================================
中英双语 | 多源热点 | AI伪原创 | 内链网络 | 结构化数据 | AdSense+Amazon变现
"""

import os, sys, re, json, time, random, hashlib, requests

# Windows GBK 终端兼容
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
from datetime import datetime
from pathlib import Path

try:
    import jwt
except ImportError:
    jwt = None

# ==================== 配置 ====================

API_KEY = os.environ.get("ZHIPU_API_KEY", "")
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4-flash"

ARTICLES_PER_RUN = 20  # 每次生成20个话题，每个话题中英文各一篇 = 40篇

# 中文站点
OUTPUT_DIR = Path("articles")
MANIFEST_FILE = OUTPUT_DIR / "manifest.json"
SITE_NAME = "每日热点速递"
SITE_URL = "https://gudaoqihuo.com"
SITE_DESC = "AI智能聚合热点资讯,每日更新,一站了解天下事"

# 英文站点
EN_OUTPUT_DIR = Path("en/articles")
EN_MANIFEST_FILE = EN_OUTPUT_DIR / "manifest.json"
EN_SITE_NAME = "Daily Trending News"
EN_SITE_URL = "https://gudaoqihuo.com"
EN_SITE_DESC = "AI-powered trending news, updated daily"

INDEX_FILE = Path("index.html")
EN_INDEX_FILE = Path("en/index.html")
SITEMAP_FILE = Path("sitemap.xml")

# 中文分类
CATEGORIES = {
    "hot":          {"name": "社会热点",   "icon": "🔥"},
    "tech":         {"name": "科技数码",   "icon": "📱"},
    "health":       {"name": "健康养生",   "icon": "🏥"},
    "life":         {"name": "生活百科",   "icon": "💡"},
    "entertainment":{"name": "娱乐八卦",   "icon": "🎬"},
}

# 英文分类
EN_CATEGORIES = {
    "hot":          {"name": "Trending",     "icon": "🔥"},
    "tech":         {"name": "Tech",         "icon": "📱"},
    "health":       {"name": "Health",       "icon": "🏥"},
    "life":         {"name": "Lifestyle",    "icon": "💡"},
    "entertainment":{"name": "Entertainment","icon": "🎬"},
}

# 中文CPS推广链接(亚马逊)
CPS_LINKS = {
    "tech": [
        {"text": "2025高性价比手机推荐", "url": "https://www.amazon.cn/gp/bestsellers/electronics?tag=gudaoqihuo-20", "desc": "热销数码"},
        {"text": "AI智能工具实用合集", "url": "https://www.amazon.cn/s?k=AI工具&tag=gudaoqihuo-20", "desc": "效率神器"},
    ],
    "health": [
        {"text": "养生保健精选好物", "url": "https://www.amazon.cn/s?k=养生&tag=gudaoqihuo-20", "desc": "健康生活"},
        {"text": "运动健身必备装备", "url": "https://www.amazon.cn/s?k=运动健身&tag=gudaoqihuo-20", "desc": "活力每一天"},
    ],
    "life": [
        {"text": "居家好物省钱攻略", "url": "https://www.amazon.cn/s?k=居家好物&tag=gudaoqihuo-20", "desc": "品质生活"},
        {"text": "图书畅销榜TOP20", "url": "https://www.amazon.cn/gp/bestsellers/books?tag=gudaoqihuo-20", "desc": "阅读充电"},
    ],
    "entertainment": [
        {"text": "热门影视周边好物", "url": "https://www.amazon.cn/s?k=影视周边&tag=gudaoqihuo-20", "desc": "追剧必备"},
        {"text": "明星同款推荐单品", "url": "https://www.amazon.cn/s?k=明星同款&tag=gudaoqihuo-20", "desc": "潮流好物"},
    ],
    "hot": [
        {"text": "今日热搜相关好物", "url": "https://www.amazon.cn/?tag=gudaoqihuo-20", "desc": "发现更多"},
        {"text": "限时优惠活动专区", "url": "https://www.amazon.cn/gp/goldbox?tag=gudaoqihuo-20", "desc": "今日特价"},
    ],
}

# 英文CPS推广链接(Amazon.com)
EN_CPS_LINKS = {
    "tech": [
        {"text": "Best Selling Electronics 2025", "url": "https://www.amazon.com/gp/bestsellers/electronics?tag=gudaoqihuo-20", "desc": "Top Rated"},
        {"text": "AI Tools & Gadgets", "url": "https://www.amazon.com/s?k=AI+gadgets&tag=gudaoqihuo-20", "desc": "Smart Tech"},
    ],
    "health": [
        {"text": "Health & Wellness Picks", "url": "https://www.amazon.com/s?k=health+wellness&tag=gudaoqihuo-20", "desc": "Stay Healthy"},
        {"text": "Fitness Must-Haves", "url": "https://www.amazon.com/s?k=fitness+equipment&tag=gudaoqihuo-20", "desc": "Get Fit"},
    ],
    "life": [
        {"text": "Home Essentials", "url": "https://www.amazon.com/s?k=home+essentials&tag=gudaoqihuo-20", "desc": "Quality Living"},
        {"text": "Best Selling Books", "url": "https://www.amazon.com/gp/bestsellers/books?tag=gudaoqihuo-20", "desc": "Must Read"},
    ],
    "entertainment": [
        {"text": "Movie & TV Merchandise", "url": "https://www.amazon.com/s?k=movie+merchandise&tag=gudaoqihuo-20", "desc": "Fan Favorites"},
        {"text": "Celebrity Style Picks", "url": "https://www.amazon.com/s?k=celebrity+style&tag=gudaoqihuo-20", "desc": "Trending Now"},
    ],
    "hot": [
        {"text": "Today's Deals", "url": "https://www.amazon.com/gp/goldbox?tag=gudaoqihuo-20", "desc": "Limited Time"},
        {"text": "Trending Products", "url": "https://www.amazon.com/gp/bestsellers?tag=gudaoqihuo-20", "desc": "What's Hot"},
    ],
}

# 广告位配置(中英文共用)
AD_CODE_TOP = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9935054113253833" data-ad-slot="XXXXXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

AD_CODE_MIDDLE = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-client="ca-pub-9935054113253833" data-ad-slot="XXXXXXXXXX" data-ad-format="fluid" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

AD_CODE_BOTTOM = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9935054113253833" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

# 备用常青话题
FALLBACK_TOPICS = [
    "人工智能发展趋势", "健康养生小知识", "科技数码测评", "生活小妙招", "娱乐八卦热点",
    "职场生存指南", "理财投资入门", "教育学习方法", "旅游攻略推荐", "美食烹饪技巧",
]

# ==================== 热点抓取 ====================

def fetch_with_retry(url, headers=None, timeout=10, retries=2):
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=headers or {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}, timeout=timeout)
            resp.raise_for_status()
            return resp
        except Exception as e:
            if attempt < retries:
                time.sleep(1.5)
            else:
                print(f"    请求失败: {e}")
    return None

def fetch_baidu_hot():
    print("    抓取百度热搜...")
    resp = fetch_with_retry("https://top.baidu.com/board?tab=realtime")
    if not resp: return []
    words = re.findall(r'"word":"(.*?)"', resp.text)
    return words[:30]

def fetch_weibo_hot():
    print("    抓取微博热搜...")
    resp = fetch_with_retry("https://weibo.com/ajax/side/hotSearch")
    if not resp: return []
    try:
        data = resp.json()
        return [item.get("word", "") for item in data.get("data", {}).get("realtime", []) if item.get("word")][:30]
    except: return []

def fetch_toutiao_hot():
    print("    抓取今日头条...")
    resp = fetch_with_retry("https://www.toutiao.com/hot-event/hot-board/")
    if not resp: return []
    try:
        data = resp.json()
        return [item.get("Title", "") for item in data.get("data", []) if item.get("Title")][:30]
    except: return []

def fetch_zhihu_hot():
    print("    抓取知乎热榜...")
    resp = fetch_with_retry("https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total")
    if not resp: return []
    try:
        data = resp.json()
        return [item.get("target", {}).get("title", "") for item in data.get("data", []) if item.get("target", {}).get("title")][:30]
    except: return []

def get_hot_topics():
    print("📡 开始抓取热点话题...")
    all_topics = []
    sources = [fetch_baidu_hot, fetch_weibo_hot, fetch_toutiao_hot, fetch_zhihu_hot]
    for source in sources:
        try:
            topics = source()
            if topics:
                all_topics.extend(topics)
                print(f"    {source.__name__}: 获取 {len(topics)} 条")
        except Exception as e:
            print(f"    {source.__name__} 异常: {e}")

    seen = set()
    unique = []
    for t in all_topics:
        t_clean = t.strip()
        if t_clean and t_clean not in seen and 2 < len(t_clean) < 50:
            seen.add(t_clean)
            unique.append(t_clean)

    print(f"  共抓取 {len(all_topics)} 条,去重后 {len(unique)} 条")

    if len(unique) < ARTICLES_PER_RUN:
        needed = ARTICLES_PER_RUN - len(unique)
        extra = [t for t in FALLBACK_TOPICS if t not in seen]
        random.shuffle(extra)
        unique.extend(extra[:needed])
        print(f"  热点不足,补充 {needed} 条常青话题")

    random.shuffle(unique)
    return unique[:ARTICLES_PER_RUN]

# ==================== AI内容生成 ====================

def get_zhipu_token():
    if not jwt: return API_KEY
    parts = API_KEY.split(".")
    if len(parts) != 2: return API_KEY
    kid, secret = parts[0], parts[1]
    payload = {"api_key": kid, "exp": int(time.time()) + 3600, "timestamp": int(time.time())}
    return jwt.encode(payload, secret, algorithm="HS256", headers={"alg": "HS256", "sign_type": "SIGN"})

STYLE_PROMPTS = [
    '你是一个资深自媒体写手，风格接地气、像朋友聊天，喜欢用"说实话"、"讲真"、"你敢信"这类口语。',
    "你是一个犀利的社会观察者,喜欢用反问句、感叹号,观点鲜明,敢说敢评。",
    "你是一个生活达人,擅长把复杂的事情说简单,喜欢举例说明,语气亲切温暖。",
    "你是一个深度分析型作者,喜欢扒细节、挖内幕,但表达方式通俗不装。",
    "你是一个带点毒舌的评论员,说话一针见血,偶尔带点黑色幽默,但信息量足。",
]

TITLE_STYLES = [
    "标题带数字(如'3个真相'、'5大变化'),制造好奇心,让人想点进去,25字以内",
    "标题用疑问句式(如'到底怎么回事?'、'真的假的?'),引发好奇,25字以内",
    "标题制造悬念(如'背后的真相'、'很多人不知道'),暗示有猛料,25字以内",
    "标题用反差感(如'看似XX其实XX'),打破认知,25字以内",
    "标题强调时效性(如'刚刚曝光'、'最新消息'),制造紧迫感,25字以内",
]

# 英文风格提示
EN_STYLE_PROMPTS = [
    "You are a seasoned tech journalist who writes in a conversational, engaging style like a friend sharing news.",
    "You are a sharp social commentator who loves asking rhetorical questions and making bold statements.",
    "You are a lifestyle expert who simplifies complex topics with relatable examples and a warm tone.",
    "You are an investigative writer who digs deep but keeps the language accessible and jargon-free.",
    "You are a witty columnist with a dry sense of humor who delivers hard truths with a smile.",
]

EN_TITLE_STYLES = [
    "Create a numbered headline (like '3 Secrets', '5 Changes') that sparks curiosity, under 60 characters",
    "Use a question format (like 'What Really Happened?', 'Is This Real?') to create intrigue, under 60 characters",
    "Create suspense (like 'The Truth Behind', 'What Nobody Tells You') suggesting hidden information, under 60 characters",
    "Use contrast (like 'Seems X But Actually Y') to challenge assumptions, under 60 characters",
    "Emphasize urgency (like 'Just Revealed', 'Breaking') to create immediacy, under 60 characters",
]

def generate_article_zh(topic):
    """生成中文文章"""
    style = random.choice(STYLE_PROMPTS)
    title_style = random.choice(TITLE_STYLES)

    prompt = f"""{style}

请根据以下热门话题写一篇1200-1800字的文章。

话题:{topic}

要求:
1. {title_style}
2. 第一段包含核心关键词,一两句话抓住眼球
3. 分4-6个小节,每节有##小标题
4. 每个小节内容充实,有观点有例子
5. 自然插入2-3个长尾关键词
6. 结尾引导互动(提问或评论引导)
7. 语气口语化,避免"首先其次最后"这种僵硬表达
8. 不要出现"作为AI"、"本文由AI生成"等字样

输出格式:
第一行:标题(纯文字,不加任何标记)
空一行
正文(markdown格式,##标记小标题)"""

    try:
        token = get_zhipu_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.9, "max_tokens": 2500}
        resp = requests.post(API_URL, headers=headers, json=data, timeout=90)
        result = resp.json()

        if "choices" not in result:
            print(f"  中文AI返回异常: {str(result)[:200]}")
            return None, None

        content = result["choices"][0]["message"]["content"]
        lines = content.strip().split("\n")
        title = lines[0].strip().strip("#").strip()
        body = "\n".join(lines[1:]).strip()

        title = _de_ai_title_zh(title)
        body = _de_ai_process_zh(body)

        return title, body
    except Exception as e:
        print(f"  中文AI生成失败: {e}")
        return None, None

def generate_article_en(topic_zh):
    """生成英文文章(基于中文话题)"""
    style = random.choice(EN_STYLE_PROMPTS)
    title_style = random.choice(EN_TITLE_STYLES)

    prompt = f"""{style}

Write a 800-1200 word article in ENGLISH ONLY based on this trending topic from China: {topic_zh}

CRITICAL RULES:
1. {title_style}
2. EVERYTHING must be in English - title, body, subheadings ALL in English
3. NEVER use Chinese characters anywhere in your output
4. First paragraph hooks the reader immediately
5. 4-6 sections with ## subheadings (in English)
6. Each section has substance - opinions and examples, no fluff
7. Naturally include 2-3 long-tail keywords (in English)
8. End with an engaging question or call-to-action
9. Conversational tone - avoid formal academic language
10. No AI disclaimers like "As an AI" or "This article was generated"
11. If you include any Chinese characters, the article will be rejected

Output format:
First line: Title in English only (no markdown formatting)
Blank line
Body in English only (markdown format with ## for subheadings)"""

    try:
        token = get_zhipu_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.9, "max_tokens": 2000}
        resp = requests.post(API_URL, headers=headers, json=data, timeout=90)
        result = resp.json()

        if "choices" not in result:
            print(f"  英文AI返回异常: {str(result)[:200]}")
            return None, None

        content = result["choices"][0]["message"]["content"]
        lines = content.strip().split("\n")
        title = lines[0].strip().strip("#").strip()
        body = "\n".join(lines[1:]).strip()

        title = _de_ai_title_en(title)
        
        # 后处理：检测并过滤中文内容
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', title + body)
        if len(chinese_chars) > 5:
            print(f"    ⚠️ 英文文章含中文({len(chinese_chars)}字),重新生成...")
            # 重试一次，用更严格的prompt
            title, body = _retry_generate_en_strict(topic_zh)
            if not title:
                print(f"    ❌ 英文生成失败(含中文过多)")
                return None, None

        return title, body
    except Exception as e:
        print(f"  英文AI生成失败: {e}")
        return None, None

def _de_ai_process_zh(text):
    """中文去AI味"""
    replacements = {
        "首先": "先说", "其次": "再来看", "最后": "说到底",
        "总而言之": "说白了", "综上所述": "所以啊",
        "值得注意的是": "这里有个重点", "不可否认": "谁都知道",
        "众所周知": "大家都清楚", "引发了广泛关注": "网上都炸了",
        "引起了热议": "网友吵翻了", "引起了广泛讨论": "大家都在讨论",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def _de_ai_title_zh(title):
    """中文标题优化"""
    if len(title) < 8 or title.startswith("关于") or title.startswith("对于"):
        prefixes = ["突发!", "重磅!", "刚刚!", "速看!", "震惊!", "刚刚曝光!", "出大事了!"]
        title = random.choice(prefixes) + title
    if len(title) > 30:
        title = title[:28] + "..."
    return title

def _de_ai_title_en(title):
    """英文标题优化"""
    if len(title) < 10:
        prefixes = ["Breaking:", "Just In:", "Must Read:", "Shocking:", "Revealed:"]
        title = random.choice(prefixes) + " " + title
    if len(title) > 70:
        title = title[:67] + "..."
    return title

def _retry_generate_en_strict(topic_zh):
    """严格模式重试生成英文文章(禁止中文)"""
    strict_prompt = f"""You are an English news writer. Write an article in 100% ENGLISH.

Topic (Chinese reference): {topic_zh}

ABSOLUTE RULES:
- Title: ENGLISH ONLY, no Chinese characters at all
- Body: ENGLISH ONLY, every single word must be English
- Subheadings: ENGLISH ONLY
- 800-1200 words, 4-6 sections with ## subheadings
- Conversational, engaging style
- Output: Title on first line, then blank line, then body

VIOLATION: If ANY Chinese character appears in output, it is WRONG."""
    try:
        token = get_zhipu_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"model": MODEL, "messages": [{"role": "user", "content": strict_prompt}], "temperature": 0.85, "max_tokens": 2000}
        resp = requests.post(API_URL, headers=headers, json=data, timeout=90)
        result = resp.json()
        if "choices" not in result:
            return None, None
        content = result["choices"][0]["message"]["content"]
        lines = content.strip().split("\n")
        title = lines[0].strip().strip("#").strip()
        body = "\n".join(lines[1:]).strip()
        return _de_ai_title_en(title), body
    except Exception as e:
        print(f"    严格模式重试失败: {e}")
        return None, None

# ==================== 分类 ====================

def classify_topic(topic):
    """中文分类"""
    keywords = {
        "tech": ["AI", "人工智能", "手机", "电脑", "科技", "数码", "互联网", "软件", "芯片", "5G", "编程", "APP", "智能"],
        "health": ["健康", "养生", "医疗", "医院", "疫情", "病毒", "疫苗", "减肥", "健身", "营养", "睡眠", "心理"],
        "life": ["生活", "美食", "旅游", "房产", "汽车", "教育", "职场", "理财", "购物", "家居", "亲子"],
        "entertainment": ["娱乐", "明星", "电影", "电视剧", "综艺", "音乐", "游戏", "网红", "八卦", "偶像"],
    }
    for cat, kws in keywords.items():
        if any(kw in topic for kw in kws):
            return cat
    return "hot"

def classify_topic_en(topic):
    """英文分类(基于中文话题关键词)"""
    return classify_topic(topic)  # 使用相同的关键词匹配

# ==================== Manifest管理 ====================

def load_manifest(lang="zh"):
    fp = MANIFEST_FILE if lang == "zh" else EN_MANIFEST_FILE
    if fp.exists():
        try:
            return json.loads(fp.read_text(encoding="utf-8"))
        except: return []
    return []

def save_manifest(manifest, lang="zh"):
    if lang == "zh":
        OUTPUT_DIR.mkdir(exist_ok=True)
        MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        EN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        EN_MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

def slug_exists(slug, lang="zh"):
    return any(a["slug"] == slug for a in load_manifest(lang))

def add_to_manifest(slug, title, category, filename, lang="zh"):
    manifest = load_manifest(lang)
    # 用精确到秒的时间戳确保新文章永远排在最前面
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 插入到列表头部(最新的在最前面)
    manifest.insert(0, {"slug": slug, "title": title, "category": category, "date": datetime.now().strftime("%Y-%m-%d"), "timestamp": timestamp, "filename": filename})
    save_manifest(manifest, lang)

def get_related_articles(category, current_slug, lang="zh", limit=3):
    manifest = load_manifest(lang)
    related = [a for a in manifest if a["category"] == category and a["slug"] != current_slug]
    return sorted(related, key=lambda x: x.get("date", ""), reverse=True)[:limit]

# ==================== HTML生成 ====================

def topic_to_slug(topic):
    h = hashlib.md5(topic.encode()).hexdigest()[:10]
    clean = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", topic)[:15]
    return f"{clean}-{h}"

def topic_to_slug_en(topic):
    """英文slug(基于中文话题)"""
    h = hashlib.md5(topic.encode()).hexdigest()[:10]
    return f"article-{h}"

def _md2html(text):
    html = text
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    paragraphs = html.split("\n\n")
    result = []
    for p in paragraphs:
        p = p.strip()
        if not p: continue
        if p.startswith("<h"): result.append(p)
        else:
            lines = p.split("\n")
            p_html = "<br>".join(l.strip() for l in lines if l.strip())
            result.append(f"<p>{p_html}</p>")
    return "\n".join(result)

def _cps_block(category, lang="zh"):
    links = CPS_LINKS.get(category, CPS_LINKS["hot"]) if lang == "zh" else EN_CPS_LINKS.get(category, EN_CPS_LINKS["hot"])
    if lang == "zh":
        html = '<div class="cps-box"><h3>🛒 猜你也感兴趣</h3><ul>'
    else:
        html = '<div class="cps-box"><h3>🛒 You May Also Like</h3><ul>'
    for link in links:
        desc = link.get("desc", "")
        if desc:
            html += f'<li><a href="{link["url"]}" target="_blank" rel="nofollow">{link["text"]}</a><span class="cps-desc">{desc}</span></li>'
        else:
            html += f'<li><a href="{link["url"]}" target="_blank" rel="nofollow">{link["text"]}</a></li>'
    html += '</ul></div>'
    return html

def _related_block(related_articles, lang="zh"):
    if not related_articles: return ""
    if lang == "zh":
        html = '<div class="related"><h3>📖 相关推荐</h3><ul>'
    else:
        html = '<div class="related"><h3>📖 Related Articles</h3><ul>'
    for a in related_articles:
        prefix = "/articles/" if lang == "zh" else "/en/articles/"
        html += f'<li><a href="{prefix}{a["filename"]}">{a["title"]}</a><span class="date">{a.get("date","")}</span></li>'
    html += "</ul></div>"
    return html

def _jsonld_article(title, cat_name, date_iso, slug, lang="zh"):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "datePublished": date_iso,
        "dateModified": date_iso,
        "publisher": {"@type": "Organization", "name": SITE_NAME if lang == "zh" else EN_SITE_NAME}
    }, ensure_ascii=False)

def generate_article_html_zh(title, body, category, slug, related_articles):
    cat_info = CATEGORIES.get(category, CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    html_body = _md2html(body)

    # 插入中间广告
    parts = html_body.split("</p>")
    if len(parts) > 3:
        parts.insert(3, f"</p>\n{AD_CODE_MIDDLE}")
        html_body = "".join(parts)

    json_ld = _jsonld_article(title, cat_name, date_iso, slug, "zh")

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<title>{title} - {SITE_NAME}</title>
<meta name="description" content="{title},{cat_name}深度解读">
<link rel="canonical" href="{SITE_URL}/articles/{slug}.html">
<script type="application/ld+json">{json_ld}</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;line-height:1.8;color:#333;max-width:800px;margin:0 auto;padding:15px;background:#fafafa}}
.header{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:2px solid #ff6b35;margin-bottom:15px}}
.header h1{{font-size:1.1em;color:#ff6b35}}
.breadcrumb{{font-size:.85em;color:#999;margin-bottom:15px}}
.breadcrumb a{{color:#ff6b35;text-decoration:none}}
.article-title{{font-size:1.6em;font-weight:bold;margin-bottom:8px;color:#1a1a1a}}
.meta{{color:#888;font-size:.88em;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid #eee}}
h2{{font-size:1.3em;margin:25px 0 10px;color:#2c2c2c;border-left:4px solid #ff6b35;padding-left:10px}}
p{{margin-bottom:15px;text-align:justify}}
.ad-slot{{margin:20px 0;min-height:90px;text-align:center}}
.cps-box{{background:linear-gradient(135deg,#fff9f0,#fff5e6);border:1px solid #ffe0c0;border-radius:10px;padding:18px;margin:25px 0}}
.cps-box h3{{margin:0 0 12px;color:#d4680a}}
.cps-box ul{{list-style:none;padding:0}}
.cps-box li{{padding:8px 0;border-bottom:1px dashed #ffd9b3;display:flex;justify-content:space-between}}
.cps-box a{{color:#d4680a;text-decoration:none}}
.cps-desc{{color:#999;font-size:.82em}}
.related{{background:#fff;border:1px solid #eee;border-radius:10px;padding:18px;margin:25px 0}}
.related h3{{margin:0 0 12px;color:#333}}
.related ul{{list-style:none;padding:0}}
.related li{{padding:8px 0;border-bottom:1px solid #f5f5f5}}
.related a{{color:#333;text-decoration:none}}
.related .date{{color:#ccc;font-size:.8em;margin-left:10px}}
.footer{{margin-top:30px;padding-top:15px;border-top:1px solid #eee;text-align:center;color:#aaa;font-size:.82em}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
</style>
</head>
<body>
<div class="header">
<h1>📰 {SITE_NAME}</h1>
<div><a href="/">中文</a> | <a href="/en/">English</a></div>
</div>
<nav class="breadcrumb">
<a href="/">首页</a> &gt; <a href="/articles/{category}.html">{cat_icon} {cat_name}</a> &gt; {title}
</nav>
<article>
<h1 class="article-title">{title}</h1>
<div class="meta"><span>📅 {date_str}</span> <span>{cat_icon} {cat_name}</span></div>
<div class="ad-slot">{AD_CODE_TOP}</div>
{html_body}
{_cps_block(category, "zh")}
{_related_block(related_articles, "zh")}
</article>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025 {SITE_NAME}</p>
<p><a href="/">首页</a><a href="/articles/hot.html">社会热点</a><a href="/articles/tech.html">科技数码</a><a href="/articles/health.html">健康养生</a><a href="/articles/life.html">生活百科</a><a href="/articles/entertainment.html">娱乐八卦</a></p>
</div>
</body>
</html>"""

def generate_article_html_en(title, body, category, slug, related_articles):
    cat_info = EN_CATEGORIES.get(category, EN_CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    html_body = _md2html(body)

    parts = html_body.split("</p>")
    if len(parts) > 3:
        parts.insert(3, f"</p>\n{AD_CODE_MIDDLE}")
        html_body = "".join(parts)

    json_ld = _jsonld_article(title, cat_name, date_iso, slug, "en")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<title>{title} - {EN_SITE_NAME}</title>
<meta name="description" content="{title} - in-depth analysis">
<link rel="canonical" href="{EN_SITE_URL}/en/articles/{slug}.html">
<script type="application/ld+json">{json_ld}</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.8;color:#333;max-width:800px;margin:0 auto;padding:15px;background:#fafafa}}
.header{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:2px solid #ff6b35;margin-bottom:15px}}
.header h1{{font-size:1.1em;color:#ff6b35}}
.breadcrumb{{font-size:.85em;color:#999;margin-bottom:15px}}
.breadcrumb a{{color:#ff6b35;text-decoration:none}}
.article-title{{font-size:1.6em;font-weight:bold;margin-bottom:8px;color:#1a1a1a}}
.meta{{color:#888;font-size:.88em;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid #eee}}
h2{{font-size:1.3em;margin:25px 0 10px;color:#2c2c2c;border-left:4px solid #ff6b35;padding-left:10px}}
p{{margin-bottom:15px;text-align:justify}}
.ad-slot{{margin:20px 0;min-height:90px;text-align:center}}
.cps-box{{background:linear-gradient(135deg,#fff9f0,#fff5e6);border:1px solid #ffe0c0;border-radius:10px;padding:18px;margin:25px 0}}
.cps-box h3{{margin:0 0 12px;color:#d4680a}}
.cps-box ul{{list-style:none;padding:0}}
.cps-box li{{padding:8px 0;border-bottom:1px dashed #ffd9b3;display:flex;justify-content:space-between}}
.cps-box a{{color:#d4680a;text-decoration:none}}
.cps-desc{{color:#999;font-size:.82em}}
.related{{background:#fff;border:1px solid #eee;border-radius:10px;padding:18px;margin:25px 0}}
.related h3{{margin:0 0 12px;color:#333}}
.related ul{{list-style:none;padding:0}}
.related li{{padding:8px 0;border-bottom:1px solid #f5f5f5}}
.related a{{color:#333;text-decoration:none}}
.related .date{{color:#ccc;font-size:.8em;margin-left:10px}}
.footer{{margin-top:30px;padding-top:15px;border-top:1px solid #eee;text-align:center;color:#aaa;font-size:.82em}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
</style>
</head>
<body>
<div class="header">
<h1>📰 {EN_SITE_NAME}</h1>
<div><a href="/">中文</a> | <a href="/en/">English</a></div>
</div>
<nav class="breadcrumb">
<a href="/en/">Home</a> &gt; <a href="/en/articles/{category}.html">{cat_icon} {cat_name}</a> &gt; {title}
</nav>
<article>
<h1 class="article-title">{title}</h1>
<div class="meta"><span>📅 {date_str}</span> <span>{cat_icon} {cat_name}</span></div>
<div class="ad-slot">{AD_CODE_TOP}</div>
{html_body}
{_cps_block(category, "en")}
{_related_block(related_articles, "en")}
</article>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025 {EN_SITE_NAME}</p>
<p><a href="/en/">Home</a><a href="/en/articles/hot.html">Trending</a><a href="/en/articles/tech.html">Tech</a><a href="/en/articles/health.html">Health</a><a href="/en/articles/life.html">Lifestyle</a><a href="/en/articles/entertainment.html">Entertainment</a></p>
</div>
</body>
</html>"""

# ==================== 分类页 ====================

def generate_category_page_zh(category):
    cat_info = CATEGORIES.get(category, CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    articles = sorted([a for a in load_manifest("zh") if a["category"] == category], key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)[:50]
    list_items = "\n".join(f'<li><span class="date">{a.get("date","")}</span><a href="/articles/{a["filename"]}">{a["title"]}</a></li>' for a in articles) or '<li style="color:#999">暂无文章...</li>'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<title>{cat_icon} {cat_name} - {SITE_NAME}</title>
<link rel="canonical" href="{SITE_URL}/articles/{category}.html">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;line-height:1.8;color:#333;max-width:900px;margin:0 auto;padding:15px;background:#fafafa}}
.header{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:2px solid #ff6b35;margin-bottom:15px}}
.header h1{{font-size:1.1em;color:#ff6b35}}
.breadcrumb{{font-size:.85em;color:#999;margin-bottom:15px}}
.breadcrumb a{{color:#ff6b35;text-decoration:none}}
.cat-title{{font-size:1.5em;margin:20px 0;font-weight:bold}}
ul{{list-style:none}}
li{{padding:12px 10px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:10px}}
li:hover{{background:#fff}}
.date{{color:#999;font-size:.85em;white-space:nowrap;min-width:85px}}
a{{color:#333;text-decoration:none}}
a:hover{{color:#ff6b35}}
.footer{{margin-top:30px;text-align:center;color:#aaa;font-size:.82em;padding-top:15px;border-top:1px solid #eee}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
.ad-slot{{margin:20px 0;min-height:90px;text-align:center}}
</style>
</head>
<body>
<div class="header">
<h1>📰 {SITE_NAME}</h1>
<div><a href="/">中文</a> | <a href="/en/">English</a></div>
</div>
<nav class="breadcrumb"><a href="/">首页</a> &gt; {cat_icon} {cat_name}</nav>
<h2 class="cat-title">{cat_icon} {cat_name}</h2>
<div class="ad-slot">{AD_CODE_TOP}</div>
<ul>{list_items}</ul>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025 {SITE_NAME}</p>
<p><a href="/">首页</a><a href="/articles/hot.html">社会热点</a><a href="/articles/tech.html">科技数码</a><a href="/articles/health.html">健康养生</a><a href="/articles/life.html">生活百科</a><a href="/articles/entertainment.html">娱乐八卦</a></p>
</div>
</body>
</html>"""

def generate_category_page_en(category):
    cat_info = EN_CATEGORIES.get(category, EN_CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    articles = sorted([a for a in load_manifest("en") if a["category"] == category], key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)[:50]
    list_items = "\n".join(f'<li><span class="date">{a.get("date","")}</span><a href="/en/articles/{a["filename"]}">{a["title"]}</a></li>' for a in articles) or '<li style="color:#999">No articles yet...</li>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<title>{cat_icon} {cat_name} - {EN_SITE_NAME}</title>
<link rel="canonical" href="{EN_SITE_URL}/en/articles/{category}.html">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.8;color:#333;max-width:900px;margin:0 auto;padding:15px;background:#fafafa}}
.header{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:2px solid #ff6b35;margin-bottom:15px}}
.header h1{{font-size:1.1em;color:#ff6b35}}
.breadcrumb{{font-size:.85em;color:#999;margin-bottom:15px}}
.breadcrumb a{{color:#ff6b35;text-decoration:none}}
.cat-title{{font-size:1.5em;margin:20px 0;font-weight:bold}}
ul{{list-style:none}}
li{{padding:12px 10px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:10px}}
li:hover{{background:#fff}}
.date{{color:#999;font-size:.85em;white-space:nowrap;min-width:85px}}
a{{color:#333;text-decoration:none}}
a:hover{{color:#ff6b35}}
.footer{{margin-top:30px;text-align:center;color:#aaa;font-size:.82em;padding-top:15px;border-top:1px solid #eee}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
.ad-slot{{margin:20px 0;min-height:90px;text-align:center}}
</style>
</head>
<body>
<div class="header">
<h1>📰 {EN_SITE_NAME}</h1>
<div><a href="/">中文</a> | <a href="/en/">English</a></div>
</div>
<nav class="breadcrumb"><a href="/en/">Home</a> &gt; {cat_icon} {cat_name}</nav>
<h2 class="cat-title">{cat_icon} {cat_name}</h2>
<div class="ad-slot">{AD_CODE_TOP}</div>
<ul>{list_items}</ul>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025 {EN_SITE_NAME}</p>
<p><a href="/en/">Home</a><a href="/en/articles/hot.html">Trending</a><a href="/en/articles/tech.html">Tech</a><a href="/en/articles/health.html">Health</a><a href="/en/articles/life.html">Lifestyle</a><a href="/en/articles/entertainment.html">Entertainment</a></p>
</div>
</body>
</html>"""

# ==================== 首页 ====================

def rebuild_index_zh():
    manifest = load_manifest("zh")
    if not manifest:
        print("  中文首页:暂无文章")
        return
    articles = sorted(manifest, key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)[:100]
    list_items = "\n".join(f'<li><span class="date">{a.get("date","")}</span><span class="cat">[{CATEGORIES.get(a["category"],CATEGORIES["hot"])["name"]}]</span><a href="/articles/{a["filename"]}">{a["title"]}</a></li>' for a in articles)
    cat_links = "\n".join(f'<a href="/articles/{k}.html" class="cat-link">{v["icon"]} {v["name"]}</a>' for k, v in CATEGORIES.items())

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<title>{SITE_NAME} - {SITE_DESC}</title>
<meta name="description" content="{SITE_DESC}">
<link rel="canonical" href="{SITE_URL}/">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;line-height:1.8;color:#333;max-width:900px;margin:0 auto;padding:15px;background:#fafafa}}
.site-header{{text-align:center;padding:25px 0 20px}}
.site-header h1{{font-size:1.8em;color:#1a1a1a;margin-bottom:5px}}
.site-header p{{color:#888;font-size:.95em}}
.lang-switch{{text-align:center;margin-bottom:15px}}
.lang-switch a{{color:#ff6b35;text-decoration:none;margin:0 10px;padding:5px 15px;border:1px solid #ff6b35;border-radius:20px}}
.lang-switch a:hover{{background:#ff6b35;color:#fff}}
.cat-nav{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:15px 0 25px;padding:15px;background:#fff;border-radius:10px}}
.cat-link{{padding:6px 16px;border-radius:20px;background:#fff5ed;color:#d4680a;text-decoration:none;font-size:.9em;border:1px solid #ffe0c0}}
.cat-link:hover{{background:#ff6b35;color:#fff}}
ul{{list-style:none}}
li{{padding:12px 10px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:8px}}
li:hover{{background:#fff}}
.date{{color:#999;font-size:.85em;white-space:nowrap;min-width:85px}}
.cat{{color:#ff6b35;font-size:.8em;white-space:nowrap;min-width:75px}}
a{{color:#333;text-decoration:none}}
a:hover{{color:#ff6b35}}
.footer{{margin-top:30px;text-align:center;color:#aaa;font-size:.82em;padding-top:15px;border-top:1px solid #eee}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
.ad-slot{{margin:20px 0;min-height:90px;text-align:center}}
</style>
</head>
<body>
<div class="site-header">
<h1>📰 {SITE_NAME}</h1>
<p>{SITE_DESC}</p>
</div>
<div class="lang-switch">
<a href="/">中文</a> | <a href="/en/">English</a>
</div>
<nav class="cat-nav">{cat_links}</nav>
<div class="ad-slot">{AD_CODE_TOP}</div>
<ul>{list_items}</ul>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025 {SITE_NAME}</p>
<p><a href="/">首页</a><a href="/articles/hot.html">社会热点</a><a href="/articles/tech.html">科技数码</a><a href="/articles/health.html">健康养生</a><a href="/articles/life.html">生活百科</a><a href="/articles/entertainment.html">娱乐八卦</a></p>
</div>
</body>
</html>"""
    INDEX_FILE.write_text(html, encoding="utf-8")
    print(f"  中文首页已更新,展示 {len(articles)} 篇")

def rebuild_index_en():
    manifest = load_manifest("en")
    if not manifest:
        print("  英文首页:暂无文章")
        return
    articles = sorted(manifest, key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)[:100]
    list_items = "\n".join(f'<li><span class="date">{a.get("date","")}</span><span class="cat">[{EN_CATEGORIES.get(a["category"],EN_CATEGORIES["hot"])["name"]}]</span><a href="/en/articles/{a["filename"]}">{a["title"]}</a></li>' for a in articles)
    cat_links = "\n".join(f'<a href="/en/articles/{k}.html" class="cat-link">{v["icon"]} {v["name"]}</a>' for k, v in EN_CATEGORIES.items())

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<title>{EN_SITE_NAME} - {EN_SITE_DESC}</title>
<meta name="description" content="{EN_SITE_DESC}">
<link rel="canonical" href="{EN_SITE_URL}/en/">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.8;color:#333;max-width:900px;margin:0 auto;padding:15px;background:#fafafa}}
.site-header{{text-align:center;padding:25px 0 20px}}
.site-header h1{{font-size:1.8em;color:#1a1a1a;margin-bottom:5px}}
.site-header p{{color:#888;font-size:.95em}}
.lang-switch{{text-align:center;margin-bottom:15px}}
.lang-switch a{{color:#ff6b35;text-decoration:none;margin:0 10px;padding:5px 15px;border:1px solid #ff6b35;border-radius:20px}}
.lang-switch a:hover{{background:#ff6b35;color:#fff}}
.cat-nav{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:15px 0 25px;padding:15px;background:#fff;border-radius:10px}}
.cat-link{{padding:6px 16px;border-radius:20px;background:#fff5ed;color:#d4680a;text-decoration:none;font-size:.9em;border:1px solid #ffe0c0}}
.cat-link:hover{{background:#ff6b35;color:#fff}}
ul{{list-style:none}}
li{{padding:12px 10px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:8px}}
li:hover{{background:#fff}}
.date{{color:#999;font-size:.85em;white-space:nowrap;min-width:85px}}
.cat{{color:#ff6b35;font-size:.8em;white-space:nowrap;min-width:75px}}
a{{color:#333;text-decoration:none}}
a:hover{{color:#ff6b35}}
.footer{{margin-top:30px;text-align:center;color:#aaa;font-size:.82em;padding-top:15px;border-top:1px solid #eee}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
.ad-slot{{margin:20px 0;min-height:90px;text-align:center}}
</style>
</head>
<body>
<div class="site-header">
<h1>📰 {EN_SITE_NAME}</h1>
<p>{EN_SITE_DESC}</p>
</div>
<div class="lang-switch">
<a href="/">中文</a> | <a href="/en/">English</a>
</div>
<nav class="cat-nav">{cat_links}</nav>
<div class="ad-slot">{AD_CODE_TOP}</div>
<ul>{list_items}</ul>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025 {EN_SITE_NAME}</p>
<p><a href="/en/">Home</a><a href="/en/articles/hot.html">Trending</a><a href="/en/articles/tech.html">Tech</a><a href="/en/articles/health.html">Health</a><a href="/en/articles/life.html">Lifestyle</a><a href="/en/articles/entertainment.html">Entertainment</a></p>
</div>
</body>
</html>"""
    Path("en").mkdir(exist_ok=True)
    EN_INDEX_FILE.write_text(html, encoding="utf-8")
    print(f"  英文首页已更新,展示 {len(articles)} 篇")

# ==================== Sitemap ====================

def rebuild_sitemap():
    urls = [f"<url><loc>{SITE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>"]
    urls.append(f"<url><loc>{SITE_URL}/en/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>")

    # 中文分类
    for cat in CATEGORIES:
        urls.append(f"<url><loc>{SITE_URL}/articles/{cat}.html</loc><changefreq>daily</changefreq><priority>0.8</priority></url>")
    # 英文分类
    for cat in EN_CATEGORIES:
        urls.append(f"<url><loc>{SITE_URL}/en/articles/{cat}.html</loc><changefreq>daily</changefreq><priority>0.8</priority></url>")

    # 中文文章
    for a in load_manifest("zh"):
        urls.append(f"<url><loc>{SITE_URL}/articles/{a['filename']}</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>")
    # 英文文章
    for a in load_manifest("en"):
        urls.append(f"<url><loc>{SITE_URL}/en/articles/{a['filename']}</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>"""
    SITEMAP_FILE.write_text(xml, encoding="utf-8")
    print(f"  Sitemap已更新,共 {len(urls)} 条URL")

# ==================== 主流程 ====================

def main():
    if not API_KEY:
        print("❌ 未设置 ZHIPU_API_KEY 环境变量")
        return

    print(f"🚀 双语内容生成器 v3.0 启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    OUTPUT_DIR.mkdir(exist_ok=True)
    EN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. 抓热点
    topics = get_hot_topics()
    print(f"📋 本轮话题: {len(topics)} 个")

    # 2. 逐篇生成(中英文)
    zh_generated, en_generated = 0, 0
    for i, topic in enumerate(topics):
        slug_zh = topic_to_slug(topic)
        slug_en = topic_to_slug_en(topic)
        
        # 中文版
        if not slug_exists(slug_zh, "zh"):
            print(f"  ✍️ [{i+1}/{len(topics)}] 中文: {topic}")
            title_zh, body_zh = generate_article_zh(topic)
            if title_zh and body_zh:
                category = classify_topic(topic)
                filename_zh = f"{slug_zh}.html"
                related_zh = get_related_articles(category, slug_zh, "zh")
                html_zh = generate_article_html_zh(title_zh, body_zh, category, slug_zh, related_zh)
                (OUTPUT_DIR / filename_zh).write_text(html_zh, encoding="utf-8")
                add_to_manifest(slug_zh, title_zh, category, filename_zh, "zh")
                zh_generated += 1
                print(f"    ✅ 中文完成: {filename_zh}")
            time.sleep(1)
        else:
            print(f"  ⏭ [{i+1}/{len(topics)}] 中文跳过(重复): {topic}")

        # 英文版
        if not slug_exists(slug_en, "en"):
            print(f"  ✍️ [{i+1}/{len(topics)}] 英文: {topic}")
            title_en, body_en = generate_article_en(topic)
            if title_en and body_en:
                category = classify_topic_en(topic)
                filename_en = f"{slug_en}.html"
                related_en = get_related_articles(category, slug_en, "en")
                html_en = generate_article_html_en(title_en, body_en, category, slug_en, related_en)
                (EN_OUTPUT_DIR / filename_en).write_text(html_en, encoding="utf-8")
                add_to_manifest(slug_en, title_en, category, filename_en, "en")
                en_generated += 1
                print(f"    ✅ 英文完成: {filename_en}")
            time.sleep(1)
        else:
            print(f"  ⏭ [{i+1}/{len(topics)}] 英文跳过(重复)")

    # 3. 重建站点
    if zh_generated > 0 or en_generated > 0:
        print("\n📐 重建站点页面...")
        rebuild_index_zh()
        rebuild_index_en()
        for cat in CATEGORIES:
            (OUTPUT_DIR / f"{cat}.html").write_text(generate_category_page_zh(cat), encoding="utf-8")
            (EN_OUTPUT_DIR / f"{cat}.html").write_text(generate_category_page_en(cat), encoding="utf-8")
        rebuild_sitemap()

    print(f"\n🏁 完成! 本次生成: 中文 {zh_generated} 篇, 英文 {en_generated} 篇")

if __name__ == "__main__":
    main()
