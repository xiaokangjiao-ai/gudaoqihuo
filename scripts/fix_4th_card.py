"""Remove only the 4th (last) Amazon card from files that have 4 cards."""
import re, os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
targets = [
    os.path.join(base, "en", "articles", "article-ai-fraud-detection.html"),
    os.path.join(base, "en", "articles", "article-medical-imaging.html"),
]

for path in targets:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    before = content.count("View on Amazon")
    
    # Find ALL amazon-card divs
    card_pattern = r'<div class="amazon-card">.*?</div>'
    cards = re.findall(card_pattern, content, flags=re.DOTALL)
    
    if len(cards) == 4:
        # Keep first 3, remove last one
        # Find position of 4th card and remove it
        last_card = cards[-1]
        content_new = content.replace(last_card, "", 1)
        
        after = content_new.count("View on Amazon")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content_new)
        print(f"OK {os.path.basename(path)}: {before} -> {after} cards")
    else:
        print(f"SKIP {os.path.basename(path)}: has {len(cards)} cards (not 4)")
