from pathlib import Path
p = Path("C:/Users/Administrator/.qclaw/workspace-37i6raipm851ul5j/gudaoqihuo/en/articles")
broken = []
for f in sorted(p.glob("article-*.html")):
    c = f.read_text(encoding="utf-8")
    # Broken if: multiple <html> OR no proper closing
    if c.count("<html") > 1 or "</html>" not in c:
        broken.append((f.name, "duplicate or missing html tag"))
    elif not c.strip().endswith("</html>") and not c.strip().endswith("</article></html>"):
        broken.append((f.name, "missing final closing tag"))
print(f"Total articles: {len(list(p.glob('article-*.html')))}")
print(f"Still broken: {len(broken)}")
if broken:
    for b, reason in broken:
        print(f"  - {b}: {reason}")
else:
    print("All 29 article HTML files are structurally sound!")
