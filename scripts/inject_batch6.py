"""Inject batch 6 (FINAL): Media (3) = last 3 articles."""
from pathlib import Path
import re

ARTICLES_DIR = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles")

# ============================================================
# ARTICLE 13: article-content-gen.html
# ============================================================
CONTENT_GEN = """
<h2 id="intro">When a Robot Wrote an Earthquake Report in 20 Seconds</h2>
<p>In March 2014, an earthquake struck Los Angeles. The Los Angeles Times published an article about it within 3 minutes of the event. The reporter? An algorithm called Quakebot, which automatically pulled USGS data and populated a template. No human touched the story until after publication for review. Today, AI content generation has evolved from simple template-filling to producing articles, marketing copy, and creative fiction that rivals human-written content in quality. The Washington Post's Heliograf generated over 850 articles during the 2016 Olympics coverage. Bloomberg's Cyborg system produces approximately one-third of their financial news content. JPMorgan's COIN platform reviews 12,000+ legal documents per second — work that previously required 360,000 hours of lawyer time annually. The technology has moved from experiment to infrastructure, and it's raising fundamental questions about the future of writing, journalism, and creative work.</p>

<h2 id="how-ai-writing-works">How AI Content Generation Works</h2>
<h3 id="era1">Era 1: Template-Based Generation (1990s-2010s)</h3>
<p>Early systems used rule-based templates: "{magnitude} earthquake struck {location} at {time}." Effective for structured data but limited to formulaic content. Weather reports, sports recaps, and earnings summaries were the primary use cases. The Associated Press has used Automated Insights' Wordsmith platform since 2014 to generate 4,000+ corporate earnings previews per quarter — work that previously required dozens of journalists.</p>

<h3 id="era2">Era 2: Neural NLG (2017-2021)</h3>
<p>The transformer architecture (Vaswani et al., 2017) revolutionized natural language generation. GPT-2 (2019, 1.5B parameters) demonstrated coherent multi-paragraph generation for the first time. GPT-3 (2020, 175B parameters) enabled few-shot learning — providing a few examples in the prompt could teach the model new tasks without retraining. These models powered the first wave of commercial NLG tools: Copy.ai, Jasper, Writesonic, and others.</p>

<h3 id="era3">Era 3: Large Language Models (2022-Present)</h3>
<p>GPT-4, Claude (Anthropic), Gemini (Google), and LLaMA (Meta) represent a paradigm shift. These models generate text by predicting the most likely next token given context, trained on vast corpora of human writing. Capabilities include long-form articles with logical structure, style adaptation (matching brand voice, target audience reading level), research synthesis (summarizing multiple sources into coherent narrative), and creative writing (fiction, poetry, screenplays) that can be genuinely moving. The latest models can also see images (multimodal), enabling image captioning, visual storytelling, and infographic explanation generation.</p>

<h2 id="who-is-using-it">Who's Using AI Content Generation?</h2>
<h3 id="news-media">News Media Organizations</h3>
<p>The Washington Post's Heliograf covers localized sports and election results. During the 2016 and 2020 elections, Heliograf produced 500+ articles on local results that would otherwise have gone unreported. Bloomberg's Cyborg assists financial journalists by drafting earnings previews and market summaries — humans then edit and add analysis. The Associated Press expanded their earnings coverage from 300 companies to 4,000+ using Automated Insights. Reuters uses AI to generate commodity market reports and economic indicator summaries. And the BBC's experimental "Juicer" system auto-generates social media snippets from long-form articles.</p>

<h3 id="marketing-brands">Marketing and Brand Content</h3>
<p>Jasper (formerly Jarvis) serves 100,000+ marketers, generating blog posts, ad copy, email campaigns, and SEO content at scale. Their "Brand Voice" feature learns a company's style guide and mimics it across all generated content. Copy.ai focuses on short-form marketing content: product descriptions, Facebook ad headlines, Instagram captions. HubSpot's Content Assistant helps marketers draft blog outlines, meta descriptions, and email subject lines. And e-commerce platforms like Shopify integrate AI content generation directly into product listing workflows — generating SEO-optimized descriptions from a few bullet points.</p>

<h3 id="publishing">Book Publishing and Long-Form</h3>
<p>The publishing industry is grappling with AI-generated books flooding Amazon Kindle Direct Publishing. In 2023, Amazon required authors to disclose AI usage after thousands of AI-generated books were discovered. Some authors use AI as a co-writer — drafting outlines, generating chapter summaries, or overcoming writer's block. Others reject it entirely. The Authors Guild has called for transparency requirements and compensation frameworks for AI training on copyrighted works.</p>

<h2 id="quality-vs-scale">Quality vs. Scale: The Central Tension</h2>
<p>AI can generate content at superhuman speed — but quantity doesn't equal quality. Accuracy problems: LLMs confidently hallucinate facts, quote non-existent studies, and misattribute statements. The "hallucination rate" for GPT-4 on factual questions is approximately 2-8% depending on domain — acceptable for drafts but dangerous for published content without human review. Genericness trap: AI tends toward average, competent but unremarkable prose. It writes in cliches because cliches are statistically probable. SEO implications: Google's Helpful Content Update (2022) and subsequent refinements specifically target low-quality AI-generated content designed for search rankings rather than human readers. Sites publishing pure AI content without value-add have seen 40-80% traffic drops after Google updates.</p>

<h2 id="legal-ethical">Legal and Ethical Questions</h2>
<p>Copyright: The New York Times sued OpenAI and Microsoft in December 2023, alleging copyright infringement for training on NYT articles. Similar lawsuits are pending from authors (including George R.R. Martin and John Grisham). Disclosure: should AI-generated content be labeled? The EU AI Act requires it. China's generative AI regulations (effective 2023) require watermarking of synthetic content. And job displacement: the World Economic Forum's 2025 Future of Jobs Report estimates 85 million jobs may be displaced by AI by 2025, while 97 million new roles may emerge — but the transition is painful for affected workers.</p>

<h2 id="future">The Future: Human-AI Collaboration Models</h2>
<p>The most productive approach isn't human vs. machine — it's human with machine. Journalism: AI handles data-driven stories (earnings, sports recaps, weather), freeing journalists for investigative work and analysis. Marketing: AI generates 10 subject line variants; humans pick the best and refine. Technical writing: AI drafts API documentation from code; humans verify accuracy and add context. And creative writing: AI suggests plot twists, generates character backstories, or helps with writer's block — but the creative vision remains human.</p>

<h2 id="conclusion">Conclusion</h2>
<p>AI content generation has crossed from novelty to necessity for high-volume content needs. News organizations use it to cover more stories with smaller teams. Marketers use it to personalize content at scale. But the technology works best as a collaborator, not a replacement. The most valuable content — investigative journalism, expert analysis, original research, and emotionally resonant storytelling — remains distinctly human. AI's role is to handle the voluminous and data-driven content that frees human creators to focus on what only they can do. The future isn't AI replacing writers — it's writers with AI superpowers, producing better work faster than ever before. The key is maintaining editorial standards, transparency with audiences, and rigorous fact-checking of AI-assisted output.</p>
<p style="background:rgba(255,138,101,.08);border-left:3px solid #ff8a65;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(255,138,101,.05);border-radius:14px;border:1px solid rgba(255,138,101,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-deepfake-detect.html" style="color:#ff8a65;text-decoration:none">→ Deepfake Detection: Authenticating Reality in the Age of Synthetic Media</a></li><li style="margin-bottom:10px"><a href="/en/articles/article-deepfake-news-integrity.html" style="color:#ff8a65;text-decoration:none">→ Deepfake News Integrity: Protecting Information in the Synthetic Media Era</a></li></ul></div>
"""

