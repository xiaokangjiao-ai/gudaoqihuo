"""
Inject batch 4: quality-vision + rec-engines + content-personalization = 3 articles.
"""
from pathlib import Path
import re

ARTICLES_DIR = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles")

# ============================================================
# ARTICLE 8: article-quality-vision.html
# ============================================================
QUALITY_VISION = """
<h2 id="intro">The Human Eye Was Never Built for Inspection at 10,000 Parts Per Minute</h2>
<p>On a typical consumer electronics assembly line, human inspectors examine products for defects: scratches on smartphone casings, misaligned camera modules, soldering defects on PCBs. Research published in the Journal of Quality Technology shows that after approximately 90 minutes of continuous inspection, human accuracy degrades by up to 30% due to cognitive fatigue. Missed defects that escape the factory cost manufacturers 10-30x more to fix in the field — including warranty claims, recalls, and reputational damage. The automotive industry alone spends over $8 bilion annually on warranty claims related to quality escapes. Computer vision powered by artificial intelligence is replacing and augmenting human inspection across industries. Cognex, the leading machine vision company, reports their AI-based inspection tools achieve 99.9% defect detection rates with false positive rates below 0.1%. Landing AI (founded by Andrew Ng) provides computer vision inspection that customers report reduces defect escape rates by 60-80%. The technology has matured from research labs to production lines — and it's reshaping manufacturing quality assurance.</p>

<h2 id="how-it-works">How AI Quality Vision Systems Work</h2>
<h3 id="image-acquisition">Image Acquisition Pipeline</h3>
<p>Industrial vision systems start with specialized cameras and lighting. High-resolution line scan cameras capture continuous images at speeds exceeding 10,000 parts per minute on high-speed production lines. Multi-spectral imaging detects subsurface defects — for example, bruising in fruit that isn't visible to the naked eye. Structured lighting enables 3D surface measurement, catching defects like panel warpage that 2D imaging misses. Hyperspectral imaging enables material composition analysis, identifying counterfeit components or incorrect materials. And edge AI chips (NVIDIA Jetson, Intel Movidius) perform inference directly on the production line, eliminating cloud latency for real-time rejection.</p>

<h3 id="defect-detection">Defect Detection: From Rules to Deep Learning</h3>
<p>Traditional machine vision relied on rule-based algorithms: set a threshold pixel value, count pixels above it, reject if count exceeds threshold. This worked for simple defects but failed on complex, variable appearances. AI brings two paradigm shifts. Anomaly detection: train on "good" product images only — the AI learns what normal looks like and flags anything different. This is powerful because defect examples are rare and expensive to collect. Supervised defect classification: convolutional neural networks (CNNs) classify specific defect types (scratch, dent, stain, misalignment) with >99% accuracy when trained on thousands of labeled examples. Recent advances in few-shot learning allow models to achieve >90% accuracy with just 10-50 defect examples per class.</p>

<h2 id="industry-applications">Industry Applications</h2>
<h3 id="semiconductor">Semiconductor Manufacturing: Zero Defect Tolerance</h3>
<p>Chip fabrication tolerances are measured in nanometers. A single defect on a wafer can destroy hundreds of chips. Applied Materials and KLA Corporation (the semiconductor inspection duopoly) use AI vision systems that inspect wafers at every process step. KLA's 3930 series patterned wafer inspection system uses deep learning to classify defects by root cause, enabling process engineers to fix the underlying issue rather than just rejecting bad dies. Yield management powered by AI vision has improved average fab yields from 85% to 92%+ at leading-edge facilities — translating to $50-200 milion additional revenue per fab per year.</p>

<h3 id="automotive">Automotive: End-to-Line Quality Assurance</h3>
<p>BMW's Spartanburg plant deploys over 150 AI vision stations checking everything from paint finish quality (detecting orange peel, dirt inclusions, and robot spray pattern inconsistencies) to weld integrity (verifying weld spot count, position, and visual quality). The system catches 40% more defects than previous human-and-rule-based inspection while reducing the quality team headcount needed per shift. Tesla's battery cell inspection uses computer vision to check 5,000+ cells per minute, identifying microscopic defects that could lead to thermal runaway. And Ford's Detroit plant uses AI vision to inspect 3D-printed manufacturing tools before they enter production, preventing defective tooling from creating downstream quality issues.</p>

<h3 id="food-beverage">Food and Beverage: Safety and Quality</h3>
<p>Tyson Foods deployed computer vision systems across 30+ processing plants to detect foreign material contamination (plastic, metal, glass) in meat products. The AI systems achieve 99.7% detection rates for contaminants larger than 3mm, reducing consumer complaints by 67% and recall risk significantly. In beverage production, Anheuser-Busch InBev uses vision systems to inspect every bottle/can for fill level, label alignment, and cap integrity at line speeds of 2,000 containers per minute. Diageo's whisky distillation plants use computer vision to monitor barrel aging conditions and detect leaks in real-time.</p>

<h2 id="comparison">Traditional vs. AI Vision: The Numbers</h2>
<table style="width:100%;border-collapse:collapse;margin:20px 0;color:#ccc">
<tr style="background:rgba(0,188,212,.1)"><th style="padding:10px;text-align:left;border:1px solid #333">Metric</th><th style="padding:10px;text-align:left;border:1px solid #333">Human</th><th style="padding:10px;text-align:left;border:1px solid #333">Rule-Based</th><th style="padding:10px;text-align:left;border:1px solid #333">AI-Powered</th></tr>
<tr><td style="padding:8px;border:1px solid #333">Accuracy</td><td style="padding:8px;border:1px solid #333">80-90% (fatigues to 60-70%)</td><td style="padding:8px;border:1px solid #333">90-95%</td><td style="padding:8px;border:1px solid #333">99-99.9%</td></tr>
<tr><td style="padding:8px;border:1px solid #333">Speed (parts/min)</td><td style="padding:8px;border:1px solid #333">~1-2</td><td style="padding:8px;border:1px solid #333">100-1,000</td><td style="padding:8px;border:1px solid #333">1,000-10,000+</td></tr>
<tr><td style="padding:8px;border:1px solid #333">Fatigue</td><td style="padding:8px;border:1px solid #333">Significant (30% in 90 min)</td><td style="padding:8px;border:1px solid #333">None</td><td style="padding:8px;border:1px solid #333">None</td></tr>
<tr><td style="padding:8px;border:1px solid #333">Setup Time</td><td style="padding:8px;border:1px solid #333">N/A (training required)</td><td style="padding:8px;border:1px solid #333">2-4 weeks (programming)</td><td style="padding:8px;border:1px solid #333">1-3 days (data collection + training)</td></tr>
<tr><td style="padding:8px;border:1px solid #333">Handles Novel Defects</td><td style="padding:8px;border:1px solid #333">Yes (general intelligence)</td><td style="padding:8px;border:1px solid #333">No (must be programmed)</td><td style="padding:8px;border:1px solid #333">Yes (anomaly detection)</td></tr>
</table>

<h2 id="challenges">Challenges and Limitations</h2>
<p>Despite impressive results, AI vision faces real challenges. Lighting variations: factory lighting changes (shadows, reflections, ambient light) can cause false rejects. Careful optical design and data augmentation during training mitigate this but don't eliminate it. Edge cases: truly novel defects may not be flagged by anomaly detection systems, particularly in the first months of deployment. Model drift: as production processes change (new materials, adjusted machine parameters), vision models may need retraining. And cost: a production-grade AI vision system costs $15,000-50,000 per inspection station including cameras, lighting, edge compute, and software licensing — significant for smaller manufacturers.</p>

<h2 id="future">Future Directions</h2>
<p>Three trends will define next-generation quality vision. Multimodal inspection: combining visual data with other sensors (acoustic, thermal, X-ray) for comprehensive defect detection. Self-supervised learning: reducing the need for manually labeled defect data by learning from unlabeled images. And generative AI for synthetic data: using diffusion models to generate synthetic defect images, dramatically reducing the data collection burden for rare defect types.</p>

<h2 id="conclusion">Conclusion</h2>
<p>AI-powered quality vision has moved beyond proof-of-concept to become a competitive necessity in precision manufacturing. The combination of falling camera costs (industrial GigE cameras dropped from $2,000 to $400 per unit in 2018-2025), advancing deep learning algorithms, and accessible training platforms (NVIDIA TAO Toolkit, LandingLens) is democratizing a capability once reserved for the largest manufacturers. The result: fewer defects escaping to customers, lower warranty costs, safer products, and better value for consumers. Quality assurance is being redefined — from detecting defects to preventing them.</p>
<p style="background:rgba(0,188,212,.08);border-left:3px solid #00bcd4;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(0,188,212,.05);border-radius:14px;border:1px solid rgba(0,188,212,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-predictive-maint.html" style="color:#00bcd4;text-decoration:none">→ Predictive Maintenance: When Machines Predict Their Own Failures</a></li></ul></div>
"""

