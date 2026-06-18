#!/usr/bin/env python3
"""
polish_16_articles.py — Rewrite all 16 articles to 800-1200 words of genuine quality.
Called from an auto-content workflow dispatch. Requires ZHIPU_API_KEY in env.
"""
import json, os, re, sys, requests, time, base64
from datetime import datetime

API_KEY = os.environ.get("ZHIPU_API_KEY", "")
MODEL = "glm-4-flash"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
REPO = "xiaokangjiao-ai/gudaoqihuo"
BRANCH = "main"

ARTICLES_PATH = "en/articles"
MANIFEST_PATH = "en/articles/manifest.json"
GH_TOKEN = os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def gh_api(method, path, data=None):
    headers = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    url = f"https://api.github.com/repos/{REPO}/{path.lstrip('/')}"
    r = requests.request(method, url, headers=headers, json=data, timeout=30)
    if r.status_code not in (200, 201):
        print(f"  gh_api {method} {path}: {r.status_code} {r.text[:200]}", file=sys.stderr)
    return r

def get_zhipu_token():
    if not API_KEY:
        raise ValueError("ZHIPU_API_KEY not set")
    try:
        from jwt import encode
        headers = {"alg": "HS256", "sign_type": "SIGN"}
        payload = {
            "api_key": API_KEY,
            "exp": int(time.time()) + 3600,
            "timestamp": int(time.time() * 1000)
        }
        return encode(payload, API_KEY, algorithm="HS256", headers=headers)
    except Exception as e:
        print(f"  Token gen failed: {e}, trying direct key…", file=sys.stderr)
        return API_KEY

def read_file_sha(path):
    r = gh_api("GET", f"contents/{path}?ref={BRANCH}")
    if r.status_code == 200:
        return r.json()["sha"], base64.b64decode(r.json()["content"]).decode("utf-8", errors="replace")
    if r.status_code == 404:
        return None, ""
    return None, ""

def push_file(path, content_utf8, sha, message):
    b64 = base64.b64encode(content_utf8.encode("utf-8")).decode("ascii")
    data = {"message": message, "content": b64, "sha": sha, "branch": BRANCH}
    r = gh_api("PUT", f"contents/{path}", data)
    return r.status_code in (200, 201)

def call_ai(prompt, max_tokens=3000, temperature=0.7):
    token = get_zhipu_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    resp = requests.post(API_URL, headers=headers, json=data, timeout=180)
    result = resp.json()
    if "choices" not in result:
        raise RuntimeError(f"AI API error: {result.get('error', result)}")
    return result["choices"][0]["message"]["content"]

def build_article_html(file, title, cat, body_html, date_str):
    cat_slug = cat.lower()
    badge_color_map = {
        "finance": "rgba(79,195,247,.15);color:#4fc3f7",
        "healthcare": "rgba(239,83,80,.15);color:#ef5350",
        "legal": "rgba(206,147,216,.15);color:#ce93d8",
        "education": "rgba(129,199,132,.15);color:#81c784",
        "manufacturing": "rgba(255,183,77,.15);color:#ffb74d",
        "retail": "rgba(77,208,225,.15);color:#4dd0e1",
        "hr": "rgba(165,214,167,.15);color:#a5d6a7",
        "media": "rgba(255,138,101,.15);color:#ff8a65"
    }
    badge_color = badge_color_map.get(cat_slug, "rgba(108,99,255,.15);color:#6c63ff")

    # Build body — process markdown-ish content into HTML
    body_html = re.sub(r'### (.+)', r'<h3>\1</h3>', body_html)
    body_html = re.sub(r'## (.+)', r'<h2>\1</h2>', body_html)
    body_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body_html)
    body_html = re.sub(r'(?m)^\d+\.\s+(.+)$', lambda m: f'<li>{m.group(1)}</li>', body_html)
    body_html = re.sub(r'(?m)^[-*]\s+(.+)$', lambda m: f'<li>{m.group(1)}</li>', body_html)
    # Wrap consecutive li in ul
    body_html = re.sub(r'(<li>.*?(?:\n<li>.*?)*)', r'<ul>\1</ul>', body_html)
    body_html = re.sub(r'</ul>\s*<ul>', '', body_html)
    body_html = body_html.replace('\n\n', '</p><p>').replace('\n', ' ')
    body_html = re.sub(r'<p>(.*?)</p>', lambda m: f'<p>{m.group(1)}</p>' if m.group(1).strip() else '', body_html)
    body_html = '<p>' + body_html + '</p>'
    body_html = re.sub(r'<p>\s*</p>', '', body_html)
    body_html = re.sub(r'<ul><p>', '<ul>', body_html)
    body_html = re.sub(r'</p></ul>', '</ul>', body_html)

    desc_match = re.search(r'<p>(.+?)[.!?]', body_html[:300])
    meta_desc = (desc_match.group(1) + '.') if desc_match else f"Deep dive into {title}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | AI Verticals</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://gudaoqihuo.com/en/articles/{file}">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0a0a0f;color:#e8e8f0;line-height:1.7;min-height:100vh}}
