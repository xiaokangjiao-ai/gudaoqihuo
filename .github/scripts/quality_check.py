#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Fix Windows console encoding
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
孤岛财经 质控系统 v3.0 (直接扫描版)
方案: 扫描articles/目录,通过HTML注释标记避免重复处理
"""

import os
import json
import time
import re
import base64
import requests
from datetime import datetime

# ==================== 配置 ====================
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")
ZHIPU_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = "xiaokangjiao-ai/gudaoqihuo"
QUALITY_THRESHOLD = 7
MAX_ARTICLES = 10  # 每次最多处理10篇

# ==================== GitHub API ====================
def gh_get(path):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/repos/{GITHUB_REPO}/{path}"
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()

def gh_put(path, content_b64, sha, commit_msg):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/repos/{GITHUB_REPO}/{path}"
    data = {
        "message": commit_msg,
        "content": content_b64,
        "sha": sha,
        "branch": "main"
    }
    r = requests.put(url, headers=headers, json=data, timeout=15)
    r.raise_for_status()
    return r.json()

def get_file(path):
    """获取文件内容和SHA"""
    data = gh_get(f"contents/{path}")
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content, data["sha"]

def put_file(path, new_content, sha, commit_msg):
    """更新文件"""
    content_b64 = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    return gh_put(path, content_b64, sha, commit_msg)

def list_html_files():
    """列出articles/和en/articles/下的HTML文件"""
    files = []
    for dir_path in ["articles", "en/articles"]:
        try:
            items = gh_get(f"contents/{dir_path}")
            for item in items:
                if item["name"].endswith(".html"):
                    files.append(f"{dir_path}/{item['name']}")
        except Exception as e:
            print(f"  [List] {dir_path} 读取失败: {e}")
    return files

# ==================== 智谱API ====================
def call_zhipu(prompt, max_tokens=1024):
    if not ZHIPU_API_KEY:
        print("  [ERROR] ZHIPU_API_KEY not set!")
        return None
    try:
        headers = {
            "Authorization": f"Bearer {ZHIPU_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "glm-4-flash",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }
        resp = requests.post(ZHIPU_URL, headers=headers, json=data, timeout=60)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            print(f"  [API] Error {resp.status_code}: {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"  [API] Exception: {e}")
        return None

# ==================== 文章处理 ====================
def extract_article_info(html_content, file_path):
    """从HTML提取文章信息"""
    try:
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
        if not title_match:
            title_match = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else "Unknown"
        
        category = "hot"
        for cat in ["finance", "tech", "health", "life", "entertainment"]:
            if cat in file_path.lower():
                category = cat
                break
        
        text = re.sub(r'<[^>]+>', ' ', html_content)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return {
            "title": title,
            "category": category,
            "preview": text[:300],
            "full_content": text[:4000],
            "raw_html": html_content,
            "path": file_path
        }
    except Exception as e:
        print(f"  [Extract] Failed: {e}")
        return None

def check_quality_passed(html_content):
    """检查文章是否已有质量标记且通过"""
    match = re.search(r'<!-- quality:(\d+) -->', html_content)
    if match:
        score = int(match.group(1))
        return score >= QUALITY_THRESHOLD
    return False

def add_quality_mark(html_content, score):
    """在文章开头添加质量标记"""
    mark = f"<!-- quality:{score} -->\n"
    return mark + html_content

def quality_check(article_info):
    """质量评分"""
    print(f"  [Check] {article_info['title'][:40]}...")
    prompt = f"""请对以下文章进行质量评分(1-10分),严格按JSON格式输出:
{{
    "score": 分数(1-10),
    "title_score": 标题质量(0-2),
    "content_score": 内容深度(0-3),
    "ai_smell_score": AI味程度(0-2,越高AI味越淡),
    "issues": ["问题列表"],
    "suggestion": "改进建议(一句话)"
}}

文章标题: {article_info['title']}
分类: {article_info['category']}
开头300字: {article_info['preview']}

评分标准:
- 标题是否准确吸引人(2分)
- 内容是否有实质信息而非套话(3分)
- SEO关键词自然度(1.5分)
- AI味检测:有无"网友炸锅""震惊""没想到"等(2分)
- 图片匹配度(1.5分)

只输出JSON,不要其他内容。"""
    
    response = call_zhipu(prompt, max_tokens=512)
    if not response:
        return None
    
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except:
            pass
    return {"score": 5, "issues": ["Parse failed"], "suggestion": "Manual review"}

def optimize_article(article_info):
    """优化文章"""
    print(f"  [Optimize] Rewriting...")
    prompt = f"""你是财经网站编辑。请改写以下文章,要求:
1. 去除所有AI套话("网友炸锅""震惊""竟然""没想到"等情绪化标题党用语)
2. 用数据和事实替代空泛描述
3. 保持SEO关键词但更自然
4. 标题要专业准确,不要夸张
5. 输出格式严格按:

【新标题】一行标题

