#!/usr/bin/env python3
"""Check word counts for all articles."""
import re
from pathlib import Path

articles_dir = Path(__file__).parent.parent / "en" / "articles"
articles = list(articles_dir.glob("article-*.html"))

print(f"Found {len(articles)} article files\n")

total_words = 0
articles_needing_work = []

for article in sorted(articles):
    content = article.read_text(encoding="utf-8")
    # Extract article body
    match = re.search(r'<div class="article-body">(.*?)</div>', content, re.DOTALL)
    if match:
        body = match.group(1)
        # Count words (rough estimate - strip HTML tags)
        text = re.sub(r'<[^>]+>', ' ', body)
        text = re.sub(r'\s+', ' ', text).strip()
        words = len(text.split())
        total_words += words
        
        status = "[OK]" if words >= 1000 else "[NEEDS WORK]"
        if words < 1000:
            articles_needing_work.append((article.name, words))
        
        print(f"{article.name}: ~{words} words {status}")
    else:
        print(f"{article.name}: Could not extract body")
        articles_needing_work.append((article.name, 0))

print(f"\n{'='*60}")
print(f"Total words across all articles: ~{total_words}")
print(f"Articles needing work (<1000 words): {len(articles_needing_work)}")
if articles_needing_work:
    print("\nArticles that need expansion:")
    for name, count in articles_needing_work:
        print(f"  - {name}: {count} words")
