from pathlib import Path
import re

f = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles\article-algo-trading.html")
c = f.read_text(encoding="utf-8")

# Find content between </header> and amazon-section
start = c.find("</header>")
end_marker = '<div class="amazon-section">'
end = c.find(end_marker)

if start == -1 or end == -1:
    print("ERROR: could not find boundaries")
else:
    content = c[start:end]
    clean = re.sub(r"<[^>]+>", " ", content)
    words = len(clean.split())
    print(f"Current word count: {words}")
    # Show first 300 chars of clean content
    print("First 300 chars:")
    print(clean.strip()[:300])
