#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精准补丁：插入 get_hot_topics_en() + 修改 main() 分离中英文热点
用法: python patch_v2.py
"""

import re

FILE = "scripts/generate_content.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

# ========== 1. 在 get_hot_topics() 后插入 get_hot_topics_en() ==========
# 定位标记：AI内容生成 注释
marker = "# ==================== AI内容生成 ===================="
insert_pos = content.find(marker)

if insert_pos > 0:
    # 在新函数前加两个换行
    new_func = '''

def get_hot_topics_en():
    """英文热点抓取：Reddit + Hacker News + Twitter"""
    print("📡 开始抓取英文热点话题...")
    all_topics = []
    
    # Reddit热点
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
            # 提取带#号的热词
            trends = re.findall(r'#([A-Za-z0-9_]+)', resp.text)
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
    
    content = content[:insert_pos] + new_func + marker + content[insert_pos + len(marker):]
    print("✅ 插入 get_hot_topics_en()")
else:
    print("❌ 未找到插入位置（AI内容生成标记）")

# ========== 2. 修改 main() 分离中英文热点 ==========
# 把 "topics = get_hot_topics()" 替换为分别调用
old_call = "    # 1. 抓热点\n    topics = get_hot_topics()"
new_call = '''    # 1. 抓热点(中英文分离)
    topics_zh = get_hot_topics()
    topics_en = get_hot_topics_en()
    print(f"📋 中文话题: {len(topics_zh)} 个, 英文话题: {len(topics_en)} 个")'''

if old_call in content:
    content = content.replace(old_call, new_call)
    print("✅ 修改 main(): 分离中英文热点调用")
else:
    print("⚠️ 未找到 main() 中的热点调用")

# ========== 3. 修改循环：中文用 topics_zh，英文用 topics_en ==========
# 原代码：for i, topic in enumerate(topics):
# 改为：for i, topic in enumerate(topics_zh):
old_loop = "    for i, topic in enumerate(topics):\n        slug_zh = topic_to_slug(topic)"
new_loop = "    for i, topic in enumerate(topics_zh):\n        slug_zh = topic_to_slug(topic)"

if old_loop in content:
    content = content.replace(old_loop, new_loop)
    print("✅ 修改 main(): 中文循环使用 topics_zh")
else:
    print("⚠️ 未找到中文循环")

# 英文循环：在中文循环后添加（复杂，先跳过，输出提示）
print("⚠️ 英文循环需要手动调整（在中文循环后添加 topics_en 循环）")

# ========== 4. 内容偏向AI+金融：修改 prompt ==========
# 在 generate_article_zh 的 prompt 中添加偏向提示
old_prompt_zh = "请根据以下热门话题写一篇1200-1800字的文章。"
new_prompt_zh = """请根据以下热门话题写一篇1200-1800字的文章。

**内容偏向提示**（如果适用）：
- 如果话题涉及人工智能(AI)、大模型、机器学习，请生成更深入的内容（可写到1800字），包含最新案例、数据和技术趋势。
- 如果话题涉及科技数码、芯片、5G/6G，请包含产品对比、参数分析和购买建议。
- 如果话题涉及财经投资、股票、基金、加密货币，请包含数据分析、市场趋势和风险提示。
- 优先选择上述领域的话题进行深入报道。"""

if old_prompt_zh in content:
    content = content.replace(old_prompt_zh, new_prompt_zh)
    print("✅ 修改中文 prompt: 添加AI/金融偏向")
else:
    print("⚠️ 未找到中文 prompt（可能已修改）")

# ========== 5. 脑图改渐变要点卡片 ==========
# 修改 _mindmap_html_block() 函数
old_mindmap = '''def _mindmap_html_block(markdown_text, slug, lang="zh"):
    """将AI生成的markdown脑图转为HTML block"""
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
    """将AI生成的要点转为渐变卡片HTML"""
    if not markdown_text:
        return ""
    
    # 解析markdown，提取要点
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
    
    # 取前8个要点，生成渐变卡片
    points = points[:8]
    
    if lang == "zh":
        section_title = "🧠 核心要点"
    else:
        section_title = "🧠 Key Points"
    
    # 渐变卡片HTML
    html = f'''<div style="background:linear-gradient(135deg,#f8f9ff,#fff5f0);border:1px solid #e8e0f0;border-radius:16px;padding:24px;margin:25px 0;box-shadow:0 4px 20px rgba(0,0,0,0.06)">
<h3 style="margin:0 0 18px;font-size:1.1em;color:#333;display:flex;align-items:center;gap:8px"><span style="font-size:1.3em">🧠</span>{section_title}</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
'''
    
    emoji_list = ["💡", "🔥", "⚡", "🎯", "🚀", "💎", "📊", "🧩"]
    
    for i, point in enumerate(points):
        emoji = emoji_list[i % len(emoji_list)]
        # 限制每点字数
        short_point = point[:80] + "..." if len(point) > 80 else point
        html += f'''<div style="background:rgba(255,255,255,0.85);border-radius:10px;padding:14px 16px;display:flex;align-items:flex-start;gap:10px;font-size:.92em;line-height:1.5;color:#444;box-shadow:0 2px 8px rgba(0,0,0,0.04);transition:transform .2s" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
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
    print("⚠️ 未找到 _mindmap_html_block()（可能已修改）")

# ========== 6. 添加 PropellerAds 广告位占位 ==========
# 在配置区添加占位变量
propeller_placeholder = '''
# PropellerAds 广告代码 (审核通过后替换)
# 注册地址: https://propellerads.com/
# 登录后台获取 Client ID 和 Ad Slot ID
PROPELLER_AD_CLIENT = "XXXXXXXXX"  # 替换为实际值
PROPELLER_AD_SLOT = "XXXXXXXXX"   # 替换为实际值
# 广告代码格式示例:
# <script async src="https://royprop2.com/boot/XXX/"></script>
'''

# 插入到 AD_CODE_BOTTOM 定义之后
ad_bottom_pos = content.find('AD_CODE_BOTTOM = """')
if ad_bottom_pos > 0:
    # 找到 AD_CODE_BOTTOM 定义的结束位置
    ad_end = content.find('"""', ad_bottom_pos + len('AD_CODE_BOTTOM = """'))
    if ad_end > 0:
        insert_pos = ad_end + 3  # 跳过 """
        content = content[:insert_pos] + '\n' + propeller_placeholder + '\n' + content[insert_pos:]
        print("✅ 添加 PropellerAds 广告代码占位")
    else:
        print("⚠️ 未找到 AD_CODE_BOTTOM 结束位置")
else:
    print("⚠️ 未找到 AD_CODE_BOTTOM 定义")

# ========== 写回文件 ==========
with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("\n🎉 补丁应用完成！")
print("\n⚠️ 重要提示:")
print("1. main() 中的英文循环需要手动调整")
print("2. 请测试 generate_content.py 是否能正常运行")
print("3. PropellerAds 审核通过后再替换占位代码")