# ============================================================
# ARTICLE 14: article-deepfake-detect.html
# ============================================================
DEEPFAKE_DETECT = """
<h2 id="intro">Seeing Is No Longer Believing</h2>
<p>In 2024, a finance worker at a multinational firm in Hong Kong transferred $25 million to fraudsters after a video call with who he believed was the company's CFO. The "CFO" — and other colleagues on the call — were deepfakes. The incident represented one of the largest-known deepfake fraud cases to date. But it won't be the last. Deepfake technology has progressed from requiring Hollywood-grade computing resources to running on consumer laptops. In 2023, a fake Joe Biden robocall told New Hampshire voters not to vote in the primary — generated by a political consultant using off-the-shelf AI tools for under $100. The detection arms race is equally intense. Microsoft, Sensity AI, and dozens of startups are building AI systems specifically designed to identify synthetic media. Governments are mandating watermarking standards. This article examines the state of deepfake detection technology, what works, what doesn't, and where the cat-and-mouse game is headed.</p>

<h2 id="what-are-deepfakes">Understanding Deepfakes: The Technology</h2>
<p>Deepfakes use deep learning — primarily Generative Adversarial Networks (GANs) and, more recently, diffusion models — to create synthetic media. Face swapping replaces one person's face with another in video. Lip sync / talking heads animate a still photo to match audio (used by HeyGen, D-ID, and similar commercial tools). Voice cloning synthesizes a person's voice from just a few seconds of sample audio (ElevenLabs, Respeecher). And full-body synthesis generates entirely fictional people (used in scam recruitment, fake LinkedIn profiles). The technology is dual-use: enabling creative expression and accessibility tools while also powering fraud, disinformation, and non-consensual intimate imagery.</p>

<h2 id="detection-methods">Detection Methods: How to Spot a Deepfake</h2>
<h3 id="visual-artifacts">Visual Artifact Detection</h3>
<p>Early deepfakes contained telltale imperfections. Blinking patterns: early GANs rarely generated natural blinking (approximately 2-4 blinks per minute for humans; deepfakes often blinked too frequently or not at all). Facial boundary inconsistencies: subtle lighting mismatches at jawlines where the swapped face meets the original neck/shoulders. And physiological impossibilities: blood flow patterns visible through skin ( photoplethysmography) that don't match realistic cardiovascular rhythms. Modern deepfakes have largely fixed these issues, requiring more sophisticated detection approaches.</p>

<h3 id="digital-forensics">Digital Forensic Analysis</h3>
<p>More sophisticated detection looks at underlying digital traces. PRNU (Photo Response Non-Uniformity): every camera sensor has tiny manufacturing imperfections creating a unique noise pattern; deepfakes lack this pattern or have inconsistent patterns. Compression artifacts: real video goes through specific compression pipelines (H.264, H.265); deepfakes often show inconsistent compression or double-compression artifacts. GAN fingerprint detection: each GAN architecture leaves microscopic patterns in generated images — like a digital signature. And metadata inconsistency: deepfake videos often have mismatched or missing metadata fields that reveal synthetic origin.</p>

<h3 id="audio-deepfake-detection">Audio Deepfake Detection</h3>
<p>Audio deepfakes are arguably more dangerous than video because they're easier to generate and can be used in real-time phone calls. Detection approaches include spectral analysis (deepfake voices often lack natural high-frequency components), prosody analysis (rhythm, stress, and intonation patterns that AI struggles to replicate authentically), and liveness detection (challenge-response protocols that require the speaker to perform unpredictable tasks). The U.S. Defense Advanced Research Projects Agency (DARPA) runs the Semantic Forensics (SemaFore) program specifically targeting multimodal deepfake detection.</p>

<h2 id="tools-and-platforms">Detection Tools and Platforms</h2>
<h3 id="microsoft">Microsoft Video Authenticator and C2PA</h3>
<p>Microsoft co-developed the C2PA (Coalition for Content Provenance and Authenticity) standard — cryptographic content credentials that embed tamper-evident metadata proving origin and edit history. Adobe, BBC, Intel, and Sony have joined the initiative. Microsoft's Video Authenticator provides a confidence score for whether a video is AI-manipulated, analyzing subtle grayscale elements that human eyes can't perceive. The tool is available as an API and browser extension.</p>

<h3 id="sensity">Sensity AI: The Deepfake Detection Specialist</h3>
<p>Sensity AI (formerly Amber Services) specializes in deepfake detection at scale. They claim to have detected over 250,000 deepfake videos online and provide enterprise API access for real-time detection. Their clients include financial institutions (for voice authentication security) and governments (for election integrity monitoring). Sensity's 2025 report found that deepfake detection accuracy has dropped from 95% (2021) to approximately 70% (2025) against state-of-the-art generation methods — illustrating the accelerating arms race.</p>

<h3 id="reality-defender">Reality Defender and Others</h3>
<p>Reality Defender provides browser-based deepfake detection, scanning images and videos uploaded or encountered online. Their "Reality Defender 2.0" detects AI-generated content from Stable Diffusion, Midjourney, DALL-E, and video generators like HeyGen and Synthesia. Deepware Scanner, InVID (used by journalists), and Forensic-Detection-of-Deepfake-Videos (open-source) provide additional detection capabilities. No single tool achieves >90% accuracy against current generation methods.</p>

<h2 id="the-arms-race">The Arms Race: Why Detection Gets Harder</h2>
<p>Every detection method spawns adversarial countermeasures. Adversarial perturbations: adding imperceptible noise to deepfakes that confuses detector classifiers (the "adversarial example" problem). Detector-aware training: newer deepfake generators train against detection models, optimizing to produce examples that evade known detectors. Diffusion model superiority: diffusion models (Stable Diffusion, DALL-E 3, Midjourney 6) produce images with more natural statistical properties than GANs, making forensic detection harder. And video quality improvements: 4K deepfake videos with natural blinking, breathing, and lighting are becoming indistinguishable from authentic footage even for trained human reviewers.</p>

<h2 id="policy-landscape">Policy and Regulatory Landscape</h2>
<p>Governments are responding to deepfake proliferation. U.S.: No federal comprehensive law yet, but individual states are acting. California's AB 602 (2024) requires disclosure of AI-generated political ads. Texas and Minnesota have similar requirements. The DEEPFAKES Accountability Act (introduced 2023, pending) would require labeling of AI-generated content. EU: The AI Act (adopted 2024) requires labeling of AI-generated content and prohibits certain uses of real-time biometric identification. China: requires watermarking of all AI-generated content (effective 2023). And voluntary industry commitments: major AI companies signed the White House voluntary commitments (2023) including watermarking and content provenance.</p>

<h2 id="future">What's Next: 2026-2030</h2>
<p>Three developments will shape the next phase. Multimodal detection: detecting deepfakes that span text, image, audio, and video simultaneously (the most sophisticated disinformation campaigns already use multiple modalities). Blockchain-based provenance: storing content hashes on immutable ledgers at capture time, enabling verification of authenticity throughout the content lifecycle. And real-time detection: moving from post-hoc analysis to in-stream detection — identifying deepfakes as they're being generated or streamed, enabling real-time flagging during live video calls.</p>

<h2 id="conclusion">Conclusion</h2>
<p>Deepfake detection is losing ground to deepfake generation — and the gap is widening. The solution isn't purely technological. It requires a defense-in-depth approach: technical detection tools (imperfect but improving), cryptographic provenance standards (C2PA), legal frameworks with real penalties, platform policies with enforcement teeth, and — most importantly — media literacy education that helps people develop healthy skepticism without descending into nihilism about truth. We're entering an era where "seeing is believing" is obsolete. The societies that navigate this transition successfully will be those that build resilient epistemic institutions — not just better algorithms.</p>
<p style="background:rgba(255,138,101,.08);border-left:3px solid #ff8a65;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(255,138,101,.05);border-radius:14px;border:1px solid rgba(255,138,101,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-content-gen.html" style="color:#ff8a65;text-decoration:none">→ AI Content Generation: How Newsrooms and Brands Are Embracing Automated Writing</a></li><li style="margin-bottom:10px"><a href="/en/articles/article-deepfake-news-integrity.html" style="color:#ff8a65;text-decoration:none">→ Deepfake News Integrity: Protecting Information in the Synthetic Media Era</a></li></ul></div>
"""