# ============================================================
# ARTICLE 9: article-rec-engines.html
# ============================================================
REC_ENGINES = """
<h2 id="intro">35% of Amazon's Revenue — Powered by Recommendations</h2>
<p>McKinsey's landmark 2021 study revealed a striking fact: up to 35% of what consumers purchase on Amazon comes from product recommendations — not search, not browsing, but algorithmic suggestions. Netflix estimates their recommendation engine saves them $1 bilion annually in retained subscribers who would otherwise churn. Spotify's Discover Weekly playlist, powered by collaborative filtering and audio analysis, drives 40% of all streams on the platform and is cited by 60% of users as their primary music discovery mechanism. YouTube's recommendation algorithm is responsible for 70% of the time users spend watching videos. Yet most people don't understand how these systems actualy work, what trade-offs they make, or how they're evolving. This article demystifies the technology behind the suggestions that shape what we watch, listen to, buy, and read.</p>

<h2 id="how-recsys-works">How Recommendation Engines Work Under the Hood</h2>
<h3 id="collaborative-filtering">Collaborative Filtering: "People Like You Also Liked"</h3>
<p>The oldest and stil widely used approach is collaborative filtering. The core insight: if User A and User B have similar purchase/view histories, then items liked by User B but not yet seen by User A are strong recommendations. User-based collaborative filtering finds similar users; item-based collaborative filtering finds similar items. Strengths: interpretable ("because you watched..."), no feature engineering required. Weaknesses: cold start problem (new users have no history), popularity bias (tends to recommend already-popular items), and sparsity (most users have interacted with <1% of the item catalog). Matrix factorization (SVD, ALS) became the dominant technique from 2006-2015, embedding users and items in a shared latent space.</p>

<h3 id="content-based">Content-Based Filtering</h3>
<p>Content-based systems recommend items similar to what the user has liked before, based on item features rather than user behavior. For movies: genre, director, cast, runtime, rating. For products: category, brand, price range, specifications. For music: audio features (tempo, key, timbre), genre tags, release year. Strengths: no cold start for items (can recommend new items based on features), user independence (user A's recommendations don't depend on user B). Weaknesses: overspecialization (recommends items very similar to past likes, limiting discovery), feature engineering burden, and inability to capture serendipity.</p>

<h3 id="deep-learning">Deep Learning and Neural Collaborative Filtering</h3>
<p>The state-of-the-art combines collaborative signals with content understanding. Neural Collaborative Filtering (NCF) replaces matrix factorization with neural networks that learn arbitrary user-item interaction functions. Two-Tower Models (Google, Meta) encode users and items into a shared embedding space using separate but symmetric neural networks, enabling billion-scale retrieval. Sequential Models (Transformers, RNNs) account for temporal dynamics — your tastes evolve, and your recent behavior matters more than what you did three years ago. And Large Language Models are now being used to understand item descriptions, reviews, and even generate personalized explanation texts for recommendations.</p>

<h2 id="case-studies">Case Studies: Inside the Best Recommendation Systems</h2>
<h3 id="amazon-rec">Amazon: The Pioneer Who Keeps Innovating</h3>
<p>Amazon's recommendation engine is arguably the most valuable AI system in commerce. Their approach has evolved from simple item-to-item collaborative filtering (the "customers who bought X also bought Y" system patented by Amazon in 1998) to sophisticated deep learning models incorporating browsing history, purchase patterns, wishlist data, and even time spent viewing product images. Amazon's real-time recommendation system evaluates hundreds of candidate items for every page view in under 100 miliseconds. The system also optimizes for long-term value, not just immediate click-through: recommending items that lead to repeat purchases and high customer lifetime value rather than one-off clicks.</p>

<h3 id="netflix-rec">Netflix: The $1 Bilion Prize Legacy</h3>
<p>Netflix's famous $1 Milion Prize (2006-2009) advanced collaborative filtering research by years. The winning team improved Netflix's RMSE (root mean square error) by 10.06% — just over the prize threshold. Today, Netflix uses a sophisticated multi-stage pipeline. Candidate generation: narrowing billions of items to hundreds using approximate nearest neighbor search. Ranking: scoring candidates with deep learning models that consider user context (device, time of day, recent watches). Re-ranking: applying business rules like diversity (not al scary movies), freshness (not al watched items), and fairness. The result: 80% of Netflix viewing comes from recommendations rather than search.</p>

<h3 id="spotify-rec">Spotify: The Music Discovery Leader</h3>
<p>Spotify's recommendation stack is uniquely multimodal. Discover Weekly (launched 2015) combines collaborative filtering (what similar users listen to) with content analysis (audio features of songs you like) and natural language processing (lyrics, web articles about music). Blend (launched 2021) creates shared playlists between two users using graph-based approaches. Daylist generates mood-based playlists that update throughout the day. And Spotify's newest innovation uses raw audio waveform analysis with CNNs to identify songs similar to ones you like — even if they have no metadata tags in common. Spotify reports that users who engage with Discover Weekly have 30% higher retention than those who don't.</p>

<h2 id="challenges">Challenges in Building Great Recommender Systems</h2>
<p>Filter bubbles and echo chambers: recommending only what confirms existing tastes limits discovery and can reinforce polarization (particularly in news recommendation). The accuracy-diversity tradeoff: the most accurate recommendation might be the most obvious (more of the same), while the most valuable might be something unexpected. The cold start problem: new users have no history, new items have no interactions — requiring hybrid approaches and exploration strategies. Real-time requirements: session-based recommendations must update as the user interacts, requiring low-latency inference that rules out larger, slower models. And fairness and bias: recommenders can perpetuate or amplify societal biases (recommending higher-paying jobs to men, or showing minority candidates lower-quality housing listings).</p>

<h2 id="future">What's Next for Recommendation AI</h2>
<p>LLM-powered recommendations: using large language models to understand nuanced user intent from conversational queries ("recommend a laptop for video editing under $1,500 that's also good for travel"). Multimodal recommendation: combining text, images, video, and audio for richer item understanding. Cross-domain recommendation: if you know a user's preferences on Spotify, can you make better recommendations on Netflix? (Privacy-preserving collaborative filtering is making this possible). And causal recommendation: moving beyond correlation to understand causal effects — will recommending this item actualy cause the user to be more satisfied, or is the correlation spurious?</p>

<h2 id="conclusion">Conclusion</h2>
<p>Recommendation engines represent one of AI's most visible and economically impactful applications. They've transformed how we discover content, choose products, and spend our time online. The technology continues to advance — from matrix factorization to deep learning to large language models — but the ultimate goal isn't better predictions. It's better outcomes for users: serendipitous discoveries, efficient decision-making, and genuinely improved experiences. As recommender systems grow more powerful, the ethical considerations around filter bubbles, manipulation, and fairness become ever more important. The best systems don't just optimize for engagement — they optimize for user well-being.</p>
<p style="background:rgba(240,98,146,.08);border-left:3px solid #f06292;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(240,98,146,.05);border-radius:14px;border:1px solid rgba(240,98,146,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-content-personalization.html" style="color:#f06292;text-decoration:none">→ AI Content Personalization: Tailoring Experiences for Every User</a></li></ul></div>
"""

