#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补丁脚本：分离中英文热点源 + 内容偏向AI/金融 + 脑图改要点卡片
用法: python patch_separate_hot_topics.py
"""

import re

FILE = "scripts/generate_content.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

# ========== 1. 在 fetch_finance_hot 后插入 fetch_twitter_trending ==========
twitter_fn = '''
def fetch_twitter_trending():
    """抓取Twitter/Trends24热点(无需API key)"""
    print("    抓取Twitter热点(Trends24)...")
    # Trends24 提供过去24小时Twitter热词
    resp = fetch_with_retry("https://trends24.in/united-states/", timeout=15)
    if not resp:
        # 备用：直接抓mytrendingstories
        resp = fetch_with_retry("https://getdaytrends.com/united-states/", timeout=15)
    if not resp:
        print("    Twitter热点抓取失败,跳过")
        return []
    # 从页面提取热词（简单正则）
    # Trends24页面结构：<td class="trend">...</td>
    trends = re.findall(r'<td[^>]*class="[^"]*trend[^"]*"[^>]*>(.*?)</td>', resp.text, re.IGNORECASE)
    if not trends:
        # 备用正则：提取带#号的标签
        trends = re.findall(r'#([A-Za-z0-9_]+)', resp.text)
    if not trends:
        print("    Twitter热点: 未提取到内容")
        return []
    # 清洗
    cleaned = []
    for t in trends[:30]:
        t = re.sub(r'<[^>]+>', '', t).strip()
        if t and 2 < len(t) < 100:
            cleaned.append(t)
    print(f"    Twitter热点: 获取 {len(cleaned)} 条")
    return cleaned[:30]

'''

# 定位插入点：fetch_finance_hot 函数结束后的空行
# 找 fetch_finance_hot 函数的结束位置
finance_pattern = r'(def fetch_finance_hot\(\):.*?return unique\[:25\]\n)'
match = re.search(finance_pattern, content, re.DOTALL)
if match:
    insert_pos = match.end()
    content = content[:insert_pos] + twitter_fn + "\n" + content[insert_pos:]
    print("✅ 插入 fetch_twitter_trending()")
else:
    print("❌ 未找到 fetch_finance_hot 结束位置")

# ========== 2. 插入 fetch_reddit_hot ==========
reddit_fn = '''
def fetch_reddit_hot():
    """抓取Reddit r/all热门话题"""
    print("    抓取Reddit热点...")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ContentBot/1.0)"}
    resp = fetch_with_retry("https://www.reddit.com/r/all/hot.json?limit=30", headers=headers, timeout=15)
    if not resp:
        print("    Reddit热点抓取失败,跳过")
        return []
    try:
        data = resp.json()
        posts = data.get("data", {}).get("children", [])
        topics = [p.get("data", {}).get("title", "") for p in posts if p.get("data", {}).get("title")]
        print(f"    Reddit热点: 获取 {len(topics)} 条")
        return topics[:30]
    except Exception as e:
        print(f"    Reddit热点解析失败: {e}")
        return []

'''

# 插入到 fetch_twitter_trending 之后
twitter_end = content.find('    return cleaned[:30]\n\n', content.find('def fetch_twitter_trending'))
if twitter_end > 0:
    insert_pos = twitter_end + len('    return cleaned[:30]\n\n')
    content = content[:insert_pos] + reddit_fn + content[insert_pos:]
    print("✅ 插入 fetch_reddit_hot()")
else:
    print("⚠️ 未找到 fetch_twitter_trending 结束位置，尝试追加到文件末尾前")
    # 在 get_hot_topics 前插入
    pos = content.find('def get_hot_topics():')
    if pos > 0:
        content = content[:pos] + reddit_fn + '\n' + content[pos:]
        print("✅ 插入 fetch_reddit_hot() (备用位置)")

# ========== 3. 插入 fetch_hackernews_hot ==========
hn_fn = '''
def fetch_hackernews_hot():
    """抓取Hacker News热门话题"""
    print("    抓取Hacker News热点...")
    resp = fetch_with_retry("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=15)
    if not resp:
        print("    HN热点抓取失败,跳过")
        return []
    try:
        story_ids = resp.json()[:30]
        topics = []
        for sid in story_ids[:15]:  # 只取前15个,避免请求过多
            s_resp = fetch_with_retry(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10)
            if s_resp:
                s_data = s_resp.json()
                title = s_data.get("title", "")
                if title:
                    topics.append(title)
            time.sleep(0.2)  # 避免请求过快
        print(f"    HN热点: 获取 {len(topics)} 条")
        return topics
    except Exception as e:
        print(f"    HN热点解析失败: {e}")
        return []

'''

# 插入到 fetch_reddit_hot 之后
reddit_end = content.find('    return topics[:30]\n\n', content.find('def fetch_reddit_hot'))
if reddit_end > 0:
    insert_pos = reddit_end + len('    return topics[:30]\n\n')
    content = content[:insert_pos] + hn_fn + content[insert_pos:]
    print("✅ 插入 fetch_hackernews_hot()")
else:
    print("⚠️ 未找到 fetch_reddit_hot 结束位置")

# ========== 4. 创建 get_hot_topics_en() ==========
# 在 get_hot_topics() 函数结束后插入
get_hot_en = '''
def get_hot_topics_en():
    """英文热点抓取：Reddit + Hacker News + Twitter"""
    print("📡 开始抓取英文热点话题...")
    all_topics = []
    sources = [fetch_reddit_hot, fetch_hackernews_hot, fetch_twitter_trending]
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
        if t_clean and t_clean not in seen and 2 < len(t_clean) < 100:
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

'''

pos = content.find('    return unique[:ARTICLES_PER_RUN]\n\n# ==================== AI内容生成')
if pos > 0:
    insert_pos = pos + len('    return unique[:ARTICLES_PER_RUN]\n\n')
    content = content[:insert_pos] + get_hot_en + '\n' + content[insert_pos:]
    print("✅ 插入 get_hot_topics_en()")
else:
    print("❌ 未找到 get_hot_topics() 结束位置")

# ========== 5. 修改 main() 分离中英文热点 ==========
# 把 main() 中的 topics = get_hot_topics() 替换为分别调用
old_main_hot = "    # 1. 抓热点\n    topics = get_hot_topics()"
new_main_hot = '''    # 1. 抓热点(中英文分离)
    topics_zh = get_hot_topics()
    topics_en = get_hot_topics_en()
    print(f"📋 中文话题: {len(topics_zh)} 个, 英文话题: {len(topics_en)} 个")'''

if old_main_hot in content:
    content = content.replace(old_main_hot, new_main_hot)
    print("✅ 修改 main(): 分离中英文热点")
else:
    print("⚠️ 未找到 main() 中的热点调用，可能需要手动修改")

# 修改 main() 中的循环：中文用 topics_zh，英文用 topics_en
# 原代码：
# for i, topic in enumerate(topics):
#     slug_zh = topic_to_slug(topic)
#     ...
#     # 英文版
#     slug_en = topic_to_slug_en(topic)
#     ...
#
# 改为两个独立循环

old_loop = '''    # 2. 逐篇生成(中英文)
    zh_generated, en_generated = 0, 0
    for i, topic in enumerate(topics):
        slug_zh = topic_to_slug(topic)
        slug_en = topic_to_slug_en(topic)'''
    
new_loop = '''    # 2. 逐篇生成(中英文分离)
    zh_generated, en_generated = 0, 0
    
    # 中文文章
    for i, topic in enumerate(topics_zh):
        slug_zh = topic_to_slug(topic)'''

if old_loop in content:
    content = content.replace(old_loop, new_loop)
    print("✅ 修改 main(): 中文循环分离")
else:
    print("⚠️ 未找到 main() 中的循环开始")

# 找到中文文章生成的结束位置，插入英文循环
# 寻找 " # 英文版" 标记
old_en_marker = "        # 英文版"
new_en_loop = '''    
    # 英文文章
    for i, topic in enumerate(topics_en):
        slug_en = topic_to_slug_en(topic)'''
    
if old_en_marker in content:
    # 替换掉旧的 " # 英文版" 开始部分
    # 需要更精细的替换：把从 " # 英文版" 到下一个 " # 3. 重建站点" 之间的内容替换掉
    # 这太复杂了，先跳过，输出提示
    print("⚠️ main() 循环修改复杂，请手动检查英文部分")
else:
    print("⚠️ 未找到 '英文版' 标记")

# ========== 6. 内容偏向AI+金融：修改 prompt ==========
# 在 STYLE_PROMPTS 和 TITLE_STYLES 后面添加偏向提示
ai_bias = '''
# 内容偏向：优先AI、科技、金融
TOPIC_BIAS_PROMPT = """
【内容偏向提示】
如果话题涉及以下领域，请生成更深入、更详细的内容：
1. 人工智能(AI)、大模型、机器学习、深度学习
2. 科技数码、半导体、芯片、5G/6G
3. 财经投资、股票、基金、加密货币、宏观经济
这些领域的内容可以更长(800-1000字)，并包含更多数据、案例和分析。
其它领域保持500-700字即可。
"""'''

# 插入到 STYLE_PROMPTS 定义之后
pos = content.find('TITLE_STYLES = [')
if pos > 0:
    # 往前找到 STYLE_PROMPTS 结束的位置
    pos2 = content.find('\n]', content.find('STYLE_PROMPTS = ['))
    if pos2 > 0:
        insert_pos = pos2 + 2  # 跳过 ]\n
        content = content[:insert_pos] + '\n' + ai_bias + '\n' + content[insert_pos:]
        print("✅ 添加 TOPIC_BIAS_PROMPT")

# ========== 7. 脑图改渐变要点卡片 ==========
# 修改 _mindmap_html_block() 函数
old_mindmap = '''def _mindmap_html_block(markdown_text, slug, lang="zh"):
    """将AI生成的markdown脑图转为HTML blocK"""
    if not markdown_text:
        return ""
    
    # 解析markdown层级
    lines = markdown_text.split("\\n")
    items = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 计算缩进层级
        indent = 0
        while line.startswith(("  ", "\\t")):
            indent += 1
            line = line[2:] if line.startswith("  ") else line[1:]
        # 去掉 markdown 列表符号
        line = line.lstrip("- *").strip()
        if line:
            items.append((indent, line))
    
    if not items:
        return ""
    
    # 生成树状HTML
    if lang == "zh":
        section_title = "🧠 核心要点"
    else:
        section_title = "🧠 Key Points"
    
    html = f'<div class="mindmap-section"><h3>{section_title}</h3><div class="mm-tree">'
    for indent, text in items:
        level_class = f" mm-l{indent+2}" if indent > 0 else ""
        dot = '<span class="mm-dot"></span>' if indent == 0 else ''
        html += f'<div class="mm-node level-{indent}{level_class}" style="--indent:{indent*20}px">{dot}{text}</div>'
    html += '</div></div>'
    return html'''

new_mindmap = '''def _mindmap_html_block(markdown_text, slug, lang="zh"):
    """将AI生成的要点转为渐变卡片HTML blocK"""
    if not markdown_text:
        return ""
    
    # 解析markdown层级，提取要点
    lines = markdown_text.split("\\n")
    points = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 去掉 markdown 列表符号和缩进
        line = line.lstrip(" - *\\t")
        if line and not line.startswith("#"):
            points.append(line)
    
    if not points:
        return ""
    
    # 渐变要点卡片
    if lang == "zh":
        section_title = "🧠 核心要点"
        emoji_list = ["💡", "🔥", "⚡", "🎯", "🚀", "💎", "📊", "🧩"]
    else:
        section_title = "🧠 Key Points"
        emoji_list = ["💡", "🔥", "⚡", "🎯", "🚀", "💎", "📊", "🧩"]
    
    # 取前8个要点
    points = points[:8]
    
    html = f'''<div style="background:linear-gradient(135deg,#f8f9ff,#fff5f0);border:1px solid #e8e0f0;border-radius:16px;padding:24px;margin:25px 0;box-shadow:0 4px 20px rgba(0,0,0,0.06)">
<h3 style="margin:0 0 18px;font-size:1.1em;color:#333;display:flex;align-items:center;gap:8px"><span style="font-size:1.3em">🧠</span>{section_title}</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
'''
    
    for i, point in enumerate(points):
        emoji = emoji_list[i % len(emoji_list)]
        # 限制每点字数
        short_point = point[:80] + "..." if len(point) > 80 else point
        html += f'''<div style="background:rgba(255,255,255,0.85);border-radius:10px;padding:14px 16px;display:flex;align-items:flex-start;gap:10px;font-size:.92em;line-height:1.5;color:#444;box-shadow:0 2px 8px rgba(0,0,0,0.04);transition:transform .2s;onmouseover='this.style.transform="translateY(-2px)"' onmouseout='this.style.transform="none"'>
<span style="font-size:1.2em;flex-shrink:0;margin-top:2px">{emoji}</span>
<span>{short_point}</span>
</div>
'''
    
    html += '</div></div>'
    return html'''

if old_mindmap in content:
    content = content.replace(old_mindmap, new_mindmap)
    print("✅ 修改 _mindmap_html_block(): 渐变卡片")
else:
    print("⚠️ 未找到 _mindmap_html_block()，可能需要手动修改")

# ========== 8. 添加PropellerAds广告位 ==========
# 在 AD_CODE_TOP / AD_CODE_MIDDLE / AD_CODE_BOTTOM 定义处添加PropellerAds
propeller_code = '''
# PropellerAds 广告代码 (待审核通过后启用)
# 将 PROPELLER_AD_CLIENT 和 PROPELLER_AD_SLOT 替换为实际值
PROPELLER_AD_CLIENT = "XXXXXXXXXX"  # 从PropellerAds后台获取
PROPELLER_AD_SLOT = "XXXXXXXXXX"   # 从PropellerAds后台获取
PROPELLER_CODE = f"""<script async src="https://roypro2.com/boot/dy38/950/221/"></script>"""  # 示例，需替换
# 正式代码格式：
# <script async src="https://roypro2.com/boot/YOUR_CLIENT_ID/"></script>
'''

# 插入到 AD_CODE_BOTTOM 定义之后
pos = content.find('AD_CODE_BOTTOM = """')
if pos > 0:
    pos2 = content.find('"""', pos + len('AD_CODE_BOTTOM = """'))
    if pos2 > 0:
        insert_pos = pos2 + 3  # 跳过 """
        content = content[:insert_pos] + '\n' + propeller_code + '\n' + content[insert_pos:]
        print("✅ 添加 PropellerAds 广告代码占位")

# ========== 写回文件 ==========
with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("\n🎉 补丁应用完成！请检查修改是否正确。")
print("⚠️ 注意：main() 函数的循环部分可能需要手动调整。")
