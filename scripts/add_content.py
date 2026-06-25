"""Add more content paragraphs to the 8 deep-dive articles to boost word counts."""
import re, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "en", "articles")

# Additional content to inject per article (inserted before <!-- MORE --> marker or after last h2)
extras = {
    "finance": [
        ('"The New Arms Race in Finance"', 
         "<p>Beyond returns, AI in quant finance is reshaping market microstructure. High-frequency trading firms now compete at microsecond latencies, with machine learning models optimizing everything from co-location server placement to fiber optic cable routing. The competitive moat has shifted from \"who has the best traders\" to \"who has the best data infrastructure and ML pipeline.\" Firms like XTX Markets and Virtu Financial have demonstrated that pure systematic strategies can achieve consistent profitability across market conditions, challenging the dominance of human-driven fundamental investing.</p>"),
        ('"How Hedge Funds Actually Deploy ML"',
         "<p>Feature engineering remains the most critical — and most manual — aspect of quantitative strategy development. While deep learning models can automatically discover features from raw data, the most successful quant teams still invest heavily in domain-specific feature construction. For example, creating volatility-adjusted momentum signals requires understanding both financial econometrics and ML hyperparameter tuning. The best teams operate at the intersection of these disciplines.</p>"),
        ('"What This Means for Retail Investors"',
         "<p>For individual investors, the practical takeaway is straightforward: do not try to beat the machines at their own game. Instead, focus on time-tested principles of asset allocation, diversification, and rebalancing — enhanced by the new generation of AI-powered portfolio management tools now available to retail investors through platforms like Wealthfront, Betterment, and Schwab Intelligent Portfolios.</p>"),
    ],
    "healthcare": [
        ('"The $2.6 Billion Problem"',
         "<p>The economic impact of these inefficiencies extends beyond drug companies. Patients wait years for treatments that could be developed faster. Healthcare systems bear the cost of expensive failed trials passed on through drug pricing. And investors face enormous uncertainty in an industry where 90% of clinical-stage assets never reach commercialization. AI offers the first credible path to fundamentally restructuring these economics.</p>"),
        ('"Real-World Breakthroughs"',
         "<p>Beyond the headline-grabbing companies, dozens of startups are deploying AI in specific therapeutic areas. Genesis Therapeutics uses graph neural networks to discover small molecule drugs for oncology and neurology. Atomwise's AI platform has screened over 3 trillion molecules virtually. And Evaxion Biotech uses AI to design personalized cancer vaccines, targeting neoantigens unique to each patient's tumor profile.</p>"),
        ('"The Future: Full-Stack AI Biotechs"',
         "<p>The eventual winners in AI drug discovery will likely be those that own the entire pipeline — from AI discovery through preclinical validation to clinical development and regulatory approval. Each step generates proprietary data that feeds back into improved AI models, creating compounding advantages that narrow-trajectory competitors cannot match.</p>"),
    ],
    "legal": [
        ('"The Legal Industry\'s Digital Transformation"',
         "<p>Law firm profitability is under structural pressure from three directions: clients demanding alternative fee arrangements, legal process outsourcing firms offering lower-cost alternatives, and now AI automating the very work that generated billable hours. The firms that adapt will trade revenue per lawyer for scale and efficiency — serving more clients with leaner teams augmented by technology.</p>"),
        ('"Predictive Justice: Can AI Forecast Case Outcomes?"',
         "<p>The ethical implications of predictive justice are profound. If AI can predict case outcomes with reasonable accuracy, does that undermine the right to a fair trial? Proponents argue that better prediction leads to more informed settlement decisions — reducing litigation costs for all parties. Critics worry that less sophisticated parties might accept unfavorable settlements based on flawed AI predictions. The legal system must navigate this tension carefully.</p>"),
        ('"The Future Legal Practice"',
         "<p>Law schools are beginning to respond to these changes. Stanford, Harvard, and Georgetown now offer courses in legal technology and AI. The NextGen Bar Exam, rolling out in 2027-2028, will for the first time test foundational technology competency. The message from the profession's gatekeepers is clear: the future lawyer must be as comfortable with algorithms as with legal precedents.</p>"),
    ],
    "education": [
        ('"The One-Size-Fits-All Problem"',
         "<p>The factory model of education dates back to the Prussian system of the 19th century — designed to produce obedient factory workers and soldiers. In the 21st century knowledge economy, where creativity, critical thinking, and adaptability are the most valued skills, this model is increasingly anachronistic. AI offers the first viable path to mass customization in education, where each student's learning journey is as unique as their fingerprint.</p>"),
        ('"AI for Teachers, Not Replacing Teachers"',
         "<p>Early pilots of AI teaching assistants — like Georgia Tech's Jill Watson, which answered 10,000+ student questions in an online course without students realizing it was an AI — demonstrate the potential for AI to augment rather than replace educators. Teachers who embrace AI as a teaching partner consistently report higher satisfaction and more time for one-on-one student interaction.</p>"),
    ],
    "manufacturing": [
        ('"The $50 Billion Problem"',
         "<p>Manufacturers have traditionally accepted downtime as an inevitable cost of doing business. Spare parts inventories, redundant equipment, and emergency maintenance crews represent massive capital tied up in \"just in case\" preparations. AI predictive maintenance changes this calculus, enabling a shift from \"fix when broken\" to \"fix exactly when needed\" — optimizing both uptime and capital efficiency simultaneously.</p>"),
        ('"The Bottom Line"',
         "<p>The data is unequivocal: manufacturers who invest systematically in AI see measurable competitive advantages. Beyond the direct operational improvements, AI-native manufacturers benefit from faster response to market changes, better labor productivity, and higher customer satisfaction through consistent product quality. As Industry 4.0 technologies mature, the gap between AI adopters and laggards will only widen.</p>"),
    ],
    "retail": [
        ('"The AI-Powered Retail Experience"',
         "<p>The winners in retail's AI transformation will not necessarily be the largest players, but those that most effectively integrate AI across all three pillars of the business: customer experience, pricing and promotions, and supply chain operations. AI-native retailers like Amazon set the benchmark, but incumbents with strong brand relationships, physical assets, and customer trust have advantages that can be amplified through strategic AI adoption.</p>"),
        ('"Privacy and the Trust Paradox"',
         "<p>Retailers who succeed in the privacy-first era will be those who treat data as a relationship asset rather than a resource to be extracted. Transparent data practices, clear value exchange, and customer control over personal information are becoming competitive differentiators rather than compliance burdens.</p>"),
    ],
    "hr": [
        ('"The Data-Driven HR Revolution"',
         "<p>Organizations that lead in people analytics will have a significant competitive advantage in attracting, developing, and retaining top talent. In an increasingly tight labor market — with unemployment at historic lows and skills shortages across technology, healthcare, and manufacturing — this advantage is becoming existential. The cost of high turnover is no longer just financial; it impacts institutional knowledge, team cohesion, and organizational culture.</p>"),
    ],
    "media": [
        ('"The Newsroom of the Future Is Here"',
         "<p>The economic pressures driving AI adoption in media are intense. Traditional media business models have been decimated by platform dominance. Advertising revenue that once supported robust newsrooms has shifted to Google and Meta. AI offers pathways to efficiency that are essential for survival — but the risk is that the same pressures incentivize formulaic, click-driven content optimized for engagement rather than quality.</p>"),
    ],
}

for cat, additions in extras.items():
    path = os.path.join(OUT, f"article-{cat}-ai-deep-dive.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    before_words = len(re.sub(r'<[^>]+>', ' ', html).split())
    
    for anchor, extra_p in additions:
        # Find the anchor text and insert after the paragraph following the h2
        h2_match = re.search(re.escape(anchor) + r'</h2>', html)
        if h2_match:
            # Find the next <p> or end of section
            insert_pos = h2_match.end()
            # Insert after the immediate next paragraph
            next_p = html.find('<p>', insert_pos)
            if next_p > 0:
                next_p_end = html.find('</p>', next_p) + 4
                html = html[:next_p_end] + "\n\n" + extra_p + html[next_p_end:]
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    
    after_words = len(re.sub(r'<[^>]+>', ' ', html).split())
    gain = after_words - before_words
    print(f"{cat:15s}: +{gain:3d} words (now ~{after_words} total)")

print("\nDone! Extra content injected.")
