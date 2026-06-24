"""
Generate 1200+ word high-quality articles using Zhipu AI API.
Then inject them into the 15 article HTML files.
"""
import os, re, json, time
from pathlib import Path
import requests

API_KEY = os.environ.get("ZHIPU_API_KEY", "")
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4-flash"

ARTICLES_DIR = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles")

# 15 article topics with detailed prompts
TOPICS = [
    {
        "file": "article-algo-trading.html",
        "title": "How AI is Reshaping Algorithmic Trading in 2026",
        "category": "finance",
        "prompt": """Write a comprehensive 1400-1600 word article titled "How AI is Reshaping Algorithmic Trading in 2026" for an AI industry insights website.

Requirements:
- Professional financial journalism tone, data-driven, no AI cliches
- Include specific examples: Renaissance Technologies, Two Sigma, Citadel, JPMorgan COIN platform
- Cover: evolution from rule-based to ML, alternative data (satellite, sentiment, credit card), reinforcement learning for execution, regulatory challenges (SEC 2025 rules), talent war
- Include a comparison table of traditional vs AI-driven trading
- Add concrete numbers: Medallion Fund returns, data points processed per second, cost of talent
- End with a conclusion about human-AI collaboration
- Use HTML formatting: <h2 id="...">, <h3>, <p>, <ul>, <ol>, <table> (for comparisons)
- Include an AI disclosure notice in a styled <p> at the end (style="background:rgba(108,99,255,.08);border-left:3px solid #6c63ff;padding:12px 16px")
- Add a "Related Reading" <div class="related-articles"> section at the end linking to /en/articles/article-ai-fraud-detection.html
- NO emojis in the HTML tags or titles
- Write in proper English, no placeholder text"""
    },
    {
        "file": "article-ai-fraud-detection.html",
        "title": "AI Fraud Detection: How Banks Catch Billions in Financial Crime",
        "category": "finance",
        "prompt": """Write a comprehensive 1400-1600 word article titled "AI Fraud Detection: How Banks Catch Billions in Financial Crime" for an AI industry insights website.

Requirements:
- Professional tone, focused on real-world implementations
- Cover: transaction monitoring at scale (JPMorgan 2B transactions/day), Stripe Radar ($12B blocked 2025), Mastercard Decision Intelligence
- Technical depth: feature engineering, gradient boosted trees vs neural networks vs graph neural networks, anomaly detection
- Include the fraud stats: $485B global losses, $32B credit card fraud
- Cover challenges: adversarial attacks, synthetic identity fraud (up 73% YoY), explainability vs accuracy tradeoff
- Mention specific vendors: Feedzai, Kount, Featurespace
- HTML formatting with <h2>, <h3>, <p>, <ul>, <table>
- AI disclosure notice styled with rgba(79,195,247,.08) and border-left #4fc3f7
- Related Reading div linking to article-algo-trading.html
- No emojis"""
    },
    {
        "file": "article-medical-imaging.html",
        "title": "AI in Medical Imaging: From Research Labs to Clinical Practice",
        "category": "healthcare",
        "prompt": """Write a comprehensive 1400-1600 word article titled "AI in Medical Imaging: From Research Labs to Clinical Practice" for an AI industry insights website.

Requirements:
- Professional medical/tech journalism tone
- Cover: CNNs for image analysis, Google's diabetic retinopathy detection in Thailand/India, Nature Medicine study
- Specific applications: chest X-ray (CheXNet), mammography (Google Health -9.4% false negatives), stroke detection (Viz.ai - under 6 min)
- FDA clearance landscape (900+ devices by 2026), EU AI Act classification
- Challenges: data scarcity, annotation costs ($100-500 per image), bias across populations
- Include real numbers and study results
- HTML formatting, AI disclosure with rgba(239,83,80,.08) and border #ef5350
- Related Reading linking to article-drug-discovery.html
- No emojis"""
    },
    {
        "file": "article-drug-discovery.html",
        "title": "AI Drug Discovery: Shrinking 10-Year Timelines to Months",
        "category": "healthcare",
        "prompt": """Write a comprehensive 1400-1600 word article titled "AI Drug Discovery: Shrinking 10-Year Timelines to Months" for an AI industry insights website.

Requirements:
- Professional biotech/pharma journalism tone
- Cover: Insilico Medicine case study (IPF drug, 30 months to Phase II, $2.6M cost vs $400M industry avg)
- AlphaFold protein structure prediction (200M+ proteins predicted)
- Generative models for molecule design (GANs, diffusion models)
- Clinical trial optimization (patient recruitment, site selection)
- Challenges: the "valley of death", no FDA-approved AI drug yet as of 2026
- Include real company examples: Exscientia, Recursion, Atomwise
- HTML formatting, AI disclosure with rgba(239,83,80,.08) and border #ef5350
- Related Reading linking to article-medical-imaging.html
- No emojis"""
    },
    {
        "file": "article-contract-review.html",
        "title": "AI Contract Review: Transforming Legal Due Diligence",
        "category": "legal",
        "prompt": """Write a comprehensive 1400-1600 word article titled "AI Contract Review: Transforming Legal Due Diligence" for an AI industry insights website.

Requirements:
- Professional legal tech journalism tone
- Cover: M&A due diligence (20K-100K contracts per deal), error rates (10-30%), cost statistics ($4.2B in post-acquisition liabilities)
- Specific vendors: Kira Systems (acquired by Litera for $500M), Luminance ($120M raised), Lawgeex
- Technical: NLP for legal text, clause classification, risk flagging, knowledge graphs
- Challenges: nuance understanding, data privacy, integration complexity, liability questions
- HTML formatting, AI disclosure with rgba(129,199,132,.08) and border #81c784
- Related Reading linking to article-deepfake-detect.html
- No emojis"""
    },
    {
        "file": "article-adaptive-learning.html",
        "title": "Adaptive Learning: Personalizing Education at Scale",
        "category": "education",
        "prompt": """Write a comprehensive 1400-1600 word article titled "Adaptive Learning: Personalizing Education at Scale" for an AI industry insights website.

Requirements:
- Professional education technology journalism tone
- Cover: Khan Academy's Khanmigo (GPT-4 powered), Carnegie Learning MATHia (0.35 SD gain in RCTs), Duolingo's adaptive spaced repetition
- Technical: knowledge tracing (BKT, DKT), content adaptation, multimodal learning
- Challenges: digital divide, data privacy (COPPA, FERPA), teacher displacement fears, algorithmic bias
- Include NAEP statistics (26% math proficiency)
- Future: emotion-aware AI, VR/AR integration, lifelong learning profiles
- HTML formatting, AI disclosure with rgba(255,183,77,.08) and border #ffb74d
- Related Reading: no links or empty
- No emojis"""
    },
    {
        "file": "article-predictive-maint.html",
        "title": "Predictive Maintenance: When Machines Predict Their Own Failures",
        "category": "manufacturing",
        "prompt": """Write a comprehensive 1400-1600 word article titled "Predictive Maintenance: When Machines Predict Their Own Failures" for an AI industry insights website.

Requirements:
- Professional industrial IoT journalism tone
- Cover: Siemens MindSphere (15M devices, 30% downtime reduction, $8M savings), Rolls-Royce TotalCare (20GB per engine/day), GE digital twin (99.5% availability)
- Technical: sensor data (vibration, temperature, acoustics), RUL prediction, anomaly detection, physics-informed neural networks
- Barriers: legacy equipment, data silos, skills gap ($180K-$280K salaries), change management
- Include cost statistics: $50B annual downtime cost, $250K per hour automotive plant
- HTML formatting, AI disclosure with rgba(0,188,212,.08) and border #00bcd4
- Related Reading linking to article-quality-vision.html
- No emojis"""
    },
    {
        "file": "article-quality-vision.html",
        "title": "AI-Powered Quality Vision: Computer Vision on the Factory Floor",
        "category": "manufacturing",
        "prompt": """Write a comprehensive 1400-1600 word article titled "AI-Powered Quality Vision: Computer Vision on the Factory Floor" for an AI industry insights website.

Requirements:
- Professional manufacturing/computer vision journalism tone
- Cover: Cognex 99.9% detection rate, Landing AI (Andrew Ng), BMW Spartanburg (150+ vision stations, 40% more defects caught)
- Technical: image acquisition pipeline, anomaly detection (one-class learning), supervised defect classification
- Industry applications: semiconductor (10nm defect detection, 85% to 92%+ yield improvement), automotive, food & beverage (Tyson Foods - 67% reduction in foreign material incidents)
- Include comparison table: human vs rule-based vs AI vision (accuracy, speed, fatigue, cost)
- Challenges: lighting variations, edge cases, model drift
- HTML formatting, AI disclosure with rgba(0,188,212,.08) and border #00bcd4
- Related Reading linking to article-predictive-maint.html
- No emojis"""
    },
    {
        "file": "article-rec-engines.html",
        "title": "Recommendation Engines: The AI Powering Amazon, Netflix, and Spotify",
        "category": "retail",
        "prompt": """Write a comprehensive 1400-1600 word article titled "Recommendation Engines: The AI Powering Amazon, Netflix, and Spotify" for an AI industry insights website.

Requirements:
- Professional tech journalism tone
- Cover: Amazon 35% revenue from recommendations, Netflix $1B saved, Spotify Discover Weekly (40% of streams)
- Technical: collaborative filtering, content-based, two-tower models, sequential models (Transformers)
- Company deep dives: Amazon item-to-item CF, Netflix prize legacy, YouTube two-tower
- Challenges: filter bubbles, cold start, real-time latency, fairness/bias
- Future: LLM-powered recommendations, multimodal, cross-domain
- HTML formatting, AI disclosure with rgba(240,98,146,.08) and border #f06292
- Related Reading linking to article-content-personalization.html
- No emojis"""
    },
    {
        "file": "article-content-personalization.html",
        "title": "AI Content Personalization: Tailoring Experiences for Every User",
        "category": "retail",
        "prompt": """Write a comprehensive 1400-1600 word article titled "AI Content Personalization: Tailoring Experiences for Every User" for an AI industry insights website.

Requirements:
- Professional digital marketing/tech journalism tone
- Cover: Accenture 2025 survey (76% prefer personalized), Amazon dynamic homepage, NYT personalized front page, Washington Post Bandito engine
- Technical: user profiling (explicit + implicit + contextual + inferred), real-time decisioning (bandit algorithms, deep learning rankers)
- Privacy balance: GDPR, CCPA, cookie deprecation, privacy-preserving ML
- Challenges: data integration, cold start, measurement, organizational alignment
- Future: hyper-personalization, predictive personalization, voice UI, AR personalization
- HTML formatting, AI disclosure with rgba(240,98,146,.08) and border #f06292
- Related Reading linking to article-rec-engines.html
- No emojis"""
    },
    {
        "file": "article-resume-screening.html",
        "title": "AI Resume Screening: Efficiency, Bias, and the Future of Hiring",
        "category": "hr",
        "prompt": """Write a comprehensive 1400-1600 word article titled "AI Resume Screening: Efficiency, Bias, and the Future of Hiring" for an AI industry insights website.

Requirements:
- Professional HR tech journalism tone
- Cover: 250 resumes per job, 75% filtered before human review, HireVue 4M+ candidates, Eightfold AI $2.1B valuation
- Technical: resume parsing, semantic matching, predictive scoring
- Bias problem: Amazon recruiting bot (2018), racial bias in name recognition, university prestige bias
- Regulation: NYC Local Law 144, EU AI Act high-risk classification
- Best practices: bias audits, human-in-the-loop, transparency
- HTML formatting, AI disclosure with rgba(171,71,188,.08) and border #ab47bc
- Related Reading linking to article-people-analytics.html
- No emojis"""
    },
    {
        "file": "article-people-analytics.html",
        "title": "People Analytics: Data-Driven Insights for Workforce Decisions",
        "category": "hr",
        "prompt": """Write a comprehensive 1400-1600 word article titled "People Analytics: Data-Driven Insights for Workforce Decisions" for an AI industry insights website.

Requirements:
- Professional HR/people analytics journalism tone
- Cover: Visier ROI stats (26% higher revenue/employee, 22% lower turnover), Google attrition prediction (20% reduction in high-risk segments)
- Use cases: attrition prediction, workforce planning, engagement analysis (Glint/Viva Glint - 14% higher engagement)
- Tools ecosystem: Visier, Glint, Culture Amp, Workday, ChartHop - include a comparison table
- Ethical concerns: surveillance, predictive injustice, data security, union implications
- Future: skills ontologies, passive listening, AI-generated insights, real-time dashboards
- HTML formatting, AI disclosure with rgba(171,71,188,.08) and border #ab47bc
- Related Reading linking to article-resume-screening.html
- No emojis"""
    },
    {
        "file": "article-content-gen.html",
        "title": "AI Content Generation: How Newsrooms and Brands Are Embracing Automated Writing",
        "category": "media",
        "prompt": """Write a comprehensive 1400-1600 word article titled "AI Content Generation: How Newsrooms and Brands Are Embracing Automated Writing" for an AI industry insights website.

Requirements:
- Professional media/tech journalism tone
- Cover: LA Times Quakebot (2014), Washington Post Heliograf (850+ articles Olympics 2016), Bloomberg Cyborg (1/3 of financial news)
- Evolution: template-based -> NLG -> LLMs (GPT-3, Claude, Gemini)
- News media use: AP (4,000+ earnings reports/quarter), Forbes (controversial AI content)
- Marketing: Jasper (100K+ marketers), Copy.ai, HubSpot Content Assistant
- Quality vs scale tension: hallucinations, genericness, SEO implications (Google Helpful Content Update)
- Copyright/ethics: NYT vs OpenAI lawsuit, disclosure requirements
- Future: multimodal generation, personalized content, real-time updating, human-AI collaboration
- HTML formatting, AI disclosure with rgba(255,138,101,.08) and border #ff8a65
- Related Reading linking to article-deepfake-detect.html and article-deepfake-news-integrity.html
- No emojis"""
    },
    {
        "file": "article-deepfake-detect.html",
        "title": "Deepfake Detection: Authenticating Reality in the Age of Synthetic Media",
        "category": "media",
        "prompt": """Write a comprehensive 1400-1600 word article titled "Deepfake Detection: Authenticating Reality in the Age of Synthetic Media" for an AI industry insights website.

Requirements:
- Professional cybersecurity/AI journalism tone
- Cover: Hong Kong $25M deepfake fraud case (2024), Biden robocall (New Hampshire primary 2024)
- Technical: visual artifact detection, digital forensics (PRNU, compression artifacts, GAN fingerprints), audio deepfake detection
- Tools: Microsoft Video Authenticator, C2PA standard, Sensity AI (250K+ deepfakes detected, accuracy dropped from 95% to 70%)
- The arms race: adversarial perturbations, detector-aware training, diffusion model superiority
- Policy: EU AI Act, China deepfake regulations (2023), US state laws
- HTML formatting, AI disclosure with rgba(255,138,101,.08) and border #ff8a65
- Related Reading linking to article-content-gen.html and article-deepfake-news-integrity.html
- No emojis"""
    },
    {
        "file": "article-deepfake-news-integrity.html",
        "title": "Deepfake News Integrity: Protecting Information in the Synthetic Media Era",
        "category": "media",
        "prompt": """Write a comprehensive 1400-1600 word article titled "Deepfake News Integrity: Protecting Information in the Synthetic Media Era" for an AI industry insights website.

Requirements:
- Professional journalism/media ethics tone
- Cover: threat landscape (coordinated disinformation, context manipulation, synthetic witnesses, financial market manipulation)
- Defensive measures: verification toolkits (First Draft News, Reuters Facts, AFP Fact Check), updated newsroom workflows (source authentication, provenance documentation, C2PA)
- Platform responsibility: Meta, YouTube, TikTok labeling systems and their limitations
- Media literacy: lateral reading, source evaluation, emotional awareness, reverse image search (Finland case study)
- Future path: technical standards, legal frameworks, platform accountability, journalism investment, education
- HTML formatting, AI disclosure with rgba(255,138,101,.08) and border #ff8a65
- Related Reading linking to article-deepfake-detect.html and article-content-gen.html
- No emojis"""
    },
]


