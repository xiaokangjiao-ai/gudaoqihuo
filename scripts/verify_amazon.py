"""全面检查所有文章页的 Amazon 区块状态"""
import re
from pathlib import Path

ARTICLES_DIR = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles")

print(f"{'File':<50} {'CSS':<12} {'Imgs':<6} {'Cards':<6}")
print("-" * 80)

issues = []
for f in sorted(ARTICLES_DIR.glob("article-*.html")):
    c = f.read_text(encoding="utf-8")
    # CSS
    css_match = "repeat(3,1fr)" in c
    # Amazon imgs
    amazon_imgs = len(re.findall(r"<img\s+[^>]*m\.media-amazon\.com[^>]*>", c))
    # Amazon cards
    cards = len(re.findall(r'<div class="amazon-card">', c))

    status_c = "OK" if css_match else "OLD"
    status_i = "0" if amazon_imgs == 0 else f"{amazon_imgs}!!"
    status_k = str(cards)

    print(f"{f.name:<50} {status_c:<12} {status_i:<6} {status_k:<6}")

    if not css_match or amazon_imgs > 0:
        issues.append(f.name)

print()
if issues:
    print(f"!! {len(issues)} files need fixing:")
    for n in issues:
        print(f"   - {n}")
else:
    print("All files are in the correct state (3-col, no images).")
