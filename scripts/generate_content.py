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

# SEO Ping服务
PING_SERVICES = [
    "http://ping.baidu.com/ping/RPC2",
    "http://rpc.weblogs.com/RPC2",
]

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
        JD_LINK, PDD_LINK,
    ],
    "health": [
        {"text": "养生保健精选好物", "url": "https://www.amazon.cn/s?k=养生&tag=gudaoqihuo-20", "desc": "健康生活"},
        JD_LINK, PDD_LINK,
    ],
    "life": [
        {"text": "居家好物省钱攻略", "url": "https://www.amazon.cn/s?k=居家好物&tag=gudaoqihuo-20", "desc": "品质生活"},
        JD_LINK, PDD_LINK,
    ],
    "entertainment": [
        {"text": "热门影视周边好物", "url": "https://www.amazon.cn/s?k=影视周边&tag=gudaoqihuo-20", "desc": "追剧必备"},
        JD_LINK, PDD_LINK,
    ],
    "hot": [
        {"text": "今日热搜相关好物", "url": "https://www.amazon.cn/?tag=gudaoqihuo-20", "desc": "发现更多"},
        JD_LINK, PDD_LINK,
    ],
}

# 财经分类CPS推广链接
CPS_LINKS["finance"] = [
    {"text": "理财入门必读书籍", "url": "https://www.amazon.cn/s?k=理财书籍&tag=gudaoqihuo-20", "desc": "财商提升"},
    JD_LINK, PDD_LINK,
]

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

EN_CPS_LINKS["finance"] = [
    {"text": "Finance & Investment Books", "url": "https://www.amazon.com/s?k=finance+books&tag=gudaoqihuo-20", "desc": "Money Smart"},
    {"text": "Stock Market Tools", "url": "https://www.amazon.com/s?k=stock+market+tools&tag=gudaoqihuo-20", "desc": "Trade Smart"},
]

# 广告位配置(中英文共用)
AD_CODE_TOP = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<!-- PropellerAds Placeholder -->
<script src="https://propellerads.com/splash.js?id=YOUR_ZONE_ID" async></script>
<div style="margin:20px 0;text-align:center;min-height:90px;background:#f9f9f9;border:1px dashed #ccc;display:flex;align-items:center;justify-content:center;color:#999;font-size:.8em">Ad Space - Contact: 543837216@qq.com</div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9935054113253833" data-ad-slot="XXXXXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

AD_CODE_MIDDLE = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<!-- PropellerAds Placeholder -->
<script src="https://propellerads.com/splash.js?id=YOUR_ZONE_ID" async></script>
<div style="margin:20px 0;text-align:center;min-height:90px;background:#f9f9f9;border:1px dashed #ccc;display:flex;align-items:center;justify-content:center;color:#999;font-size:.8em">Ad Space - Contact: 543837216@qq.com</div>
<ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-client="ca-pub-9935054113253833" data-ad-slot="XXXXXXXXXX" data-ad-format="fluid" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

