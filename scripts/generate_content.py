# -*- coding: utf-8 -*-
"""
全自动双语热点流量站内容生成器 v4.0
================================
中英双语 | 多源热点 | AI高质量原创 | 内链网络 | 结构化数据 | AdSense+Amazon变现
版本更新: v4.0 - 大幅提升内容质量,去除AI套话,强制数据支撑
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

# Agnes AI 图片生成(完全免费)
AGNES_API_KEY = os.environ.get("AGNES_API_KEY", "")
AGNES_API_URL = "https://apihub.agnes-ai.com/v1/images/generations"
AGNES_MODEL = "agnes-image-2.1-flash"

ARTICLES_PER_RUN = 8  # 每次生成20个话题,每个话题中英文各一篇 = 40篇

# SEO Ping服务
PING_SERVICES = [
    "http://ping.baidu.com/ping/RPC2",
    "http://rpc.weblogs.com/RPC2",
]

# 中文站点
OUTPUT_DIR = Path("articles")
MANIFEST_FILE = OUTPUT_DIR / "manifest.json"
SITE_NAME = "孤岛财经"
SITE_URL = "https://gudaoqihuo.com"
SITE_DESC = "孤岛财经 - AI聚合全球股票、期货、币圈与AI金融资讯"

# 英文站点
EN_OUTPUT_DIR = Path("en/articles")
EN_MANIFEST_FILE = EN_OUTPUT_DIR / "manifest.json"
EN_SITE_NAME = "GuDu Finance"
EN_SITE_URL = "https://gudaoqihuo.com"
EN_SITE_DESC = "GuDu Finance - AI-powered global market insights & investment knowledge"

INDEX_FILE = Path("index.html")
EN_INDEX_FILE = Path("en/index.html")
SITEMAP_FILE = Path("sitemap.xml")

# GA4 追踪代码
GA4_ID = "G-XE3F4GQQM5"
GA4_CODE = f'''<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{GA4_ID}');
</script>'''

# 中文分类
CATEGORIES = {
    "finance":      {"name": "财经投资",   "icon": "📈"},
    "hot":          {"name": "社会热点",   "icon": "🔥"},
    "tech":         {"name": "科技数码",   "icon": "📱"},
    "health":       {"name": "健康养生",   "icon": "🏥"},
    "life":         {"name": "生活百科",   "icon": "💡"},
    "entertainment":{"name": "娱乐八卦",   "icon": "🎬"},
}

# 英文分类
EN_CATEGORIES = {
    "finance":      {"name": "Finance",      "icon": "📈"},
    "hot":          {"name": "Trending",     "icon": "🔥"},
    "tech":         {"name": "Tech",         "icon": "📱"},
    "health":       {"name": "Health",       "icon": "🏥"},
    "life":         {"name": "Lifestyle",    "icon": "💡"},
    "entertainment":{"name": "Entertainment","icon": "🎬"},
}

# Category thumbnail colors
THUMB_COLORS = {
    "finance": "#1a73e8",
    "hot": "#ff6b35",
    "tech": "#7c3aed",
    "health": "#10b981",
    "life": "#f59e0b",
    "entertainment": "#ec4899",
}

# 中文CPS推广链接(亚马逊)
# 拼多多CPS推广链接(PID: 39923394_315955963)
PDD_LINK = {"text": "百亿补贴×春夏服饰狂欢", "url": "https://p.pinduoduo.com/1SQ3UtrO?sc=EFAC", "desc": "换季特惠5折起"}
# 京东联盟推广链接
JD_LINK = {"text": "京东好物特惠", "url": "https://u.jd.com/HOm83O5", "desc": "品质保障"}

# 中文CPS推广链接(亚马逊+拼多多)
CPS_LINKS = {
    "tech": [
        {"text": "2025高性价比手机推荐", "url": "https://www.amazon.cn/gp/bestsellers/electronics?tag=gudaoqihuo-20", "desc": "热销数码"},
    ],
    "health": [
        {"text": "养生保健精选好物", "url": "https://www.amazon.cn/s?k=养生&tag=gudaoqihuo-20", "desc": "健康生活"},
    ],
    "life": [
        {"text": "居家好物省钱攻略", "url": "https://www.amazon.cn/s?k=居家好物&tag=gudaoqihuo-20", "desc": "品质生活"},
    ],
    "entertainment": [
        {"text": "热门影视周边好物", "url": "https://www.amazon.cn/s?k=影视周边&tag=gudaoqihuo-20", "desc": "追剧必备"},
    ],
    "hot": [
        {"text": "今日热搜相关好物", "url": "https://www.amazon.cn/?tag=gudaoqihuo-20", "desc": "发现更多"},
    ],
}

# 财经分类CPS推广链接
CPS_LINKS["finance"] = [
    {"text": "理财入门必读书籍", "url": "https://www.amazon.cn/s?k=理财书籍&tag=gudaoqihuo-20", "desc": "财商提升"},
]

# 英文CPS推广链接(Amazon.com)
EN_CPS_LINKS = {
    "tech": [
        {"text": "Best Selling Electronics 2025", "url": "https://www.amazon.com/gp/bestsellers/electronics?tag=gudaoqihuo-20", "desc": "Top Rated"},
    ],
    "health": [
        {"text": "Health & Wellness Picks", "url": "https://www.amazon.com/s?k=health+wellness&tag=gudaoqihuo-20", "desc": "Stay Healthy"},
    ],
    "life": [
        {"text": "Home Essentials", "url": "https://www.amazon.com/s?k=home+essentials&tag=gudaoqihuo-20", "desc": "Quality Living"},
    ],
    "entertainment": [
        {"text": "Movie & TV Merchandise", "url": "https://www.amazon.com/s?k=movie+merchandise&tag=gudaoqihuo-20", "desc": "Fan Favorites"},
    ],
    "hot": [
        {"text": "Today's Deals", "url": "https://www.amazon.com/gp/goldbox?tag=gudaoqihuo-20", "desc": "Limited Time"},
    ],
}

EN_CPS_LINKS["finance"] = [
    {"text": "Finance & Investment Books", "url": "https://www.amazon.com/s?k=finance+books&tag=gudaoqihuo-20", "desc": "Money Smart"},
]

# 广告位配置(中英文共用)
AD_CODE_TOP = '''<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-client="ca-pub-9935054113253833" data-ad-slot="4353278167" data-ad-format="fluid" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

AD_CODE_MIDDLE = '''<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-client="ca-pub-9935054113253833" data-ad-slot="4353278167" data-ad-format="fluid" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

AD_CODE_BOTTOM = '''<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9935054113253833" data-ad-slot="4353278167" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

# ==================== 免费图片源(多级降级)====================
# 优先级:Unsplash -> Pixabay -> Lorem Picsum -> SVG兜底
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY', '')
PIXABAY_API_KEY = os.environ.get('PIXABAY_API_KEY', '')  # 可选,不填也能用

# 分类关键词映射(用于图片搜索)
CATEGORY_IMAGE_KEYWORDS = {
    'finance': ['stock market', 'money', 'investment', 'business chart'],
    'hot': ['breaking news', 'world news', 'crowd', 'city'],
    'tech': ['technology', 'computer', 'AI artificial intelligence', 'smartphone'],
    'health': ['health', 'medical', 'wellness', 'fitness'],
    'life': ['lifestyle', 'home', 'travel', 'food'],
    'entertainment': ['entertainment', 'concert', 'movie', 'music'],
}

# 中文关键词快速翻译(用于图片搜索)
ZH_TO_EN_KEYWORDS = {
    '科技': 'technology', '人工智能': 'AI', '财经': 'finance', '股市': 'stock market',
    '健康': 'health', '娱乐': 'entertainment', '社会': 'society', '教育': 'education',
    '手机': 'smartphone', '经济': 'economy', '互联网': 'internet', '新能源': 'new energy',
    '房地产': 'real estate', '体育': 'sports', '环境': 'environment', '医疗': 'medical',
    '苹果': 'Apple iPhone', '华为': 'Huawei', '特斯拉': 'Tesla', '电动车': 'electric car',
    '芯片': 'semiconductor chip', '机器人': 'robot', '元宇宙': 'metaverse VR',
    '房价': 'housing prices', '基金': 'investment fund', '比特币': 'Bitcoin crypto',
    '高考': 'students exam', '教师': 'teacher classroom', '养老': 'elderly care',
}

def _get_image_query(topic, category, lang):
    """根据话题和分类生成英文搜索关键词"""
    query = topic[:50] if len(topic) > 3 else ''
    if lang == 'zh' and query:
        for zh_word, en_word in sorted(ZH_TO_EN_KEYWORDS.items(), key=lambda x: -len(x[0])):
            if zh_word in topic:
                query = en_word
                break
    if not query or len(query) < 3:
        keywords = CATEGORY_IMAGE_KEYWORDS.get(category, CATEGORY_IMAGE_KEYWORDS['hot'])
        query = random.choice(keywords)
    return query


def _try_unsplash(query):
    """尝试从Unsplash获取图片URL"""
    if not UNSPLASH_ACCESS_KEY:
        return None
    try:
        headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
        params = {'query': query, 'w': 800, 'h': 400, 'fit': 'crop', 'per_page': 1}
        resp = requests.get('https://api.unsplash.com/search/photos', headers=headers, params=params, timeout=10)
        if resp.status_code == 200 and resp.json().get('results'):
            url = resp.json()['results'][0]['urls']['regular']
            print(f'    [Unsplash] OK: {query}')
            return url
        resp2 = requests.get('https://api.unsplash.com/photos/random', headers=headers, params={'w': 800, 'h': 400, 'fit': 'crop'}, timeout=10)
        if resp2.status_code == 200:
            url = resp2.json()['urls']['regular']
            print(f'    [Unsplash] Random OK')
            return url
    except Exception as e:
        print(f'    [Unsplash] Failed: {e}')
    return None


def _try_picsum():
    """Lorem Picsum - 完全免费无需认证的随机图片(直接返回URL,不验证)"""
    seed = random.randint(1, 100000)
    url = f'https://picsum.photos/seed/{seed}/800/400'
    print(f'    [Picsum] Using (seed={seed})')
    return url


def _try_agnes(topic, lang='zh'):
    """Agnes AI 文生图 - 完全免费,根据文章主题生成匹配图片"""
    if not AGNES_API_KEY:
        return None
    try:
        # 根据主题生成英文prompt(Agnes对英文支持更好)
        prompt = _get_image_query(topic, '', lang)
        if len(prompt) > 200:
            prompt = prompt[:200]
        resp = requests.post(
            AGNES_API_URL,
            headers={
                'Authorization': f'Bearer {AGNES_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': AGNES_MODEL,
                'prompt': prompt,
                'size': '1024x512'
            },
            timeout=60
        )
        if resp.status_code == 200:
            data = resp.json()
            url = data.get('data', [{}])[0].get('url')
            if url:
                print(f'    [Agnes AI] Generated image for: {topic[:30]}...')
                return url
    except Exception as e:
        print(f'    [Agnes AI] Failed: {e}')
    return None


def fetch_unsplash_image(topic, category='hot', lang='zh'):
    """多级降级获取封面图片:Agnes AI -> Unsplash -> Picsum -> None(SVG兜底)"""
    query = _get_image_query(topic, category, lang)

    # Level 1: Agnes AI 文生图(完全免费,根据主题生成)
    url = _try_agnes(topic, lang)
    if url:
        return url

    # Level 2: Unsplash
    url = _try_unsplash(query)
    if url:
        return url

    # Level 3: Lorem Picsum (100%可用,无需认证,GitHub Actions可访问)
    url = _try_picsum()
    if url:
        return url

    print(f'    [Image] All sources failed, using SVG fallback')
    return None

def get_cover_image(topic, category, lang='zh', existing_url=None):
    """获取封面图片:优先用已有URL,否则调Unsplash API"""
    if existing_url:
        return existing_url
    return fetch_unsplash_image(topic, category, lang)

# 文章头图SVG模板(按分类)
SVG_HERO_TEMPLATES = {
    "finance": {
        "gradient": ["#FF8C00", "#FFD700", "#FFA500"],
        "icon_svg": '<path d="M30 70 L50 50 L60 60 L80 30" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="30" cy="70" r="3" fill="rgba(255,255,255,0.7)"/><circle cx="50" cy="50" r="3" fill="rgba(255,255,255,0.7)"/><circle cx="60" cy="60" r="3" fill="rgba(255,255,255,0.7)"/><circle cx="80" cy="30" r="3" fill="rgba(255,255,255,0.7)"/><polygon points="75,28 83,28 80,22" fill="rgba(255,255,255,0.8)"/>',
        "pattern": '<line x1="0" y1="90" x2="300" y2="90" stroke="rgba(255,255,255,0.08)" stroke-width="1"/><line x1="0" y1="60" x2="300" y2="60" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>',
    },
    "hot": {
        "gradient": ["#FF4444", "#FF6B35", "#FF8C42"],
        "icon_svg": '<path d="M55 25 C55 25 70 45 70 55 C70 63 63 70 55 70 C50 70 46 67 45 63 C44 67 40 70 35 70 C27 70 20 63 20 55 C20 45 35 25 35 25 C35 25 42 35 42 42" stroke="rgba(255,255,255,0.9)" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
        "pattern": '<circle cx="50" cy="20" r="8" fill="rgba(255,255,255,0.06)"/><circle cx="250" cy="70" r="12" fill="rgba(255,255,255,0.04)"/>',
    },
    "tech": {
        "gradient": ["#0066FF", "#0099FF", "#00D4FF"],
        "icon_svg": '<rect x="40" y="35" width="30" height="40" rx="3" stroke="rgba(255,255,255,0.9)" stroke-width="2" fill="none"/><line x1="48" y1="72" x2="62" y2="72" stroke="rgba(255,255,255,0.7)" stroke-width="2" stroke-linecap="round"/><circle cx="55" cy="42" r="2" fill="rgba(255,255,255,0.6)"/><path d="M25 50 L35 50 M75 50 L85 50 M55 20 L55 30 M55 75 L55 80" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-linecap="round"/>',
        "pattern": '<circle cx="200" cy="30" r="20" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/><circle cx="220" cy="50" r="15" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>',
    },
    "health": {
        "gradient": ["#2ECC71", "#27AE60", "#1ABC9C"],
        "icon_svg": '<path d="M55 40 C55 32 62 28 67 33 C72 38 67 48 55 58 C43 48 38 38 43 33 C48 28 55 32 55 40Z" fill="rgba(255,255,255,0.85)"/>',
        "pattern": '<circle cx="40" cy="60" r="6" fill="rgba(255,255,255,0.06)"/><circle cx="260" cy="40" r="4" fill="rgba(255,255,255,0.05)"/>',
    },
    "life": {
        "gradient": ["#F39C12", "#E67E22", "#D35400"],
        "icon_svg": '<path d="M55 25 L60 45 L80 45 L64 57 L70 77 L55 65 L40 77 L46 57 L30 45 L50 45Z" fill="rgba(255,255,255,0.85)"/>',
        "pattern": '<rect x="150" y="15" width="8" height="8" rx="1" transform="rotate(30 154 19)" fill="rgba(255,255,255,0.05)"/>',
    },
    "entertainment": {
        "gradient": ["#9B59B6", "#E91E63", "#FF5722"],
        "icon_svg": '<rect x="35" y="30" width="40" height="30" rx="3" stroke="rgba(255,255,255,0.9)" stroke-width="2" fill="none"/><path d="M35 33 L55 45 L75 33" stroke="rgba(255,255,255,0.7)" stroke-width="2" fill="none"/><line x1="48" y1="30" x2="48" y2="25" stroke="rgba(255,255,255,0.6)" stroke-width="2" stroke-linecap="round"/><line x1="55" y1="30" x2="55" y2="22" stroke="rgba(255,255,255,0.6)" stroke-width="2" stroke-linecap="round"/><line x1="62" y1="30" x2="62" y2="25" stroke="rgba(255,255,255,0.6)" stroke-width="2" stroke-linecap="round"/>',
        "pattern": '<polygon points="200,15 203,22 210,22 204,27 206,34 200,30 194,34 196,27 190,22 197,22" fill="rgba(255,255,255,0.06)"/>',
    },
}

def generate_svg_hero(title, category, lang="zh"):
    """生成文章头图SVG"""
    cat_key = category if category in SVG_HERO_TEMPLATES else "hot"
    tmpl = SVG_HERO_TEMPLATES[cat_key]
    g = tmpl["gradient"]
    if lang == "zh":
        display_title = title[:28] + ("..." if len(title) > 28 else "")
    else:
        display_title = title[:38] + ("..." if len(title) > 38 else "")
    display_title = display_title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    cat_info = CATEGORIES.get(category, CATEGORIES["hot"]) if lang == "zh" else EN_CATEGORIES.get(category, EN_CATEGORIES["hot"])
    cat_name = cat_info["name"]
    cat_icon = cat_info["icon"]
    site_label = SITE_NAME if lang == "zh" else EN_SITE_NAME
    date_label = datetime.now().strftime("%Y-%m-%d")
    svg = (
        '<div class="hero-svg"><svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">'
        '<defs><linearGradient id="hg" x1="0%" y1="0%" x2="100%" y2="100%">'
        '<stop offset="0%" style="stop-color:' + g[0] + '"/>'
        '<stop offset="50%" style="stop-color:' + g[1] + '"/>'
        '<stop offset="100%" style="stop-color:' + g[2] + '"/>'
        '</linearGradient>'
        '<filter id="glow"><feGaussianBlur stdDeviation="2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '</defs>'
        '<rect width="800" height="280" fill="url(#hg)"/>'
        '<circle cx="680" cy="60" r="120" fill="rgba(255,255,255,0.04)"/>'
        '<circle cx="720" cy="200" r="80" fill="rgba(255,255,255,0.03)"/>'
        '<circle cx="100" cy="240" r="60" fill="rgba(255,255,255,0.03)"/>'
        + tmpl["pattern"]
        + '<g transform="translate(620,80) scale(1.8)" filter="url(#glow)">' + tmpl["icon_svg"] + '</g>'
        + f'<text x="40" y="70" font-size="14" fill="rgba(255,255,255,0.7)" font-family="-apple-system,sans-serif" font-weight="500">{cat_icon} {cat_name}</text>'
        + f'<text x="40" y="135" font-size="30" fill="white" font-family="-apple-system,sans-serif" font-weight="700">{display_title}</text>'
        '<line x1="40" y1="158" x2="200" y2="158" stroke="rgba(255,255,255,0.4)" stroke-width="3" stroke-linecap="round"/>'
        + f'<text x="40" y="190" font-size="13" fill="rgba(255,255,255,0.6)" font-family="-apple-system,sans-serif">{site_label} {chr(183)} {date_label}</text>'
        '</svg></div>'
    )
    return svg

# 财经免责声明
FINANCE_DISCLAIMER_ZH = '''<div style="background:linear-gradient(135deg,#fff8f0,#fff3e0);border:1px solid #ffcc80;border-radius:8px;padding:14px 18px;margin:25px 0;font-size:.88em;color:#8d6e63;line-height:1.7">
⚠️ <strong>免责声明</strong><br>
本频道所有内容仅供参考和学习交流之用,不构成任何投资建议、交易指导或财务顾问意见。市场有风险,投资需谨慎。文中提及的股票、基金、数字货币、大宗商品等金融产品,均不构成买入、卖出或持有的推荐。投资者应根据自身风险承受能力独立判断,并自行承担投资风险。过往表现不代表未来收益。如需专业投资建议,请咨询持牌金融机构。本站及作者对任何因参考本文内容而造成的直接或间接损失不承担任何责任。
</div>'''

FINANCE_DISCLAIMER_EN = '''<div style="background:linear-gradient(135deg,#fff8f0,#fff3e0);border:1px solid #ffcc80;border-radius:8px;padding:14px 18px;margin:25px 0;font-size:.88em;color:#8d6e63;line-height:1.7">
⚠️ <strong>Disclaimer</strong><br>
All content in this section is for informational and educational purposes only and does not constitute investment advice, trading guidance, or financial advisory services. Market involves risk; invest with caution. Stocks, funds, cryptocurrencies, commodities, and other financial instruments mentioned herein do not constitute recommendations to buy, sell, or hold. Investors should make independent judgments based on their own risk tolerance and bear their own investment risks. Past performance does not guarantee future results. For professional investment advice, please consult a licensed financial institution. This site and its authors accept no liability for any direct or indirect losses resulting from reliance on content published herein.
</div>'''

# 备用常青话题(AI+金融偏向)
FALLBACK_TOPICS = [
    # AI+金融方向
    "AI概念股投资机会", "大模型厂商财报分析", "英伟达产业链投资", "DeepSeek对金融市场影响",
    "量化交易策略入门", "智能投顾发展趋势", "数字人民币应用场景", "AI赋能金融科技",
    "AI芯片股配置逻辑", "算力概念股投资分析", "金融AI大模型应用", "FinTech人工智能前沿",
    # 科技数码
    "人工智能发展趋势", "AI手机怎么选", "大模型应用实测", "智能穿戴设备",
    # 生活健康
    "健康养生小知识", "职场生存指南", "理财投资入门",
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
        return [item.get("Title", "") for item in data.get("data", []) if item.get("Title")][:50]
    except: return []

def fetch_zhihu_hot():
    print("    抓取知乎热榜...")
    resp = fetch_with_retry("https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total")
    if not resp: return []
    try:
        data = resp.json()
        return [item.get("target", {}).get("title", "") for item in data.get("data", []) if item.get("target", {}).get("title")][:30]
    except: return []

def fetch_finance_hot():
    print("    抓取财经热点...")
    # 东方财富热门话题
    sources = []
    try:
        resp = fetch_with_retry("https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f12,f14&_=1")
        if resp:
            text = resp.text
            # 提取股票名称
            names = re.findall(r'"f14":"([^"]+)"', text)
            topics = [f"{n}股票" for n in names if n][:10]
            sources.extend(topics)
    except: pass
    # 全球热门股票与大宗商品点评
    global_market_topics = [
        "特斯拉股价最新动态", "苹果公司财报分析", "英伟达AI芯片市场前景",
        "微软市值走势分析", "谷歌AI战略布局",
        "阿里巴巴港股走势", "腾讯控股投资价值分析", "比亚迪新能源汽车市场",
        "贵州茅台股价点评", "中国平安投资策略",
        "黄金价格走势与避险情绪", "原油价格分析OPEC产量",
        "比特币以太坊行情分析", "铜价走势与新能源需求",
        "美联储利率决议影响", "人民币对美元汇率",
    ]
    sources.extend(global_market_topics)
    # 补充财经固定热点词(AI+金融垂直偏向)
    finance_keywords = [
        "AI概念股投资机会", "大模型厂商财报", "英伟达产业链分析", "DeepSeek概念股",
        "算力概念股行情", "AI芯片板块走势", "金融AI大模型应用", "智能投顾发展趋势",
        "量化交易策略动态", "数字货币行情", "比特币以太坊走势", "AI赋能券商概念",
        "科技股最新动态", "新能源汽车板块", "半导体行业分析", "美联储加息",
        "人民币汇率走势", "黄金价格走势", "A股大盘分析", "科创板AI公司",
        "AI+金融跨界投资", "FinTech人工智能前沿", "数字人民币最新进展",
    ]
    sources.extend(finance_keywords)
    # 去重
def fetch_sohu_hot():
    """搜狐新闻热点"""
    print("    抓取搜狐新闻...")
    try:
        resp = fetch_with_retry("https://www.sohu.com/", timeout=15)
        if not resp: return []
        titles = re.findall(r'<h3[^>]*>(.*?)</h3>', resp.text, re.DOTALL)
        titles = [re.sub(r'<.*?>', '', t).strip() for t in titles if 4 < len(t) < 120]
        return list(set(titles))[:25]
    except: return []

def fetch_163_hot():
    """网易新闻热点"""
    print("    抓取网易新闻...")
    try:
        resp = fetch_with_retry("https://news.163.com/rank/", timeout=15)
        if not resp: return []
        titles = re.findall(r'<a[^>]*>([一-鿿][^<]{3,40})</a>', resp.text)
        return list(set(titles))[:25]
    except: return []

def fetch_qq_hot():
    """腾讯新闻热点"""
    print("    抓取腾讯新闻...")
    try:
        resp = fetch_with_retry("https://news.qq.com/", timeout=15)
        if not resp: return []
        titles = re.findall(r'"title":"([^"]{4,80})"', resp.text)
        return list(set(titles))[:25]
    except: return []

def fetch_sina_hot():
    """新浪新闻热点"""
    print("    抓取新浪新闻...")
    try:
        resp = fetch_with_retry("https://news.sina.com.cn/", timeout=15)
        if not resp: return []
        titles = re.findall(r'<a[^>]+href[^>]*>([^<]{4,60})</a>', resp.text)
        return list(set(titles))[:25]
    except: return []

def fetch_thepaper_hot():
    """澎湃新闻热点"""
    print("    抓取澎湃新闻...")
    try:
        resp = fetch_with_retry("https://www.thepaper.cn/", timeout=15)
        if not resp: return []
        titles = re.findall(r'"name":"([^"]{4,60})"', resp.text)
        return list(set(titles))[:25]
    except: return []

def fetch_cctv_hot():
    """央视新闻热点"""
    print("    抓取央视新闻...")
    try:
        resp = fetch_with_retry("https://news.cctv.com/", timeout=15)
        if not resp: return []
        titles = re.findall(r'"title":"([^"]{4,80})"', resp.text)
        return list(set(titles))[:25]
    except: return []

def fetch_36kr_hot():
    """36氪科技热点"""
    print("    抓取36氪...")
    try:
        resp = fetch_with_retry("https://36kr.com/newsflashes", timeout=15)
        if not resp: return []
        titles = re.findall(r'"title":"([^"]{4,100})"', resp.text)
        return list(set(titles))[:25]
    except: return []

def fetch_huxiu_hot():
    """虎嗅商业热点"""
    print("    抓取虎嗅...")
    try:
        resp = fetch_with_retry("https://www.huxiu.com/", timeout=15)
        if not resp: return []
        titles = re.findall(r'<h[2-5][^>]*>.*?<a[^>]*>([^<]+)</a>', resp.text, re.DOTALL)
        if not titles:
            titles = re.findall(r'"title":"([^"]{4,100})"', resp.text)
        return list(set(titles))[:25]
    except: return []
    seen = set()
    unique = []
    for t in sources:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique[:25]

def get_hot_topics():
    print("📡 开始抓取热点话题...")
    all_topics = []
    sources = [fetch_baidu_hot, fetch_weibo_hot, fetch_toutiao_hot, fetch_zhihu_hot, fetch_finance_hot, fetch_sohu_hot, fetch_163_hot, fetch_qq_hot, fetch_sina_hot, fetch_thepaper_hot, fetch_cctv_hot, fetch_36kr_hot, fetch_huxiu_hot]
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

    # === 强制分类比例: 财经50% + 科技20% + 其他30% ===
    finance_topics = [t for t in unique if classify_topic(t) == "finance"]
    tech_topics = [t for t in unique if classify_topic(t) == "tech"]
    other_topics = [t for t in unique if classify_topic(t) not in ("finance", "tech")]

    target_finance = max(4, ARTICLES_PER_RUN // 2)  # 至少4篇财经
    target_tech = max(2, ARTICLES_PER_RUN // 5)     # 至少2篇科技
    target_other = ARTICLES_PER_RUN - target_finance - target_tech

    # 财经不足时从FALLBACK补充
    if len(finance_topics) < target_finance:
        extra_finance = [t for t in FALLBACK_TOPICS if t not in seen and classify_topic(t) == "finance"]
        random.shuffle(extra_finance)
        finance_topics.extend(extra_finance[:target_finance - len(finance_topics)])
        print(f"  财经热点不足,补充常青话题到 {len(finance_topics)} 条")

    selected = []
    selected.extend(finance_topics[:target_finance])
    selected.extend(tech_topics[:target_tech])
    remaining = [t for t in other_topics if t not in selected]
    selected.extend(remaining[:target_other])

    # 如果还不够,从所有话题补
    if len(selected) < ARTICLES_PER_RUN:
        need = ARTICLES_PER_RUN - len(selected)
        pool = [t for t in unique if t not in selected and t not in seen]
        selected.extend(pool[:need])

    random.shuffle(selected)
    print(f"  分类分布: 财经{sum(1 for t in selected if classify_topic(t)=='finance')} 科技{sum(1 for t in selected if classify_topic(t)=='tech')} 其他{sum(1 for t in selected if classify_topic(t) not in ('finance','tech'))}")
    return selected[:ARTICLES_PER_RUN]

def fetch_bbc_hot():
    """BBC News热点"""
    print("    抓取BBC News...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}
        resp = fetch_with_retry("https://www.bbc.com/news", headers=headers, timeout=15)
        if not resp: return []
        titles = re.findall(r'<h3[^>]*>([^<]{8,120})</h3>', resp.text)
        return list(set(titles))[:20]
    except: return []
def fetch_reuters_hot():
    """Reuters热点"""
    print("    抓取Reuters...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}
        resp = fetch_with_retry("https://www.reuters.com/", headers=headers, timeout=15)
        if not resp: return []
        titles = re.findall(r'<h[2-4][^>]*>.*?<a[^>]*>([^<]{6,150})</a>', resp.text, re.DOTALL)
        return list(set(titles))[:20]
    except: return []
def fetch_cnn_hot():
    """CNN热点"""
    print("    抓取CNN...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}
        resp = fetch_with_retry("https://www.cnn.com/", headers=headers, timeout=15)
        if not resp: return []
        titles = re.findall(r'"headline":"([^"]{6,150})"', resp.text)
        return list(set(titles))[:20]
    except: return []
def fetch_guardian_hot():
    """Guardian热点"""
    print("    抓取Guardian...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}
        resp = fetch_with_retry("https://www.theguardian.com/international", headers=headers, timeout=15)
        if not resp: return []
        titles = re.findall(r'<h[2-4][^>]*>([^<]{8,150})</h[2-4]>', resp.text)
        return list(set(titles))[:20]
    except: return []
def fetch_ap_hot():
    """AP News热点"""
    print("    抓取AP News...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}
        resp = fetch_with_retry("https://apnews.com/", headers=headers, timeout=15)
        if not resp: return []
        titles = re.findall(r'<h[2-3][^>]*>.*?<a[^>]*>([^<]+)</a>', resp.text, re.DOTALL)
        if not titles:
            titles = re.findall(r'"headline":"([^"]{6,150})"', resp.text)
        return list(set(titles))[:20]
    except: return []
def fetch_google_news_hot():
    """Google News热点"""
    print("    抓取Google News...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}
        resp = fetch_with_retry("https://news.google.com/home?hl=en-US&gl=US&ceid=US:en", headers=headers, timeout=15)
        if not resp: return []
        titles = re.findall(r'<h[3-5][^>]*>([^<]{6,150})</h[3-5]>', resp.text)
        if not titles:
            titles = re.findall(r'aria-label="([^"]{8,120})"', resp.text)
        return list(set(titles))[:20]
    except: return []
def get_hot_topics_en():
    """英文热点抓取:Reddit + Hacker News + Twitter(Trends24)"""
    print("[EN] 开始抓取英文热点话题...")
    all_topics = []

    # Reddit热点 (r/all/hot)
    print("    抓取Reddit热点...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}
        resp = fetch_with_retry("https://www.reddit.com/r/all/hot.json?limit=30", headers=headers, timeout=15)
        if resp:
            data = resp.json()
            posts = data.get("data", {}).get("children", [])
            topics = [p.get("data", {}).get("title", "") for p in posts if p.get("data", {}).get("title")]
            all_topics.extend(topics[:30])
            print(f"    Reddit: 获取 {len(topics)} 条")
    except Exception as e:
        print(f"    Reddit热点异常: {e}")

    # Hacker News热点
    print("    抓取Hacker News热点...")
    try:
        resp = fetch_with_retry("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=15)
        if resp:
            story_ids = resp.json()[:15]
            topics = []
            for sid in story_ids:
                s_resp = fetch_with_retry(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10)
                if s_resp:
                    s_data = s_resp.json()
                    title = s_data.get("title", "")
                    if title:
                        topics.append(title)
                time.sleep(0.2)
            all_topics.extend(topics)
            print(f"    HN: 获取 {len(topics)} 条")
    except Exception as e:
        print(f"    HN热点异常: {e}")

    # Twitter热点 (Trends24)
    print("    抓取Twitter热点...")
    try:
        resp = fetch_with_retry("https://trends24.in/united-states/", timeout=15)
        if resp:
            import re as _re
            trends = _re.findall(r'#([A-Za-z0-9_]+)', resp.text)
            if trends:
                all_topics.extend(trends[:30])
                print(f"    Twitter: 获取 {len(trends)} 条")
    except Exception as e:
        print(f"    Twitter热点异常: {e}")

    # BBC News
    print("    抓取BBC News...")
    try:
        bbc = fetch_bbc_hot()
        if bbc: all_topics.extend(bbc); print(f"    BBC: 获取 {len(bbc)} 条")
    except Exception as e: print(f"    BBC异常: {e}")

    # Reuters
    print("    抓取Reuters...")
    try:
        reuters = fetch_reuters_hot()
        if reuters: all_topics.extend(reuters); print(f"    Reuters: 获取 {len(reuters)} 条")
    except Exception as e: print(f"    Reuters异常: {e}")

    # CNN
    print("    抓取CNN...")
    try:
        cnn = fetch_cnn_hot()
        if cnn: all_topics.extend(cnn); print(f"    CNN: 获取 {len(cnn)} 条")
    except Exception as e: print(f"    CNN异常: {e}")

    # Guardian
    print("    抓取Guardian...")
    try:
        guardian = fetch_guardian_hot()
        if guardian: all_topics.extend(guardian); print(f"    Guardian: 获取 {len(guardian)} 条")
    except Exception as e: print(f"    Guardian异常: {e}")

    # AP News
    print("    抓取AP News...")
    try:
        ap = fetch_ap_hot()
        if ap: all_topics.extend(ap); print(f"    AP: 获取 {len(ap)} 条")
    except Exception as e: print(f"    AP异常: {e}")

    # Google News
    print("    抓取Google News...")
    try:
        gn = fetch_google_news_hot()
        if gn: all_topics.extend(gn); print(f"    Google News: 获取 {len(gn)} 条")
    except Exception as e: print(f"    Google News异常: {e}")

    # 去重
    seen = set()
    unique = []
    for t in all_topics:
        t_clean = t.strip()
        if t_clean and t_clean not in seen and 2 < len(t_clean) < 100:
            seen.add(t_clean)
            unique.append(t_clean)

    print(f"  [EN] 共抓取 {len(all_topics)} 条,去重后 {len(unique)} 条")

    if len(unique) < ARTICLES_PER_RUN:
        needed = ARTICLES_PER_RUN - len(unique)
        # 英文常青话题(如果热点不足时补充)
        en_fallback = [
            "How AI is Transforming Healthcare in 2026",
            "Top 10 Tech Gadgets You Need This Year",
            "Stock Market Outlook: What Investors Should Know",
            "Remote Work Revolution: Future of Employment",
            "Electric Vehicle Market Trends and Predictions",
            "Cybersecurity Threats Everyone Should Be Aware Of",
            "Cryptocurrency Regulation Updates Around the World",
            "Best Programming Languages to Learn in 2026",
            "Climate Change: Latest Research and Solutions",
            "Social Media Impact on Mental Health",
            "Space Exploration Milestones This Year",
            "5G vs 6G: The Future of Connectivity",
        ]
        extra = [t for t in en_fallback if t not in seen]
        random.shuffle(extra)
        unique.extend(extra[:needed])
        print(f"  [EN] 热点不足,补充 {needed} 条常青话题")

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
    '你是一个专业财经分析师,写作风格务实、数据驱动,用事实和逻辑说话,不用任何口语化表达或情绪化措辞。',
    '你是一个深度调查记者,追求信息密度和事实准确性,用具体数据和来源支撑每个论点,风格冷静客观。',
    '你是一个行业研究员,擅长从数据中发现趋势,用图表般的文字呈现分析,避免主观判断,只用"数据显示""根据XX报告"这类客观表述。',
    '你是一个资深财经编辑,像《财经》杂志的风格,专业但不晦涩,有观点但必须用数据和案例佐证,绝不空谈。',
    '你是一个投资顾问,写作风格简洁有力,每句话都有信息量,不说废话,不卖弄文采,用事实说话。',
]

TITLE_STYLES = [
    "标题用具体数据+结论(如'XX行业Q1营收增长35%,三大趋势解读'),专业可信,25字以内",
    "标题用陈述句含关键数据(如'XX政策落地:影响YY万人ZZ亿元市场'),25字以内",
    "标题用时间+核心结论(如'2026年XX趋势:三大变化及投资方向'),25字以内",
    "标题用行业+数据洞察(如'XX赛道增速放缓,头部企业如何应对'),25字以内",
    "标题用对比数据(如'XX指数涨15% vs YY跌8%,背后逻辑分析'),25字以内",
    "标题用政策/事件+影响范围(如'XX决议通过:对YY行业ZZ市场的三重影响'),25字以内",
    "标题用清单+数据(如'关于XX的5个关键数据:投资者必须了解'),25字以内",
    "标题用因果逻辑(如'XX导致YY行业格局重塑,三个判断'),25字以内",
]

# 英文风格提示
EN_STYLE_PROMPTS = [
    "You are a professional financial analyst. Your writing is data-driven, factual, and logical. You cite specific sources and numbers, never use emotional or sensational language.",
    "You are an investigative business journalist. You prioritize information density and factual accuracy, supporting every claim with concrete data and sources. Your tone is calm and objective.",
    "You are an industry researcher skilled at finding trends in data. You present analysis with precision, avoid subjective judgments, and only use phrases like 'data shows' or 'according to [report]'.",
    "You are a senior financial editor in the style of The Economist or Bloomberg - professional but accessible, opinionated but always backed by data and cases, never empty rhetoric.",
    "You are an investment advisor. Your writing is concise and powerful, every sentence carries information, no filler words, no showing off, just facts and analysis.",
]

EN_TITLE_STYLES = [
    "Use a data-driven headline with specific numbers (like 'X Sector Grows 35% in Q1: 3 Key Trends') for credibility, under 60 characters",
    "Use a policy/event + impact headline (like 'X Decision: 3 Impacts on Y Market Worth Z Billion') under 60 characters",
    "Use a year + trend headline (like '2026 X Outlook: 3 Changes & Investment Directions') under 60 characters",
    "Use an industry + data insight headline (like 'X Sector Slowdown: How Top Players Are Responding') under 60 characters",
    "Use a contrast data headline (like 'X Up 15% vs Y Down 8%: The Logic Behind It') under 60 characters",
    "Use a list + data headline (like '5 Key Data Points About X Investors Must Know') under 60 characters",
    "Use a causal logic headline (like 'X Reshapes Y Industry: 3 Predictions') under 60 characters",
]

def generate_article_zh(topic):
    """生成中文文章 - v4.0 高质量版"""
    style = random.choice(STYLE_PROMPTS)
    title_style = random.choice(TITLE_STYLES)
    # AI+金融偏向:财经/科技分类的文章注入垂直角度
    cat = classify_topic(topic)
    angle_hint = ""
    if cat == "finance":
        angle_hint = "\n【写作角度】本篇属于财经/投资类内容,请从以下角度切入:结合AI技术对金融行业的影响,分析投资机会与风险,可引用具体数据或案例,结尾引导读者对AI+金融趋势的思考。"
    elif cat == "tech":
        angle_hint = "\n【写作角度】本篇涉及科技/AI领域,请侧重AI应用场景、技术落地进展、行业竞争格局等角度,让读者感受到AI技术的真实影响力。"

    prompt = f"""{style}

