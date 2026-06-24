from pathlib import Path
p = Path("C:/Users/Administrator/.qclaw/workspace-37i6raipm851ul5j/gudaoqihuo/en/articles")
no_amazon = [f for f in sorted(p.glob("article-*.html"))
             if "amazon-section" not in f.read_text(encoding="utf-8")]
print(f"Articles without amazon-section: {len(no_amazon)}")
for f in no_amazon:
    c = f.read_text(encoding="utf-8")
    dupe = c.count("<html") > 1
    broken = "</body></html>" not in c or c.count("</body></html>") > 1
    size = len(c)
    print(f"  {f.name}: dup_html={dupe}, no_body_end={broken}, size={size}")
