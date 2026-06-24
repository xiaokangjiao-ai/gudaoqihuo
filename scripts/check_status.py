from pathlib import Path

d = Path("C:/Users/Administrator/.qclaw/workspace-37i6raipm851ul5j/gudaoqihuo/en")
for f in ["about.html", "contact.html", "privacy.html", "terms.html"]:
    p = d / f
    if p.exists():
        c = p.read_text(encoding="utf-8")
        print(f"{f}: {len(c)} bytes, has_content: {len(c) > 500}")
    else:
        print(f"{f}: NOT FOUND")

idx = (d / "index.html").read_text(encoding="utf-8")
print(f"AI banner in index: {'ai-disclaimer' in idx or 'AI-generated' in idx or 'AI Assisted' in idx}")

# check article word counts
import re
articles_dir = d / "articles"
for f in sorted(articles_dir.glob("article-*.html")):
    c = f.read_text(encoding="utf-8")
    m = re.search(r'class="article-body">(.*?)class="amazon-section"', c, re.DOTALL)
    if m:
        text = re.sub(r"<[^>]+>", "", m.group(1))
        words = len(text.strip().split())
        if words > 200:
            print(f"  {f.name}: ~{words} words")