请根据以下热门话题写一篇2500-3500字的专业深度分析文章。必须是原创深度分析，不能只是热点复述或套话堆砌。

话题:{topic}{angle_hint}

【硬性要求 - 违反任何一条都会被打回重写】
1. {title_style}
2. 第一段必须直接切入核心事件/观点，用1-2句话制造信息密度，禁止铺垫、禁止"随着...""近年来"这类废话开头
3. 分5-7个小节，每节用##小标题。小标题必须包含具体信息，禁止"XX的真相""XX的秘密"这种空洞标题
4. 每小节必须同时满足：
   - 有独立观点（用"数据显示""根据XX报告"支撑，禁止"我觉得""我认为"这类主观废话）
   - 至少1个具体案例/数据（必须注明来源或背景，禁止瞎编"XX品牌""某专家"）
   - 对读者的 actionable 建议（能直接照着做，不是"要谨慎"这种废话）
5. 【原创分析 - 质量红线】必须包含：
   - 深层原因分析：用"因为A导致B"的逻辑链，引用行业报告/数据/历史案例佐证（至少200字）
   - 影响与应对：具体到"谁、在什么场景、该怎么做"，给出可执行步骤（至少200字）
   - 至少2个带来源的数据或案例（如"据工信部2026年Q1数据""XX公司2025年报显示"）
