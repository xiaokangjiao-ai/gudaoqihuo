import re
with open('en/articles/article-ai-fraud-detection.html','r',encoding='utf-8') as f:
    c = f.read()
idx = c.find("Recommended Resources")
if idx == -1:
    idx = c.find('class="amazon-grid"')
print(c[idx:idx+2500])