.container{{max-width:800px;margin:0 auto;padding:40px 24px 60px}}
.back{{display:inline-block;color:#6c63ff;text-decoration:none;font-size:.88em;margin-bottom:24px;font-weight:600}}.back:hover{{text-decoration:underline}}
h1{{font-size:clamp(1.8em,4vw,2.6em);font-weight:800;line-height:1.2;margin-bottom:16px;letter-spacing:-.5px}}
.meta{{display:flex;gap:16px;align-items:center;margin-bottom:32px;flex-wrap:wrap;font-size:.82em;color:#8888a0}}
.cat-badge{{padding:3px 12px;border-radius:20px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;font-size:.72em}}
.cat-badge.{cat_slug}{{background:{badge_color}}}
.article-body h2{{font-size:1.4em;font-weight:700;margin:32px 0 12px;color:#fff}}
.article-body h3{{font-size:1.15em;font-weight:600;margin:24px 0 10px;color:#ddd}}
.article-body p{{margin-bottom:16px;color:#cccce0}}
.article-body ul{{margin-bottom:16px;padding-left:20px}}
.article-body li{{margin-bottom:8px;color:#cccce0}}
.article-body blockquote{{border-left:3px solid #6c63ff;padding:12px 20px;margin:20px 0;background:rgba(108,99,255,.08);border-radius:0 8px 8px 0;color:#aaaac0}}
.footer-nav{{margin-top:48px;padding-top:24px;border-top:1px solid #1e1e2e;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;font-size:.85em}}
.footer-nav a{{color:#6c63ff;text-decoration:none;font-weight:600}}.footer-nav a:hover{{text-decoration:underline}}
</style>
</head>
<body>
<div class="container">
<a href="/en/articles/{cat_slug}.html" class="back">← Back to {cat.title()}</a>
<h1>{title}</h1>
<div class="meta">
<span class="cat-badge {cat_slug}">{cat_slug}</span>
<span>{date_str}</span>
</div>
<article class="article-body">
{body_html}
<div style="margin-top:40px;padding:20px;background:#13131a;border:1px solid #1e1e2e;border-radius:12px;font-size:0.82em;color:#8888a0;line-height:1.7">
<strong>Disclaimer:</strong> The analysis provided on AI Verticals is for informational purposes only and does not constitute financial, investment, legal, or medical advice. Always consult qualified professionals before making decisions based on this content.
</div>
</article>
<div class="footer-nav">
<a href="/">Home</a>
<a href="/en/privacy.html">Privacy Policy</a>
<a href="/en/terms.html">Terms of Service</a>
</div>
</div>
</body>
</html>"""
    return html

def generate_topic_content(title, cat, slug):
    """Generate 800-1200 word article body for a specific topic."""
    angle_guides = {
        "finance": "Focus on real-world ROI, adoption metrics at major institutions, specific algorithms/models used, and concrete dollar figures. Include named banks, fintech companies, and regulatory frameworks.",
        "healthcare": "Focus on clinical outcomes, FDA/regulatory approval timelines, specific accuracy metrics vs human baselines, cost savings at hospital systems. Name specific hospitals and research institutions.",
        "legal": "Focus on billable hour disruption, accuracy benchmarks vs human paralegals, specific law firm adoption cases, court acceptance of AI-generated materials. Name specific law firms and legal tech companies.",
        "education": "Focus on learning outcome improvements, school district adoption data, personalized learning efficacy metrics, cost per student reductions. Name specific schools and edtech companies.",
        "manufacturing": "Focus on downtime reduction percentages, yield improvements, specific sensor/IoT implementations, ROI payback periods at factories. Name specific manufacturers and industrial automation vendors.",
        "retail": "Focus on revenue lift percentages, conversion rate improvements, specific retailer case studies, A/B test results. Name specific retailers and e-commerce platforms.",
        "hr": "Focus on hiring time reduction, quality-of-hire metrics, bias audit results, retention improvement data. Name specific companies and HR tech vendors.",
        "media": "Focus on production speed gains, cost reductions, content performance metrics, specific publisher case studies. Name specific media companies and content platforms."
    }
    angle = angle_guides.get(cat, "Include specific company names, data points, and real-world case studies.")

    prompt = f"""Write an 800-1200 word, in-depth analysis article in English about: {title}

Category: {cat}
Slug: {slug}

{angle}

REQUIREMENTS (strict):
1. Start with a compelling hook — specific statistic, surprising finding, or provocative question. NO "In recent years" or "The integration of AI" openings.
2. Include 5-7 sections with informative ## subheadings — each section must advance a specific argument or reveal a specific aspect.
3. EVERY major claim must cite a real, specific source: "According to JPMorgan's 2025 annual report", "A 2026 McKinsey study of 800 enterprises found", "Stanford's 2025 AI Index reports". NO vague "experts say" or "studies show".
4. Include at least 3 concrete company/organization examples with named individuals where possible.
5. Include at least 3 specific data points with numbers: percentages, dollar values, time savings, accuracy rates.
6. One paragraph should present a contrarian viewpoint or acknowledge limitations honestly. Credibility requires balance.
7. End with a forward-looking section that identifies an emerging trend or unresolved challenge.
8. Write in the voice of a knowledgeable industry analyst — confident, evidence-driven, concise. NO fluff, NO padding.
9. Use plain English paragraphs. NO bullet lists, NO numbered lists in the body (use actual prose).
10. Minimum 800 words, target 1000 words. Quality over quantity — every paragraph should teach something specific.

OUTPUT FORMAT:
Return only the article body as clean HTML inside <p> and <h2> tags. NO markdown, NO code fences, NO meta-commentary.
Start directly with the content."""

    print(f"  Calling AI for: {title[:60]}...")
    content = call_ai(prompt, max_tokens=4000, temperature=0.75)
    # Strip any code fences
    content = re.sub(r'```html\s*', '', content)
    content = re.sub(r'```\s*', '', content)
    content = content.strip()
    return content

def main():
    # Read manifest
    _, manifest_json = read_file_sha(MANIFEST_PATH)
    if not manifest_json:
        print("ERROR: Cannot read manifest.json", file=sys.stderr)
        sys.exit(1)
    manifest = json.loads(manifest_json)

    total = len(manifest)
    date_str = datetime.now().strftime("%Y-%m-%d")

    for idx, article in enumerate(manifest, 1):
        title = article["title"]
        cat = article["category"]
        slug = article["slug"]
        file = article["file"]

        print(f"\n[{idx}/{total}] {cat}: {title}")

        # Generate content
        try:
            body_html = generate_topic_content(title, cat, slug)
            if len(body_html) < 300:
                print(f"  Content too short ({len(body_html)} chars), retrying...")
                time.sleep(2)
                body_html = generate_topic_content(title, cat, slug)
        except Exception as e:
            print(f"  FAILED generation: {e}", file=sys.stderr)
            continue

        # Build HTML
        html = build_article_html(file, title, cat, body_html, date_str)
        word_count = len(re.sub(r'<[^>]+>', '', html).split())

        # Push
        article_path = f"en/articles/{file}"
        sha, _ = read_file_sha(article_path)
        ok = push_file(article_path, html, sha, f"Polish: {title} ({word_count} words)")
        print(f"  {'OK' if ok else 'FAIL'} push — ~{word_count} words")

        # Rate limit respect
        time.sleep(1.5)

    print(f"\nDone! {total} articles processed.")

if __name__ == "__main__":
    main()
