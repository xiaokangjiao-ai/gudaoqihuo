from pathlib import Path
import re
c = Path("C:/Users/Administrator/.qclaw/workspace-37i6raipm851ul5j/gudaoqihuo/en/index.html").read_text(encoding="utf-8")
links = re.findall(r'href="/en/articles/(article-[^"]+)"', c)
articles_dir = Path("C:/Users/Administrator/.qclaw/workspace-37i6raipm851ul5j/gudaoqihuo/en/articles")
print(f"Total links in index: {len(links)}")
print("\nChecking each link:")
all_good = True
for link in links:
    f = articles_dir / link
    exists = f.exists()
    has_amazon = "amazon-section" in f.read_text(encoding="utf-8") if exists else False
    status = "OK" if exists else "MISSING"
    print(f"  {link}: {status}, amazon={has_amazon}")
    if not exists:
        all_good = False
print(f"\nAll links valid: {all_good}")
