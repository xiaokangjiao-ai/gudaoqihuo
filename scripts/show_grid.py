from pathlib import Path
c = Path("C:/Users/Administrator/.qclaw/workspace-37i6raipm851ul5j/gudaoqihuo/en/articles/article-algo-trading.html").read_text(encoding="utf-8")
idx = c.find('<div class="amazon-grid">')
print(c[idx:idx+500])
