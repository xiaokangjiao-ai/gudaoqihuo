"""
Inject batch 5 (final): HR (2) + Media (3) = 5 articles.
"""
from pathlib import Path
import re

ARTICLES_DIR = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles")

# ============================================================
# ARTICLE 11: article-resume-screening.html
# ============================================================
RESUME_SCREENING = """
<h2 id="intro">75% of Resumes Are Never Seen by a Human</h2>
<p>A corporate job posting attracts an average of 250 resumes. Of those, 75% are filtered out before any human reviewer reads them. For Fortune 500 companies receiving milions of applications annually, manual resume screening is logistically impossible. Enter AI-powered resume screening: software that parses, scores, and ranks candidates in seconds, promising to reduce time-to-hire by 75% and cost-per-hire by 50%. HireVue reports their clients screen over 4 milion candidates annually using their AI systems. Eightfold AI, valued at $2.1 bilion in their 2024 funding round, counts Microsoft, Bayer, and Macy's among its customers. The technology is transforming recruiting — but not without significant controversy about bias, fairness, and the very definition of merit.</p>

<h2 id="how-it-works">How AI Resume Screening Works</h2>
<h3 id="parsing">Resume Parsing and Structuring</h3>
<p>Before AI can evaluate a resume, it must convert unstructured text into structured data. Entity extraction identifies names, contact information, education institutions, work experience (company, title, dates, accomplishments), and skills (programming languages, certifications, soft skills). Normalization maps varied job titles to canonical roles: "Software Engineer," "Backend Developer," and "Python Developer" al converge to a standardized taxonomy. And enrichment cross-references company names with industry classifications, sizes, and growth trajectories to contextualize candidate experience levels.</p>

<h3 id="scoring">Scoring and Ranking</h3>
<p>Once parsed, AI systems evaluate candidates against job requirements using multiple approaches. Keyword matching (the simplest) checks for required skills and qualifications — but fails to capture semantic meaning. Semantic matching uses NLP models (BERT, RoBERTa) to understand that "managed a team of 12 engineers" implies leadership experience even without the exact keyword "leadership." Contextual evaluation considers career trajectory (steady progression vs. job hopping), company caliber, and achievement quality. And predictive scoring uses historical hiring data to predict which candidates are most likely to receive offers, accept offers, and succeed in the role — though this approach carries significant bias risks.</p>

<h2 id="bias-problem">The Bias Problem: Real Concerns and Evidence</h2>
<p>AI resume screening's biggest challenge is algorithmic bias — and the evidence is sobering. Amazon scrapped their internal recruiting bot in 2018 after discovering it penalized resumes containing the word "women's" (as in "women's chess club captain") and downgraded graduates of al-women's colleges. A 2023 study by the University of California found that resume screening algorithms consistently scored resumes with traditionally White names higher than identical resumes with Black names. University prestige bias is another well-documented problem: models trained on historical hiring data from elite firms learn to favor Ivy League graduates, perpetuating class-based exclusion. And language bias emerges when models penalize non-native English speakers whose resumes contain grammatical quirks that don't reflect job capability.</p>

<h3 id="regulation">Regulation: The Legal Landscape</h3>
<p>Governments are responding. New York City Local Law 144 (effective July 2023) requires bias audits for automated employment decision tools and disclosure to candidates. The EU AI Act (adopted 2024) classifies AI resume screening as "high-risk," requiring conformity assessments, transparency measures, and human oversight. Similarly, the California Fair Employment and Housing Act was updated in 2025 to cover algorithmic screening. At the federal level, the EEOC's "Enforcement Guidance on Algorithmic Fairness" (May 2024) makes clear that employers are liable for discriminatory outcomes from AI tools, even if the discrimination is unintentional.</p>

<h2 id="market-leaders">Market Leaders and Their Approaches</h2>
<h3 id="eightfold">Eightfold AI: The Talent Intelligence Platform</h3>
<p>Eightfold (founded by Ashutosh Garg and Varun Kacholia, both ex-Google) takes a "talent intelligence" approach — not just screening resumes but building a comprehensive understanding of each candidate's skills, potential, and career aspirations. Their "deep-learning" matching considers 50+ factors beyond what's on the resume: career velocity, skill adjacency (can a Java developer quickly learn C#?), and even personality fit based on language patterns. Eightfold reports that clients using their platform see 25% improvement in quality-of-hire and 35% reduction in time-to-fill for hard-to-fil positions.</p>

<h3 id="hirevue">HireVue: Video + AI (And the Controversy)</h3>
<p>HireVue gained notoriety in 2019 when they introduced AI analysis of video interviews — analyzing facial expressions, word choice, and speaking patterns to predict job performance. The practice drew fierce criticism from AI ethicists and was ultimately scaled back significantly. HireVue now focuses more on structured interview scheduling, skills assessments, and resume screening — and they've published detailed bias audit results showing their models don't exhibit significant demographic disparities. The episode taught the industry a valuable lesson: just because you can analyze something with AI doesn't mean you should.</p>

<h3 id="workday">Workday: The Enterprise Plaform Leader</h3>
<p>Workday's "Skills Cloud" and recruiting modules use AI to match internal and external candidates to roles based on verified skills rather than just job titles. With over 10,500 enterprise customers, Workday's approach has enormous reach. Their 2025 "Global Skills Gap" report found that 60% of enterprise roles now require skills that didn't exist five years ago — making AI-powered skills mapping essential for agile workforce planning. Workday also emphasizes "responsible AI" with built-in bias monitoring dashboards for HR teams.</p>

<h2 id="best-practices">Best Practices for Ethical AI Hiring</h2>
<p>Organizations deploying AI resume screening should follow several best practices. Regular bias audits: test models for disparate impact across demographic groups using withheld application data. Human-in-the-loop: never make final reject decisions based purely on AI scores; always have human review of top-ranked candidates. Transparent evaluation criteria: candidates should be able to request information about how AI evaluated them (required under NYC Local Law 144 and soon other jurisdictions). Diverse training data: ensure historical hiring data used for model training is balanced across demographics. And continuous monitoring: hiring outcome distributions by demographic group should be reviewed monthly, with model retraining or adjustment when disparities emerge.</p>

<h2 id="future">The Future of AI in Recruiting</h2>
<p>Three trends will define the next era. Skills-based hiring: shifting from degree requirements and job titles to verified skills, enabled by AI that can extract and validate competencies from diverse experiences. Passive candidate sourcing: AI that identifies "silver medalists" — candidates who were runner-up for past roles and might be perfect for new openings — and engages them proactively. And conversational AI: chatbots that conduct initial screening interviews, answer candidate questions, and provide status updates — reducing time-to-response from days to seconds and improving candidate experience metrics significantly.</p>

<h2 id="conclusion">Conclusion</h2>
<p>AI resume screening solves a genuine problem: the sheer volume of job applications makes manual screening impractical at scale. Well-implemented systems can reduce time-to-hire, expand candidate reach, and reduce unconscious bias compared to human screeners (who are also biased, but in less measurable ways). But the technology carries serious risks — primarily the amplification of historical biases and the "black box" problem where candidates and employers can't understand why a decision was made. The organizations that wil succeed with AI hiring aren't those with the most sophisticated algorithms, but those that implement rigorous bias auditing, maintain human oversight, prioritize transparency, and treat AI as a tool for efficiency rather than a replacement for human judgment. The goal isn't to automate hiring — it's to augment human recruiters so they can focus on what humans do best: assessing cultural fit, evaluating potential, and building relationships.</p>
<p style="background:rgba(171,71,188,.08);border-left:3px solid #ab47bc;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(171,71,188,.05);border-radius:14px;border:1px solid rgba(171,71,188,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-people-analytics.html" style="color:#ab47bc;text-decoration:none">→ People Analytics: Data-Driven Insights for Workforce Decisions</a></li></ul></div>
"""

