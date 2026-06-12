#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
孤岛财经 质控系统 v3.1
在GitHub Actions中直接修改本地文件，由workflow负责git commit/push
也支持本地运行(通过GitHub API)
"""

import os
import json
import time
import re
import base64
import requests
from datetime import datetime
from pathlib import Path

# ==================== 配置 ====================
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")
ZHIPU_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = "xiaokangjiao-ai/gudaoqihuo"
QUALITY_THRESHOLD = 7
MAX_ARTICLES = 10

# 检测运行环境
IN_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"
if IN_ACTIONS:
    REPO_DIR = Path(os.environ.get("GITHUB_WORKSPACE", "."))
else:
    REPO_DIR = None  # 本地无clone,走API

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

# ==================== GitHub API (本地运行时使用) ====================
def gh_get(path):
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/repos/{GITHUB_REPO}/{path}"
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()

def gh_put(path, content_b64, sha, commit_msg):
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/repos/{GITHUB_REPO}/{path}"
    data = {"message": commit_msg, "content": content_b64, "sha": sha, "branch": "main"}
    r = requests.put(url, headers=headers, json=data, timeout=15)
    r.raise_for_status()
    return r.json()

# ==================== 文件操作 ====================
def list_html_files():
    """列出articles/下的HTML文件"""
    files = []
    if IN_ACTIONS and REPO_DIR:
        # 本地文件系统
        for dir_path in ["articles", "en/articles"]:
            full_dir = REPO_DIR / dir_path
            if full_dir.exists():
                for f in sorted(full_dir.glob("*.html"), key=lambda x: x.stat().st_mtime, reverse=True):
                    files.append(f"{dir_path}/{f.name}")
    else:
        # GitHub API
        for dir_path in ["articles", "en/articles"]:
            try:
                items = gh_get(f"contents/{dir_path}")
                for item in items:
                    if item["name"].endswith(".html"):
                        files.append(f"{dir_path}/{item['name']}")
            except Exception as e:
                print(f"  [List] {dir_path} failed: {e}")
    return files

def read_file(path):
    """读取文件内容"""
    if IN_ACTIONS and REPO_DIR:
        full_path = REPO_DIR / path
        return full_path.read_text(encoding='utf-8')
    else:
        data = gh_get(f"contents/{path}")
        return base64.b64decode(data["content"]).decode("utf-8"), data["sha"]

def write_file(path, content, sha=None):
    """写入文件"""
    if IN_ACTIONS and REPO_DIR:
        full_path = REPO_DIR / path
        full_path.write_text(content, encoding='utf-8')
        return True
    else:
        content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        gh_put(path, content_b64, sha, f"Quality optimize: {path}")
        return True

# ==================== 文章处理 ====================
def extract_article_info(html_content, file_path):
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
    match = re.search(r'<!-- quality:(\d+) -->', html_content)
    if match:
        return int(match.group(1)) >= QUALITY_THRESHOLD
    return False

def quality_check(article_info):
    print(f"  [Check] {article_info['title'][:50]}...")
    prompt = f"""请对以下文章进行质量评分(1-10分),严格按JSON格式输出:
{{
    "score": 6,
    "title_score": 1,
    "content_score": 2,
    "ai_smell_score": 1,
    "issues": ["问题1","问题2"],
    "suggestion": "改进建议"
}}

文章标题: {article_info['title']}
分类: {article_info['category']}
开头300字: {article_info['preview']}

评分标准:
- 标题准确专业(2分),标题党扣分
- 内容有实质信息(3分),套话空洞扣分
- AI味检测(2分):有"网友炸锅""震惊""没想到""竟然"等词则扣分
- SEO自然度(1.5分)
- 图片匹配度(1.5分)

只输出JSON。"""
    
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
    print(f"  [Optimize] Rewriting...")
    prompt = f"""你是专业财经编辑。改写文章,要求:
