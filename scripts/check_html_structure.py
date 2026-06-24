from pathlib import Path
import re

f = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles\article-algo-trading.html")
c = f.read_text(encoding="utf-8")

# Find all divs with class
divs = re.findall(r'<div[^>]*class="[^"]*"[^>]*>', c)
for d in divs[:20]:
    print(d)

print("===")
# Find where real content starts - look for <h2> after </header>
idx = c.find("</header>")
print("header ends at:", idx)
print("After header (300 chars):")
print(c[idx:idx+500])
