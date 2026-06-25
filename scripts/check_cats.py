"""Check what articles each category page links to."""
import os, re

cats = ['finance','healthcare','legal','education','manufacturing','retail','hr','media']
base = 'en/articles'

for cat in cats:
    path = os.path.join(base, f'{cat}.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    # Find all article links that start with /en/articles/article-
    links = re.findall(r'href="([^"]*article-[^"]*)"', c)
    unique = sorted(set(l.replace('/en/articles/','') for l in links))
    print(f'=== {cat.upper()} ({len(unique)} articles) ===')
    for l in unique:
        print(f'  {l}')
    print()