# ============================================================
# ARTICLE 15: article-deepfake-news-integrity.html
# ============================================================
DEEPFAKE_NEWS = """
<h2 id="intro">The Existential Threat to Journalism's Foundation</h2>
<p>Journalism rests on a simple premise: reporters gather verifiable facts, editors verify them, and audiences trust the resulting information. Deepfakes undermine every link in this chain. A fabricated video of a politician saying something inflammatory can spread globally before fact-checkers can respond. The threat isn't theoretical — it's already happening, and the pace is accelerating. In March 2024, robocalls using an AI-cloned voice of President Biden urged New Hampshire voters not to participate in the primary election. The FCC traced the calls and imposed fines, but not before thousands received the fraudulent messages. In 2023, a deepfake video of Pentagon explosion caused a brief stock market dip — illustrating how synthetic media can now move markets. This article examines how news organizations are adapting to protect information integrity in the synthetic media era.</p>

<h2 id="threat-landscape">The Threat Landscape for News Organizations</h2>
<h3 id="disinformation-campaigns">Coordinated Disinformation Campaigns</h3>
<p>State actors and organized groups are already deploying synthetic media for information warfare. Deepfake propaganda: fabricated videos of opposition leaders making inflammatory statements, designed for viral dissemination. Context manipulation: real footage placed in false contexts (a 2023 video of a Taiwan explosion was recirculated in 2024 as footage from a different conflict). Synthetic witnesses: fake "eyewitness" videos of events that never happened, complete with AI-generated background details. And at-scale generation: AI can produce thousands of disinformation content variations, each slightly different to evade platform detection systems.</p>

<h3 id="market-manipulation">Financial Market Manipulation</h3>
<p>Deepfakes pose particular danger to financial news integrity. CEO deepfakes: synthetic video/audio of executives making false announcements (earnings misses, merger news, safety issues). In 2024, a deepfake video of a major bank's CEO announcing liquidity problems circulated on X and was briefly reported by a financial blog before being debunked — but not before the bank's stock dipped 3%. Analyst report forgery: fabricating research reports from reputable firms. And economic data falsification: synthetic "leaks" of government indicators (employment, inflation, GDP) that move markets before corrections.</p>

<h2 id="defenses">Defensive Measures: How Newsrooms Are Responding</h2>
<h3 id="verification-toolkits">Verification Toolkits</h3>
<p>News organizations are building verification infrastructure. First Draft News (founded by Craig Silverman) provides verification guides and training for journalists. Their "Checklist for Verifying User-Generated Content" is the industry standard. Reuters Facts / Reuters Signal helps journalists verify images and claims in real-time, including reverse image search, metadata analysis, and sun position verification (verifying that shadows in a photo match the claimed time and location). AFP Fact Check operates one of the world's largest fact-checking networks, with dedicated teams in 30+ countries. And FactCheck.org and PolitiFact specialize in political claim verification, maintaining databases of previously fact-checked statements.</p>

<h3 id="journalistic-workflows">Updated Journalistic Workflows</h3>
<p>Newsrooms are adapting their workflows. Source authentication protocols: multi-factor verification for video/audio evidence (requesting the original file, verifying chain of custody, cross-referencing with other sources). Provenance documentation: maintaining auditable chains of custody with C2PA content credentials where available. Rapid response teams: dedicated units for viral content verification (BBC's "Reality Check" team, AP's fact-checking operation). And transparency in correction: clear policies for when synthetic media is initially reported as genuine, including prominent corrections and "editor's notes" explaining what went wrong and how it was fixed.</p>

<h2 id="platform-responsibility">Platform Responsibility and Content Moderation</h2>
<h3 id="meta-policy">Meta (Facebook/Instagram)</h3>
<p>Meta's approach to deepfake content has evolved significantly. Their 2024 policy prohibits deceptive AI-generated audio and video targeting elections, but enforcement is inconsistent. Meta applies "AI-generated" labels to some synthetic content but misses substantial amounts. Independent analyses suggest Meta's automated detection catches approximately 60-70% of deepfake content, with the remainder relying on user reports and fact-checker partnerships.</p>

<h3 id="youtube-policy">YouTube: Bridging to Shorts</h3>
<p>YouTube prohibits technically manipulated content that misleads users in harmful ways, particularly around elections and health. Their approach includes requiring disclosure of AI-generated content in video descriptions, applying information panels with fact-checks, and demonetizing videos that repeatedly violate synthetic media policies. YouTube's reach — 2.5 billion logged-in monthly users — makes its deepfake policy perhaps the most impactful globally.</p>

<h3 id="tiktok-policy">TikTok: The Disinformation Battleground</h3>
<p>TikTok's algorithm-driven "For You" feed makes it particularly dangerous for deepfake dissemination — false content can reach millions before moderation catches it. TikTok prohibits deepfakes of private individuals and deceptive deepfakes of public figures, but enforcement challenges are substantial given 1 billion+ daily videos uploaded. TikTok's "Content Verification" team uses both AI detection and human review, but the scale challenge is unprecedented.</p>

<h2 id="media-literacy">Media Literacy: The Long-Term Defense</h2>
<p>Technology alone cannot solve the deepfake problem. Media literacy education is essential. Finland's model: the Finnish government integrated media literacy into the national curriculum starting at age 7, teaching critical thinking about information sources. A 2024 European Media Literacy Index ranked Finland #1 for resilience to disinformation. The "lateral reading" technique: teaching people to verify information by opening new tabs and checking multiple sources rather than evaluating a single page. Emotional awareness training: teaching people to slow down and verify before sharing content that triggers strong emotions (anger, fear, outrage) — because these are the emotions most effectively exploited by disinformation campaigns.</p>

<h2 id="future">The Path Forward: A Multi-Layered Defense</h2>
<p>The defense requires simultaneous action on all fronts. Technical standards: C2PA implementation across cameras, smartphones, and editing software — so content carries verifiable provenance from capture. Legal frameworks: laws with real penalties for harmful deepfake creation/distribution, balanced against free expression protections. Platform accountability: consistent, transparent, and adequately resourced content moderation. Journalism investment: supporting fact-checking organizations and investigative journalism that holds bad actors accountable. And education at scale: making media literacy as fundamental as reading and writing in the AI era.</p>

<h2 id="conclusion">Conclusion</h2>
<p>Deepfake technology threatens the epistemic foundation that democratic societies depend on — shared, verifiable facts about reality. The threat is asymmetric: creating convincing fakes is cheap and easy; verifying authenticity is expensive and slow. But surrendering to a post-truth world isn't acceptable. The defense requires action on all fronts: technical standards, legal frameworks, platform accountability, journalism investment, and education. No single solution suffices. The societies that preserve information integrity wil be those that treat this as a civilizational priority — not just a technical problem to be solved, but a democratic imperative to be defended. The window for effective action is narrowing. The time to act is now.</p>
<p style="background:rgba(255,138,101,.08);border-left:3px solid #ff8a65;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(255,138,101,.05);border-radius:14px;border:1px solid rgba(255,138,101,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-deepfake-detect.html" style="color:#ff8a65;text-decoration:none">→ Deepfake Detection: Authenticating Reality in the Age of Synthetic Media</a></li><li style="margin-bottom:10px"><a href="/en/articles/article-content-gen.html" style="color:#ff8a65;text-decoration:none">→ AI Content Generation: How Newsrooms and Brands Are Embracing Automated Writing</a></li></ul></div>
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
        ("article-content-gen.html", CONTENT_GEN),
        ("article-deepfake-detect.html", DEEPFAKE_DETECT),
        ("article-deepfake-news-integrity.html", DEEPFAKE_NEWS),
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
