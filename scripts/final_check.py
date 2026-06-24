"""Final comprehensive check before AdSense re-application."""
from pathlib import Path
import re, os

os.chdir(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo")

print("=" * 60)
print("FINAL PRE-ADSENSE CHECK")
print("=" * 60)

# 1. Check B task pages
print("\n[B] About / Contact / Privacy / Terms pages:")
files = ["en/about-en.html", "en/contact-en.html", "en/privacy-en.html", "en/terms-en.html"]
for f in files:
    p = Path(f)
    if p.exists():
        html = p.read_text(encoding="utf-8")
        words = len(re.sub(r"<[^>]+>", " ", html).split())
        print(f"  OK {f}: {words} words")
    else:
        print(f"  MISSING: {f}")

# 2. Check homepage AI declaration banner
print("\n[C] SEO / AI Declaration:")
hp = Path("en/index.html")
if hp.exists():
    html = hp.read_text(encoding="utf-8")
    has_banner = "ai-declaration" in html or "AI-generated" in html or "ai content" in html.lower()
    print(f"  AI declaration banner: {'YES' if has_banner else 'NO'}")
    has_adsense = "googlesyndication" in html or "adsbygoogle" in html or "ca-pub" in html
    print(f"  AdSense code present: {'YES' if has_adsense else 'NO'}")
    # Check auto-ads script
    has_auto_ads = "enable_page_level_ads" in html or "auto_ads" in html
    print(f"  AdSense auto-ads: {'YES' if has_auto_ads else 'NO (may use manual placement)'}")

# 3. Check robots.txt
print("\n[C] robots.txt:")
r = Path("robots.txt")
if r.exists():
    lines = r.read_text(encoding="utf-8").splitlines()
    print(f"  EXISTS ({len(lines)} lines)")
    for line in lines:
        print(f"    {line}")
else:
    print("  MISSING!")

# 4. Check sitemap accuracy
print("\n[C] sitemap.xml accuracy (spot check):")
sitemap = Path("sitemap.xml")
if sitemap.exists():
    content = sitemap.read_text(encoding="utf-8")
    urls = re.findall(r"<loc>(.*?)</loc>", content)
    print(f"  Total URLs in sitemap: {len(urls)}")
    # Spot check first 3 and last 3 URLs
    check_urls = urls[:3] + urls[-3:]
    for url in check_urls:
        # Convert to local path
        if "gudaoqihuo.com" in url:
            rel_path = url.replace("https://www.gudaoqihuo.com/", "").rstrip("/")
            if not rel_path.endswith(".html"):
                rel_path += "/index.html"
            local = Path(rel_path)
            if local.exists():
                print(f"  OK {url}")
            else:
                print(f"  DEAD LINK in sitemap: {url} (local: {local})")

# 5. Article word counts summary
print("\n[A] Article word count summary (all 15):")
articles = [
    "en/articles/article-algo-trading.html",
    "en/articles/article-ai-fraud-detection.html",
    "en/articles/article-medical-imaging.html",
    "en/articles/article-drug-discovery.html",
    "en/articles/article-contract-review.html",
    "en/articles/article-adaptive-learning.html",
    "en/articles/article-predictive-maint.html",
    "en/articles/article-quality-vision.html",
    "en/articles/article-rec-engines.html",
    "en/articles/article-content-personalization.html",
    "en/articles/article-resume-screening.html",
    "en/articles/article-people-analytics.html",
    "en/articles/article-content-gen.html",
    "en/articles/article-deepfake-detect.html",
    "en/articles/article-deepfake-news-integrity.html",
]
total_words = 0
all_pass = True
for f in articles:
    p = Path(f)
    if not p.exists():
        print(f"  MISSING: {f}")
        all_pass = False
        continue
    html = p.read_text(encoding="utf-8")
    # Extract body content (between </header> and amazon-section)
    header_end = html.find("</header>")
    amazon_idx = html.find('<div class="amazon-section">')
    if header_end == -1 or amazon_idx == -1:
        print(f"  STRUCTURE ERROR: {f}")
        all_pass = False
        continue
    # Find img end
    search_from = header_end
    best_img_end = None
    while True:
        img_idx = html.find("<img", search_from)
        if img_idx == -1 or img_idx > amazon_idx:
            break
        gt_idx = html.find(">", img_idx)
        if gt_idx != -1 and gt_idx < amazon_idx:
            best_img_end = gt_idx + 1
            search_from = gt_idx + 1
        else:
            slash_gt = html.find("/>", img_idx)
            if slash_gt != -1 and slash_gt < amazon_idx:
                best_img_end = slash_gt + 2
                search_from = slash_gt + 2
            else:
                break
    if best_img_end:
        content = html[best_img_end:amazon_idx]
    else:
        meta_end = html.find("</div>", html.find('class="meta"'))
        if meta_end != -1:
            content = html[meta_end+6:amazon_idx]
        else:
            content = ""
    words = len(re.sub(r"<[^>]+>", " ", content).split())
    total_words += words
    status = "PASS" if words >= 1000 else "FAIL"
    if words < 1000:
        all_pass = False
    print(f"  [{status}] {Path(f).name}: {words} words")

print(f"\n  Total words across 15 articles: {total_words}")
print(f"  Average words per article: {total_words//15}")

print("\n" + "=" * 60)
print("OVERALL STATUS:")
print(f"  [A] Content Rewrite: {'COMPLETE' if all_pass else 'INCOMPLETE'}")
print(f"  [B] About/Contact/Privacy/Terms: CHECK ABOVE")
print(f"  [C] SEO Optimizations: CHECK ABOVE")
print("=" * 60)
