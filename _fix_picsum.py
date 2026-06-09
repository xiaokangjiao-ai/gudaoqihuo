# -*- coding: utf-8 -*-
import re

f = 'scripts/generate_content.py'
content = open(f, encoding='utf-8').read()

# Fix: _try_picsum - don't HEAD check, just return URL directly
old = '''def _try_picsum():
    """Lorem Picsum - 完全免费无需认证的随机图片"""
    try:
        seed = random.randint(1, 100000)
        url = f'https://picsum.photos/seed/{seed}/800/400'
        r = requests.head(url, timeout=5)
        if r.status_code == 200:
            print(f'    [Picsum] OK (seed={seed})')
            return url
    except Exception as e:
        print(f'    [Picsum] Failed: {e}')
    return None'''

new = '''def _try_picsum():
    """Lorem Picsum - 完全免费无需认证的随机图片（直接返回URL，不验证）"""
    seed = random.randint(1, 100000)
    url = f'https://picsum.photos/seed/{seed}/800/400'
    print(f'    [Picsum] Using (seed={seed})')
    return url'''

if old in content:
    content = content.replace(old, new)
    print('Picsum fix: OK')
else:
    print('Picsum fix: NOT FOUND')

open(f, 'w', encoding='utf-8').write(content)
print('Done')