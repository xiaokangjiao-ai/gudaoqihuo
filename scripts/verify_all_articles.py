"""Verify all 15 articles have 1000+ words of body content."""
from pathlib import Path
import re

ARTICLES_DIR = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles")

ARTICLE_FILES = [
    "article-algo-trading.html",
    "article-ai-fraud-detection.html",
    "article-medical-imaging.html",
    "article-drug-discovery.html",
    "article-contract-review.html",
    "article-adaptive-learning.html",
    "article-predictive-maint.html",
    "article-quality-vision.html",
    "article-rec-engines.html",
    "article-content-personalization.html",
    "article-resume-screening.html",
    "article-people-analytics.html",
    "article-content-gen.html",
    "article-deepfake-detect.html",
    "article-deepfake-news-integrity.html",
]

def extract_body_content(html):
    """Extract content between </header> and <div class="amazon-section">."""
    header_end = html.find("</header>")
    if header_end == -1:
        return None, "missing </header>"
    amazon_idx = html.find('<div class="amazon-section">')
    if amazon_idx == -1:
        return None, "missing amazon-section"
    # Find the end of the last <img> tag before amazon section
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
    if best_img_end is not None:
        content = html[best_img_end:amazon_idx]
    else:
        meta_div_end = html.find("</div>", html.find('class="meta"'))
        if meta_div_end != -1:
            content = html[meta_div_end+6:amazon_idx]
        else:
            return None, "cannot find content boundaries"
    return content, None

def count_words(html_fragment):
    clean = re.sub(r"<[^>]+>", " ", html_fragment)
    clean = re.sub(r"\s+", " ", clean).strip()
    return len(clean.split())

def main():
    print("=" * 70)
    print("ARTICLE WORD COUNT VERIFICATION")
    print("=" * 70)
    total_articles = 0
    passed = 0
    failed = 0
    total_words = 0
    for fname in ARTICLE_FILES:
        fpath = ARTICLES_DIR / fname
        if not fpath.exists():
            print(f"  ✗ {fname}: FILE NOT FOUND")
            failed += 1
            continue
        html = fpath.read_text(encoding="utf-8")
        content, err = extract_body_content(html)
        if content is None:
            print(f"  ✗ {fname}: {err}")
            failed += 1
            continue
        words = count_words(content)
        total_words += words
        total_articles += 1
        status = "PASS" if words >= 1000 else "FAIL"
        flag = "" if words >= 1000 else "  <-- BELOW 1000"
        print(f"  [{status}] {fname}: {words} words{flag}")
        if words >= 1000:
            passed += 1
        else:
            failed += 1
    print("=" * 70)
    print(f"TOTAL: {total_articles} articles")
    print(f"PASS (>=1000 words): {passed}")
    print(f"FAIL (<1000 words): {failed}")
    print(f"TOTAL WORDS ACROSS ALL ARTICLES: {total_words}")
    print(f"AVERAGE WORDS PER ARTICLE: {total_words/total_articles if total_articles else 0:.0f}")
    print("=" * 70)

if __name__ == "__main__":
    main()