AD_CODE_BOTTOM = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<!-- PropellerAds Placeholder -->
<script src="https://propellerads.com/splash.js?id=YOUR_ZONE_ID" async></script>
<div style="margin:20px 0;text-align:center;min-height:90px;background:#f9f9f9;border:1px dashed #ccc;display:flex;align-items:center;justify-content:center;color:#999;font-size:.8em">Ad Space - Contact: 543837216@qq.com</div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9935054113253833" data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

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
本频道所有内容仅供参考和学习交流之用，不构成任何投资建议、交易指导或财务顾问意见。市场有风险，投资需谨慎。文中提及的股票、基金、数字货币、大宗商品等金融产品，均不构成买入、卖出或持有的推荐。投资者应根据自身风险承受能力独立判断，并自行承担投资风险。过往表现不代表未来收益。如需专业投资建议，请咨询持牌金融机构。本站及作者对任何因参考本文内容而造成的直接或间接损失不承担任何责任。
</div>'''

FINANCE_DISCLAIMER_EN = '''<div style="background:linear-gradient(135deg,#fff8f0,#fff3e0);border:1px solid #ffcc80;border-radius:8px;padding:14px 18px;margin:25px 0;font-size:.88em;color:#8d6e63;line-height:1.7">
⚠️ <strong>Disclaimer</strong><br>
All content in this section is for informational and educational purposes only and does not constitute investment advice, trading guidance, or financial advisory services. Market involves risk; invest with caution. Stocks, funds, cryptocurrencies, commodities, and other financial instruments mentioned herein do not constitute recommendations to buy, sell, or hold. Investors should make independent judgments based on their own risk tolerance and bear their own investment risks. Past performance does not guarantee future results. For professional investment advice, please consult a licensed financial institution. This site and its authors accept no liability for any direct or indirect losses resulting from reliance on content published herein.
</div>'''

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
    # 补充财经固定热点词
    finance_keywords = [
        "A股今日行情", "美联储加息", "人民币汇率", "黄金价格走势",
        "科技股最新动态", "新能源汽车板块", "半导体行业分析", "房地产政策",
        "数字货币行情", "基金定投技巧"
    ]
    sources.extend(finance_keywords)
    # 去重
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
    sources = [fetch_baidu_hot, fetch_weibo_hot, fetch_toutiao_hot, fetch_zhihu_hot, fetch_finance_hot]
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

def get_hot_topics_en():
    """英文热点抓取：Reddit + Hacker News + Twitter(Trends24)"""
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
        # 英文常青话题（如果热点不足时补充）
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
    '你是一个资深自媒体写手，风格接地气、像朋友聊天，喜欢用"说实话"、"讲真"、"你敢信"这类口语。',
    "你是一个犀利的社会观察者,喜欢用反问句、感叹号,观点鲜明,敢说敢评。",
    "你是一个生活达人,擅长把复杂的事情说简单,喜欢举例说明,语气亲切温暖。",
    "你是一个深度分析型作者,喜欢扒细节、挖内幕,但表达方式通俗不装。",
    "你是一个带点毒舌的评论员,说话一针见血,偶尔带点黑色幽默,但信息量足。",
]

TITLE_STYLES = [
    "标题用数字+场景(如'男子XX时发现YY'),制造代入感,25字以内",
    "标题用具体人物+动作(如'XX做了件让所有人震惊的事'),制造好奇,25字以内",
    "标题用问答式(如'XX是怎么回事?'),引发点击欲望,25字以内",
    "标题用陈述句但包含具体数据(如'XX事件涉及YY人ZZ万元'),专业可信,25字以内",
    "标题用情绪共鸣(如'网友怒了!'、'所有人都在问'),引发讨论,25字以内",
    "标题用时间/地点+事件(如'今日XX地发生YY'),信息感强,25字以内",
    "标题用专家解读视角(如'XX行业人士揭示YY真相'),权威感,25字以内",
    "标题用对比冲突(如'XX却让YY更难了'),制造张力,25字以内",
    "标题用清单式(如'关于XX,你需要知道的事'),实用感强,25字以内",
    "标题用动词+结果(如'XX教会我们YY'),启发性强,25字以内",
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
    "Create a specific scenario headline (like 'When X Does Y, The Result Is Z') with strong specificity, under 60 characters",
    "Use a person-action headline (like 'Expert Reveals The Secret Nobody Talks About') to build authority, under 60 characters",
    "Use a data-driven headline (like 'X People Are Now Doing Y - Here Is Why') with concrete numbers, under 60 characters",
    "Use a contrast headline (like 'X But Y Is Actually Getting Harder') to create tension, under 60 characters",
    "Create a helpful list headline (like 'Everything You Need to Know About X') for practical value, under 60 characters",
    "Use a news-anchor style headline (like 'X Just Announced Y, And It Changes Everything') for authority, under 60 characters",
    "Use an emotional resonance headline (like 'People Are Speaking Up About X - Here Is What They Say') for community feel, under 60 characters",
    "Use a How-To or guide headline (like 'How to X Without Y: A Complete Guide') for evergreen appeal, under 60 characters",
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
3. 分4-6个小节,每节有##小标题,小标题要包含关键词
4. 每个小节内容充实,有观点有例子
5. 自然插入3-5个长尾关键词变体(如同义词、相关词),不要堆砌
6. 在文章中间段落自然插入一个FAQ段落,用### 标记问题,紧跟简短回答(2-3句)
7. 结尾引导互动(提问或评论引导)
8. 语气口语化,避免"首先其次最后"这种僵硬表达
9. 不要出现"作为AI"、"本文由AI生成"等字样
10. 文章末尾加一行总结,用粗体标记核心关键词

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
7. Naturally include 3-5 long-tail keyword variations (synonyms, related terms), no keyword stuffing
8. Include a FAQ section in the middle using ### for questions, with brief 2-3 sentence answers
9. End with an engaging question or call-to-action
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

# ==================== 思维导图生成 ====================

def generate_mindmap_zh(title, body):
    """根据文章内容用AI生成思维导图大纲"""
    body_excerpt = body[:1800] if len(body) > 1800 else body
    prompt = f"""你是一个内容提炼专家。请根据以下文章提取"核心要点"卡片内容。

文章标题: {title}
文章内容(节选):
{body_excerpt}

要求:
1. 提炼4-6个核心要点，每个要点一句话（20字以内），直击要害
2. 每个要点用emoji符号开头，分类清晰（避免纯文字墙）
3. 格式：emoji + 要点标题 + 简短说明（1-2句）
4. 最后一行总结金句（1句话，25字以内）
5. 只输出内容，不要解释，不要markdown列表格式

输出示例:
[KEY] 关键结论：标题即观点，一句话说明白
[DATA] 数据支撑：文章中最有力的数字或事实
[?!] 反常识点：读者意想不到的那个真相
[HOT] 热度来源：为什么这件事现在很火
[+] 社会影响：对普通人有什么影响
[GOLD] 总结金句：一句话记住这篇文章"""
    try:
        token = get_zhipu_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3, "max_tokens": 400}
        resp = requests.post(API_URL, headers=headers, json=data, timeout=60)
        result = resp.json()
        if "choices" not in result:
            print(f"    脑图AI异常: {str(result)[:100]}")
            return _fallback_mindmap(body, "zh")
        content = result["choices"][0]["message"]["content"].strip()
        if '#' not in content:
            return _fallback_mindmap(body, "zh")
        return content
    except Exception as e:
        print(f"    脑图生成失败: {e}")
        return _fallback_mindmap(body, "zh")

def generate_mindmap_en(title, body):
    """根据英文文章用AI生成思维导图"""
    body_excerpt = body[:1800] if len(body) > 1800 else body
    prompt = f"""You are a mind map expert. Extract key points from this article into a mind map outline.

Title: {title}
Content (excerpt):
{body_excerpt}

Requirements:
1. Distill 4-6 core points, each one sentence (under 25 words), punchy and direct
2. Each point starts with an emoji, clearly categorized (no wall of text)
3. Format: emoji + point title + brief explanation (1-2 sentences)
4. End with a summary gold sentence (1 sentence, under 30 words)
5. Output only content, no explanation, no markdown list format

Output example:
[KEY] KEY INSIGHT: One sentence that nails the entire article
[DATA] DATA POINT: The most powerful number or fact from the piece
[?!] COUNTERINTUITIVE: The one truth readers won't expect
[HOT] WHY IT'S HOT: Why this topic is trending right now
[+] IMPACT: What it means for regular people
[GOLD] GOLD LINE: One memorable takeaway sentence"""
    try:
        token = get_zhipu_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3, "max_tokens": 400}
        resp = requests.post(API_URL, headers=headers, json=data, timeout=60)
        result = resp.json()
        if "choices" not in result:
            return _fallback_mindmap(body, "en")
        content = result["choices"][0]["message"]["content"].strip()
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
        if len(chinese_chars) > 3 or '#' not in content:
            return _fallback_mindmap(body, "en")
        return content
    except Exception as e:
        print(f"    Mindmap gen failed: {e}")
        return _fallback_mindmap(body, "en")

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

def add_to_manifest(slug, title, category, filename, lang="zh"):
    manifest = load_manifest(lang)
    # 用精确到秒的时间戳确保新文章永远排在最前面
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 插入到列表头部(最新的在最前面)
    manifest.insert(0, {"slug": slug, "title": title, "category": category, "date": datetime.now().strftime("%Y-%m-%d"), "timestamp": timestamp, "filename": filename})
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

def generate_article_html_zh(title, body, category, slug, related_articles, mindmap_text=""):
    cat_info = CATEGORIES.get(category, CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    html_body = _md2html(body)
    svg_hero = generate_svg_hero(title, category, "zh")
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
@media(max-width:480px){{.hero-svg{{margin:15px 0;border-radius:8px}}.cps-box{{padding:14px;margin:18px 0}}.cps-box li{{flex-direction:column;align-items:flex-start;gap:2px;padding:10px 0}}.cps-box a{{white-space:normal;font-size:.95em}}.cps-desc{{margin-top:2px}}.mindmap-section{{padding:14px}}}}
.share-box{{margin:20px 0;padding:15px 20px;background:#f0f8ff;border-radius:10px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;border:1px solid #d0e8ff}}
.share-box span{{color:#666;font-size:.9em;white-space:nowrap}}
.share-box a{{padding:6px 16px;border-radius:20px;text-decoration:none;font-size:.85em;font-weight:500;transition:all .2s}}
.share-box a:nth-child(2){{background:#ff5a4c;color:#fff}}
.share-box a:nth-child(3){{background:#1da1f2;color:#fff}}
.share-box a:nth-child(4){{background:#1877f2;color:#fff}}
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
<div class="meta"><span>📅 {date_str}</span> <span>{cat_icon} {cat_name}</span> {reading_time_html}</div>
{svg_hero}
{mindmap_block}
{html_body}
{disclaimer}
{_cps_block(category, "zh")}
{_related_block(related_articles, "zh")}
<div class="share-box">
<span>📤 分享：</span>
<a href="https://service.weibo.com/share/share.php?url={SITE_URL}/articles/{slug}.html&title={title}" target="_blank" rel="nofollow noopener">微博</a>
<a href="https://twitter.com/intent/tweet?url={SITE_URL}/articles/{slug}.html&text={title}" target="_blank" rel="nofollow noopener">Twitter</a>
<a href="https://www.facebook.com/sharer/sharer.php?u={SITE_URL}/articles/{slug}.html" target="_blank" rel="nofollow noopener">Facebook</a>
</div>
</article>
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025-2026 {SITE_NAME}</p>
<p><a href="/">首页</a><a href="/articles/hot.html">社会热点</a><a href="/articles/tech.html">科技数码</a><a href="/articles/health.html">健康养生</a><a href="/articles/life.html">生活百科</a><a href="/articles/entertainment.html">娱乐八卦</a><a href="/articles/finance.html">财经投资</a></p>
<p><a href="/about.html">About</a> | <a href="/privacy.html">Privacy</a> | <a href="/terms.html">Terms</a> | <a href="/dmca.html">DMCA</a> | <a href="/cookies.html">Cookies</a></p>
</div>
</body>
</html>"""

def generate_article_html_en(title, body, category, slug, related_articles, mindmap_text=""):
    cat_info = EN_CATEGORIES.get(category, EN_CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    html_body = _md2html(body)
    svg_hero = generate_svg_hero(title, category, "en")
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
@media(max-width:480px){{.hero-svg{{margin:15px 0;border-radius:8px}}.cps-box{{padding:14px;margin:18px 0}}.cps-box li{{flex-direction:column;align-items:flex-start;gap:2px;padding:10px 0}}.cps-box a{{white-space:normal;font-size:.95em}}.cps-desc{{margin-top:2px}}.mindmap-section{{padding:14px}}}}
.share-box{{margin:20px 0;padding:15px 20px;background:#f0f8ff;border-radius:10px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;border:1px solid #d0e8ff}}
.share-box span{{color:#666;font-size:.9em;white-space:nowrap}}
.share-box a{{padding:6px 16px;border-radius:20px;text-decoration:none;font-size:.85em;font-weight:500;transition:all .2s}}
.share-box a:nth-child(2){{background:#1da1f2;color:#fff}}
.share-box a:nth-child(3){{background:#1877f2;color:#fff}}
.share-box a:nth-child(4){{background:#ff4500;color:#fff}}
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
<div class="meta"><span>📅 {date_str}</span> <span>{cat_icon} {cat_name}</span> {reading_time_html}</div>
{svg_hero}
{mindmap_block}
{html_body}
{disclaimer}
{_cps_block(category, "en")}
{_related_block(related_articles, "en")}
<div class="share-box">
<span>📤 Share:</span>
<a href="https://twitter.com/intent/tweet?url={SITE_URL}/en/articles/{slug}.html&text={title}" target="_blank" rel="nofollow noopener">Twitter</a>
<a href="https://www.facebook.com/sharer/sharer.php?u={SITE_URL}/en/articles/{slug}.html" target="_blank" rel="nofollow noopener">Facebook</a>
<a href="https://www.reddit.com/submit?url={SITE_URL}/en/articles/{slug}.html&title={title}" target="_blank" rel="nofollow noopener">Reddit</a>
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
    articles = sorted([a for a in load_manifest("zh") if a["category"] == category], key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)[:50]
    list_items = "\n".join(f'<li><span class="thumb" style="background:{THUMB_COLORS.get(category,THUMB_COLORS["hot"])}">{cat_icon}</span><span class="date">{a.get("date","")}</span><a href="/articles/{a["filename"]}">{a["title"]}</a></li>' for a in articles) or '<li style="color:#999">暂无文章...</li>'
    cat_disclaimer = '<div style="background:#fff3e0;border:1px solid #ffcc80;border-radius:8px;padding:14px 18px;margin:25px 0;font-size:.85em;color:#8d6e63;text-align:center">⚠️ <strong>免责声明：</strong>本频道内容仅供学习参考，不构成任何投资建议。市场有风险，投资需谨慎。</div>' if category == "finance" else ""

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
.ad-slot{{margin:20px 0;text-align:center}}
.thumb{{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:6px;margin-right:8px;font-size:14px;flex-shrink:0;color:#fff}}
</style>
{GA4_CODE}
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
{cat_disclaimer}
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025-2026 {SITE_NAME}</p>
<p><a href="/">首页</a><a href="/articles/hot.html">社会热点</a><a href="/articles/tech.html">科技数码</a><a href="/articles/health.html">健康养生</a><a href="/articles/life.html">生活百科</a><a href="/articles/entertainment.html">娱乐八卦</a></p>
</div>
</body>
</html>"""

def generate_category_page_en(category):
    cat_info = EN_CATEGORIES.get(category, EN_CATEGORIES["hot"])
    cat_name, cat_icon = cat_info["name"], cat_info["icon"]
    articles = sorted([a for a in load_manifest("en") if a["category"] == category], key=lambda x: x.get("timestamp", x.get("date", "") + " 00:00:00"), reverse=True)[:50]
    list_items = "\n".join(f'<li><span class="thumb" style="background:{THUMB_COLORS.get(category,THUMB_COLORS["hot"])}">{cat_icon}</span><span class="date">{a.get("date","")}</span><a href="/en/articles/{a["filename"]}">{a["title"]}</a></li>' for a in articles) or '<li style="color:#999">No articles yet...</li>'
    cat_disclaimer = '<div style="background:#fff3e0;border:1px solid #ffcc80;border-radius:8px;padding:14px 18px;margin:25px 0;font-size:.85em;color:#8d6e63;text-align:center">⚠️ <strong>Disclaimer:</strong> Content is for informational purposes only and does not constitute investment advice. Invest at your own risk.</div>' if category == "finance" else ""

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
.ad-slot{{margin:20px 0;text-align:center}}
.thumb{{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:6px;margin-right:8px;font-size:14px;flex-shrink:0;color:#fff}}
</style>
{GA4_CODE}
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
{cat_disclaimer}
<div class="ad-slot">{AD_CODE_BOTTOM}</div>
<div class="footer">
<p>© 2025-2026 {EN_SITE_NAME}</p>
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
.site-header{{text-align:center;padding:25px 0 20px}}
.site-header h1{{font-size:1.8em;color:#1a1a1a;margin-bottom:5px}}
.site-header p{{color:#888;font-size:.95em}}
.lang-switch{{text-align:center;margin-bottom:15px}}
.lang-switch a{{color:#ff6b35;text-decoration:none;margin:0 10px;padding:5px 15px;border:1px solid #ff6b35;border-radius:20px}}
.lang-switch a:hover{{background:#ff6b35;color:#fff}}
.top-bar{{display:flex;justify-content:center;align-items:center;gap:15px;margin-bottom:10px}}
.contact-btn{{color:#2e7d32;text-decoration:none;font-size:.9em;cursor:pointer;border:1px solid #a5d6a7;padding:4px 14px;border-radius:20px;background:#e8f5e9}}
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
</div>
<div class="top-bar">
<div class="lang-switch">
<a href="/">&#x1F1E8;&#x1F1F3; &#x4E2D;&#x6587;</a> | <a href="/en/">&#x1F1FA;&#x1F1F8; English</a>
</div>
<a class="contact-btn" onclick="document.getElementById('contactBox').classList.add('show');document.getElementById('contactOverlay').classList.add('show')">&#x2709;&#xFE0F; &#x8054;&#x7CFB;&#x6211;&#x4EEC;</a>
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
<p><a href="/about.html">About</a> | <a href="/privacy.html">Privacy</a> | <a href="/terms.html">Terms</a> | <a href="/dmca.html">DMCA</a> | <a href="/cookies.html">Cookies</a></p>
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
.top-bar{{display:flex;justify-content:center;align-items:center;gap:15px;margin-bottom:10px}}
.contact-btn{{color:#2e7d32;text-decoration:none;font-size:.9em;cursor:pointer;border:1px solid #a5d6a7;padding:4px 14px;border-radius:20px;background:#e8f5e9}}
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
</div>
<div class="top-bar">
<div class="lang-switch">
<a href="/">中文</a> | <a href="/en/">English</a>
</div>
<a class="contact-btn" onclick="document.getElementById('contactBox').classList.add('show');document.getElementById('contactOverlay').classList.add('show')">✉️ Contact Us</a>
</div>
<div class="contact-overlay" id="contactOverlay" onclick="this.classList.remove('show');document.getElementById('contactBox').classList.remove('show')"></div>
<div class="contact-box" id="contactBox">
<h3>✉️ Contact Us</h3>
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
    """清理N天前的旧文章，保持仓库轻量"""
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

    # 1. 抓热点（中英文分离：中文用国内源，英文用国外源）
    topics_zh = get_hot_topics()
    topics_en = get_hot_topics_en()
    print(f"📋 中文话题: {len(topics_zh)} 个, 英文话题: {len(topics_en)} 个")

    # 2. 逐篇生成
    zh_generated, en_generated = 0, 0

    # 2a. 中文循环（使用国内热点：百度/微博/头条/知乎/财经）
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
                html_zh = generate_article_html_zh(title_zh, body_zh, category, slug_zh, related_zh, mindmap_zh)
                (OUTPUT_DIR / filename_zh).write_text(html_zh, encoding="utf-8")
                add_to_manifest(slug_zh, title_zh, category, filename_zh, "zh")
                zh_generated += 1
                print(f"    ✅ 中文完成: {filename_zh}")
            time.sleep(1)
        else:
            print(f"  ⏭ [ZH {i+1}/{len(topics_zh)}] 跳过(重复): {topic}")

    # 2b. 英文循环（使用国外热点：Reddit/HN/Twitter）
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
                html_en = generate_article_html_en(title_en, body_en, category, slug_en, related_en, mindmap_en)
                (EN_OUTPUT_DIR / filename_en).write_text(html_en, encoding="utf-8")
                add_to_manifest(slug_en, title_en, category, filename_en, "en")
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

if __name__ == "__main__":
    main()