def call_zhipu_api(prompt, max_tokens=4000):
    """Call Zhipu AI API to generate article content."""
    if not API_KEY:
        print("ERROR: ZHIPU_API_KEY not set")
        return None
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert technology journalist writing for AI Verticals, a professional industry insights website. Write in polished, data-driven prose. Never use emojis. Always output valid HTML."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": max_tokens,
        "top_p": 0.9
    }
    
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API call failed: {e}")
        return None


def find_content_boundaries(html):
    """Find the start and end of article content in HTML file."""
    # Find content start: after the article hero image, which is after </header>
    header_end = html.find("</header>")
    if header_end == -1:
        return None
    
    # Find the img tag after header (article hero image)
    search_start = header_end
    while True:
        img_idx = html.find("<img", search_start)
        if img_idx == -1:
            break
        # Check if this img is before amazon-section
        amazon_idx = html.find('<div class="amazon-section">')
        if amazon_idx == -1:
            break
        if img_idx < amazon_idx:
            # This is a candidate - find its closing tag
            close_idx = html.find(">", img_idx)
            if close_idx == -1:
                close_idx = html.find("/>", img_idx)
                if close_idx != -1:
                    return (close_idx + 2, amazon_idx)
            else:
                return (close_idx + 1, amazon_idx)
            search_start = img_idx + 1
        else:
            break
    
    # Fallback: find content after meta div
    meta_end = html.find("</div>", html.find('class="meta"'))
    if meta_end != -1:
        amazon_idx = html.find('<div class="amazon-section">')
        if amazon_idx != -1:
            return (meta_end + 6, amazon_idx)
    
    return None