6. 自然融入3-5个相关词和2-3个长尾关键词，禁止堆砌，必须自然融入句子
7. FAQ段落要求：必须是读者真正会问的实用问题，回答要有具体数据或操作步骤，禁止"视情况而定"这类废话
8. 结尾：抛一个有争议性的问题或明确站队的观点，引导讨论，禁止"让我们一起期待"这种和稀泥结尾
9. 语气：专业分析师的语气，有数据、有逻辑、有态度，但绝不使用口语化表达（禁用"说实话""讲真""你敢信""我的观点"）
10. 【绝对禁用词汇】:"首先""其次""最后""总而言之""综上所述""让我们来看看""不可否认""值得注意的是""需要指出的是""在当今社会""随着...的发展""越来越多的人""从某种意义上说""希望这篇文章能够帮助大家""我觉得""我认为""可能""大概""或许""说实话""讲真""你敢信""我的观点""我的看法""不得不说""相信大家"
11. 【禁止自我指涉】:"作为AI""本文由AI生成""作为一个语言模型"
12. 【禁止模板开头】:"近年来""最近""最近一段时间""最近网上"
13. 字数：2500字以上，每小节350字以上，总字符不少于8000（含标题）
14. 【质量自检】生成完成后检查：
    - 是否有"我觉得""可能""说实话"这类模糊/口语表达？有就删掉重写
    - 每个数据都有来源吗？没有就补充或删掉
    - 建议是可执行的吗？不是就改具体
    - 读完能获得什么新信息？如果没有，加深度分析

