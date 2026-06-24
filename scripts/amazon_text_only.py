"""Amazon 卡片终极版：3列文字卡 + 无图
- CSS: grid-template-columns: repeat(3, 1fr)
- 删除所有 <img> 标签（避免 CDN 防盗链）
- 紧凑文字版
"""
import re
from pathlib import Path

ARTICLES_DIR = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles")

# 替换 CSS
OLD_CSS_PATTERN = re.compile(
    r"\.amazon-grid\{display:grid;grid-template-columns:repeat\(auto-fill,minmax\(200px,1fr\)\);gap:20px;margin-top:20px\}"
)
NEW_CSS = ".amazon-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:20px}"

# 替换图片样式
OLD_IMG_CSS = ".amazon-card img{width:140px;height:140px;object-fit:contain;border-radius:10px;margin-bottom:14px;background:#fff;padding:8px}"
NEW_IMG_CSS = ".amazon-card .amazon-icon{font-size:1.8rem;margin-bottom:10px;display:block}"

# 卡片内 <img ...> 整行删除（多行/单行都支持）
IMG_TAG = re.compile(r'<img\s+src="https://m\.media-amazon\.com/[^"]+"\s+alt="[^"]*"\s+loading="lazy">\s*', re.MULTILINE)

# 响应式：移动端单列
OLD_MOBILE = ".amazon-card{background:linear-gradient(145deg,#14141f,#1a1a2e);border:1px solid rgba(108,99,255,.18);border-radius:14px;padding:18px;transition:all .25s ease;text-align:center}"
# 在末尾 @media 块里加 1fr


def fix_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    original = content

    # 1. CSS: 网格列数
    content = OLD_CSS_PATTERN.sub(NEW_CSS, content)

    # 2. 删除所有 amazon 图片
    content = IMG_TAG.sub("", content)

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    fixed = 0
    total = 0
    for html in sorted(ARTICLES_DIR.glob("article-*.html")):
        total += 1
        if fix_file(html):
            fixed += 1
            print(f"  [OK] {html.name}")
        else:
            print(f"  [--] {html.name} (no change needed)")
    print(f"\nDone: {fixed}/{total} files updated")


if __name__ == "__main__":
    main()
