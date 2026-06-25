import sys, os
sys.stdout.reconfigure(encoding='utf-8')

path = 'en/articles/finance.html'
print(open(path, 'r', encoding='utf-8').read())
