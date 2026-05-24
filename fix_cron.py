#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改 auto-content.yml：4次/天 → 6次/天
用法: python fix_cron.py
"""

FILE = ".github/workflows/auto-content.yml"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 旧 cron 配置（4次/天）
old_cron = """    # 北京时间 5:00, 12:00, 19:00, 22:00 (UTC 21:00, 4:00, 11:00, 14:00)
    - cron: '0 21 * * *'    # 北京 5:00 — 中国早晨(7点前2h缓冲)
    - cron: '0 4  * * *'     # 北京 12:00 — 中国中午(不变)
    - cron: '0 11 * * *'    # 北京 19:00 — 中国晚上(不变) / 美东早晨
    - cron: '0 14 * * *'    # 北京 22:00 — 美西早晨(PT 6:00)"""

# 新 cron 配置（6次/天）
new_cron = """    # 北京时间 5:00/9:00/12:00/15:00/19:00/22:00 (UTC 21/1/4/7/11/14)
    - cron: '0 21 * * *'  # 北京 05:00
    - cron: '0 1  * * *'  # 北京 09:00
    - cron: '0 4  * * *'  # 北京 12:00
    - cron: '0 7  * * *'  # 北京 15:00
    - cron: '0 11 * * *'  # 北京 19:00
    - cron: '0 14 * * *'  # 北京 22:00"""

if old_cron in content:
    content = content.replace(old_cron, new_cron)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: cron 已更新为 6 次/天")
    print("  北京时间点: 05:00 / 09:00 / 12:00 / 15:00 / 19:00 / 22:00")
else:
    print("WARN: 未找到旧 cron 配置，可能已修改")
    # 打印当前 cron 行供检查
    for line in content.split("\n"):
        if "cron:" in line:
            print(f"  当前: {line.strip()}")
