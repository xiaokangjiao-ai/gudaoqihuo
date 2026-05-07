"""
全自动热点流量站内容生成器 v2.0
================================
多源热点抓取 | AI伪原创 | 标题党 | 内链网络 | 结构化数据 | 广告+CPS变现
"""

import os, re, json, time, random, hashlib, requests
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

ARTICLES_PER_RUN = 5
OUTPUT_DIR = Path("articles")
MANIFEST_FILE = OUTPUT_DIR / "manifest.json"
INDEX_FILE = Path("index.html")
SITEMAP_FILE = Path("sitemap.xml")

SITE_NAME = "每日热点速递"
SITE_URL = "https://gudaoqihuo.com"
SITE_DESC = "AI智能聚合热点资讯,每日更新,一站了解天下事"

CATEGORIES = {
    "hot":         {"name": "社会热点",   "icon": "🔥"},
    "tech":        {"name": "科技数码",   "icon": "📱"},
    "health":      {"name": "健康养生",   "icon": "🏥"},
    "life":        {"name": "生活百科",   "icon": "💡"},
    "entertainment":{"name": "娱乐八卦",   "icon": "🎬"},
}

# CPS推广链接(亚马逊联盟格式,替换为真实 Associates 链接后生效)
# 获取链接: https://affiliate-program.amazon.com/
# 格式: https://www.amazon.cn/dp/商品ASIN?tag=你的AssociateTag
CPS_LINKS = {
    "tech": [
        {"text": "2025高性价比手机推荐",      "url": "https://www.amazon.cn/gp/bestsellers/electronics/ref=zg_bs_electronics?tag=gudaoqihuo-20", "desc": "热销数码产品"},
        {"text": "AI智能工具实用合集",       "url": "https://www.amazon.cn/s?k=AI%E5%B7%A5%E5%85%B7&i=office-products&tag=gudaoqihuo-20", "desc": "效率神器"},
    ],
    "health": [
        {"text": "养生保健精选好物",         "url": "https://www.amazon.cn/s?k=%E5%85%BB%E7%94%9F&i=hpc&tag=gudaoqihuo-20", "desc": "健康生活"},
        {"text": "运动健身必备装备",         "url": "https://www.amazon.cn/s?k=%E8%BF%90%E5%8A%A8%E5%81%A5%E8%BA%AB&i=sporting-goods&tag=gudaoqihuo-20", "desc": "活力每一天"},
    ],
    "life": [
        {"text": "居家好物省钱攻略",          "url": "https://www.amazon.cn/s?k=%E5%B1%85%E5%AE%B6%E5%A5%BD%E7%89%A9&i=kitchen&tag=gudaoqihuo-20", "desc": "品质生活"},
        {"text": "图书畅销榜TOP20",           "url": "https://www.amazon.cn/gp/best sellers/books/ref=zg_bs_books?tag=gudaoqihuo-20", "desc": "阅读充电"},
    ],
    "entertainment": [
        {"text": "热门影视周边好物",          "url": "https://www.amazon.cn/s?k=%E5%BD%B1%E8%A7%86%E5%91%A8%E8%BE%B9&tag=gudaoqihuo-20", "desc": "追剧必备"},
        {"text": "明星同款推荐单品",          "url": "https://www.amazon.cn/s?k=%E6%98%8E%E6%98%9F%E5%90%8C%E6%AC%BE&tag=gudaoqihuo-20", "desc": "潮流好物"},
    ],
    "hot": [
        {"text": "今日热搜相关好物",          "url": "https://www.amazon.cn/?_encoding=UTF8&tag=gudaoqihuo-20", "desc": "发现更多"},
        {"text": "限时优惠活动专区",          "url": "https://www.amazon.cn/gp/goldbox?ref_=gs_gb_top&tag=gudaoqihuo-20", "desc": "今日特价"},
    ],
}

# ==================== 广告位配置 ====================
# Google AdSense: 申请地址 https://www.google.com/adsense/
# 拿到代码后直接替换下面的占位符即可
# 注意: AdSense 要求内容为主、广告为辅，不要放太多广告位
AD_CODE_TOP     = ''''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-9935054113253833"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="horizontal"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

AD_CODE_MIDDLE  = ''''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-client="ca-pub-9935054113253833"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="fluid"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

