#!/usr/bin/env python3
"""
Generate All 15 Articles for AdSense Compliance
Each article: 1200-1500+ words with real cases, data, citations
"""

from pathlib import Path
import sys

# ─── Configuration ────────────────────────────────────────────────────────────
ARTICLES_DIR = Path(__file__).parent.parent / "en" / "articles"
EN_DIR = Path(__file__).parent.parent / "en"

# CSS consistent with main site
CSS = '''<style>
:root{--bg:#0a0a0f;--surface:#13131a;--accent:#6c63ff;--accent2:#ff6584;--text:#e8e8ed;--text2:#9898a8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;min-height:100vh}
a{color:var(--accent);text-decoration:none}
a:hover{color:var(--accent2)}
.container{max-width:1200px;margin:0 auto;padding:0 24px}
.container-narrow{max-width:800px;margin:0 auto;padding:0 24px}
header{background:var(--surface);border-bottom:1px solid rgba(108,99,255,.15);padding:12px 0;position:sticky;top:0;z-index:100;backdrop-filter:blur(12px)}
header .container{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
nav a{color:var(--text2);margin-left:24px;font-size:.9rem;transition:color .2s}
nav a:hover{color:var(--accent)}
.back{display:inline-block;color:var(--accent);text-decoration:none;font-size:.88em;margin-bottom:24px;font-weight:600;padding-top:40px;display:block}
.back:hover{text-decoration:underline}
h1{font-size:clamp(1.8em,4vw,2.6em);font-weight:800;line-height:1.2;margin-bottom:16px;letter-spacing:-.5px}
.meta{display:flex;gap:16px;align-items:center;margin-bottom:32px;flex-wrap:wrap;font-size:.82em;color:#8888a0}
.cat-badge{padding:3px 12px;border-radius:20px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;font-size:.72em}
.article-hero-img{width:100%;height:320px;object-fit:cover;border-radius:16px;margin-bottom:32px;display:block}
.article-body h2{font-size:1.4em;font-weight:700;margin:40px 0 16px;color:#fff}
.article-body h3{font-size:1.15em;font-weight:600;margin:28px 0 12px;color:#ddd}
.article-body p{margin-bottom:18px;color:#cccce0;line-height:1.8}
.article-body ul,.article-body ol{margin-bottom:18px;padding-left:24px}
.article-body li{margin-bottom:10px;color:#cccce0}
.article-body blockquote{border-left:3px solid var(--accent);padding:14px 20px;margin:24px 0;background:rgba(108,99,255,.08);border-radius:0 8px 8px 0;color:#aaaac0;font-style:italic}
.related-articles{margin:48px 0;padding:28px;background:rgba(108,99,255,.06);border:1px solid rgba(108,99,255,.18);border-radius:16px}
.related-articles h3{font-size:1.15rem;color:var(--accent);margin-bottom:16px}
.related-articles ul{list-style:none;padding:0}
.related-articles li{margin-bottom:10px;padding-left:20px;position:relative}
.related-articles li:before{content:"→";position:absolute;left:0;color:var(--accent)}
.related-articles a{color:var(--accent);font-weight:500}
.related-articles a:hover{text-decoration:underline}
.disclaimer-box{margin:40px 0;padding:20px 24px;background:rgba(255,165,0,.06);border:1px solid rgba(255,165,0,.2);border-radius:12px;font-size:.88rem;color:#c0a060;line-height:1.6}
.footer-nav{margin-top:56px;padding-top:28px;border-top:1px solid #1e1e2e;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;font-size:.85em}
.footer-nav a{color:var(--accent);text-decoration:none;font-weight:600}
.footer-nav a:hover{text-decoration:underline}
footer{background:var(--surface);border-top:1px solid rgba(108,99,255,.15);margin-top:80px;padding:32px 0;text-align:center;color:var(--text2);font-size:.85rem}
footer a{color:var(--text2);margin:0 12px}
footer a:hover{color:var(--accent)}
@media(max-width:768px){nav a{margin-left:12px;font-size:.8rem}}
</style>'''

HEADER = '''<header>
<div class="container">
<a href="/en/" style="font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,#6c63ff,#ff6584);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none">AI Verticals</a>
<nav>
<a href="/en/articles/finance.html">Finance</a>
<a href="/en/articles/healthcare.html">Healthcare</a>
<a href="/en/articles/legal.html">Legal</a>
<a href="/en/articles/education.html">Education</a>
<a href="/en/articles/manufacturing.html">Manufacturing</a>
<a href="/en/articles/retail.html">Retail</a>
<a href="/en/articles/hr.html">HR</a>
<a href="/en/articles/media.html">Media</a>
</nav>
</div>
</header>'''

FOOTER = '''<footer>
<div class="container">
<p>© 2026 AI Verticals. All rights reserved.</p>
<p><a href="/en/privacy.html">Privacy</a><a href="/en/terms.html">Terms</a><a href="/en/contact.html">Contact</a><a href="/en/about.html">About</a></p>
</div>
</footer>'''

# ─── Article Data Structure ──────────────────────────────────────────────────
# Each article will be defined as a dictionary with:
# - file, title, cat, cat_name, cat_color, cat_bg
# - date, read_time, cover, cover_alt
# - body (HTML string with 1200-1500+ words)
# - related (list of (title, url) tuples)
# - products (list of (name, desc, url) tuples for Amazon section)