输出格式:
第一行:标题(纯文字,不加任何标记)
空一行
正文(纯文本/markdown,禁止##小标题,用自然段落过渡)"""

    try:
        token = get_zhipu_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.5, "max_tokens": 4500}
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
    """生成英文文章 - v4.0 高质量版(基于中文话题)"""
    style = random.choice(EN_STYLE_PROMPTS)
    title_style = random.choice(EN_TITLE_STYLES)
    cat_en = classify_topic_en(topic_zh)
    angle_hint = ""
    if cat_en == "finance":
        angle_hint = "\n[WRITING ANGLE] This is a finance/investment topic - focus on AI's impact on financial markets, investment opportunities, and risk analysis. Use specific data or cases, and end by prompting readers to think about AI+Finance trends."
    elif cat_en == "tech":
        angle_hint = "\n[WRITING ANGLE] This is a tech/AI topic - emphasize AI application scenarios, real-world impact, and industry competition dynamics. Make readers feel the tangible power of AI technology."

    prompt = f"""{style}

Write a 2000-2800 word, HIGH-QUALITY, ORIGINAL analysis article in ENGLISH ONLY based on this trending topic from China: {topic_zh}{angle_hint}

This MUST be original analysis with genuine insights, NOT a summary of news or generic commentary.

[QUALITY STANDARDS - Violating any will result in rejection]
1. {title_style}
2. ALL content in English - title, body, subheadings - ZERO Chinese characters allowed
3. First paragraph: immediate hook with specific information, NO fluff, NO "In recent years" "Nowadays" openings
4. 5-7 sections with ## subheadings that contain SPECIFIC information, NO generic titles like "The Truth About X" or "X Secrets"
5. Each section MUST simultaneously have:
   - Original insight backed by "According to [source]" or "Data from [report]" (NO "I think" "I believe" "Maybe" hedging)
   - At least 1 concrete data point or real case with attribution (NO made-up "some experts" "a study")
   - Actionable advice readers can implement immediately (NO "be careful" vague suggestions)
6. [MANDATORY ORIGINAL ANALYSIS - Quality Gate]:
   - Root cause analysis: Use "A leads to B" logic chains, cite industry reports/data/historical cases (min 200 words)
   - Impact & response: Specific "who, in what scenario, should do what" with executable steps (min 200 words)
   - At least 2 data points with sources (e.g., "According to Q1 2026 MIIT data" "XX Company's 2025 annual report shows")
7. Naturally weave 3-5 related terms and 2-3 long-tail keywords, NO stuffing, must flow naturally
8. FAQ requirements: Must be practical questions readers actually ask, answers need specific data or steps, NO "it depends" cop-outs
9. Ending: Controversial question or clear stance that invites debate, NO "let's wait and see" weak endings
10. Tone: Like an informed friend in the field - opinionated, information-dense, NO false objectivity, NO lecturing
11. [BANNED PHRASES]: "In today's society" "With the development of" "More and more people" "It is worth noting that" "Let's take a look" "In conclusion" "To sum up" "As we can see" "Needless to say" "It goes without saying" "At the end of the day" "First and foremost" "Last but not least" "I think" "I believe" "Maybe" "Probably" "Perhaps"
12. [NO AI DISCLAIMERS]: "As an AI" "This article was generated" "As a language model"
13. [NO TEMPLATE OPENINGS]: "Recently" "In recent years" "Lately" "These days"
14. Length: 2000+ words, each section 300+ words, total 5500+ characters
15. [QUALITY CHECK before output]:
    - Any "I think" "maybe" hedging? Remove and rewrite with data
    - Every data point has a source? Add attribution or remove
    - Is advice actionable and specific? Make it concrete if not
    - What new information does reader gain? Add depth analysis if none

Output format:
First line: Title in English (no markdown)
Blank line
Body in English (markdown with ## subheadings)"""

    try:
        token = get_zhipu_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.5, "max_tokens": 4000}
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
        body = _de_ai_process_en(body)

        # 后处理:检测并过滤中文内容
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', title + body)
        if len(chinese_chars) > 5:
            print(f"    ⚠️ 英文文章含中文({len(chinese_chars)}字),重新生成...")
            # 重试一次,用更严格的prompt
            title, body = _retry_generate_en_strict(topic_zh)
            if not title:
                print(f"    ❌ 英文生成失败(含中文过多)")
                return None, None

        return title, body
    except Exception as e:
        print(f"  英文AI生成失败: {e}")
        return None, None