AD_CODE_BOTTOM  = ''''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-9935054113253833"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

# ==================== 热点抓取(带重试+备用) ====================

def fetch_with_retry(url, headers=None, timeout=10, retries=2):
    for attempt in range(retries + 1):
        try:
            resp = requests.get(
                url,
                headers=headers or {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                },
                timeout=timeout,
            )
            resp.raise_for_status()
            return resp
        except Exception as e:
            if attempt < retries:
                time.sleep(1.5)
            else:
                print(f"    请求失败: {e}")
    return None


def fetch_baidu_hot():
    """百度热搜实时榜"""
    print("    抓取百度热搜...")
    resp = fetch_with_retry("https://top.baidu.com/board?tab=realtime")
    if not resp:
        return []
    words = re.findall(r'"word":"(.*?)"', resp.text)
    return words[:30]


def fetch_weibo_hot():
    """微博热搜"""
    print("    抓取微博热搜...")
    resp = fetch_with_retry("https://weibo.com/ajax/side/hotSearch")
    if not resp:
        return []
    try:
        data = resp.json()
        return [item.get("word", "") for item in data.get("data", {}).get("realtime", []) if item.get("word")][:30]
    except:
        return []


def fetch_toutiao_hot():
    """头条热榜"""
    print("    抓取头条热榜...")
    resp = fetch_with_retry("https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc")
    if not resp:
        return []
    try:
        data = resp.json()
        return [item.get("Title", "") for item in data.get("data", []) if item.get("Title")][:30]
    except:
        return []


def fetch_zhihu_hot():
    """知乎热榜"""
    print("    抓取知乎热榜...")
    resp = fetch_with_retry("https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50")
    if not resp:
        return []
    try:
        data = resp.json()
        return [item.get("target", {}).get("title", "") for item in data.get("data", []) if item.get("target", {}).get("title")][:30]
    except:
        return []


# 常青话题池(热点源全部失效时的保底)
FALLBACK_TOPICS = [
    "2025年最值得买的手机推荐", "如何快速提升睡眠质量", "年轻人副业赚钱方法",
    "ChatGPT最新使用技巧大全", "减肥最有效的方法是什么", "手机电池保养秘诀",
    "2025年房价走势预测", "居家健身最有效的动作", "信用卡省钱攻略",
    "AI写作工具哪个最好用", "电动牙刷真的比普通牙刷好吗", "上班族如何缓解颈椎疼痛",
    "2025年最火的短视频赛道", "拼多多和淘宝哪个更省钱", "失眠怎么办最有效",
    "远程办公效率提升技巧", "厨房收纳神器推荐", "2025年高考政策变化",
    "退休金计算方法详解", "驾照考试新规解读", "空调省电技巧",
    "洗衣机清洗方法", "手机信号差怎么解决", "微波炉加热食物注意事项",
    "租房合同注意事项", "社保断缴有什么影响", "个人养老金怎么交最划算",
    "2025年新能源汽车推荐", "WiFi信号增强方法", "冰箱食物存放正确方式",
]


def get_hot_topics():
    """多源热点聚合,去重,备用"""
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

    # 去重
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
    """智谱API JWT token生成"""
    if not jwt:
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
    return jwt.encode(payload, secret, algorithm="HS256",
                      headers={"alg": "HS256", "sign_type": "SIGN"})


# 随机风格prompt池(降低AI味)
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


def generate_article(topic):
    """AI生成伪原创文章"""
    style = random.choice(STYLE_PROMPTS)
    title_style = random.choice(TITLE_STYLES)

    prompt = f"""{style}

请根据以下热门话题写一篇1200-1800字的文章。

话题:{topic}

要求:
1. {title_style}
2. 第一段包含核心关键词,一两句话抓住眼球
3. 分4-6个小节,每节有##小标题
4. 每个小节内容充实,有观点有例子,不是废话
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
        data = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9,
            "max_tokens": 2500,
        }
        resp = requests.post(API_URL, headers=headers, json=data, timeout=90)
        result = resp.json()

        if "choices" not in result:
            print(f"  AI返回异常: {str(result)[:200]}")
            return None, None

        content = result["choices"][0]["message"]["content"]
        lines = content.strip().split("\n")
        title = lines[0].strip().strip("#").strip()
        body = "\n".join(lines[1:]).strip()

        body = _de_ai_process(body)
        title = _de_ai_title(title)

        return title, body
    except Exception as e:
        print(f"  AI生成失败: {e}")
        return None, None


def _de_ai_process(text):
    """去AI味后处理"""
    replacements = {
        "首先": "先说", "其次": "再来看", "最后": "说到底",
        "总而言之": "说白了", "综上所述": "所以啊",
        "值得注意的是": "这里有个重点", "不可否认": "谁都知道",
        "众所周知": "大家都清楚", "引发了广泛关注": "网上都炸了",
        "引起了热议": "网友吵翻了", "引起了广泛讨论": "大家都在讨论",
        "不言而喻": "懂的都懂", "至关重要": "特别关键",
        "息息相关": "紧密相连", "举足轻重": "非常重要",
        "日新月异": "变化太快", "蓬勃发展": "越搞越火",
        "与此同时": "再一个", "在当今社会": "现在",
        "随着社会的发展": "现在", "在日常生活中": "平时",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # 随机插入填充词
    fillers = ["说实话", "讲真", "你敢信", "我跟你讲", "老实说", "真的", "确实"]
    paragraphs = text.split("\n\n")
    result = []
    for p in paragraphs:
        p_stripped = p.strip()
        if not p_stripped or p_stripped.startswith("#"):
            result.append(p)
            continue
        if random.random() < 0.25 and not any(p_stripped.startswith(w) for w in fillers):
            p = random.choice(fillers) + "," + p[0].lower() + p[1:]
        result.append(p)

    return "\n\n".join(result)


def _de_ai_title(title):
    """标题党优化"""
    if len(title) < 8 or title.startswith("关于") or title.startswith("对于"):
        prefixes = ["突发!", "重磅!", "刚刚!", "速看!", "震惊!", "刚刚曝光!", "出大事了!"]
        title = random.choice(prefixes) + title
    if len(title) > 30:
        title = title[:28] + "..."
    return title


# ==================== 分类 ====================

def classify_topic(topic):
    """关键词分类"""
    rules = {
        "tech": ["手机","AI","芯片","科技","数码","电脑","苹果","华为","小米","ChatGPT",
                 "人工智能","互联网","软件","APP","5G","机器人","电动车","特斯拉","比亚迪",
                 "新能源车","自动驾驶","智能","OpenAI","GPT","编程","代码","操作系统",
                 "GPU","显卡","CPU","智能家居","耳机","平板"],
        "health": ["健康","养生","睡眠","减肥","医","病","食物","营养","锻炼","健身",
                   "医院","中医","食疗","维生素","体检","癌症","长寿","慢性病","心理",
                   "抑郁","焦虑","疫苗","过敏","眼睛","牙齿"],
        "life": ["生活","省钱","副业","赚钱","工作","职场","房","车","贷款","社保",
                 "养老金","退休","保险","税收","公积金","信用卡","存款","利率","消费","物价"],
        "entertainment": ["明星","综艺","电影","电视剧","演员","导演","票房","恋情",
                          "离婚","八卦","偶像","演唱会","歌手","网红","直播","选秀",
                          "粉丝","塌房","热搜","出轨","复合","韩剧","美剧"],
    }
    for cat, keywords in rules.items():
        for kw in keywords:
            if kw in topic:
                return cat
    # 二级兜底：对"hot"再做一次分类尝试
    secondary_rules = {
        "tech": ["新","消息","曝光","最新"],
        "life": ["建议","方法","攻略","技巧"],
        "health": ["注意","提醒","专家","研究"],
        "entertainment": ["网友","热搜","冲上","刷屏"],
    }
    for cat, kws in secondary_rules.items():
        if any(kw in topic for kw in kws):
            return cat
    return "hot"


def ensure_category_balance():
    """兜底：保证每个分类至少有2篇文章，不够的用热点关键词强制补充"""
    manifest = load_manifest()
    extra_generated = 0
    for cat in CATEGORIES:
        count = sum(1 for a in manifest if a["category"] == cat)
        needed = max(0, 2 - count)
        if needed == 0:
            continue
        # 取未被使用过的热点词来补
        used_slugs = {a["slug"] for a in manifest}
        for topic in HOT_TOPICS:
            if needed == 0:
                break
            slug = topic_to_slug(topic)
            if slug in used_slugs:
                continue
            # 强制放入该分类
            print(f"  📦 补充分类「{CATEGORIES[cat]['name']}」: {topic}")
            title, body = generate_article(topic)
            if not title or not body:
                continue
            related = get_related_articles(cat, slug)
            filename = f"{slug}.html"
            html = generate_article_html(title, body, cat, slug, related)
            (OUTPUT_DIR / filename).write_text(html, encoding="utf-8")
            add_to_manifest(slug, title, cat, filename)
            used_slugs.add(slug)
            needed -= 1
            extra_generated += 1
            print(f"  ✅ 补充完成: {filename} → {cat}")
            time.sleep(2)
    if extra_generated > 0:
        print(f"  📊 分类补充分别完成，共补 {extra_generated} 篇")
    return extra_generated


# ==================== Manifest管理 ====================

def load_manifest():
    if MANIFEST_FILE.exists():
        try:
            return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_manifest(manifest):
    OUTPUT_DIR.mkdir(exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def slug_exists(slug):
    return any(a["slug"] == slug for a in load_manifest())


def add_to_manifest(slug, title, category, filename):
    manifest = load_manifest()
    manifest.append({
        "slug": slug,
        "title": title,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "filename": filename,
    })
    save_manifest(manifest)


def get_related_articles(category, current_slug, limit=3):
    manifest = load_manifest()
    related = [a for a in manifest if a["category"] == category and a["slug"] != current_slug]
    related = sorted(related, key=lambda x: x.get("date", ""), reverse=True)[:limit]
    return related


# ==================== HTML生成 ====================

def topic_to_slug(topic):
    h = hashlib.md5(topic.encode()).hexdigest()[:10]
    clean = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", topic)[:15]
    return f"{clean}-{h}"


def _md2html(text):
    """简易markdown转HTML"""
    html = text
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)

    paragraphs = html.split("\n\n")
    result = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<h"):
            result.append(p)
        else:
            lines = p.split("\n")
            p_html = "<br>".join(l.strip() for l in lines if l.strip())
            result.append(f"<p>{p_html}</p>")
    return "\n".join(result)


def _cps_block(category):
    links = CPS_LINKS.get(category, CPS_LINKS["hot"])
    html = '<div class="cps-box"><h3>🛒 猜你也感兴趣</h3><ul>'
    for link in links:
        desc = link.get("desc", "")
        url = link["url"]
        text = link["text"]
        if desc:
            html += f'<li><a href="{url}" target="_blank" rel="nofollow">{text}</a><span class="cps-desc">{desc}</span></li>'
        else:
            html += f'<li><a href="{url}" target="_blank" rel="nofollow">{text}</a></li>'
    html += '</ul></div>'
    return html


def _related_block(related_articles):
    if not related_articles:
        return ""
    html = '<div class="related"><h3>📖 相关推荐</h3><ul>'
    for a in related_articles:
        html += f'<li><a href="/articles/{a["filename"]}">{a["title"]}</a><span class="date">{a.get("date","")}</span></li>'
    html += "</ul></div>"
    return html


def _jsonld_article(title, cat_name, date_iso, slug):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "datePublished": date_iso,
        "dateModified": date_iso,
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
        "description": f"{title},{cat_name}深度解读",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE_URL}/articles/{slug}.html"},
    }, ensure_ascii=False)


def _jsonld_breadcrumb(category, cat_name, title, slug):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页",         "item": SITE_URL},
            {"@type": "ListItem", "position": 2, "name": cat_name,       "item": f"{SITE_URL}/articles/{category}.html"},
            {"@type": "ListItem", "position": 3, "name": title,           "item": f"{SITE_URL}/articles/{slug}.html"},
        ]
    }, ensure_ascii=False)


def generate_article_html(title, body, category, slug, related_articles):
    cat_info = CATEGORIES.get(category, CATEGORIES["hot"])
    cat_name = cat_info["name"]
    cat_icon = cat_info["icon"]
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    html_body = _md2html(body)

    # 在第2个</p>后插入中间广告位
    parts = html_body.split("</p>")
    if len(parts) > 3:
        parts.insert(3, f"</p>\n{AD_CODE_MIDDLE}")
        html_body = "".join(parts)

    json_ld_article = _jsonld_article(title, cat_name, date_iso, slug)
    json_ld_breadcrumb = _jsonld_breadcrumb(category, cat_name, title, slug)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - {SITE_NAME}</title>
<meta name="description" content="{title},{cat_name}深度解读,了解更多请阅读全文。">
<meta name="keywords" content="{title},{cat_name},热点资讯,最新消息,深度解读">
<link rel="canonical" href="{SITE_URL}/articles/{slug}.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{title},{cat_name}深度解读">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE_URL}/articles/{slug}.html">
<meta property="og:site_name" content="{SITE_NAME}">
<meta name="robots" content="index, follow">
<script type="application/ld+json">{json_ld_article}</script>
<script type="application/ld+json">{json_ld_breadcrumb}</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Hiragino Sans GB",sans-serif;line-height:1.8;color:#333;max-width:800px;margin:0 auto;padding:15px;background:#fafafa}}
.header{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:2px solid #ff6b35;margin-bottom:15px}}
.header h1{{font-size:1.1em;color:#ff6b35}}
.header a{{color:#666;text-decoration:none;font-size:.9em}}
.breadcrumb{{font-size:.85em;color:#999;margin-bottom:15px}}
.breadcrumb a{{color:#ff6b35;text-decoration:none}}
.article-title{{font-size:1.6em;font-weight:bold;margin-bottom:8px;color:#1a1a1a;line-height:1.4}}
.meta{{color:#888;font-size:.88em;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid #eee;display:flex;gap:15px;flex-wrap:wrap}}
.meta span{{display:flex;align-items:center;gap:4px}}
h2{{font-size:1.3em;margin:25px 0 10px;color:#2c2c2c;border-left:4px solid #ff6b35;padding-left:10px}}
h3{{font-size:1.1em;margin:20px 0 8px;color:#444}}
p{{margin-bottom:15px;text-align:justify}}
.ad-slot{{margin:20px 0;min-height:90px;text-align:center}}
.cps-box{{background:linear-gradient(135deg,#fff9f0,#fff5e6);border:1px solid #ffe0c0;border-radius:10px;padding:18px;margin:25px 0}}
.cps-box h3{{margin:0 0 12px;font-size:1.05em;color:#d4680a}}
.cps-box ul{{list-style:none;padding:0}}
.cps-box li{{padding:8px 0;border-bottom:1px dashed #ffd9b3;display:flex;justify-content:space-between;align-items:center}}
.cps-box li:last-child{{border-bottom:none}}
.cps-box a{{color:#d4680a;text-decoration:none;font-weight:500;font-size:.95em}}
.cps-box a:hover{{text-decoration:underline}}
.cps-desc{{color:#999;font-size:.82em;margin-left:auto}}
.related{{background:#fff;border:1px solid #eee;border-radius:10px;padding:18px;margin:25px 0}}
.related h3{{margin:0 0 12px;font-size:1.05em;color:#333}}
.related ul{{list-style:none;padding:0}}
.related li{{padding:8px 0;border-bottom:1px solid #f5f5f5;display:flex;justify-content:space-between;align-items:center}}
.related li:last-child{{border-bottom:none}}
.related a{{color:#333;text-decoration:none;flex:1}}
.related a:hover{{color:#ff6b35}}
.related .date{{color:#ccc;font-size:.8em;white-space:nowrap;margin-left:10px}}
.footer{{margin-top:30px;padding-top:15px;border-top:1px solid #eee;text-align:center;color:#aaa;font-size:.82em}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
@media(max-width:600px){{.article-title{{font-size:1.3em}}.meta{{flex-direction:column;gap:5px}}}}
</style>
</head>
<body>
<div class="header">
<h1>📰 {SITE_NAME}</h1>
<a href="/">← 返回首页</a>
</div>
<nav class="breadcrumb">
<a href="/">首页</a> &gt; <a href="/articles/{category}.html">{cat_icon} {cat_name}</a> &gt; {title}
</nav>
<article>
<h1 class="article-title">{title}</h1>
<div class="meta">
<span>📅 {date_str}</span>
<span>{cat_icon} {cat_name}</span>
<span>⏱ 约5分钟</span>
</div>
<div class="ad-slot">{AD_CODE_TOP}</div>
{html_body}
{_cps_block(category)}
{_related_block(related_articles)}
</article>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025 {SITE_NAME} | 内容由AI智能生成仅供参考</p>
<p>
<a href="/">首页</a>
<a href="/articles/hot.html">社会热点</a>
<a href="/articles/tech.html">科技数码</a>
<a href="/articles/health.html">健康养生</a>
<a href="/articles/life.html">生活百科</a>
<a href="/articles/entertainment.html">娱乐八卦</a>
</p>
</div>
</body>
</html>"""
    return html


# ==================== 分类页 ====================

def generate_category_page(category):
    cat_info = CATEGORIES.get(category, CATEGORIES["hot"])
    cat_name = cat_info["name"]
    cat_icon = cat_info["icon"]

    articles = sorted(
        [a for a in load_manifest() if a["category"] == category],
        key=lambda x: x.get("date", ""), reverse=True
    )[:50]

    list_items = "\n".join(
        f'<li><span class="date">{a.get("date","")}</span><a href="/articles/{a["filename"]}">{a["title"]}</a></li>'
        for a in articles
    ) or '<li style="color:#999">暂无文章,敬请期待...</li>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cat_icon} {cat_name} - {SITE_NAME}</title>
<meta name="description" content="{cat_name}最新资讯,每日更新,{cat_name}深度解读。">
<meta name="keywords" content="{cat_name},最新资讯,热点,深度解读">
<link rel="canonical" href="{SITE_URL}/articles/{category}.html">
<meta name="robots" content="index, follow">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC",sans-serif;line-height:1.8;color:#333;max-width:900px;margin:0 auto;padding:15px;background:#fafafa}}
.header{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:2px solid #ff6b35;margin-bottom:15px}}
.header h1{{font-size:1.1em;color:#ff6b35}}
.header a{{color:#666;text-decoration:none;font-size:.9em}}
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
<a href="/">← 返回首页</a>
</div>
<nav class="breadcrumb">
<a href="/">首页</a> &gt; {cat_icon} {cat_name}
</nav>
<h2 class="cat-title">{cat_icon} {cat_name}</h2>
<div class="ad-slot">{AD_CODE_TOP}</div>
<ul>
{list_items}
</ul>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025 {SITE_NAME}</p>
<p>
<a href="/">首页</a>
<a href="/articles/hot.html">社会热点</a>
<a href="/articles/tech.html">科技数码</a>
<a href="/articles/health.html">健康养生</a>
<a href="/articles/life.html">生活百科</a>
<a href="/articles/entertainment.html">娱乐八卦</a>
</p>
</div>
</body>
</html>"""
    return html


# ==================== 首页 ====================

def rebuild_index():
    manifest = load_manifest()
    if not manifest:
        print("  首页:暂无文章")
        return

    articles = sorted(manifest, key=lambda x: x.get("date", ""), reverse=True)[:100]
    list_items = "\n".join(
        f'<li><span class="date">{a.get("date","")}</span>'
        f'<span class="cat">[{CATEGORIES.get(a["category"],CATEGORIES["hot"])["name"]}]</span>'
        f'<a href="/articles/{a["filename"]}">{a["title"]}</a></li>'
        for a in articles
    )

    cat_links = "\n".join(
        f'<a href="/articles/{k}.html" class="cat-link">{v["icon"]} {v["name"]}</a>'
        for k, v in CATEGORIES.items()
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{SITE_NAME} - {SITE_DESC}</title>
<meta name="description" content="{SITE_DESC}">
<meta name="keywords" content="今日热点,热搜,最新消息,社会新闻,科技资讯,健康养生,生活百科,娱乐八卦">
<link rel="canonical" href="{SITE_URL}/">
<meta property="og:title" content="{SITE_NAME}">
<meta property="og:description" content="{SITE_DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:site_name" content="{SITE_NAME}">
<meta name="robots" content="index, follow">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC",sans-serif;line-height:1.8;color:#333;max-width:900px;margin:0 auto;padding:15px;background:#fafafa}}
.site-header{{text-align:center;padding:25px 0 20px}}
.site-header h1{{font-size:1.8em;color:#1a1a1a;margin-bottom:5px}}
.site-header p{{color:#888;font-size:.95em}}
.cat-nav{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:15px 0 25px;padding:15px;background:#fff;border-radius:10px;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.cat-link{{padding:6px 16px;border-radius:20px;background:#fff5ed;color:#d4680a;text-decoration:none;font-size:.9em;font-weight:500;border:1px solid #ffe0c0}}
.cat-link:hover{{background:#ff6b35;color:#fff;border-color:#ff6b35}}
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
<nav class="cat-nav">
{cat_links}
</nav>
<div class="ad-slot">{AD_CODE_TOP}</div>
<ul>
{list_items}
</ul>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025 {SITE_NAME} | AI智能聚合,每日多次更新</p>
<p>
<a href="/">首页</a>
<a href="/articles/hot.html">社会热点</a>
<a href="/articles/tech.html">科技数码</a>
<a href="/articles/health.html">健康养生</a>
<a href="/articles/life.html">生活百科</a>
<a href="/articles/entertainment.html">娱乐八卦</a>
</p>
</div>
</body>
</html>"""

    INDEX_FILE.write_text(html, encoding="utf-8")
    print(f"  首页已更新,展示 {len(articles)} 篇")


# ==================== Sitemap ====================

def rebuild_sitemap():
    manifest = load_manifest()
    urls = [f'<url><loc>{SITE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>']
    for cat in CATEGORIES:
        urls.append(f'<url><loc>{SITE_URL}/articles/{cat}.html</loc><changefreq>daily</changefreq><priority>0.8</priority></url>')
    for a in manifest:
        urls.append(f'<url><loc>{SITE_URL}/articles/{a["filename"]}</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>')

    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{"".join(urls)}\n</urlset>'
    SITEMAP_FILE.write_text(sitemap, encoding="utf-8")
    print(f"  Sitemap已更新,共 {len(urls)} 条URL")


# ==================== 主流程 ====================

def main():
    if not API_KEY:
        print("❌ 未设置 ZHIPU_API_KEY 环境变量")
        return

    print(f"🚀 内容生成器 v2.0 启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1. 抓热点
    topics = get_hot_topics()
    print(f"📋 本轮话题: {topics}")

    # 2. 逐篇生成
    generated = 0
    for i, topic in enumerate(topics):
        slug = topic_to_slug(topic)
        if slug_exists(slug):
            print(f"  ⏭ 跳过重复: {topic}")
            continue

        print(f"  ✍️ [{i+1}/{len(topics)}] 生成: {topic}")
        category = classify_topic(topic)
        title, body = generate_article(topic)

        if not title or not body:
            print(f"  ❌ 生成失败: {topic}")
            continue

        related = get_related_articles(category, slug)
        filename = f"{slug}.html"
        html = generate_article_html(title, body, category, slug, related)
        (OUTPUT_DIR / filename).write_text(html, encoding="utf-8")
        add_to_manifest(slug, title, category, filename)

        generated += 1
        print(f"  ✅ 已生成: {filename}")

        # 避免API限流
        if i < len(topics) - 1:
            time.sleep(2)

    # 3. 重建站点
    if generated > 0:
        print("\n📐 重建站点页面...")
        rebuild_index()
        for cat in CATEGORIES:
            (OUTPUT_DIR / f"{cat}.html").write_text(generate_category_page(cat), encoding="utf-8")
        rebuild_sitemap()

    # 4. 分类兜底（每个分类至少2篇）
    extra = ensure_category_balance()
    if extra > 0:
        print("\n📐 补充后重建站点...")
        rebuild_index()
        for cat in CATEGORIES:
            (OUTPUT_DIR / f"{cat}.html").write_text(generate_category_page(cat), encoding="utf-8")
        rebuild_sitemap()

    print(f"\n🏁 完成!本次生成 {generated} 篇新文章,补充 {extra} 篇兜底文章")


if __name__ == "__main__":
    main()
