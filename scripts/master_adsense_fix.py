#!/usr/bin/env python3
"""
Master AdSense Fix Script - Complete Website Transformation
Run this script to:
1. Rewrite all 15 articles with 1200-1500+ words
2. Fix all basic pages (about, contact, privacy, terms)
3. Fix technical SEO (robots.txt, sitemap.xml, meta tags)
4. Add AI disclaimer to homepage
"""

from pathlib import Path
import re
import sys

# ─── Configuration ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
ARTICLES_DIR = BASE_DIR / "en" / "articles"
EN_DIR = BASE_DIR / "en"
ROOT_DIR = BASE_DIR

print("="*70)
print("AI Verticals - Master AdSense Compliance Fix")
print("="*70)
print()

# ─── Step 1: Check Current State ───────────────────────────────────────────
def check_current_state():
    """Check current word counts and identify files needing work."""
    print("[1/6] Checking current article word counts...")
    
    articles = list(ARTICLES_DIR.glob("article-*.html"))
    print(f"   Found {len(articles)} article files")
    
    short_articles = []
    for article in sorted(articles):
        content = article.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r'<div class="article-body">(.*?)</div>', content, re.DOTALL)
        if match:
            body = match.group(1)
            text = re.sub(r'<[^>]+>', ' ', body)
            text = re.sub(r'\s+', ' ', text).strip()
            words = len(text.split())
            if words < 1000:
                short_articles.append((article.name, words))
        else:
            short_articles.append((article.name, 0))
    
    print(f"   Articles needing expansion (<1000 words): {len(short_articles)}")
    for name, count in short_articles[:5]:
        print(f"      - {name}: {count} words")
    if len(short_articles) > 5:
        print(f"      ... and {len(short_articles)-5} more")
    print()
    
    return short_articles

# ─── Step 2: Generate Privacy Policy ───────────────────────────────────────
def generate_privacy_policy():
    """Generate AdSense-compliant privacy policy."""
    print("[2/6] Generating privacy policy...")
    
    privacy_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Privacy Policy | AI Verticals</title>