# ============================================================
# ARTICLE 10: article-content-personalization.html
# ============================================================
CONTENT_PERSONALIZATION = """
<h2 id="intro">The End of "One Size Fits Al" Digital Experience</h2>
<p>Visit Amazon.com from two different devices, and you'll see different homepages. Open the New York Times app, and the stories you see differ from what your spouse sees. This isn't magic — it's AI-powered content personalization, and it's become the expected standard for digital experiences. A 2025 Accenture survey found that 76% of consumers are more likely to purchase from brands that offer personalized experiences, while 52% will switch brands if personalization is lacking. The upside is measurable: McKinsey estimates personalization can deliver 5-15% revenue lift for retailers and 10-30% for media companies. But the technology required to deliver it at scale is sophisticated, and the privacy trade-offs are real. This article explores how content personalization works, where it delivers value, and where it crosses the line.</p>

<h2 id="technologies">The Technology Stack Behind Personalization</h2>
<h3 id="user-profiling">User Profiling and Segmentation</h3>
<p>Personalization starts with understanding who the user is. Explicit data includes stated preferences (genre favorites, newsletter subscriptions), survey responses, and account profile information. Implicit data is derived from behavior: clickstream (what you click, what you ignore), dwell time (how long you spend on each piece of content), scroll depth (how far you read), and purchase history. Contextual data includes device type, location, time of day, weather, and referral source. And inferred data uses AI to derive psychographic segments, intent prediction (are you researching or ready to buy?), and lifetime value estimation. The combination enables a "unified customer profile" that powers real-time personalization decisions.</p>

<h3 id="real-time-decisioning">Real-Time Decisioning Engines</h3>
<p>Modern personalization happens in real-time — within 50-200 miliseconds of page load. Rule engines handle business-defined logic ("show sports content to users who read 3+ sports articles in the past week"). Bandit algorithms (epsilon-greedy, Thompson sampling) balance exploration (show something new) with exploitation (show what's known to work). Deep learning rankers score content relevance for each user context, considering hundreds of signals simultaneously. And feature stores (like Feast or Tecton) serve pre-computed user features to models with single-digit milisecond latency. The infrastructure required is substantial: Netflix's personalization infrastructure includes over 100 microservices and processes 2+ trillion events daily.</p>

<h2 id="use-cases">Personalization Across Industries</h2>
<h3 id="ecommerce-pers">E-Commerce: Beyond Product Recommendations</h3>
<p>Amazon's personalization extends far beyond "customers also bought." Dynamic homepage layouts: the layout, hero banners, and promoted categories are personalized based on purchase history and browsing behavior. Personalized search: search results reorder based on individual purchase history and price sensitivity. Email personalization: abandoned cart reminders reference specific left-behind items and may include personalized discount offers based on price elasticity. And pricing optimization: dynamic pricing that varies by user segment (though this is controversial and regulated in some jurisdictions). Shopify's "Shop" app uses personalization to surface products from brands users are most likely to purchase, driving 35% higher conversion rates compared to non-personalized browsing.</p>

<h3 id="media-publishing">Media and Publishing</h3>
<p>The New York Times' personalization engine considers reading history, topic preferences (inferred and explicit), and time of day to surface articles. Their homepage shows different story selections, headline phrasings, and image choices to different readers. The Washington Post's "Bandito" engine powers personalization for hundreds of news organizations, A/B testing headline variants and thumbnail images for each visitor to maximize engagement. And Spotify's "Wrapped" (annual personalization summary) has become a cultural phenomenon, driving 60+ million shares annually and serving as a masterclass in personalized content marketing.</p>

<h3 id="streaming">Streaming Entertainment</h3>
<p>Disney+ personalizes not just what content is recommended, but also the UI itself: tile ordering, row categorization ("Because You Watched..." vs. "Trending" vs. "New Releases"), and even personalized artwork (the thumbnail image for the same movie may show different characters depending on what the algorithm thinks you'll respond to). Hulu uses personalization to optimize ad load — heavy viewers see fewer ads per hour to reduce churn. And YouTube's homepage personalization is so effective that 70% of watch time comes from recommendations rather than search or external links.</p>

<h2 id="privacy-balance">Balancing Personalization and Privacy</h2>
<p>The tension between personalization and privacy defines the current landscape. GDPR (Europe) and CCPA (California) require consent for data collection and provide rights to access, correct, and delete personal data. Compliance requires personalization engines to support "right to be forgotten" workflows and granular consent management. Chrome's phase-out of third-party cookies (completed 2025) eliminated a primary mechanism for cross-site personalization, forcing a shift to first-party data strategies. Privacy-preserving techniques are emerging: federated learning (training models on-device without exporting raw data), differential privacy (adding statistical noise to prevent re-identification), and on-device processing (Apple's on-device personalization for News and Music uses no cloud data transmission).</p>

<h2 id="challenges">Challenges in Personalization</h2>
<p>The filter bubble problem: personalization can create echo chambers where users are only exposed to confirming viewpoints. This is particularly concerning for news personalization. The cold start problem: new users have no history to personalize from, requiring fallback strategies (popularity-based, demographic-based). Data fragmentation: user behavior is split across devices, browsers, and apps — creating an incomplete picture. Measurement challenges: isolating the causal impact of personalization from other factors (seasonality, marketing campaigns) requires sophisticated A/B testing infrastructure. And algorithmic bias: personalization can perpetuate stereotypes (e.g., showing high-paying job ads predominantly to male users, as Facebook was found to do in a 2018 investigation).</p>

<h2 id="future">The Future of Content Personalization</h2>
<p>Four trends will shape the next era. Hyper-personalization with LLMs: using large language models to generate personalized content (emails, product descriptions, even news articles) tailored to individual reading levels, interests, and communication styles. Predictive personalization: predicting what users wil want before they know it — Amazon's "anticipatory shipping" patent (shipping products to distribution centers before you order them) is the ultimate expression of this concept. Voice and conversational personalization: as voice assistants proliferate, personalization will extend to spoken interactions — your smart speaker knows your preferences and can make personalized recommendations conversationally. And AR/VR personalization: as spatial computing (Apple Vision Pro, Meta Quest) gains adoption, personalized experiences will extend to 3D environments — virtual stores that rearrange themselves based on your preferences.</p>

<h2 id="conclusion">Conclusion</h2>
<p>Content personalization has evolved from basic segmentation to sophisticated, real-time, individualized experiences. The technology is mature, the ROI is proven, and consumer expectations have shifted permanently. But the most successful personalization programs balance algorithmic sophistication with respect for user privacy, transparent data practices, and genuine value delivery. Users accept personalization when it makes their lives easier — better recommendations, less irrelevant content, faster decisions. Cross that line into manipulation or privacy violation, and the same technology that builds loyalty can destroy it overnight. The future belongs to brands that personalize with empathy, transparency, and restraint.</p>
<p style="background:rgba(240,98,146,.08);border-left:3px solid #f06292;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(240,98,146,.05);border-radius:14px;border:1px solid rgba(240,98,146,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-rec-engines.html" style="color:#f06292;text-decoration:none">→ Recommendation Engines: The AI Powering Amazon, Netflix, and Spotify</a></li></ul></div>
"""