def _de_ai_process_zh(text):
    """中文去AI味 - v4.0 严格版"""
    replacements = {
        # 原有规则
        "首先": "先说", "其次": "再来看", "最后": "说到底",
        "总而言之": "说白了", "综上所述": "所以啊",
        "值得注意的是": "这里有个重点", "不可否认": "谁都知道",
        "众所周知": "大家都清楚", "引发了广泛关注": "网上都炸了",
        "引起了热议": "网友吵翻了", "引起了广泛讨论": "大家都在讨论",
        # 新增规则 - 模板句式
        "让我们来看看": "看看", "让我们来看": "看", "让我们": "",
        "不得不说": "说实话", "不得不": "得",
        "相信大家": "你们", "大家一定": "你肯定",
        "值得注意的是": "重点是", "值得注意的是,": "重点:",
        "需要指出的是": "关键在", "需要强调的是": "强调一下",
        "在当今社会": "现在", "在当今": "现在", "在现代社会": "现在",
        "随着科技的发展": "科技发展到现在", "随着社会的进步": "社会进步后",
        "越来越多的人": "好多人", "越来越多的人开始": "好多人都开始",
        "人们开始": "大家开始", "人们逐渐": "大家慢慢",
        "不可否认的是": "确实", "不可否认,": "确实,",
        "毫无疑问": "肯定", "毫无疑问,": "肯定,",
        "一般来说": "通常", "一般而言": "通常",
        "换句话说": "也就是", "换言之": "也就是说",
        "由此可见": "所以", "由此可知": "这就能看出",
        "综上所述": "总结一下", "总而言之": "说白了",
        "从某种意义上说": "某种程度上", "从某种程度上说": "某种程度上",
        "事实上": "其实", "事实上,": "其实,",
        "实际上": "其实", "实际上,": "其实,",
        "有意思的是": "巧的是", "有意思的是,": "巧的是,",
        "更重要的是": "关键的是", "更重要的是,": "关键是,",
        "不仅如此": "而且", "不仅如此,": "而且,",
        "一方面": "一来", "另一方面": "二来",
        "总的来说": "总之", "总体来说": "总之",
        "在一定程度上": "某种程度上", "在很大程度上": "很大程度上",
        # AI 特色结尾
        "希望这篇文章": "", "希望本文": "",
        "能够帮助大家": "", "能够给大家": "",
        "有所帮助": "有收获",
        # v4.0 新增 - 主观废话(替换为更专业的表述)
        "我觉得": "", "我认为": "", "我感觉": "",
        "可能": "", "大概": "", "或许": "", "也许": "",
        "一定程度上": "", "某种程度上": "",
        "从某种程度上": "", "从一定程度上": "",
        "有人说": "", "有人觉得": "", "有人认为": "",
        "不少网友": "", "很多网友": "", "有人表示": "",
        "专家表示": "", "业内人士": "", "分析人士": "",
        # v4.1 新增 - 口语化表达
        "说实话": "", "讲真": "", "你敢信": "",
        "我的观点": "", "我的看法": "", "我的理解": "",
        "不得不说": "", "相信大家": "你们",
        "谁都知道": "", "大家都清楚": "", "网上都炸了": "引发关注",
        "网友吵翻了": "引发争议", "大家都在讨论": "引发讨论",
        "先说": "", "再来看": "", "说到底": "",
        "说白了": "", "所以啊": "",
        "确实": "", "其实": "",
        "好多人": "许多人", "好多": "许多",
        "巧的是": "", "关键是": "",
        "重点": "核心", "重点:": "核心:",
        # 模糊限定词
        "比较": "", "相对": "", "一定程度上": "",
        "某种程度上": "", "某种程度上说": "",
        # 套话
        "值得一提的是": "", "值得注意": "",
        "不难发现": "", "不难看出": "",
        "可以预见": "", "可以预期": "",
        "不难发现": "", "不难看出": "",
        "从长远来看": "", "从短期来看": "",
        "从长远角度": "", "从短期角度": "",
        # 开头废话
        "最近": "", "近日": "", "日前": "", "近期": "",
        "近来": "", "最近一段时间": "", "最近网上": "",
        "标题:": "", "标题:": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # 清理多余空格
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # v4.0 新增 - 删除空括号
    text = re.sub(r'\(\s*\)', '', text)
    text = re.sub(r'(\s*)', '', text)
    return text

def _de_ai_title_zh(title):
    """中文标题优化 - 专业版,不加标题党前缀"""
    # 去除标题党前缀
    for prefix in ["震惊!", "重磅!", "刚刚!", "速看!", "出大事了!", "刚刚曝光!", "突发!", "紧急!", "震撼!", "炸锅!", "怒了!", "沸腾!"]:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()
    if len(title) > 30:
        title = title[:28] + "..."
    if len(title) < 8:
        title = f"深度解读: {title}"
    return title

def _de_ai_title_en(title):
    """英文标题优化 - 专业版,不加标题党前缀"""
    # 去除标题党前缀
    for prefix in ["Breaking:", "Just In:", "Must Read:", "Shocking:", "Revealed:", "Breaking News:", "Alert:", "Urgent:"]:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()
    if len(title) > 70:
        title = title[:67] + "..."
    if len(title) < 10:
        title = f"Analysis: {title}"
    return title

def _de_ai_process_en(text):
    """英文去AI味 - v4.0 严格版"""
    replacements = {
        "In today's society": "Today", "in today's society": "today",
        "With the development of": "As", "with the development of": "as",
        "More and more people": "Many people", "more and more people": "many people",
        "It is worth noting that": "Note that", "it is worth noting that": "note that",
        "Let's take a look": "Let's look", "let's take a look": "let's look",
        "In conclusion": "So", "in conclusion": "so",
        "To sum up": "So", "to sum up": "so",
        "As we can see": "We see", "as we can see": "we see",
        "Needless to say": "", "needless to say": "",
        "It goes without saying that": "", "it goes without saying that": "",
        "At the end of the day": "Ultimately", "at the end of the day": "ultimately",
        "First and foremost": "First", "first and foremost": "first",
        "Last but not least": "Finally", "last but not least": "finally",
        "As an AI": "", "as an AI": "",
        "This article was generated": "", "this article was generated": "",
        "In recent years": "", "in recent years": "",
        "Recently,": "", "recently,": "",
        # v4.0 新增 - 主观废话
        "I think": "", "I believe": "", "I feel": "",
        "In my opinion": "", "In my view": "",
        "Maybe": "", "maybe": "",
        "Probably": "", "probably": "",
        "Perhaps": "", "perhaps": "",
        "Some people say": "", "some people say": "",
        "Some experts": "", "some experts": "",
        "Many people think": "", "many people think": "",
        # 模糊限定词
        "Somewhat": "", "somewhat": "",
        "Relatively": "", "relatively": "",
        "Fairly": "", "fairly": "",
        "Quite": "", "quite": "",
        "Rather": "", "rather": "",
        # 套话
        "It is interesting to note": "", "it is interesting to note": "",
        "Interestingly": "", "interestingly": "",
        "Notably": "", "notably": "",
        "Importantly": "", "importantly": "",
        "Significantly": "", "significantly": "",
        "Clearly": "", "clearly": "",
        "Obviously": "", "obviously": "",
        "Undoubtedly": "", "undoubtedly": "",
        # 开头废话
        "Lately": "", "lately": "",
        "These days": "", "these days": "",
        "Nowadays": "", "nowadays": "",
        "Title:": "", "title:": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # 清理多余空格和空行
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # v4.0 新增 - 删除空括号
    text = re.sub(r'\(\s*\)', '', text)
    return text

def _retry_generate_en_strict(topic_zh):
    """严格模式重试生成英文文章(禁止中文)"""
    strict_prompt = f"""You are an English news writer. Write an article in 100% ENGLISH.

Topic (Chinese reference): {topic_zh}

ABSOLUTE RULES:
- Title: ENGLISH ONLY, no Chinese characters at all
- Body: ENGLISH ONLY, every single word must be English
- Subheadings: ENGLISH ONLY
- 1000-1500 words, 4-6 sections with ## subheadings
- Conversational, engaging style
- Output: Title on first line, then blank line, then body

VIOLATION: If ANY Chinese character appears in output, it is WRONG."""
    try:
        token = get_zhipu_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"model": MODEL, "messages": [{"role": "user", "content": strict_prompt}], "temperature": 0.4, "max_tokens": 2000}
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

# ==================== 思维导图生成 ====================

def generate_mindmap_zh(title, body):
    """禁用脑图生成 - 直接返回空字符串"""
    return ""

def generate_mindmap_en(title, body):
    """禁用脑图生成 - 直接返回空字符串"""
    return ""
def _fallback_mindmap(body, lang="zh"):
    """从文章##/###标题提取脑图(免费兜底)"""
    headings = re.findall(r'^#{2,3}\s+(.+)$', body, re.MULTILINE)
    if not headings:
        return "# 本文要点\n## 核心内容\n### 详情见正文" if lang == "zh" else "# Key Points\n## Main Content\n### See Article"
    root = "# 文章要点" if lang == "zh" else "# Article Overview"
    lines = [root]
    for h in headings[:8]:
        h = h.strip()
        if len(h) > 25:
            h = h[:23] + ".."
        lines.append(f"## {h}" if re.match(r'^##\s', f"## {h}") else f"### {h}")
    return "\n".join(lines)

def _mindmap_html_block(mindmap_text, slug="mm", lang="zh"):
    """将markdown脑图转成CSS树状HTML(零依赖)"""
    if not mindmap_text or not mindmap_text.strip():
        return ""
    label = "🧠 文章思维导图" if lang == "zh" else "🧠 Article Mind Map"
    lines = mindmap_text.strip().split('\n')
    nodes = []
    for line in lines:
        m = re.match(r'^(#+)\s+(.+)$', line)
        if not m:
            continue
        level = len(m.group(1))
        content = m.group(2).strip()
        content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        indent_px = max(0, (level - 2) * 24)
        if level == 1:
            nodes.append(f'<div class="mm-root"><span class="mm-dot"></span>{content}</div>')
        elif level == 2:
            nodes.append(f'<div class="mm-node mm-l2" style="--indent:{indent_px}px"><span class="mm-dot"></span>{content}</div>')
        else:
            nodes.append(f'<div class="mm-node mm-l3" style="--indent:{indent_px}px"><span class="mm-dot"></span>{content}</div>')
    if not nodes:
        return ""
    tree = '\n'.join(nodes)
    return f'''<div class="mindmap-section">
<h3>{label}</h3>
<div class="mm-tree">{tree}</div>
</div>'''

# ==================== 分类 ====================

def classify_topic(topic):
    """中文分类 - 关键词扩充版"""
    keywords = {
        "finance":    ["股票", "期货", "基金", "黄金", "汇率", "美联储", "加息", "降息", "A股", "大盘", "指数", "板块", "涨停", "跌停", "期权", "数字货币", "比特币", "理财", "投资", "融资", "上市", "债券", "大宗商品", "油价", "人民币", "美元", "欧元", "央行", "经济", "通胀", "GDP", "财报", "营收", "利润", "银行", "保险", "证券", "退市", "并购", "独角兽", "估值", "私募", "风投", "创业板", "科创", "纳斯达克", "标普", "道琼斯", "港股", "中概股", "减持", "增持", "回购", "分红", "派息", "通货", "贬值", "升值", "国债", "地方债", "城投", "信托", "P2P", "网贷", "消费贷", "房贷利率", "LPR", "降准", "MLF", "逆回购", "注册制", "北交所", "AI概念股", "DeepSeek概念", "大模型", "ChatGPT概念", "人工智能", "科技股", "芯片股", "英伟达", "GPU", "算力", "算力股", "数据中心", "云服务", "SaaS", "软件股", "半导体", "光刻机", "国产替代", "科技自主", "科创板", "专精特新"],
        "tech":       ["AI", "人工智能", "手机", "电脑", "科技", "数码", "互联网", "软件", "芯片", "5G", "编程", "APP", "智能", "机器人", "自动驾驶", "量子", "云计算", "大数据", "区块链", "元宇宙", "VR", "AR", "GPU", "CPU", "半导体", "光刻", "华为", "苹果", "小米", "特斯拉", "微软", "谷歌", "OpenAI", "GPT", "大模型", "算法", "模型", "深度学习", "机器学习", "神经网络", "服务器", "数据中心", "算力", "光模块", "服务器", "新能源", "电动车", "充电桩", "电池", "光伏", "钠离子", "核聚变", "可控核", "航天", "火箭", "卫星", "空间站", "神舟", "月球", "火星", "太空", "无人机", "大疆", "操作系统", "鸿蒙", "Android", "iOS", "WiFi", "6G", "宽带", "光纤", "IOT", "物联网", "穿戴", "智能手表", "折叠屏", "OLED", "Micro LED", "面板", "京东方", "龙芯", "麒麟", "信创", "DeepSeek", "Kimi", "通义千问", "豆包", "文心一言", "GPT-5", "Claude", "Gemini", "AI应用", "AI工具", "AI生成", "AIGC", "AI绘画", "AI视频", "AI写作", "AI搜索", "AI助手", "AI模型", "开源模型", "AI芯片", "NPU", "AI算力", "边缘AI", "端侧AI", "具身智能", "人形机器人", "AppleIntelligence", "AI手机", "AI电脑", "Copilot", "Cursor", "Windsurf", "Perplexity", "Grok", "AI眼镜", "AI耳机", "AI教育", "AI医疗", "AI办公"],
        "health":     ["健康", "养生", "医疗", "医院", "疫情", "病毒", "疫苗", "减肥", "健身", "营养", "睡眠", "心理", "医生", "手术", "药物", "中药", "西药", "体检", "癌症", "肿瘤", "糖尿病", "血压", "血糖", "心脏", "肝脏", "肾脏", "肺", "骨", "眼科", "牙科", "中医", "针灸", "艾灸", "推拿", "食疗", "维生素", "蛋白", "益生菌", "过敏", "流感", "感冒", "发烧", "抗生素", "靶向", "免疫", "基因", "DNA", "干细胞", "长寿", "抗衰老", "更年期", "孕产", "婴儿", "儿童", "老年", "痴呆", "阿尔茨海默", "帕金森", "抑郁", "焦虑", "自闭", "戒烟", "戒酒", "救护", "急救", "中毒", "食安", "食品安全", "微塑料", "辐射", "卫生", "疾控", "卫健委", "世卫"],
        "life":       ["生活", "美食", "旅游", "房产", "汽车", "教育", "职场", "购物", "家居", "亲子", "烧烤", "火锅", "奶茶", "咖啡", "外卖", "小吃", "特产", "水果", "蔬菜", "海鲜", "泡菜", "做饭", "食谱", "景点", "签证", "机票", "酒店", "民宿", "自驾", "高铁", "飞机", "出国", "留学", "移民", "租房", "房价", "楼市", "物业", "装修", "家电", "家具", "清洗", "收纳", "宠物", "猫", "狗", "花", "园艺", "运动", "跑步", "游泳", "瑜伽", "钓鱼", "登山", "露营", "天气", "暴雨", "台风", "高温", "寒潮", "防汛", "抗旱", "高考", "考研", "公务员", "招聘", "简历", "面试", "工资", "社保", "公积金", "养老金", "退休", "离婚", "结婚", "生育", "幼儿园", "学区"],
        "entertainment": ["娱乐", "明星", "电影", "电视剧", "综艺", "音乐", "游戏", "网红", "八卦", "偶像", "演员", "歌手", "导演", "票房", "上映", "开播", "收官", "综艺", "选秀", "脱口秀", "相声", "小品", "喜剧", "动画", "动漫", "番剧", "漫画", "小说", "网文", "直播", "带货", "短视频", "抖音", "快手", "B站", "微博热搜", "话题", "粉丝", "CP", "塌房", "出轨", "恋情", "婚变", "离婚", "复婚", "代言", "品牌", "时装", "红毯", "颁奖", "奥斯卡", "金鸡", "金马", "跑男", "偶像", "练习生", "粉丝团", "应援", "打榜", "超话", "世界杯", "欧洲杯", "亚洲杯", "国足", "足球", "篮球", "NBA", "CBA", "中超", "英超", "西甲", "意甲", "球迷", "裁判", "教练", "转会", "球员", "梅西", "C罗"],
    }
    for cat, kws in keywords.items():
        if any(kw in topic for kw in kws):
            return cat
    return "hot"

def classify_topic_en(topic):
    """英文分类 - 独立英文关键词表"""
    keywords = {
        "finance":    ["stock", "market", "invest", "crypto", "bitcoin", "fund", "ETF", "Fed", "interest rate", "inflation", "GDP", "economy", "fiscal", "monetary", "bond", "treasury", "dividend", "earning", "revenue", "profit", "IPO", "VC", "startup valuation", "merger", "acquisition", "hedge fund", "private equity", "forex", "currency", "dollar", "euro", "yuan", "commodity", "oil price", "gold price", "real estate", "mortgage", "bank", "insurance", "fintech", "DeFi", "NFT", "trading", "portfolio", "bull", "bear", "recession", "stimulus", "tariff", "trade war", "S&P", "Nasdaq", "Dow", "Wall Street", "AI stock", "Nvidia", "AMD", "Palantir", "Snowflake", "Datadog", "Arm", "Super Micro", "AI chip", "tech stock", "Magnificent 7", "FAANG", "Meme stock", "short squeeze", "options trading", "day trading", "retail investor", "institutional investor", "hedge fund strategy", "ETF flow", "bond yield", "yield curve", "Fed rate cut", "earnings report", "SEC filing", "antitrust", "tech regulation", "OpenAI", "Microsoft", "Google", "Meta", "Amazon", "Apple", "Tesla", "deepseek", "llm", "AI model", "AI earnings", "AI valuation", "AI IPO"],
        "tech":       ["AI", "artificial intelligence", "machine learning", "deep learning", "GPT", "LLM", "OpenAI", "Google", "Apple", "Microsoft", "Tesla", "chip", "semiconductor", "GPU", "CPU", "quantum", "cloud", "server", "data center", "5G", "6G", "robot", "autonomous", "EV", "electric vehicle", "battery", "solar", "nuclear", "space", "rocket", "satellite", "ISS", "moon", "Mars", "drone", "VR", "AR", "metaverse", "blockchain", "cybersecurity", "hacker", "malware", "app", "software", "hardware", "phone", "laptop", "tablet", "wearable", "IoT", "WiFi", "broadband", "fiber", "operating system", "coding", "developer", "API", "open source", "GitHub", "startup", "unicorn", "DeepSeek", "Claude", "Gemini", "Copilot", "Cursor", "Windsurf", "Perplexity", "Grok", "ChatGPT", "AIGC", "AI video", "AI image", "AI writing", "AI search", "AI agent", "AI assistant", "edge AI", "on-device AI", "AI model", "open weight model", "multimodal", "reasoning", "context window", "token", "fine-tuning", "RAG", "agentic", "robotics", "humanoid robot", "autonomous driving", "Waymo", "Figure robot", "Boston Dynamics"],
        "health":     ["health", "medical", "hospital", "doctor", "surgery", "vaccine", "virus", "pandemic", "COVID", "flu", "cancer", "tumor", "diabetes", "heart", "mental health", "depression", "anxiety", "fitness", "diet", "nutrition", "obesity", "weight loss", "sleep", "therapy", "pharma", "drug", "FDA", "clinical trial", "gene therapy", "stem cell", "anti-aging", "longevity", "Alzheimer", "Parkinson", "autism", "allergy", "antibiotic", "supplement", "vitamin", "probiotic", "microplastic", "radiation", "WHO", "CDC", "wellness", "mindful", "meditation", "yoga", "rehab", "emergency", "first aid", "poison", "food safety"],
        "life":       ["life", "food", "recipe", "restaurant", "coffee", "travel", "flight", "hotel", "vacation", "tourism", "visa", "home", "house", "rent", "mortgage rate", "decor", "furniture", "pet", "dog", "cat", "garden", "weather", "storm", "hurricane", "heatwave", "flood", "education", "school", "college", "university", "scholarship", "job", "career", "salary", "resume", "interview", "retirement", "pension", "marriage", "divorce", "parenting", "baby", "kids", "elder", "commute", "housing", "lifestyle", "hobby", "camping", "hiking", "fishing", "cooking", "baking", "BBQ"],
        "entertainment": ["entertainment", "movie", "film", "TV", "series", "show", "music", "song", "album", "concert", "game", "gaming", "esports", "streamer", "YouTube", "TikTok", "influencer", "celebrity", "actor", "actress", "singer", "director", "box office", "Oscar", "Emmy", "Grammy", "comic", "anime", "manga", "novel", "book", "podcast", "Netflix", "Disney", "Marvel", "DC", "Star Wars", "sport", "football", "soccer", "NBA", "NFL", "MLB", "FIFA", "World Cup", "Olympic", "championship", "player", "coach", "transfer", "fan", "stadium", "draft", "MVP"],
    }
    topic_lower = topic.lower()
    for cat, kws in keywords.items():
        if any(kw.lower() in topic_lower for kw in kws):
            return cat
    return "hot"

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

def add_to_manifest(slug, title, category, filename, lang="zh", cover_url=""):
    manifest = load_manifest(lang)
    # 用精确到秒的时间戳确保新文章永远排在最前面
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 插入到列表头部(最新的在最前面)
    entry = {"slug": slug, "title": title, "category": category, "date": datetime.now().strftime("%Y-%m-%d"), "timestamp": timestamp, "filename": filename}
    if cover_url:
        entry["cover_url"] = cover_url
    manifest.insert(0, entry)
    save_manifest(manifest, lang)

def get_related_articles(category, current_slug, lang="zh", limit=5):
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

def _jsonld_article(title, cat_name, date_iso, slug, category, lang="zh"):
    site_name = SITE_NAME if lang == "zh" else EN_SITE_NAME
    site_url = SITE_URL if lang == "zh" else EN_SITE_URL
    prefix = "/articles/" if lang == "zh" else "/en/articles/"
    # Breadcrumb JSON-LD
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": site_name, "item": site_url},
            {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"{site_url}{prefix}{category}.html"},
            {"@type": "ListItem", "position": 3, "name": title, "item": f"{site_url}{prefix}{slug}.html"},
        ]
    }
    # Article JSON-LD (enhanced)
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "datePublished": date_iso,
        "dateModified": date_iso,
        "author": {"@type": "Organization", "name": site_name},
        "publisher": {"@type": "Organization", "name": site_name, "logo": {"@type": "ImageObject", "url": f"{site_url}/favicon.ico"}},
        "mainEntityOfPage": f"{site_url}{prefix}{slug}.html",
        "articleSection": cat_name,
    }
    return json.dumps(breadcrumb, ensure_ascii=False) + "\n" + json.dumps(article, ensure_ascii=False)

