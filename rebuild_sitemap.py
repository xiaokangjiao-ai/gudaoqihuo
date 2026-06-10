import os, glob
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')

cn_articles = sorted(glob.glob('articles/*.html'))
en_articles = sorted(glob.glob('en/articles/*.html'))

urls = []
static = [
    ('https://gudaoqihuo.com/', 'daily', '1.0'),
    ('https://gudaoqihuo.com/en/', 'daily', '1.0'),
    ('https://gudaoqihuo.com/about.html', 'monthly', '0.5'),
    ('https://gudaoqihuo.com/contact.html', 'monthly', '0.5'),
    ('https://gudaoqihuo.com/advertising.html', 'monthly', '0.5'),
    ('https://gudaoqihuo.com/disclaimer.html', 'monthly', '0.5'),
    ('https://gudaoqihuo.com/privacy-policy.html', 'monthly', '0.5'),
    ('https://gudaoqihuo.com/privacy.html', 'monthly', '0.4'),
    ('https://gudaoqihuo.com/articles/finance.html', 'daily', '0.8'),
    ('https://gudaoqihuo.com/articles/hot.html', 'daily', '0.8'),
    ('https://gudaoqihuo.com/en/articles/finance.html', 'daily', '0.8'),
    ('https://gudaoqihuo.com/en/articles/hot.html', 'daily', '0.8'),
]
for url, freq, pri in static:
    urls.append('<url><loc>{}</loc><lastmod>{}</lastmod><changefreq>{}</changefreq><priority>{}</priority></url>'.format(url, today, freq, pri))

for f in cn_articles:
    name = os.path.basename(f)
    urls.append('<url><loc>https://gudaoqihuo.com/articles/{}</loc><lastmod>{}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>'.format(name, today))

for f in en_articles:
    name = os.path.basename(f)
    urls.append('<url><loc>https://gudaoqihuo.com/en/articles/{}</loc><lastmod>{}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>'.format(name, today))

lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
lines.extend(urls)
lines.append('</urlset>')

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('Sitemap: {} static + {} CN + {} EN = {} total'.format(len(static), len(cn_articles), len(en_articles), len(urls)))