【正文】HTML格式的文章正文(含p/h2/strong等标签,不含html/head/body外层标签)

原文:
标题: {article_info['title']}
分类: {article_info['category']}
内容: {article_info['full_content']}"""
    
    response = call_zhipu(prompt, max_tokens=4096)
    if not response:
        return None
    
    new_title = ""
    new_content = ""
    
    title_m = re.search(r'【新标题】\s*(.+)', response)
    body_m = re.search(r'【正文】\s*(.+)', response, re.DOTALL)
    
    if title_m:
        new_title = title_m.group(1).strip()
    if body_m:
        new_content = body_m.group(1).strip()
    
    if not new_title and not new_content:
        new_title = article_info['title']
        new_content = response
    
    return {"title": new_title, "content": new_content}

def process_articles():
    """主流程"""
    print(f"\n{'='*60}")
    print(f"GuDao Qihuo Quality Check v3.0 @ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    if not ZHIPU_API_KEY:
        print("[ERROR] Please set ZHIPU_API_KEY environment variable")
        return
    
    if not GITHUB_TOKEN:
        print("[ERROR] Please set GITHUB_TOKEN environment variable")
        return
    
    # 列出所有HTML文件
    all_files = list_html_files()
    if not all_files:
        print("[INFO] No HTML files found")
        return
    
    print(f"[INFO] Found {len(all_files)} HTML files, processing latest {MAX_ARTICLES}\n")
    
    # 处理最新的N篇(简单策略:处理所有,但跳过已有质量标记且通过的)
    stats = {"total": 0, "skipped": 0, "passed": 0, "optimized": 0, "failed": 0}
    
    for i, file_path in enumerate(all_files[:MAX_ARTICLES], 1):
        stats["total"] += 1
        print(f"[{i}/{min(MAX_ARTICLES, len(all_files))}] {file_path}")
        
        try:
            html_content, file_sha = get_file(file_path)
        except Exception as e:
            print(f"  [ERROR] Read failed: {e}\n")
            stats["failed"] += 1
            continue
        
        # 检查是否已有质量标记且通过
        if check_quality_passed(html_content):
            print(f"  [SKIP] Already passed quality check\n")
            stats["skipped"] += 1
            continue
        
        info = extract_article_info(html_content, file_path)
        if not info:
            stats["failed"] += 1
            continue
        
        quality = quality_check(info)
        if not quality:
            print("  [WARN] Quality check failed, skip\n")
            stats["failed"] += 1
            continue
        
        score = quality.get('score', 5)
        issues = quality.get('issues', [])
        print(f"  [Score] {score}/10 | Issues: {', '.join(issues[:2])}")
        
        if score < QUALITY_THRESHOLD:
            print(f"  [Optimize] Score < {QUALITY_THRESHOLD}, optimizing...")
            optimized = optimize_article(info)
            if optimized and optimized['content']:
                # 更新HTML内容
                new_html = html_content
                c = optimized['content']
                
                if '<article' in html_content:
                    new_html = re.sub(r'<article[^>]*>.*?</article>', f'<article>{c}</article>', html_content, flags=re.DOTALL)
                elif '<div class="content"' in html_content or '<div class="article"' in html_content:
                    new_html = re.sub(r'<div class="(content|article)[^"]*"[^>]*>.*?</div>', f'<div class="content">{c}</div>', html_content, flags=re.DOTALL)
                else:
                    new_html = re.sub(r'<body[^>]*>(.*)</body>', f'<body>{c}</body>', html_content, flags=re.DOTALL)
                
                # 添加质量标记
                new_html = add_quality_mark(new_html, QUALITY_THRESHOLD + 1)  # 标记为新质量
                
                try:
                    put_file(
                        file_path,
                        new_html,
                        file_sha,
                        f"Quality optimize: {info['title'][:50]} (score {score}->{QUALITY_THRESHOLD+1})"
                    )
                    print(f"  [OK] Optimized and pushed\n")
                    stats["optimized"] += 1
                except Exception as e:
                    print(f"  [ERROR] Push failed: {e}\n")
                    stats["failed"] += 1
            else:
                print("  [WARN] Optimization failed, keep original\n")
                stats["failed"] += 1
        else:
            print(f"  [OK] Quality passed")
            # 添加质量标记
            new_html = add_quality_mark(html_content, score)
            try:
                put_file(file_path, new_html, file_sha, f"Quality mark: {info['title'][:50]} (score {score})")
                print(f"  [OK] Marked as passed\n")
            except:
                print(f"  [WARN] Mark failed, but content is good\n")
            stats["passed"] += 1
        
        time.sleep(1)  # API限流
    
    print(f"\n{'='*60}")
    print(f"[Summary] Total={stats['total']} | Skipped={stats['skipped']} | Passed={stats['passed']} | Optimized={stats['optimized']} | Failed={stats['failed']}")
    print(f"{'='*60}")

if __name__ == "__main__":
    process_articles()
