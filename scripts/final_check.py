import sys, re
sys.stdout.reconfigure(encoding='utf-8')
cats = ['finance','healthcare','legal','education','manufacturing','retail','hr','media']
total = 0
for cat in cats:
    html = open('en/articles/article-'+cat+'-ai-deep-dive.html','r',encoding='utf-8').read()
    # Find main body
    start = html.find('<main class="container-narrow">')
    end = html.find('</main>', start)
    if start >= 0 and end > start:
        body = html[start+len('<main class="container-narrow">'):end]
        text = re.sub(r'<[^>]+>', ' ', body)
        text = re.sub(r'\s+', ' ', text).strip()
        wc = len(text.split())
    else:
        wc = 0
    total += wc
    # features count
    features = []
    for f, icon in [('stat-box','chart'),('case-study','case'),('insight-box','idea'),('comp-table','table'),('section-img','image'),('blockquote','quote')]:
        cnt = html.count(f)
        if cnt > 0: features.append(f'{icon}x{cnt}')
    print(f'{cat:15s} ~{wc:4d} words  {", ".join(features)}')
print(f'{"Total":15s} ~{total:4d} words')