def inject_content(filepath, new_body):
    """Replace article content in HTML file."""
    html = filepath.read_text(encoding="utf-8")
    boundaries = find_content_boundaries(html)
    if boundaries is None:
        print(f"  ERROR: Could not find content boundaries in {filepath.name}")
        return False
    
    start, end = boundaries
    new_html = html[:start] + "\n" + new_body.strip() + "\n    " + html[end:]
    filepath.write_text(new_html, encoding="utf-8")
    return True


def main():
    if not API_KEY:
        print("ERROR: Please set ZHIPU_API_KEY environment variable")
        print("Or the API key is not configured in the script.")
        return
    
    print(f"Starting generation of {len(TOPICS)} articles...")
    print(f"API: {MODEL}")
    print()
    
    for i, topic in enumerate(TOPICS, 1):
        filename = topic["file"]
        filepath = ARTICLES_DIR / filename
        title = topic["title"]
        
        print(f"[{i}/{len(TOPICS)}] Generating: {title}")
        print(f"  File: {filename}")
        
        if not filepath.exists():
            print(f"  SKIP: File not found")
            continue
        
        # Call API
        content = call_zhipu_api(topic["prompt"])
        if content is None:
            print(f"  FAIL: API call failed")
            continue
        
        # Clean up content - remove ```html wrappers if present
        content = re.sub(r"```html?\s*", "", content)
        content = re.sub(r"```\s*$", "", content)
        
        # Inject into HTML
        success = inject_content(filepath, content)
        if success:
            # Count words
            clean = re.sub(r"<[^>]+>", " ", content)
            words = len(clean.split())
            print(f"  OK: {words} words injected")
        else:
            print(f"  FAIL: Could not inject content")
        
        print()
        
        # Rate limiting
        if i < len(TOPICS):
            print(f"  Waiting 3s for rate limit...")
            time.sleep(3)
    
    print("=== Done ===")


if __name__ == "__main__":
    main()