# ============================================================
# ARTICLE 12: article-people-analytics.html
# ============================================================
PEOPLE_ANALYTICS = """
<h2 id="intro">Your Employees Generate Data — Are You Using It?</h2>
<p>The average enterprise company collects more data about its employees than it realizes: login times, calendar patterns, collaboration network graphs, project management tool activity, performance review scores, compensation history, and engagement survey responses. Most of this data sits unused in HR information systems, payroll platforms, and communication tools. People analytics — also called workforce analytics or HR analytics — transforms this data into actionable insights about productivity, engagement, retention, and organizational effectiveness. Visier, the leading people analytics platform, reports that organizations with mature people analytics practices see 26% higher revenue per employee, 22% lower turnover, and 34% better hiring outcomes compared to laggards. The business case is compelling. The implementation challenge is real.</p>

<h2 id="what-is">What Is People Analytics?</h2>
<p>People analytics applies statistical analysis, machine learning, and data visualization to workforce data to answer questions like: who is at risk of leaving? (flight risk models analyze tenure, promotion velocity, compensation relative to market, engagement survey scores, and collaboration patterns); what drives performance? (correlating individual and team performance with management practices, team composition, and work environment factors); is our diversity improving? (tracking representation and pay equity over time across demographics); and what does our organizational network look like? (organizational network analysis maps email, Slack, and meeting patterns to identify informal influencers, collaboration bottlenecks, and information silos).</p>

<h2 id="key-use-cases">Key Use Cases Driving ROI</h2>
<h3 id="attrition">Attrition Prediction and Retention</h3>
<p>Replacing an employee costs 50-200% of their annual salary depending on seniority and role. People analytics tackles this problem systematically. Google's people analytics team (the famous "People Operations") developed attrition prediction models that identified key flight risk factors: having a close colleague leave, reporting to a new manager, declining meeting participation, and reduced Slack message frequency. By intervening proactively — assigning a mentor, adjusting compensation, or improving manager relationship — Google reduced turnover in high-risk segments by 20% in a controlled study. Microsoft's people analytics team uses similar approaches, with their "Work Trend Index" providing ongoing insights into global workforce dynamics.</p>

<h3 id="engagement">Employee Engagement and Experience</h3>
<p>Glint (now part of Microsoft Viva, rebranded as Viva Glint) pioneered real-time employee engagement pulse surveys. Their AI analyzes free-text comments at scale, identifying themes and sentiment without manual coding. Companies using Glint report 14% higher engagement scores after two years of data-driven intervention. The platform also identifies "engagement drivers" specific to each organization: at one tech company, flexible work hours was the #1 driver; at a manufacturing firm, it was physical safety and equipment quality. People analytics moves engagement from annual survey to continuous feedback loop.</p>

<h3 id="workforce-planning">Workforce Planning and Skills Intelligence</h3>
<p>Beyond retention and engagement, people analytics enables strategic workforce planning. Skills inventories map current employee skills to identify gaps and redundancies. Scenario planning models the impact of automation, offshoring, or market expansion on workforce needs. And internal mobility optimization uses matching algorithms to identify high-potential internal candidates for open roles — reducing external hiring costs and improving retention simultaneously. Eightfold AI's "Talent Intelligence Platform" automates much of this, maintaining "talent wallets" for each employee that track verified skills, career aspirations, and development progress.</p>

<h2 id="tools-ecosystem">The Tools Ecosystem: A Comparison</h2>
<table style="width:100%;border-collapse:collapse;margin:20px 0;color:#ccc">
<tr style="background:rgba(171,71,188,.1)"><th style="padding:10px;text-align:left;border:1px solid #333">Platform</th><th style="padding:10px;text-align:left;border:1px solid #333">Strength</th><th style="padding:10px;text-align:left;border:1px solid #333">Best For</th><th style="padding:10px;text-align:left;border:1px solid #333">Pricing</th></tr>
<tr><td style="padding:8px;border:1px solid #333">Visier</td><td style="padding:8px;border:1px solid #333">Deep analytics, benchmarking</td><td style="padding:8px;border:1px solid #333">Enterprise (1,000+ employees)</td><td style="padding:8px;border:1px solid #333">$15-30/employee/month</td></tr>
<tr><td style="padding:8px;border:1px solid #333">Viva Glint</td><td style="padding:8px;border:1px solid #333">Engagement + M365 integration</td><td style="padding:8px;border:1px solid #333">Microsoft-centric organizations</td><td style="padding:8px;border:1px solid #333">$8-12/employee/month</td></tr>
<tr><td style="padding:8px;border:1px solid #333">Culture Amp</td><td style="padding:8px;border:1px solid #333">Employee voice, DEI analytics</td><td style="padding:8px;border:1px solid #333">Mid-market (200-5,000)</td><td style="padding:8px;border:1px solid #333">$10-18/employee/month</td></tr>
<tr><td style="padding:8px;border:1px solid #333">ChartHop</td><td style="padding:8px;border:1px solid #333">Org visualization, comp planning</td><td style="padding:8px;border:1px solid #333">Growing tech companies</td><td style="padding:8px;border:1px solid #333">$12-20/employee/month</td></tr>
<tr><td style="padding:8px;border:1px solid #333">Workday</td><td style="padding:8px;border:1px solid #333">Full HCM + analytics suite</td><td style="padding:8px;border:1px solid #333">Large enterprise (5,000+)</td><td style="padding:8px;border:1px solid #333">Custom enterprise pricing</td></tr>
</table>

<h2 id="ethical-concerns">Ethical Concerns and Privacy</h2>
<p>People analytics operates in ethically fraught territory. Surveillance concerns: when every keystroke, meeting attendance, and Slack message is analyzed, employees feel monitored rather than supported. Some companies have walked back aggressive analytics programs after employee pushback. Predictive injustice: flight risk predictions can become self-fulfilling prophecies — once identified as a flight risk, employees may be passed over for projects, accelerating their decision to leave. Data security: workforce data includes salary, performance ratings, and health information — making it a target for breaches and requiring stringent access controls. Union implications: in unionized workplaces, people analytics can be seen as management surveillance, triggering labor relations issues. And transparency: employees have a right to know what data is collected about them and how it's used — a principle established in GDPR's "right to explanation" and similar regulations globally.</p>

<h2 id="future">The Future of People Analytics</h2>
<p>Three developments will shape the field through 2030. Skills ontologies: standardized, interoperable skills taxonomies (led by the HR Open Standards community) will enable portable skills profiles that follow employees across roles and organizations. Passive listening: people analytics that operates entirely on metadata (meeting attendance, email response times) without reading message content — addressing privacy concerns while preserving insight value. And AI-generated insights: large language models that analyze years of engagement surveys, performance reviews, and exit interviews to generate executive summaries and recommended actions — reducing the "last mile" problem where insights are generated but never acted upon.</p>

<h2 id="conclusion">Conclusion</h2>
<p>People analytics represents a maturing discipline that bridges data science and human resources. Done well, it helps organizations make evidence-based decisions about their most valuable asset: their people. Done poorly — without transparency, consent, and ethical guardrails — it becomes surveillance that erodes trust and damages culture. The organizations that wil thrive are those that treat people analytics as a tool for supporting employees, not just managing them. The best HR leaders already know: analytics should inform decisions, but empathy should make them.</p>
<p style="background:rgba(171,71,188,.08);border-left:3px solid #ab47bc;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(171,71,188,.05);border-radius:14px;border:1px solid rgba(171,71,188,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-resume-screening.html" style="color:#ab47bc;text-decoration:none">→ AI Resume Screening: Efficiency, Bias, and the Future of Hiring</a></li></ul></div>
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
        ("article-resume-screening.html", RESUME_SCREENING),
        ("article-people-analytics.html", PEOPLE_ANALYTICS),
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