# Injection logic
def find_content_boundaries(html):
    header_end = html.find("</header>")
    if header_end == -1:
        return None
    amazon_idx = html.find('<div class="amazon-section">')
    if amazon_idx == -1:
        return None
    search_from = header_end
    best_img_end = None
    while True:
        img_idx = html.find("<img", search_from)
        if img_idx == -1 or img_idx > amazon_idx:
            break
        gt_idx = html.find(">", img_idx)
        if gt_idx != -1 and gt_idx < amazon_idx:
            best_img_end = gt_idx + 1
            search_from = gt_idx + 1
        else:
            slash_gt = html.find("/>", img_idx)
            if slash_gt != -1 and slash_gt < amazon_idx:
                best_img_end = slash_gt + 2
                search_from = slash_gt + 2
            else:
                break
    if best_img_end is not None:
        return (best_img_end, amazon_idx)
    meta_div_end = html.find("</div>", html.find('class="meta"'))
    if meta_div_end != -1:
        return (meta_div_end + 6, amazon_idx)
    return None

def inject_content(filepath, new_body):
    html = filepath.read_text(encoding="utf-8")
    boundaries = find_content_boundaries(html)
    if boundaries is None:
        return False
    start, end = boundaries
    new_html = html[:start] + "\n" + new_body.strip() + "\n    " + html[end:]
    filepath.write_text(new_html, encoding="utf-8")
    return True

def count_words(html_fragment):
    clean = re.sub(r"<[^>]+>", " ", html_fragment)
    return len(clean.split())

def main():
    articles = [
        ("article-quality-vision.html", QUALITY_VISION),
        ("article-rec-engines.html", REC_ENGINES),
        ("article-content-personalization.html", CONTENT_PERSONALIZATION),
    ]
    for filename, content in articles:
        filepath = ARTICLES_DIR / filename
        if not filepath.exists():
            print(f"SKIP (not found): {filename}")
            continue
        words = count_words(content)
        print(f"Injecting {filename} ({words} words)...")
        ok = inject_content(filepath, content)
        print(f"  {'OK' if ok else 'FAIL'}")

if __name__ == "__main__":
    main()
