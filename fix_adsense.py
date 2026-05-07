# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = r'C:\Users\Administrator\.qclaw\workspace-agent-a03bb487\gudaoqihuo-repo\scripts\generate_content.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the placeholder with real AdSense client ID
content = content.replace(
    'ca-pub-XXXXXXXXXXXXXXXX',
    'ca-pub-9935054113253833'
)

# Also add the adsbygoogle.js script to each ad slot
# Find and replace the AD_CODE patterns
content = content.replace(
    '''AD_CODE_TOP     = \'\'\'<!-- Google AdSense - 顶部横幅广告 -->
<ins class="adsbygoogle"''',
    '''AD_CODE_TOP     = \'\'\''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"'''
)

content = content.replace(
    '''AD_CODE_MIDDLE  = \'\'\'<!-- Google AdSense - 文中广告 -->
<ins class="adsbygoogle"''',
    '''AD_CODE_MIDDLE  = \'\'\''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"'''
)

content = content.replace(
    '''AD_CODE_BOTTOM  = \'\'\'<!-- Google AdSense - 底部广告 -->
<ins class="adsbygoogle"''',
    '''AD_CODE_BOTTOM  = \'\'\''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"'''
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('OK - AdSense updated')