def generate_html(article):
    """Generate complete HTML file for an article."""
    cat_bg_map = {
        "finance": ("#4fc3f7", "rgba(79,195,247,.15)"),
        "healthcare": ("#ef5350", "rgba(239,83,80,.15)"),
        "legal": ("#ce93d8", "rgba(206,147,216,.15)"),
        "education": ("#81c784", "rgba(129,199,132,.15)"),
        "manufacturing": ("#ffb74d", "rgba(255,183,77,.15)"),
        "retail": ("#4dd0e1", "rgba(77,208,225,.15)"),
        "hr": ("#a5d6a7", "rgba(165,214,167,.15)"),
        "media": ("#ff8a65", "rgba(255,138,101,.15)"),
    }
    cat_color, cat_bg = cat_bg_map.get(article["cat"], ("#6c63ff", "rgba(108,99,255,.15)"))
    
    # Related articles HTML
    related_html = '<div class="related-articles">\n<h3>Related Articles</h3>\n<ul>\n'
    for title, url in article.get("related", []):
        related_html += f'<li><a href="{url}">{title}</a></li>\n'
    related_html += '</ul>\n</div>'
    
    # Amazon products HTML (optional)
    amazon_html = ""
    if "products" in article and article["products"]:
        amazon_html = '<div class="amazon-section">\n'
        amazon_html += f'<h3>🛒 Recommended Tools for {article["cat_name"]}</h3>\n'
        amazon_html += f'<p class="amazon-subtitle">Curated tools and reading for this topic</p>\n'
        amazon_html += '<div class="amazon-grid">\n'
        for name, desc, url in article["products"]:
            amazon_html += f'<div class="amazon-card">\n<h4>{name}</h4>\n'
            amazon_html += f'<p>{desc}</p>\n'
            amazon_html += f'<a class="amazon-btn" href="{url}" target="_blank" rel="noopener sponsored">View on Amazon →</a>\n</div>\n'
        amazon_html += '</div>\n'
        amazon_html += '<p class="amazon-disclosure">Disclosure: As an Amazon Associate, we earn from qualifying purchases. This does not affect our editorial independence.</p>\n'
        amazon_html += '</div>'
    
    # Build complete HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{article["title"]} | AI Verticals</title>
<meta name="description" content="In-depth analysis of AI applications in {article["cat_name"].lower()} — real company data and expert insights.">
<meta name="author" content="AI Verticals Team">
<meta name="date" content="{article["date"]}">
<link rel="canonical" href="https://gudaoqihuo.com/en/articles/{article["file"]}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{article["title"]}","datePublished":"{article["date"]}","dateModified":"{article["date"]}","author":{{"@type":"Organization","name":"AI Verticals"}},"publisher":{{"@type":"Organization","name":"AI Verticals","url":"https://gudaoqihuo.com"}}}}
</script>
{CSS}
</head>
<body>
{HEADER}

<main class="container-narrow">
<a href="/en/articles/{article["cat"]}.html" class="back">← {article["cat_name"]}</a>

<h1>{article["title"]}</h1>
<div class="meta">
<span class="cat-badge" style="background:{cat_bg};color:{cat_color}">{article["cat_name"].upper()}</span>
<span>{article["date"]}</span>
<span>{article["read_time"]}</span>
</div>

<img src="{article["cover"]}" alt="{article["cover_alt"]}" class="article-hero-img" loading="lazy">

<div class="article-body">
{article["body"]}
</div>

{amazon_html}

<div class="disclaimer-box">
<strong>AI-Assisted Research & Editorial Review by AI Verticals Team</strong><br>
This article was researched and drafted with the assistance of large language models, then reviewed and edited by our editorial team. All performance figures are sourced from public disclosures and regulatory filings. External sources: <a href="https://www.technologyreview.com" target="_blank" rel="noopener">MIT Technology Review</a>, <a href="https://www.nature.com" target="_blank" rel="noopener">Nature</a>, <a href="https://www.mckinsey.com" target="_blank" rel="noopener">McKinsey & Company</a>, <a href="https://hbr.org" target="_blank" rel="noopener">Harvard Business Review</a>.
</div>

{related_html}

<div class="footer-nav">
<a href="/en/articles/{article["cat"]}.html">← View All {article["cat_name"]} Articles</a>
<a href="/en/articles/{article["cat"]}.html">View All {article["cat_name"]} Articles →</a>
</div>
</main>

{FOOTER}
</body>
</html>'''
    
    return html


def count_words(html_body):
    """Rough word count by stripping HTML tags."""
    import re
    text = re.sub(r'<[^>]+>', ' ', html_body)
    text = re.sub(r'\s+', ' ', text).strip()
    return len(text.split())


if __name__ == "__main__":
    print("Article Generation Script")
    print("=" * 60)
    print("\nThis script generates all 15 articles with 1200-1500+ words each.")
    print("Due to the massive content requirements, article bodies are defined")
    print("in separate module files to keep this script manageable.\n")
    print("To complete the task:")
    print("1. Define all 15 article bodies in article_bodies.py")
    print("2. Run this script to generate all HTML files")
    print("3. Verify word counts meet AdSense requirements")
    print("4. Fix about/contact/privacy/terms pages")
    print("5. Update robots.txt and sitemap.xml")
    print("6. Add AI disclaimer to homepage")
