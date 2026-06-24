from pathlib import Path
f = Path("C:/Users/Administrator/.qclaw/workspace-37i6raipm851ul5j/gudaoqihuo/en/articles/article-adaptive-exam-ai.html")
c = f.read_text(encoding="utf-8")
print("FILE SIZE:", len(c))
print("LAST 400 CHARS:")
# Write to file instead of printing to avoid encoding issues
with open("C:/Users/Administrator/.qclaw/workspace-37i6raipm851ul5j/gudaoqihuo/scripts/tail_out.txt", "w", encoding="utf-8") as out:
    out.write(repr(c[-400:]))
print("Written to tail_out.txt")
