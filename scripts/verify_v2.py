import sys, re
sys.stdout.reconfigure(encoding='utf-8')
cats = ['finance','healthcare','legal','education','manufacturing','retail','hr','media']
total = 0
for cat in cats:
    html = open('en/articles/article-'+cat+'-ai-deep-dive.html','r',encoding='utf-8').read()
    m = re.search(r'<main class="container-narrow">(.*?)</main>', html, re.DOTALL)
    body = m.group(1) if m else html
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'\s+', ' ', text).strip()
    wc = len(text.split())
    total += wc
    features = []
    if 'stat-box' in html: features.append('chart')
    if 'case-study' in html: features.append('case')
    if 'insight-box' in html: features.append('insight')
    if 'comp-table' in html: features.append('table')
    if 'section-img' in html: features.append('image')
    if 'blockquote' in html: features.append('quote')
    print(f'{cat:15s} ~{wc:4d} words  {", ".join(features)}')
print(f'{"Total":15s} ~{total:4d} words across 8 articles')