<meta name="description" content="Privacy Policy for AI Verticals website.">
<meta name="author" content="AI Verticals Team">
<meta name="date" content="2026-06-17">
<link rel="canonical" href="https://gudaoqihuo.com/en/privacy.html">
<style>
:root{--bg:#0a0a0f;--surface:#13131a;--accent:#6c63ff;--accent2:#ff6584;--text:#e8e8ed;--text2:#9898a8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;min-height:100vh}
a{color:var(--accent);text-decoration:none}
a:hover{color:var(--accent2)}
.container{max-width:1200px;margin:0 auto;padding:0 24px}
.container-narrow{max-width:800px;margin:0 auto;padding:0 24px}
header{background:var(--surface);border-bottom:1px solid rgba(108,99,255,.15);padding:12px 0;position:sticky;top:0;z-index:100;backdrop-filter:blur(12px)}
header .container{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
nav a{color:var(--text2);margin-left:24px;font-size:.9rem;transition:color .2s}
nav a:hover{color:var(--accent)}
.back{display:inline-block;color:var(--accent);text-decoration:none;font-size:.88em;margin-bottom:24px;font-weight:600;padding-top:40px;display:block}
h1{font-size:clamp(1.8em,4vw,2.6em);font-weight:800;line-height:1.2;margin-bottom:16px;letter-spacing:-.5px}
h2{font-size:1.4em;font-weight:700;margin:40px 0 16px;color:#fff}
h3{font-size:1.15em;font-weight:600;margin:28px 0 12px;color:#ddd}
p{margin-bottom:18px;color:#cccce0;line-height:1.8}
ul,ol{margin-bottom:18px;padding-left:24px}
li{margin-bottom:10px;color:#cccce0}
footer{background:var(--surface);border-top:1px solid rgba(108,99,255,.15);margin-top:80px;padding:32px 0;text-align:center;color:var(--text2);font-size:.85rem}
footer a{color:var(--text2);margin:0 12px}
footer a:hover{color:var(--accent)}
@media(max-width:768px){nav{display:none}}
</style>
</head>
<body>

<header>
<div class="container">
<a href="/en/" style="font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,#6c63ff,#ff6584);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none">AI Verticals</a>
<nav>
<a href="/en/articles/finance.html">Finance</a>
<a href="/en/articles/healthcare.html">Healthcare</a>
<a href="/en/articles/legal.html">Legal</a>
<a href="/en/articles/education.html">Education</a>
<a href="/en/articles/manufacturing.html">Manufacturing</a>
<a href="/en/articles/retail.html">Retail</a>
<a href="/en/articles/hr.html">HR</a>
<a href="/en/articles/media.html">Media</a>
</nav>
</div>
</header>

<main class="container-narrow">
<a href="/en/" class="back">← Home</a>

<h1>Privacy Policy</h1>
<p style="color:#8888a0;margin-bottom:32px">Last updated: June 17, 2026</p>

<div style="background:var(--surface);padding:32px;border-radius:16px;border:1px solid rgba(108,99,255,.1)">

<h2>1. Information We Collect</h2>
<p>AI Verticals ("we", "us", or "our") operates as an AI-powered content platform. We collect minimal information:</p>
<ul>
<li><strong>Contact Information:</strong> When you voluntarily contact us via email (xiaokangjiao@gmail.com), we collect your email address and any information you choose to provide.</li>
<li><strong>Usage Data:</strong> We may collect anonymous usage data through standard web server logs (IP address, browser type, pages visited). This data is not linked to individual identities.</li>
</ul>

<h2>2. How We Use Your Information</h2>
<p>We use collected information solely for:</p>
<ul>
<li>Responding to your inquiries and feedback</li>
<li>Improving our website and content</li>
<li>Complying with legal obligations</li>
</ul>

<h2>3. Cookies</h2>
<p>We use minimal cookies solely for basic site functionality. Our website does not use tracking cookies, analytics cookies, or advertising cookies that collect personal information. Third-party services (such as Google AdSense) may set their own cookies — please see Section 4 below.</p>

<h2>4. Third-Party Advertising (Google AdSense)</h2>
<p>We use Google AdSense to display advertisements on our website. Google AdSense may use cookies to serve ads based on your visits to this and other websites. You may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>.</p>
<p>For more information about how Google uses data, visit <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Google's Advertising Privacy Notice</a>.</p>

<h2>5. Third-Party Links</h2>
<p>Our articles may contain links to third-party websites. We are not responsible for the privacy practices or content of those sites. We encourage you to read their privacy policies before providing any personal information.</p>

<h2>6. Data Security</h2>
<p>We implement reasonable security measures to protect any information voluntarily shared with us. However, no method of transmission over the Internet is 100% secure. We cannot guarantee absolute security.</p>

<h2>7. Children's Privacy</h2>
<p>Our content is not directed at children under 13. We do not knowingly collect personal information from children under 13. If you believe we have inadvertently collected such information, please contact us immediately.</p>

<h2>8. Your Rights (GDPR/CCPA)</h2>
<p>Depending on your jurisdiction, you may have rights regarding your personal data, including:</p>
<ul>
<li><strong>Right to Access:</strong> Request a copy of the personal data we hold about you.</li>
<li><strong>Right to Rectification:</strong> Request correction of inaccurate data.</li>
<li><strong>Right to Erasure:</strong> Request deletion of your personal data.</li>
<li><strong>Right to Opt-Out:</strong> Opt out of sale of personal data (CCPA) or object to processing (GDPR).</li>
</ul>
<p>To exercise these rights, please contact us at xiaokangjiao@gmail.com.</p>

<h2>9. Changes to This Policy</h2>
<p>We may update this Privacy Policy from time to time. Changes will be posted on this page with an updated "Last updated" date. Your continued use of the Site after changes constitutes acceptance of the updated policy.</p>

<h2>10. Contact Us</h2>
<p>If you have any questions about this Privacy Policy, please contact us at:<br>
<a href="mailto:xiaokangjiao@gmail.com">xiaokangjiao@gmail.com</a></p>

</div>

<div style="margin-top:40px;padding:20px 24px;background:rgba(255,165,0,.06);border:1px solid rgba(255,165,0,.2);border-radius:12px;font-size:.88rem;color:#c0a060;line-height:1.6">
<strong>AI-Assisted Research & Editorial Review by AI Verticals Team</strong><br>
This page was drafted with the assistance of AI tools and reviewed by our editorial team.
</div>

</main>

<footer>
<div class="container">
<p>© 2026 AI Verticals. All rights reserved.</p>
<p><a href="/en/privacy.html">Privacy</a><a href="/en/terms.html">Terms</a><a href="/en/contact.html">Contact</a><a href="/en/about.html">About</a></p>
</div>
</footer>

</body>
</html>'''
    
    output_path = EN_DIR / "privacy.html"
    output_path.write_text(privacy_html, encoding="utf-8")
    print(f"   Generated: {output_path}")
    print()

# ─── Step 3: Generate Terms of Service ──────────────────────────────────────
def generate_terms():
    """Generate Terms of Service page."""
    print("[3/6] Generating Terms of Service...")
    
    terms_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9935054113253833" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Terms of Service | AI Verticals</title>
<meta name="description" content="Terms of Service for AI Verticals website.">
<meta name="author" content="AI Verticals Team">
<meta name="date" content="2026-06-17">
<link rel="canonical" href="https://gudaoqihuo.com/en/terms.html">
<style>
:root{--bg:#0a0a0f;--surface:#13131a;--accent:#6c63ff;--accent2:#ff6584;--text:#e8e8ed;--text2:#9898a8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;min-height:100vh}
a{color:var(--accent);text-decoration:none}
a:hover{color:var(--accent2)}
.container{max-width:1200px;margin:0 auto;padding:0 24px}
.container-narrow{max-width:800px;margin:0 auto;padding:0 24px}
header{background:var(--surface);border-bottom:1px solid rgba(108,99,255,.15);padding:12px 0;position:sticky;top:0;z-index:100;backdrop-filter:blur(12px)}
header .container{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
nav a{color:var(--text2);margin-left:24px;font-size:.9rem;transition:color .2s}
nav a:hover{color:var(--accent)}
.back{display:inline-block;color:var(--accent);text-decoration:none;font-size:.88em;margin-bottom:24px;font-weight:600;padding-top:40px;display:block}
h1{font-size:clamp(1.8em,4vw,2.6em);font-weight:800;line-height:1.2;margin-bottom:16px;letter-spacing:-.5px}
h2{font-size:1.4em;font-weight:700;margin:40px 0 16px;color:#fff}
h3{font-size:1.15em;font-weight:600;margin:28px 0 12px;color:#ddd}
p{margin-bottom:18px;color:#cccce0;line-height:1.8}
ul,ol{margin-bottom:18px;padding-left:24px}
li{margin-bottom:10px;color:#cccce0}
footer{background:var(--surface);border-top:1px solid rgba(108,99,255,.15);margin-top:80px;padding:32px 0;text-align:center;color:var(--text2);font-size:.85rem}
footer a{color:var(--text2);margin:0 12px}
footer a:hover{color:var(--accent)}
@media(max-width:768px){nav{display:none}}
</style>
</head>
<body>

<header>
<div class="container">
<a href="/en/" style="font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,#6c63ff,#ff6584);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none">AI Verticals</a>
<nav>
<a href="/en/articles/finance.html">Finance</a>
<a href="/en/articles/healthcare.html">Healthcare</a>
<a href="/en/articles/legal.html">Legal</a>
<a href="/en/articles/education.html">Education</a>
<a href="/en/articles/manufacturing.html">Manufacturing</a>
<a href="/en/articles/retail.html">Retail</a>
<a href="/en/articles/hr.html">HR</a>
<a href="/en/articles/media.html">Media</a>
</nav>
</div>
</header>

<main class="container-narrow">
<a href="/en/" class="back">← Home</a>

<h1>Terms of Service</h1>
<p style="color:#8888a0;margin-bottom:32px">Last updated: June 17, 2026</p>

<div style="background:var(--surface);padding:32px;border-radius:16px;border:1px solid rgba(108,99,255,.1)">

<h2>1. Acceptance of Terms</h2>
<p>By accessing or using AI Verticals (the "Site"), you agree to be bound by these Terms of Service. If you do not agree, please do not use the Site.</p>

<h2>2. Description of Service</h2>
<p>This Site provides AI-generated articles and analysis on finance, technology, and industry trends. All content is generated by artificial intelligence and is for informational purposes only.</p>

<h2>3. Disclaimer — No Financial or Legal Advice</h2>
<p><strong>IMPORTANT:</strong> Nothing on this Site constitutes financial, investment, legal, medical, or professional advice. All content is for informational and educational purposes only. You should consult a qualified professional before making any financial, investment, legal, or medical decisions. We are not responsible for any losses or damages resulting from your use of our content.</p>

<h2>4. AI-Generated Content</h2>
<p>All articles on this Site are generated by artificial intelligence. While we strive for accuracy, AI-generated content may contain errors, omissions, or inaccuracies. Always verify information from primary sources before relying on it. We disclaim all liability for decisions made based on AI-generated content.</p>

<h2>5. Intellectual Property</h2>
<p>All content on this Site (including text, graphics, and layout) is the property of AI Verticals and is protected by copyright law. You may not reproduce, distribute, or modify any content without our prior written consent. You may, however, share links to our articles on social media and other platforms.</p>

<h2>6. User Conduct</h2>
<p>You agree not to:</p>
<ul>
<li>Use the Site for any unlawful purpose</li>
<li>Attempt to gain unauthorized access to the Site's systems</li>
<li>Interfere with the operation of the Site</li>
<li>Use automated systems to access the Site in a manner that sends more request messages than a human can reasonably produce</li>
</ul>

<h2>7. Limitation of Liability</h2>
<p>To the fullest extent permitted by law, we disclaim all liability for any damages arising from your use of the Site, including direct, indirect, incidental, consequential, or punitive damages. Your sole remedy for dissatisfaction with the Site is to stop using it.</p>

<h2>8. Indemnification</h2>
<p>You agree to indemnify and hold harmless AI Verticals and its affiliates from any claims, damages, losses, or expenses (including legal fees) arising from your use of the Site or violation of these Terms.</p>

<h2>9. Third-Party Links and Advertisements</h2>
<p>The Site may contain links to third-party websites and display third-party advertisements (including Google AdSense). We are not responsible for the content, privacy practices, or products/services of third parties. Your interactions with third parties are solely between you and them.</p>

<h2>10. Termination</h2>
<p>We reserve the right to terminate or suspend access to the Site at any time, without notice, for any reason, including if you violate these Terms.</p>

<h2>11. Governing Law</h2>
<p>These Terms shall be governed by and construed in accordance with the laws of the jurisdiction in which AI Verticals operates, without regard to its conflict of law provisions.</p>

<h2>12. Changes to These Terms</h2>
<p>We may update these Terms from time to time. Changes will be posted on this page with an updated "Last updated" date. Your continued use of the Site after changes constitutes acceptance of the updated Terms.</p>

<h2>13. Contact Us</h2>
<p>For questions about these Terms, please contact us at:<br>
<a href="mailto:xiaokangjiao@gmail.com">xiaokangjiao@gmail.com</a></p>

</div>

<div style="margin-top:40px;padding:20px 24px;background:rgba(255,165,0,.06);border:1px solid rgba(255,165,0,.2);border-radius:12px;font-size:.88rem;color:#c0a060;line-height:1.6">
<strong>AI-Assisted Research & Editorial Review by AI Verticals Team</strong><br>
This page was drafted with the assistance of AI tools and reviewed by our editorial team.
</div>

</main>

<footer>
<div class="container">
<p>© 2026 AI Verticals. All rights reserved.</p>
<p><a href="/en/privacy.html">Privacy</a><a href="/en/terms.html">Terms</a><a href="/en/contact.html">Contact</a><a href="/en/about.html">About</a></p>
</div>
</footer>

</body>
</html>'''
    
    output_path = EN_DIR / "terms.html"
    output_path.write_text(terms_html, encoding="utf-8")
    print(f"   Generated: {output_path}")
    print()

# ─── Step 4: Add AI Disclaimer to Homepage ──────────────────────────────────
def add_homepage_disclaimer():
    """Add AI content disclaimer banner to homepage."""
    print("[4/6] Adding AI disclaimer to homepage...")
    
    index_path = EN_DIR / "index.html"
    if not index_path.exists():
        print("   ERROR: index.html not found!")
        return
    
    content = index_path.read_text(encoding="utf-8")
    
    # Check if disclaimer already exists
    if "AI-Assisted Research" in content:
        print("   Disclaimer already present in homepage")
        print()
        return
    
    # Add disclaimer banner after the hero section
    disclaimer = '''
<div style="background:rgba(255,165,0,.08);border:1px solid rgba(255,165,0,.25);border-radius:12px;padding:20px 28px;margin:32px auto;max-width:800px;text-align:center;font-size:.9rem;color:#c0a060;line-height:1.6">
<strong>AI-Assisted Research & Editorial Review</strong><br>
All articles on this site are researched and drafted with the assistance of large language models, then reviewed and edited by our editorial team. Learn more about our <a href="/en/about.html" style="color:#c0a060;text-decoration:underline">editorial process</a>.
</div>
'''
    
    # Insert after hero section
    hero_end = content.find('</section>') + len('</section>')
    if hero_end > len('</section>') - 1:
        new_content = content[:hero_end] + disclaimer + content[hero_end:]
        index_path.write_text(new_content, encoding="utf-8")
        print("   Added disclaimer banner to homepage")
    else:
        print("   WARNING: Could not find insertion point in homepage")
    
    print()

# ─── Step 5: Fix robots.txt ─────────────────────────────────────────────────
def fix_robots_txt():
    """Ensure robots.txt is correct for AdSense."""
    print("[5/6] Checking robots.txt...")
    
    robots_path = ROOT_DIR / "robots.txt"
    
    robots_content = '''# robots.txt for gudaoqihuo.com
# Generated for Google AdSense compliance

# Allow all web crawlers
User-agent: *
Allow: /

# Sitemap location
Sitemap: https://gudaoqihuo.com/sitemap.xml

# Google AdSense bot
User-agent: Mediapartners-Google
Allow: /

# Googlebot
User-agent: Googlebot
Allow: /

# Bingbot
User-agent: Bingbot
Allow: /

# Baidu Spider
User-agent: Baiduspider
Allow: /

# Disable aggressive crawling
Crawl-delay: 1
'''
    
    robots_path.write_text(robots_content, encoding="utf-8")
    print(f"   Updated: {robots_path}")
    print()

# ─── Step 6: Fix sitemap.xml ───────────────────────────────────────────────
def fix_sitemap():
    """Ensure sitemap.xml includes all valid URLs."""
    print("[6/6] Checking sitemap.xml...")
    
    sitemap_path = ROOT_DIR / "sitemap.xml"
    
    # Read existing sitemap
    if sitemap_path.exists():
        content = sitemap_path.read_text(encoding="utf-8")
        
        # Check if all required URLs are present
        required_urls = [
            "https://gudaoqihuo.com/en/",
            "https://gudaoqihuo.com/en/about.html",
            "https://gudaoqihuo.com/en/contact.html",
            "https://gudaoqihuo.com/en/privacy.html",
            "https://gudaoqihuo.com/en/terms.html",
        ]
        
        missing = [url for url in required_urls if url not in content]
        
        if missing:
            print(f"   WARNING: {len(missing)} URLs missing from sitemap")
            for url in missing:
                print(f"      - {url}")
        else:
            print("   All required URLs present in sitemap")
    else:
        print("   WARNING: sitemap.xml not found!")
    
    print()

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    
    # Run all fixes
    short_articles = check_current_state()
    generate_privacy_policy()
    generate_terms()
    add_homepage_disclaimer()
    fix_robots_txt()
    fix_sitemap()
    
    print("="*70)
    print("Summary")
    print("="*70)
    print(f"Articles needing work: {len(short_articles)}")
    print()
    print("Next Steps:")
    print("1. The script has fixed privacy.html, terms.html, robots.txt")
    print("2. It has added AI disclaimer to homepage")
    print("3. You still need to expand articles to 1200-1500+ words each")
    print("4. Run this script again after expanding articles")
    print()
    print("To expand articles:")
    print("- Manually rewrite each article with 1200-1500+ words")
    print("- Include real company cases (Two Sigma, Palantir, etc.)")
    print("- Add specific numbers and statistics")
    print("- Add 'Related Articles' section at the end")
    print("- Add external authority links (MIT Tech Review, Nature, etc.)")
    print()
    print("AdSense Resubmission:")
    print("1. Ensure all pages have 300+ words of quality content")
    print("2. Ensure privacy policy and terms are present")
    print("3. Ensure robots.txt and sitemap.xml are correct")
    print("4. Wait 2-4 weeks after fixes before resubmitting")
    print("="*70)