def generate_article_html_zh(title, body, category, slug, related_articles, mindmap_text="", cover_url=""):
    cat_info = CATEGORIES.get(category, CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    html_body = _md2html(body)
    svg_hero = generate_svg_hero(title, category, "zh")
    # 封面图:优先用Unsplash真实图片,无图则用SVG兜底
    if cover_url:
        hero_block = f'''<div class="hero-image"><img src="{cover_url}" alt="{title.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')}" loading="lazy" onerror="this.parentElement.style.display='none'"><p style="text-align:center;font-size:0.75rem;color:#999;margin-top:4px">Image Source: Internet</p></div>'''
    else:
        hero_block = f'<div class="hero-svg">{svg_hero}</div>'
    mindmap_block = _mindmap_html_block(mindmap_text, slug, "zh") if mindmap_text else ""
    # Reading time: Chinese ~500 chars/min
    zh_chars = len(re.findall(r'[\u4e00-\u9fff]', body))
    reading_minutes = max(1, round(zh_chars / 500))
    reading_time_html = f'<span>📖 {reading_minutes}分钟阅读</span>'

    # 插入中间广告
    parts = html_body.split("</p>")
    if len(parts) > 3:
        parts.insert(3, f"</p>\n{AD_CODE_MIDDLE}")
        html_body = "".join(parts)

    json_ld = _jsonld_article(title, cat_name, date_iso, slug, category, "zh")
    disclaimer = FINANCE_DISCLAIMER_ZH if category == "finance" else ""

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
.ad-slot{{margin:20px 0;text-align:center}}
.hero-svg{{margin:20px 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.1)}}
.hero-svg svg{{width:100%;display:block}}
.hero-image{{margin:20px 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.1)}}
.hero-image img{{width:100%;height:auto;display:block;object-fit:cover;max-height:400px;aspect-ratio:2/1}}
.cps-box{{background:linear-gradient(135deg,#fff9f0,#fff5e6);border:1px solid #ffe0c0;border-radius:10px;padding:18px;margin:25px 0}}
.cps-box h3{{margin:0 0 12px;color:#d4680a}}
.cps-box ul{{list-style:none;padding:0}}
.cps-box li{{padding:8px 0;border-bottom:1px dashed #ffd9b3;display:flex;justify-content:space-between;align-items:center;gap:8px}}
.cps-box a{{color:#d4680a;text-decoration:none;font-weight:500;flex-shrink:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.cps-desc{{color:#999;font-size:.82em;flex-shrink:0}}
.related{{background:#fff;border:1px solid #eee;border-radius:10px;padding:18px;margin:25px 0}}
.related h3{{margin:0 0 12px;color:#333}}
.related ul{{list-style:none;padding:0}}
.related li{{padding:8px 0;border-bottom:1px solid #f5f5f5}}
.related a{{color:#333;text-decoration:none}}
.related .date{{color:#ccc;font-size:.8em;margin-left:10px}}
.footer{{margin-top:30px;padding-top:15px;border-top:1px solid #eee;text-align:center;color:#aaa;font-size:.82em}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
.mindmap-section{{background:linear-gradient(135deg,#f8f9ff,#fff5f0);border:1px solid #e8e0f0;border-radius:12px;padding:20px;margin:20px 0}}
.mindmap-section h3{{margin:0 0 16px;font-size:1.05em;color:#333}}
.mm-tree{{padding:0}}
.mm-root{{background:linear-gradient(135deg,#ff6b35,#ff8c42);color:#fff;padding:10px 20px;border-radius:8px;font-weight:bold;font-size:1.05em;margin-bottom:12px;display:inline-block;box-shadow:0 2px 8px rgba(255,107,53,0.3)}}
.mm-dot{{display:inline-block;width:6px;height:6px;border-radius:50%;background:currentColor;margin-right:8px;vertical-align:middle}}
.mm-node{{padding:7px 8px 7px calc(var(--indent,0px) + 30px);margin:4px 0;border-left:2px solid #ffccbd;position:relative;line-height:1.4}}
.mm-l2{{font-size:.95em;color:#444}}
.mm-l3{{font-size:.87em;color:#666;border-left-color:#ffe0d5;padding-left:calc(var(--indent,0px) + 45px)}}
.mm-l3 .mm-dot{{width:4px;height:4px}}
@media(max-width:480px){{body{{font-size:16px;line-height:1.7}}.article-title{{font-size:1.3em}}.hero-svg{{margin:15px 0;border-radius:8px}}.cps-box{{padding:14px;margin:18px 0}}.cps-box li{{flex-direction:column;align-items:flex-start;gap:2px;padding:10px 0}}.cps-box a{{white-space:normal;font-size:.95em}}.cps-desc{{margin-top:2px}}.mindmap-section{{padding:14px}}.share-box a{{min-height:44px;display:inline-flex;align-items:center}}}}
.share-box{{margin:20px 0;padding:15px 20px;background:#f0f8ff;border-radius:10px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;border:1px solid #d0e8ff}}
.share-box span{{color:#666;font-size:.9em;white-space:nowrap}}
.share-box a{{padding:6px 16px;border-radius:20px;text-decoration:none;font-size:.85em;font-weight:500;transition:all .2s;cursor:pointer}}
.share-box a:nth-child(2){{background:#07c160;color:#fff}}
.share-box a:nth-child(3){{background:#ff5a4c;color:#fff}}
.share-box a:nth-child(4){{background:#ff2442;color:#fff}}
.share-box a:nth-child(5){{background:#666;color:#fff}}
.share-box a:hover{{opacity:.85;transform:translateY(-1px)}}
@media(max-width:480px){{.share-box{{gap:8px;justify-content:center}}.share-box a{{font-size:.8em;padding:5px 12px}}}}
</style>
{GA4_CODE}
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
<div class="meta"><span>📅 {date_str}</span> <span>👤 每日热点速递编辑部</span> <span>🔄 更新:{date_str}</span> <span>{cat_icon} {cat_name}</span> {reading_time_html}</div>
{hero_block}
{mindmap_block}
{html_body}
{disclaimer}
{_cps_block(category, "zh")}
{_related_block(related_articles, "zh")}
<div class="share-box">
<span>📤 分享:</span>
<a href="javascript:void(0)" onclick="window.open('https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={SITE_URL}/articles/{slug}.html','_blank','width=200,height=200')" rel="nofollow">微信</a>
<a href="https://service.weibo.com/share/share.php?url={SITE_URL}/articles/{slug}.html&title={title}" target="_blank" rel="sponsored nofollow noopener"" target="_blank" rel="nofollow noopener">微博</a>
<a href="javascript:void(0)" onclick="window.open('{SITE_URL}/articles/{slug}.html','_blank');" rel="nofollow">今日头条</a>
<a href="javascript:void(0)" onclick="navigator.clipboard.writeText('{SITE_URL}/articles/{slug}.html');this.textContent='已复制';">复制链接</a>
</div>
</article>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025-2026 {SITE_NAME}</p>
<p><a href="/">首页</a><a href="/articles/hot.html">社会热点</a><a href="/articles/tech.html">科技数码</a><a href="/articles/health.html">健康养生</a><a href="/articles/life.html">生活百科</a><a href="/articles/entertainment.html">娱乐八卦</a><a href="/articles/finance.html">财经投资</a></p>
<p><a href="/about.html">关于我们</a> | <a href="/privacy-policy.html">隐私政策</a> | <a href="/terms.html">使用条款</a> | <a href="/dmca.html">DMCA</a> | <a href="/cookies.html">Cookies</a></p>
</div>
</body>
</html>"""

def generate_article_html_en(title, body, category, slug, related_articles, mindmap_text="", cover_url=""):
    cat_info = EN_CATEGORIES.get(category, EN_CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    html_body = _md2html(body)
    svg_hero = generate_svg_hero(title, category, "en")
    # Cover image: prefer Unsplash, fallback to SVG
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if cover_url:
        hero_block = '<div class="hero-image"><img src="' + cover_url + '" alt="' + safe_title + '" loading="lazy" onerror="this.parentElement.style.display=\'none\'"/><p style="text-align:center;font-size:0.75rem;color:#999;margin-top:4px">Image Source: Internet</p></div>'
    else:
        hero_block = '<div class="hero-svg">' + svg_hero + '</div>'
    mindmap_block = _mindmap_html_block(mindmap_text, slug, "en") if mindmap_text else ""
    # Reading time: English ~238 words/min
    en_words = len(body.split())
    reading_minutes = max(1, round(en_words / 238))
    reading_time_html = f'<span>📖 {reading_minutes} min read</span>'

    parts = html_body.split("</p>")
    if len(parts) > 3:
        parts.insert(3, f"</p>\n{AD_CODE_MIDDLE}")
        html_body = "".join(parts)

    json_ld = _jsonld_article(title, cat_name, date_iso, slug, category, "en")
    disclaimer = FINANCE_DISCLAIMER_EN if category == "finance" else ""

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
.ad-slot{{margin:20px 0;text-align:center}}
.hero-svg{{margin:20px 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.1)}}
.hero-svg svg{{width:100%;display:block}}
.hero-image{{margin:20px 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.1)}}
.hero-image img{{width:100%;height:auto;display:block;object-fit:cover;max-height:400px;aspect-ratio:2/1}}
.cps-box{{background:linear-gradient(135deg,#fff9f0,#fff5e6);border:1px solid #ffe0c0;border-radius:10px;padding:18px;margin:25px 0}}
.cps-box h3{{margin:0 0 12px;color:#d4680a}}
.cps-box ul{{list-style:none;padding:0}}
.cps-box li{{padding:8px 0;border-bottom:1px dashed #ffd9b3;display:flex;justify-content:space-between;align-items:center;gap:8px}}
.cps-box a{{color:#d4680a;text-decoration:none;font-weight:500;flex-shrink:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.cps-desc{{color:#999;font-size:.82em;flex-shrink:0}}
.related{{background:#fff;border:1px solid #eee;border-radius:10px;padding:18px;margin:25px 0}}
.related h3{{margin:0 0 12px;color:#333}}
.related ul{{list-style:none;padding:0}}
.related li{{padding:8px 0;border-bottom:1px solid #f5f5f5}}
.related a{{color:#333;text-decoration:none}}
.related .date{{color:#ccc;font-size:.8em;margin-left:10px}}
.footer{{margin-top:30px;padding-top:15px;border-top:1px solid #eee;text-align:center;color:#aaa;font-size:.82em}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
.mindmap-section{{background:linear-gradient(135deg,#f8f9ff,#fff5f0);border:1px solid #e8e0f0;border-radius:12px;padding:20px;margin:20px 0}}
.mindmap-section h3{{margin:0 0 16px;font-size:1.05em;color:#333}}
.mm-tree{{padding:0}}
.mm-root{{background:linear-gradient(135deg,#ff6b35,#ff8c42);color:#fff;padding:10px 20px;border-radius:8px;font-weight:bold;font-size:1.05em;margin-bottom:12px;display:inline-block;box-shadow:0 2px 8px rgba(255,107,53,0.3)}}
.mm-dot{{display:inline-block;width:6px;height:6px;border-radius:50%;background:currentColor;margin-right:8px;vertical-align:middle}}
.mm-node{{padding:7px 8px 7px calc(var(--indent,0px) + 30px);margin:4px 0;border-left:2px solid #ffccbd;position:relative;line-height:1.4}}
.mm-l2{{font-size:.95em;color:#444}}
.mm-l3{{font-size:.87em;color:#666;border-left-color:#ffe0d5;padding-left:calc(var(--indent,0px) + 45px)}}
.mm-l3 .mm-dot{{width:4px;height:4px}}
@media(max-width:480px){{body{{font-size:16px;line-height:1.7}}.article-title{{font-size:1.3em}}.hero-svg{{margin:15px 0;border-radius:8px}}.cps-box{{padding:14px;margin:18px 0}}.cps-box li{{flex-direction:column;align-items:flex-start;gap:2px;padding:10px 0}}.cps-box a{{white-space:normal;font-size:.95em}}.cps-desc{{margin-top:2px}}.mindmap-section{{padding:14px}}.share-box a{{min-height:44px;display:inline-flex;align-items:center}}}}
.share-box{{margin:20px 0;padding:15px 20px;background:#f0f8ff;border-radius:10px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;border:1px solid #d0e8ff}}
.share-box span{{color:#666;font-size:.9em;white-space:nowrap}}
.share-box a{{padding:6px 16px;border-radius:20px;text-decoration:none;font-size:.85em;font-weight:500;transition:all .2s;cursor:pointer}}
.share-box a:nth-child(2){{background:#000;color:#fff}}
.share-box a:nth-child(3){{background:#0088cc;color:#fff}}
.share-box a:nth-child(4){{background:#1877f2;color:#fff}}
.share-box a:nth-child(5){{background:#666;color:#fff}}
.share-box a:hover{{opacity:.85;transform:translateY(-1px)}}
@media(max-width:480px){{.share-box{{gap:8px;justify-content:center}}.share-box a{{font-size:.8em;padding:5px 12px}}}}
</style>
{GA4_CODE}
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
<div class="meta"><span>📅 {date_str}</span> <span>👤 By: Daily Trending News Editorial</span> <span>🔄 Updated: {date_str}</span> <span>{cat_icon} {cat_name}</span> {reading_time_html}</div>
{hero_block}
{svg_hero}
{mindmap_block}
{html_body}
{disclaimer}
{_cps_block(category, "en")}
{_related_block(related_articles, "en")}
<div class="share-box">
<span>📤 Share:</span>
<a href="https://twitter.com/intent/tweet?url={SITE_URL}/en/articles/{slug}.html&text={title}" target="_blank" rel="sponsored nofollow noopener"" target="_blank" rel="nofollow noopener">X</a>
<a href="https://t.me/share/url?url={SITE_URL}/en/articles/{slug}.html&text={title}" target="_blank" rel="sponsored nofollow noopener"" target="_blank" rel="nofollow noopener">Telegram</a>
<a href="https://www.facebook.com/sharer/sharer.php?u={SITE_URL}/en/articles/{slug}.html" target="_blank" rel="sponsored nofollow noopener"" target="_blank" rel="nofollow noopener">Facebook</a>
<a href="javascript:void(0)" onclick="navigator.clipboard.writeText('{SITE_URL}/en/articles/{slug}.html');this.textContent='Copied';">Copy Link</a>
</div>
</article>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025-2026 {EN_SITE_NAME}</p>
<p><a href="/en/">Home</a><a href="/en/articles/hot.html">Trending</a><a href="/en/articles/tech.html">Tech</a><a href="/en/articles/health.html">Health</a><a href="/en/articles/life.html">Lifestyle</a><a href="/en/articles/entertainment.html">Entertainment</a></p>
</div>
</body>
</html>"""

# ==================== 分类页 ====================

def generate_category_page_zh(category):
    cat_info = CATEGORIES.get(category, CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    cat_color = THUMB_COLORS.get(category, THUMB_COLORS["hot"])
    articles = sorted([a for a in load_manifest("zh") if a["category"] == category], key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)[:50]
    def _zh_card_html(a):
        cover = a.get("cover_url", "")
        if cover:
            thumb = f'<span class="card-thumb" style="background:{cat_color};padding:0;overflow:hidden"><img src="{cover}" alt="" style="width:100%;height:100%;object-fit:cover" loading="lazy"/></span>'
        else:
            thumb = f'<span class="card-thumb" style="background:{cat_color}">{cat_icon}</span>'
        return f'<article class="card">{thumb}<div class="card-content"><a href="/articles/{a["filename"]}" class="card-title">{a["title"]}</a><div class="card-meta"><span>{a.get("date","")}</span></div></div></article>'
    card_items = "\n".join(_zh_card_html(a) for a in articles) or '<div style="color:#999;text-align:center;padding:40px">暂无文章...</div>'
    cat_disclaimer = '<div style="background:#fff3e0;border:1px solid #ffcc80;border-radius:8px;padding:14px 18px;margin:25px 0;font-size:.85em;color:#8d6e63;text-align:center">&#9888; <strong>免责声明:</strong>本频道内容仅供学习参考,不构成任何投资建议。市场有风险,投资需谨慎。</div>' if category == "finance" else ""

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
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;line-height:1.6;color:#333;max-width:900px;margin:0 auto;padding:15px;background:#fafafa}}
.header{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:2px solid #ff6b35;margin-bottom:15px}}
.header h1{{font-size:1.1em;color:#ff6b35}}
.breadcrumb{{font-size:.85em;color:#999;margin-bottom:15px}}
.breadcrumb a{{color:#ff6b35;text-decoration:none}}
.cat-title{{font-size:1.5em;margin:20px 0;font-weight:bold}}
.card-grid{{display:grid;grid-template-columns:1fr;gap:12px}}
.card{{display:flex;align-items:flex-start;gap:12px;padding:14px;background:#fff;border-radius:10px;border:1px solid #eee;transition:box-shadow .2s}}
.card:hover{{box-shadow:0 2px 12px rgba(0,0,0,.08)}}
.card-thumb{{display:flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:10px;font-size:20px;flex-shrink:0;color:#fff}}
.card-content{{flex:1;min-width:0}}
.card-title{{color:#1a1a1a;text-decoration:none;font-size:1em;font-weight:500;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.4}}
.card-title:hover{{color:#ff6b35}}
.card-meta{{margin-top:6px;color:#999;font-size:.82em}}
.footer{{margin-top:30px;text-align:center;color:#aaa;font-size:.82em;padding-top:15px;border-top:1px solid #eee}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
.ad-slot{{margin:20px 0;text-align:center}}
@media(max-width:600px){{
.card{{padding:12px;gap:10px}}
.card-thumb{{width:40px;height:40px;font-size:18px}}
.card-title{{font-size:.95em}}
.header{{flex-wrap:wrap;gap:8px}}
}}
</style>
{GA4_CODE}
</head>
<body>
<div class="header">
<h1>&#x1F4F0; {SITE_NAME}</h1>
<div><a href="/">中文</a> | <a href="/en/">English</a></div>
</div>
<nav class="breadcrumb"><a href="/">首页</a> &gt; {cat_icon} {cat_name}</nav>
<h2 class="cat-title">{cat_icon} {cat_name}</h2>
<div class="ad-slot">{AD_CODE_TOP}</div>
<div class="card-grid">{card_items}</div>
{cat_disclaimer}
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>&copy; 2025-2026 {SITE_NAME}</p>
<p><a href="/">首页</a><a href="/articles/hot.html">社会热点</a><a href="/articles/tech.html">科技数码</a><a href="/articles/health.html">健康养生</a><a href="/articles/life.html">生活百科</a><a href="/articles/entertainment.html">娱乐八卦</a><a href="/articles/finance.html">财经投资</a></p>
<p><a href="/about-en.html">About</a> | <a href="/privacy-policy-en.html">Privacy</a> | <a href="/terms-en.html">Terms</a> | <a href="/dmca.html">DMCA</a> | <a href="/cookies.html">Cookies</a></p>
</div>
</body>
</html>"""

def generate_category_page_en(category):
    cat_info = EN_CATEGORIES.get(category, EN_CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    cat_color = THUMB_COLORS.get(category, THUMB_COLORS["hot"])
    articles = sorted([a for a in load_manifest("en") if a["category"] == category], key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)[:50]
    def _en_card_html(a):
        cover = a.get("cover_url", "")
        if cover:
            thumb = f'<span class="card-thumb" style="background:{cat_color};padding:0;overflow:hidden"><img src="{cover}" alt="" style="width:100%;height:100%;object-fit:cover" loading="lazy"/></span>'
        else:
            thumb = f'<span class="card-thumb" style="background:{cat_color}">{cat_icon}</span>'
        return f'<article class="card">{thumb}<div class="card-content"><a href="/en/articles/{a["filename"]}" class="card-title">{a["title"]}</a><div class="card-meta"><span>{a.get("date","")}</span></div></div></article>'
    card_items = "\n".join(_en_card_html(a) for a in articles) or '<div style="color:#999;text-align:center;padding:40px">No articles yet...</div>'
    cat_disclaimer = '<div style="background:#fff3e0;border:1px solid #ffcc80;border-radius:8px;padding:14px 18px;margin:25px 0;font-size:.85em;color:#8d6e63;text-align:center">&#9888; <strong>Disclaimer:</strong> Content is for informational purposes only and does not constitute investment advice. Invest at your own risk.</div>' if category == "finance" else ""

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
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.6;color:#333;max-width:900px;margin:0 auto;padding:15px;background:#fafafa}}
.header{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:2px solid #ff6b35;margin-bottom:15px}}
.header h1{{font-size:1.1em;color:#ff6b35}}
.breadcrumb{{font-size:.85em;color:#999;margin-bottom:15px}}
.breadcrumb a{{color:#ff6b35;text-decoration:none}}
.cat-title{{font-size:1.5em;margin:20px 0;font-weight:bold}}
.card-grid{{display:grid;grid-template-columns:1fr;gap:12px}}
.card{{display:flex;align-items:flex-start;gap:12px;padding:14px;background:#fff;border-radius:10px;border:1px solid #eee;transition:box-shadow .2s}}
.card:hover{{box-shadow:0 2px 12px rgba(0,0,0,.08)}}
.card-thumb{{display:flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:10px;font-size:20px;flex-shrink:0;color:#fff}}
.card-content{{flex:1;min-width:0}}
.card-title{{color:#1a1a1a;text-decoration:none;font-size:1em;font-weight:500;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.4}}
.card-title:hover{{color:#ff6b35}}
.card-meta{{margin-top:6px;color:#999;font-size:.82em}}
.footer{{margin-top:30px;text-align:center;color:#aaa;font-size:.82em;padding-top:15px;border-top:1px solid #eee}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
.ad-slot{{margin:20px 0;text-align:center}}
@media(max-width:600px){{
.card{{padding:12px;gap:10px}}
.card-thumb{{width:40px;height:40px;font-size:18px}}
.card-title{{font-size:.95em}}
.header{{flex-wrap:wrap;gap:8px}}
}}
</style>
{GA4_CODE}
</head>
<body>
<div class="header">
<h1>&#x1F4F0; {EN_SITE_NAME}</h1>
<div><a href="/">中文</a> | <a href="/en/">English</a></div>
</div>
<nav class="breadcrumb"><a href="/en/">Home</a> &gt; {cat_icon} {cat_name}</nav>
<h2 class="cat-title">{cat_icon} {cat_name}</h2>
<div class="ad-slot">{AD_CODE_TOP}</div>
<div class="card-grid">{card_items}</div>
{cat_disclaimer}
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>&copy; 2025-2026 {EN_SITE_NAME}</p>
<p><a href="/en/">Home</a><a href="/en/articles/hot.html">Trending</a><a href="/en/articles/tech.html">Tech</a><a href="/en/articles/health.html">Health</a><a href="/en/articles/life.html">Lifestyle</a><a href="/en/articles/entertainment.html">Entertainment</a><a href="/en/articles/finance.html">Finance</a></p>
<p><a href="/about-en.html">About</a> | <a href="/privacy-policy-en.html">Privacy</a> | <a href="/terms-en.html">Terms</a> | <a href="/dmca.html">DMCA</a> | <a href="/cookies.html">Cookies</a></p>
</div>
</body>
</html>"""

# ==================== 首页 ====================

def rebuild_index_zh():
    manifest = load_manifest("zh")
    if not manifest:
        print("  中文首页:暂无文章")
        return

    articles = sorted(manifest, key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)

    # Group by category
    by_cat = {}
    for a in articles:
        cat = a.get("category", "hot")
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(a)

    # Category sections HTML - show top 5 per category
    CATEGORIES_PRESENT = ["finance","hot","tech","health","life","entertainment"]
    cat_sections_html = ""
    for cat_key in CATEGORIES_PRESENT:
        cat_articles = by_cat.get(cat_key, [])
        if not cat_articles:
            continue
        top5 = cat_articles[:5]
        cat_info = CATEGORIES.get(cat_key, CATEGORIES["hot"])
        items_html = "\n".join(
            f'<li><span class="thumb" style="background:{THUMB_COLORS.get(a.get("category","hot"),THUMB_COLORS["hot"])}">{CATEGORIES.get(a["category"],CATEGORIES["hot"])["icon"]}</span><span class="date">{a.get("date","")}</span><a href="/articles/{a["filename"]}">{a["title"]}</a></li>'
            for a in top5
        )
        more_link = f'<a href="/articles/{cat_key}.html" class="cat-more">更多 {cat_info["name"]} &rarr;</a>'
        cat_sections_html += f"""
<section class="cat-section">
  <div class="cat-section-header">
    <span class="cat-section-title">{cat_info["icon"]} {cat_info["name"]}</span>
    {more_link}
  </div>
  <ul class="cat-article-list">{items_html}
  </ul>
</section>"""

    # Full timeline - latest 100
    timeline = articles[:100]
    list_items = "\n".join(
        f'<li><span class="thumb" style="background:{THUMB_COLORS.get(a.get("category","hot"),THUMB_COLORS["hot"])}">{CATEGORIES.get(a["category"],CATEGORIES["hot"])["icon"]}</span><span class="date">{a.get("date","")}</span><span class="cat">[{CATEGORIES.get(a["category"],CATEGORIES["hot"])["name"]}]</span><a href="/articles/{a["filename"]}">{a["title"]}</a></li>'
        for a in timeline
    )
    cat_links = "\n".join(f'<a href="/articles/{k}.html" class="cat-link">{v["icon"]} {v["name"]}</a>' for k, v in CATEGORIES.items())
    cat_links += '\n<a href="/treasure.html" class="cat-link" style="color:#ff6b35;font-weight:bold">💎 宝藏网址</a>'

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
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;line-height:1.8;color:#333;max-width:960px;margin:0 auto;padding:15px;background:#fafafa}}
.site-header{{position:relative;text-align:center;padding:25px 0 20px}}
.site-header h1{{font-size:1.8em;color:#1a1a1a;margin-bottom:5px}}
.site-header p{{color:#888;font-size:.95em}}
.header-actions{{position:absolute;top:15px;right:0;display:flex;gap:10px;align-items:center}}
.lang-btn{{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border-radius:25px;text-decoration:none;font-weight:bold;font-size:.95em;transition:all .2s;border:2px solid #ff6b35;color:#ff6b35}}
.lang-btn:hover{{background:#ff6b35;color:#fff;transform:scale(1.05)}}
.lang-btn.active{{background:#ff6b35;color:#fff}}
.contact-btn{{color:#2e7d32;text-decoration:none;font-size:.9em;cursor:pointer;border:1px solid #a5d6a7;padding:8px 16px;border-radius:20px;background:#e8f5e9}}
.contact-btn:hover{{background:#43a047;color:#fff}}
.contact-box{{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#fff;padding:25px 30px;border-radius:12px;box-shadow:0 4px 24px rgba(0,0,0,.18);z-index:1000;min-width:300px}}
.contact-box.show{{display:block}}
.contact-box h3{{margin:0 0 18px;font-size:1.1em;color:#333}}
.contact-item{{margin:10px 0;padding:10px 14px;background:#f5f5f5;border-radius:8px;display:flex;justify-content:space-between;align-items:center;gap:10px}}
.contact-item code{{font-size:.9em;color:#555;word-break:break-all}}
.contact-item button{{padding:4px 12px;border-radius:6px;background:#ff6b35;color:#fff;border:none;cursor:pointer;font-size:.85em;white-space:nowrap}}
.contact-item button:hover{{background:#e65100}}
.contact-close{{margin-top:18px;padding:8px 20px;border-radius:8px;background:#eee;color:#666;border:none;cursor:pointer;font-size:.9em}}
.contact-close:hover{{background:#ddd}}
.contact-overlay{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.3);z-index:999}}
.contact-overlay.show{{display:block}}
.cat-nav{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:15px 0 25px;padding:15px;background:#fff;border-radius:10px}}
.cat-link{{padding:6px 16px;border-radius:20px;background:#fff5ed;color:#d4680a;text-decoration:none;font-size:.9em;border:1px solid #ffe0c0}}
.cat-link:hover{{background:#ff6b35;color:#fff}}
ul{{list-style:none}}
li{{padding:10px 8px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:8px;font-size:.93em}}
li:hover{{background:#f5f5f5}}
.date{{color:#999;font-size:.82em;white-space:nowrap;min-width:80px}}
.cat{{color:#ff6b35;font-size:.78em;white-space:nowrap;min-width:70px}}
a{{color:#333;text-decoration:none}}
a:hover{{color:#ff6b35}}
.footer{{margin-top:30px;text-align:center;color:#aaa;font-size:.82em;padding-top:15px;border-top:1px solid #eee}}
.footer a{{color:#999;text-decoration:none;margin:0 8px}}
.ad-slot{{margin:20px 0;text-align:center}}
.cat-section{{background:#fff;border-radius:12px;margin-bottom:18px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
.cat-section-header{{display:flex;justify-content:space-between;align-items:center;padding:12px 18px;border-bottom:1px solid #f0f0f0}}
.cat-section-title{{font-size:1em;font-weight:bold;color:#333}}
.cat-more{{font-size:.82em;color:#ff6b35;text-decoration:none;white-space:nowrap}}
.cat-more:hover{{text-decoration:underline}}
.cat-article-list li{{padding:9px 18px}}
.timeline-header{{font-size:1em;font-weight:bold;color:#333;padding:15px 0 8px;border-bottom:2px solid #ff6b35;margin-bottom:5px}}
.timeline-header span{{color:#999;font-weight:normal;font-size:.85em;margin-left:10px}}
.thumb{{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:6px;margin-right:8px;font-size:14px;flex-shrink:0;color:#fff}}
</style>
{GA4_CODE}
</head>
<body>
<div class="site-header">
<h1>&#x1F4F0; {SITE_NAME}</h1>
<p>{SITE_DESC}</p>
<div class="header-actions">
<a href="/en/" class="lang-btn">&#x1F1FA;&#x1F1F8; English</a>
<a class="contact-btn" onclick="document.getElementById('contactBox').classList.add('show');document.getElementById('contactOverlay').classList.add('show')">&#x2709;&#xFE0F; &#x8054;&#x7CFB;&#x6211;&#x4EEC;</a>
</div>
</div>
<div class="contact-overlay" id="contactOverlay" onclick="this.classList.remove('show');document.getElementById('contactBox').classList.remove('show')"></div>
<div class="contact-box" id="contactBox">
<h3>&#x2709;&#xFE0F; &#x8054;&#x7CFB;&#x6211;&#x4EEC;</h3>
<div class="contact-item"><code>543837216@qq.com</code><button onclick="navigator.clipboard.writeText('543837216@qq.com');this.textContent='&#x5DF2;&#x590D;&#x5236;'">&#x590D;&#x5236;</button></div>
<div class="contact-item"><code>xiaokangjiao@gmail.com</code><button onclick="navigator.clipboard.writeText('xiaokangjiao@gmail.com');this.textContent='&#x5DF2;&#x590D;&#x5236;'">&#x590D;&#x5236;</button></div>
<button class="contact-close" onclick="document.getElementById('contactBox').classList.remove('show');document.getElementById('contactOverlay').classList.remove('show')">&#x5173;&#x95ED;</button>
</div>
<nav class="cat-nav">{cat_links}</nav>
<div class="ad-slot">{AD_CODE_TOP}</div>
{cat_sections_html}
<div class="ad-slot">{AD_CODE_MIDDLE}</div>
<div class="timeline-header">&#x1F4C5; &#x6700;&#x65B0;&#x6587;&#x7AE0; <span>&#x5171; {len(timeline)} &#x7BC7;</span></div>
<ul>{list_items}</ul>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>&copy; 2025-2026 {SITE_NAME}</p>
<p><a href="/">&#x9996;&#x9875;</a><a href="/articles/hot.html">&#x793E;&#x4F1A;&#x70ED;&#x70B9;</a><a href="/articles/tech.html">&#x79D1;&#x6280;&#x6570;&#x7801;</a><a href="/articles/health.html">&#x5065;&#x5EB7;&#x517B;&#x751F;</a><a href="/articles/life.html">&#x751F;&#x6D3B;&#x767E;&#x79D1;</a><a href="/articles/entertainment.html">&#x5A1C;&#x4E50;&#x516B;&#x7591;</a><a href="/articles/finance.html">&#x8D22;&#x7ECF;&#x6295;&#x8D44;</a></p>
<p><a href="/about-en.html">About</a> | <a href="/privacy-policy-en.html">Privacy</a> | <a href="/terms-en.html">Terms</a> | <a href="/dmca.html">DMCA</a> | <a href="/cookies.html">Cookies</a></p>
</div>
</body>
</html>"""
    INDEX_FILE.write_text(html, encoding="utf-8")
    print(f"  中文首页已更新,展示 {len(articles)} 篇,6个分类区块+完整时间线")



def rebuild_index_en():
    manifest = load_manifest("en")
    if not manifest:
        print("  英文首页:暂无文章")
        return
    articles = sorted(manifest, key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)[:100]
    list_items = "\n".join(f'<li><span class="thumb" style="background:{THUMB_COLORS.get(a.get("category","hot"),THUMB_COLORS["hot"])}">{EN_CATEGORIES.get(a["category"],EN_CATEGORIES["hot"])["icon"]}</span><span class="date">{a.get("date","")}</span><span class="cat">[{EN_CATEGORIES.get(a["category"],EN_CATEGORIES["hot"])["name"]}]</span><a href="/en/articles/{a["filename"]}">{a["title"]}</a></li>' for a in articles)
    cat_links = "\n".join(f'<a href="/en/articles/{k}.html" class="cat-link">{v["icon"]} {v["name"]}</a>' for k, v in EN_CATEGORIES.items())
    cat_links += '\n<a href="/treasure.html" class="cat-link" style="color:#ff6b35;font-weight:bold">💎 Treasure</a>'

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
.site-header{{position:relative;text-align:center;padding:25px 0 20px}}
.site-header h1{{font-size:1.8em;color:#1a1a1a;margin-bottom:5px}}
.site-header p{{color:#888;font-size:.95em}}
.header-actions{{position:absolute;top:15px;right:0;display:flex;gap:10px;align-items:center}}
.lang-btn{{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border-radius:25px;text-decoration:none;font-weight:bold;font-size:.95em;transition:all .2s;border:2px solid #ff6b35;color:#ff6b35}}
.lang-btn:hover{{background:#ff6b35;color:#fff;transform:scale(1.05)}}
.lang-btn.active{{background:#ff6b35;color:#fff}}
.contact-btn{{color:#2e7d32;text-decoration:none;font-size:.9em;cursor:pointer;border:1px solid #a5d6a7;padding:8px 16px;border-radius:20px;background:#e8f5e9}}
.contact-btn:hover{{background:#43a047;color:#fff}}
.contact-box{{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#fff;padding:25px 30px;border-radius:12px;box-shadow:0 4px 24px rgba(0,0,0,.18);z-index:1000;min-width:300px}}
.contact-box.show{{display:block}}
.contact-box h3{{margin:0 0 18px;font-size:1.1em;color:#333}}
.contact-item{{margin:10px 0;padding:10px 14px;background:#f5f5f5;border-radius:8px;display:flex;justify-content:space-between;align-items:center;gap:10px}}
.contact-item code{{font-size:.9em;color:#555;word-break:break-all}}
.contact-item button{{padding:4px 12px;border-radius:6px;background:#ff6b35;color:#fff;border:none;cursor:pointer;font-size:.85em;white-space:nowrap}}
.contact-item button:hover{{background:#e65100}}
.contact-close{{margin-top:18px;padding:8px 20px;border-radius:8px;background:#eee;color:#666;border:none;cursor:pointer;font-size:.9em}}
.contact-close:hover{{background:#ddd}}
.contact-overlay{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.3);z-index:999}}
.contact-overlay.show{{display:block}}
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
.ad-slot{{margin:20px 0;text-align:center}}
.thumb{{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:6px;margin-right:8px;font-size:14px;flex-shrink:0;color:#fff}}
</style>
{GA4_CODE}
</head>
<body>
<div class="site-header">
<h1>📰 {EN_SITE_NAME}</h1>
<p>{EN_SITE_DESC}</p>
<div class="header-actions">
<a href="/" class="lang-btn">&#x1F1E8;&#x1F1F3; 中文</a>
<a class="contact-btn" onclick="document.getElementById('contactBox').classList.add('show');document.getElementById('contactOverlay').classList.add('show')">&#x2709;&#xFE0F; Contact Us</a>
</div>
</div>
<div class="contact-overlay" id="contactOverlay" onclick="this.classList.remove('show');document.getElementById('contactBox').classList.remove('show')"></div>
<div class="contact-box" id="contactBox">
<h3>&#x2709;&#xFE0F; Contact Us</h3>
<div class="contact-item"><code>543837216@qq.com</code><button onclick="navigator.clipboard.writeText('543837216@qq.com');this.textContent='Copied'">Copy</button></div>
<div class="contact-item"><code>xiaokangjiao@gmail.com</code><button onclick="navigator.clipboard.writeText('xiaokangjiao@gmail.com');this.textContent='Copied'">Copy</button></div>
<button class="contact-close" onclick="document.getElementById('contactBox').classList.remove('show');document.getElementById('contactOverlay').classList.remove('show')">Close</button>
</div>
<nav class="cat-nav">{cat_links}</nav>
<div class="ad-slot">{AD_CODE_TOP}</div>
<ul>{list_items}</ul>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025-2026 {EN_SITE_NAME}</p>
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

def clean_old_articles(days=15):
    """清理N天前的旧文章,保持仓库轻量"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d')

    removed_zh, removed_en = 0, 0

    # 清理中文文章
    if MANIFEST_FILE.exists():
        manifest = json.loads(MANIFEST_FILE.read_text(encoding='utf-8'))
        new_manifest = []
        for item in manifest:
            if item.get('date', '9999-99-99') < cutoff_str:
                # 删除文件
                file_path = OUTPUT_DIR / item['filename']
                if file_path.exists():
                    file_path.unlink()
                    removed_zh += 1
            else:
                new_manifest.append(item)
        MANIFEST_FILE.write_text(json.dumps(new_manifest, ensure_ascii=False, indent=2), encoding='utf-8')

    # 清理英文文章
    if EN_MANIFEST_FILE.exists():
        manifest = json.loads(EN_MANIFEST_FILE.read_text(encoding='utf-8'))
        new_manifest = []
        for item in manifest:
            if item.get('date', '9999-99-99') < cutoff_str:
                file_path = EN_OUTPUT_DIR / item['filename']
                if file_path.exists():
                    file_path.unlink()
                    removed_en += 1
            else:
                new_manifest.append(item)
        EN_MANIFEST_FILE.write_text(json.dumps(new_manifest, ensure_ascii=False, indent=2), encoding='utf-8')

    if removed_zh > 0 or removed_en > 0:
        print(f"🧹 清理完成: 删除中文 {removed_zh} 篇, 英文 {removed_en} 篇 (保留 {days} 天内)")

    return removed_zh, removed_en

def main():
    if not API_KEY:
        print("❌ 未设置 ZHIPU_API_KEY 环境变量")
        return

    print(f"🚀 双语内容生成器 v4.0 (含脑图) 启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    OUTPUT_DIR.mkdir(exist_ok=True)
    EN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 0. 清理旧文章(保留15天)
    clean_old_articles(days=15)

    # 1. 抓热点(中英文分离:中文用国内源,英文用国外源)
    topics_zh = get_hot_topics()
    topics_en = get_hot_topics_en()
    print(f"📋 中文话题: {len(topics_zh)} 个, 英文话题: {len(topics_en)} 个")

    # 2. 逐篇生成
    zh_generated, en_generated = 0, 0

    # 2a. 中文循环(使用国内热点:百度/微博/头条/知乎/财经)
    for i, topic in enumerate(topics_zh):
        slug_zh = topic_to_slug(topic)

        if not slug_exists(slug_zh, "zh"):
            print(f"  ✍️ [ZH {i+1}/{len(topics_zh)}] {topic}")
            title_zh, body_zh = generate_article_zh(topic)
            if title_zh and body_zh:
                category = classify_topic(topic)
                filename_zh = f"{slug_zh}.html"
                related_zh = get_related_articles(category, slug_zh, "zh")
                print(f"    🧠 生成脑图...")
                mindmap_zh = generate_mindmap_zh(title_zh, body_zh)
                # Fetch Unsplash cover image
                cover_url_zh = fetch_unsplash_image(title_zh)
                html_zh = generate_article_html_zh(title_zh, body_zh, category, slug_zh, related_zh, mindmap_zh, cover_url_zh)
                (OUTPUT_DIR / filename_zh).write_text(html_zh, encoding="utf-8")
                add_to_manifest(slug_zh, title_zh, category, filename_zh, "zh", cover_url_zh)
                zh_generated += 1
                print(f"    ✅ 中文完成: {filename_zh}")
            time.sleep(1)
        else:
            print(f"  ⏭ [ZH {i+1}/{len(topics_zh)}] 跳过(重复): {topic}")

    # 2b. 英文循环(使用国外热点:Reddit/HN/Twitter)
    for i, topic in enumerate(topics_en):
        slug_en = topic_to_slug_en(topic)

        if not slug_exists(slug_en, "en"):
            print(f"  ✍️ [EN {i+1}/{len(topics_en)}] {topic}")
            title_en, body_en = generate_article_en(topic)
            if title_en and body_en:
                category = classify_topic_en(topic)
                filename_en = f"{slug_en}.html"
                related_en = get_related_articles(category, slug_en, "en")
                print(f"    🧠 生成脑图...")
                mindmap_en = generate_mindmap_en(title_en, body_en)
                # Fetch Unsplash cover image
                cover_url_en = fetch_unsplash_image(title_en)
                html_en = generate_article_html_en(title_en, body_en, category, slug_en, related_en, mindmap_en, cover_url_en)
                (EN_OUTPUT_DIR / filename_en).write_text(html_en, encoding="utf-8")
                add_to_manifest(slug_en, title_en, category, filename_en, "en", cover_url_en)
                en_generated += 1
                print(f"    ✅ 英文完成: {filename_en}")
            time.sleep(1)
        else:
            print(f"  ⏭ [EN {i+1}/{len(topics_en)}] 跳过(重复)")

    # 3. 重建站点
    if zh_generated > 0 or en_generated > 0:
        print("\n📐 重建站点页面...")
        rebuild_index_zh()
        rebuild_index_en()
        for cat in CATEGORIES:
            (OUTPUT_DIR / f"{cat}.html").write_text(generate_category_page_zh(cat), encoding="utf-8")
            (EN_OUTPUT_DIR / f"{cat}.html").write_text(generate_category_page_en(cat), encoding="utf-8")
        rebuild_sitemap()

    # 4. Ping搜索引擎
    if zh_generated > 0 or en_generated > 0:
        ping_search_engines()

    # 5. 百度主动推送
    if zh_generated > 0 or en_generated > 0:
        push_to_baidu()

    print(f"\n🏁 完成! 本次生成: 中文 {zh_generated} 篇, 英文 {en_generated} 篇")


# ==================== SEO Ping服务 ====================

def ping_search_engines():
    """主动通知搜索引擎有新内容"""
    sitemap_url = f"{SITE_URL}/sitemap.xml"
    ping_targets = [
        f"http://www.google.com/ping?sitemap={sitemap_url}",
        f"http://www.bing.com/ping?sitemap={sitemap_url}",
    ]
    for url in ping_targets:
        try:
            resp = requests.get(url, timeout=10)
            print(f"  📡 Ping {url.split('?')[0]}: {resp.status_code}")
        except Exception as e:
            print(f"  📡 Ping {url.split('?')[0]}: 失败({e})")


# ==================== 百度主动推送 ====================

BAIDU_PUSH_API = "http://data.zz.baidu.com/urls?site=https://gudaoqihuo.com&token=FPX5kf2VrcBLvWIk"
BAIDU_PUSH_LIMIT = 2000  # 每日限额


def push_to_baidu():
    """百度站长API主动推送新文章URL(每次cron生成后自动调用)"""
    urls = []
    manifest_path = OUTPUT_DIR / "manifest.json"
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for item in data:
                    fname = item.get("file", "") or item.get("filename", "")
                    slug = item.get("slug", "")
                    if fname and slug:
                        urls.append(f"https://gudaoqihuo.com/articles/{fname}")
                    elif slug:
                        urls.append(f"https://gudaoqihuo.com/articles/{slug}.html")
        except Exception:
            pass

    # 英文文章也推
    en_manifest_path = EN_OUTPUT_DIR / "manifest.json"
    if en_manifest_path.exists():
        try:
            data = json.loads(en_manifest_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for item in data:
                    fname = item.get("file", "") or item.get("filename", "")
                    slug = item.get("slug", "")
                    if fname and slug:
                        urls.append(f"https://gudaoqihuo.com/en/articles/{fname}")
                    elif slug:
                        urls.append(f"https://gudaoqihuo.com/en/articles/{slug}.html")
        except Exception:
            pass

    if not urls:
        print("  🔍 百度推送: 无URL可推送")
        return

    # 去重并限制数量
    urls = list(dict.fromkeys(urls))[:BAIDU_PUSH_LIMIT]

    try:
        resp = requests.post(
            BAIDU_PUSH_API,
            data="\n".join(urls),
            headers={"Content-Type": "text/plain"},
            timeout=15,
        )
        result = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        success = result.get("success", 0)
        remain = result.get("remain", "?")
        not_valid = result.get("not_valid", [])
        print(f"  📡 百度推送: 成功{success}条, 剩余额度{remain}, 无效{len(not_valid)}条")
        if not_valid:
            print(f"    ⚠️ 无效URL示例: {not_valid[:3]}")
    except Exception as e:
        print(f"  📡 百度推送失败: {e}")

if __name__ == "__main__":
    main()
