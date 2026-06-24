from pathlib import Path
p = Path("C:/Users/Administrator/.qclaw/workspace-37i6raipm851ul5j/gudaoqihuo/en/articles")
f = p / "article-adaptive-exam-ai.html"
c = f.read_text(encoding="utf-8")
print("Total html tags:", c.count("<html"))
print("Total body ends:", c.count("</body></html>"))
print("Has amazon-section:", "amazon-section" in c)
# Check for the broken pattern: garbled text before Amazon section
print("Has 'TYPE html':", "TYPE html" in c)
print("Has 'div class=amazon':", "div class=amazon" in c)
# Find the last 50 chars of the file
print("ENDS WITH:", c[-100:])