1. 去除所有AI套话("网友炸锅""震惊""竟然""没想到"等)
2. 标题专业准确,含具体数据,不用夸张用语
3. 用数据和事实替代空泛描述
4. 保持SEO关键词但更自然
5. 输出格式严格:

【新标题】一行标题

【正文】HTML正文(含p/h2/strong等标签,不含html/head/body)

原文标题: {article_info['title']}
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

# ==================== 主流程 ====================
def process_articles():
    print(f"\n{'='*60}")
    print(f"GuDao Quality Check v3.1 @ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Mode: {'GitHub Actions (local files)' if IN_ACTIONS else 'API (remote)'}")
    print(f"{'='*60}\n")
    
    if not ZHIPU_API_KEY:
        print("[ERROR] ZHIPU_API_KEY not set")
        return
    
    all_files = list_html_files()
    if not all_files:
        print("[INFO] No HTML files found")
        return
    
    # 选最新10篇(Actions模式已按mtime排序)
    to_process = all_files[:MAX_ARTICLES]
    print(f"[INFO] Found {len(all_files)} files, checking latest {len(to_process)}\n")
    
    stats = {"total": 0, "skipped": 0, "passed": 0, "optimized": 0, "failed": 0}
    
    for i, file_path in enumerate(to_process, 1):
        stats["total"] += 1
        print(f"[{i}/{len(to_process)}] {file_path}")
        
        try:
            result = read_file(file_path)
            if IN_ACTIONS:
                html_content = result
                sha = None
            else:
                html_content, sha = result
        except Exception as e:
            print(f"  [ERROR] Read failed: {e}\n")
            stats["failed"] += 1
            continue
        
        if check_quality_passed(html_content):
            print(f"  [SKIP] Already passed\n")
            stats["skipped"] += 1
            continue
        
        info = extract_article_info(html_content, file_path)
        if not info:
            stats["failed"] += 1
            continue
        
        quality = quality_check(info)
        if not quality:
            print("  [WARN] Check failed\n")
            stats["failed"] += 1
            continue
        
        score = quality.get('score', 5)
        issues = quality.get('issues', [])
        print(f"  [Score] {score}/10 | Issues: {', '.join(issues[:2])}")
        
        if score < QUALITY_THRESHOLD:
            print(f"  [Optimize] Score < {QUALITY_THRESHOLD}...")
            optimized = optimize_article(info)
            if optimized and optimized['content']:
                new_html = html_content
                c = optimized['content']
                
                if '<article' in html_content:
                    new_html = re.sub(r'<article[^>]*>.*?</article>', f'<article>{c}</article>', html_content, flags=re.DOTALL)
                elif '<div class="content"' in html_content or '<div class="article"' in html_content:
                    new_html = re.sub(r'<div class="(content|article)[^"]*"[^>]*>.*?</div>', f'<div class="content">{c}</div>', html_content, flags=re.DOTALL)
                else:
                    new_html = re.sub(r'<body[^>]*>(.*)</body>', f'<body>{c}</body>', html_content, flags=re.DOTALL)
                
                new_html = f"<!-- quality:{QUALITY_THRESHOLD+1} -->\n" + new_html
                
                try:
                    write_file(file_path, new_html, sha)
                    print(f"  [OK] Optimized\n")
                    stats["optimized"] += 1
                except Exception as e:
                    print(f"  [ERROR] Write failed: {e}\n")
                    stats["failed"] += 1
            else:
                print("  [WARN] Optimize failed\n")
                stats["failed"] += 1
        else:
            new_html = f"<!-- quality:{score} -->\n" + html_content
            try:
                write_file(file_path, new_html, sha)
                print(f"  [OK] Passed, marked\n")
            except:
                print(f"  [WARN] Mark failed\n")
            stats["passed"] += 1
        
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print(f"[Summary] Total={stats['total']} | Skipped={stats['skipped']} | Passed={stats['passed']} | Optimized={stats['optimized']} | Failed={stats['failed']}")
    print(f"{'='*60}")

if __name__ == "__main__":
    process_articles()
