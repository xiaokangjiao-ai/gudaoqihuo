# Amazon 广告卡片优化 - 2026-06-24

## 目标
修复文章页 Amazon 推荐区块的问题：图片无法显示（CDN 防盗链）、4个产品占位太大。

## 修改内容
**文件**: `scripts/fix_articles.py` → 重新生成 13 个文章页

### 改动点
1. **移除图片**: Amazon CDN (`m.media-amazon.com`) 有 Referrer Policy 防盗链，从第三方网站嵌入的图片会被拦截显示为破损。改为纯文字卡片。
2. **只显示3个产品**: 从每个文章的 products 列表取前3个（`products[:3]`），不再显示全部4个。
3. **固定3列布局**: `grid-template-columns: repeat(3, 1fr)`，一行刚好3个卡片。
4. **紧凑样式**: 去掉图片后 padding 从18px减到16px，字号微调，hover效果减弱。
5. **移动端适配**: `@media(max-width:640px)` 时改为单列。

### 涉及文件 (13个)
article-algo-trading.html, article-drug-discovery.html, article-contract-review.html,
article-adaptive-learning.html, article-predictive-maint.html, article-quality-vision.html,
article-rec-engines.html, article-content-personalization.html, article-resume-screening.html,
article-people-analytics.html, article-content-gen.html, article-deepfake-detect.html,
article-deepfake-news-integrity.html

## 验证
- 所有13个文件已重新生成，HTML结构正确
- amazon-grid 使用 repeat(3,1fr) 固定3列
- 无 img 标签在 amazon-card 内
- git commit: c8c4125
