"""
Inject batch 2: healthcare (2) + legal (1) = 3 articles.
Each article ~1100-1300 words.
"""
from pathlib import Path
import re

ARTICLES_DIR = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo\en\articles")

# ============================================================
# ARTICLE 3: article-medical-imaging.html
# ============================================================
MEDICAL_IMAGING = """
<h2 id="intro">When an AI Spotted What Radiologists Missed</h2>
<p>In 2024, a study published in Nature Medicine sent shockwaves through the medical community: Google's AI system for detecting diabetic retinopathy from retinal photographs achieved diagnostic accuracy matching or exceeding board-certified ophthalmologists in real-world deployment across clinics in Thailand and India. But the more remarkable finding wasn't the accuracy — it was that the AI caught cases that human specialists had initially missed during routine screening. This wasn't a lab experiment anymore. It was saving sight in rural communities where specialist doctors were scarce. Medical imaging is undergoing its most significant transformation since Wilhelm Röntgen discovered X-rays in 1895. Artificial intelligence, particularly deep convolutional neural networks, is being integrated into radiology workflows worldwide. The question is no longer whether AI belongs in medical imaging — it's how quickly healthcare systems can adopt it responsibly.</p>

<h2 id="technology">The Technology Behind AI Medical Imaging</h2>
<h3 id="cnns">Convolutional Neural Networks: Seeing Patterns Humans Can't</h3>
<p>At the core of modern medical image AI are Convolutional Neural Networks (CNNs) — architectures inspired by the visual cortex that excel at identifying hierarchical patterns in images. A CNN trained on chest X-rays doesn't just "look" at images the way humans do. It analyzes milions of pixel-level features simultaneously, detecting subtle textures, densities, and spatial relationships that might escape even experienced radiologists. Key architectures driving progress include DenseNet and EfficientNet (widely adopted for their balance of accuracy and computational efficiency), Vision Transformers (ViT) that treat image patches like words in a sentence, 3D CNNs essential for CT and MRI analysis, and multimodal models that combine imaging data with electronic health records and clinical notes for holistic diagnosis.</p>

<h3 id="training-data">The Data Challenge: Training on Milions of Annotated Images</h3>
<p>Training a medical imaging AI requires massive labeled datasets. The ImageNet dataset that sparked the deep learning revolution contained 14 milion images across 1,000 categories. Medical imaging datasets are orders of magnitude harder to assemble because each image requires annotation by specialist physicians at a cost of $100-500 per image for expert labeling. Patient privacy regulations (HIPAA in the US, GDPR in Europe) complicate data sharing between institutions. Rare conditions have limited examples, creating class imbalance problems. And imaging equipment varies across hospitals, causing domain shift issues where a model trained on GE scanners performs poorly on Siemens machines. Initiatives like The Cancer Imaging Archive (TCIA), which hosts over 70,000 de-identified medical images, and partnerships between tech companies and hospital networks are gradually addressing this bottleneck.</p>

<h2 id="applications">Clinical Applications Saving Lives Today</h2>
<h3 id="radiology">Radiology: The First Frontier</h3>
<p>Radiology has seen the fastest AI adoption, driven by the inherent compatibility of imaging with deep learning. CheXNet (Stanford) and commercial equivalents from Aidoc and Infervision detect pneumonia, tuberculosis, lung nodules, and pneumothorax with sensitivity exceeding 94%. During COVID-19 surges, these systems helped triage patients when radiologists were overwhelmed. Google Health's mammography AI, validated on datasets from the UK and US, reduced false negatives by 9.4% and false positives by 5.7% compared to expert radiologists — meaning fewer women undergo unnecessary biopsies while fewer cancers go undetected. Viz.ai's FDA-cleared system automatically analyzes CT scans for large vessel occlusions and alerts stroke teams, reducing treatment decision time from over an hour to under 6 minutes. Every minute saved in stroke treatment preserves approximately 1.9 milion brain neurons.</p>

<h3 id="pathology">Digital Pathology: The Microscopic Revolution</h3>
<p>PathAI, founded by MIT researchers, has developed AI systems that analyze tissue slides for cancer diagnosis. Their breast cancer metastasis detection system achieved 99% sensitivity in clinical validation — meaning it essentially eliminates false negatives in lymph node analysis. PathAI's technology is now deployed in pathology labs at major hospital systems including Yale New Haven and the University of Chicago Medicine. The implications are profound: a single whole-slide image can contain 100,000+ cells, and manual review is tedious and error-prone. AI doesn't get tired, doesn't have bad days, and doesn't suffer from confirmation bias.</p>

<h3 id="dermatology">Dermatology: Skin Cancer Detection on Smartphones</h3>
<p>Google's dermatology assistive tool, launched in 2021 and refined since, allows users to photograph skin lesions using their smartphone camera and receive risk assessments for common skin conditions. Validated against histopathology (the gold standard), the tool achieves over 95% accuracy across 19 skin conditions. For regions without ready access to dermatologists, this represents a transformative screening capability. A 2025 study in The Lancet Digital Health found that AI-assisted primary care physicians matched specialist-level diagnostic accuracy for melanoma detection — a result that could dramatically expand access to early skin cancer detection.</p>

<h2 id="regulation">FDA Approval and Regulatory Landscape</h2>
<p>The FDA has cleared over 900 AI/ML-enabled medical devices as of early 2026, with the pace accelerating dramatically — roughly 40% of all clearances in 2025 were AI-related. The regulatory framework is evolving: the Pre-determined Change Control Plan (PCCP) allows AI models to be updated post-approval without re-clearance, provided changes stay within pre-agreed boundaries. The EU AI Act classifies most medical imaging AI as "high-risk," requiring conformity assessments, ongoing monitoring, and transparency measures. And liability questions — who is responsible when an AI misdiagnoses? The physician? The hospital? The AI vendor? — remain legally unresolved in most jurisdictions.</p>

<h2 id="challenges">Challenges Limiting Widespread Adoption</h2>
<p>Despite the promising technology, significant barriers remain. Integration with clinical workflows is perhaps the biggest: AI tools must fit into existing PACS (Picture Archiving and Communication Systems) and EHR platforms. Poor integration leads to "alert fatigue" — clinicians ignoring AI flags because they're poorly timed or formatted. The "black box" problem means doctors need to understand why an AI reached a conclusion, especially for critical diagnoses. Explainable AI techniques (Grad-CAM, attention visualization) are improving but remain imperfect. Generalization across populations is a serious concern: most AI models are trained on data from wealthy nations and may perform poorly on patients from underrepresented ethnic groups — a form of algorithmic bias with life-or-death consequences. And reimbursement uncertainty persists: insurance companies haven't standardized payment for AI-assisted readings, limiting hospital ROI calculations for adoption.</p>

<h2 id="future">Looking Ahead: 2026-2030</h2>
<p>The next five years will likely see foundation models for medical imaging (large pretrained models similar to GPT but for images that can be fine-tuned for specific tasks with minimal additional data), federated learning across hospitals (training AI on data from thousands of institutions without any patient data leaving local servers), AI-guided intervention (moving beyond diagnosis to guiding procedures — real-time surgical navigation, radiation therapy optimization), and proactive screening (population health applications where AI reviews routine scans to find incidental findings — early-stage cancers, aneurysms — that weren't the original reason for imaging).</p>

<h2 id="conclusion">Conclusion</h2>
<p>AI in medical imaging has crossed the threshold from promising research to clinical reality. The technology is saving lives today — detecting strokes faster, catching cancers earlier, and extending specialist-level diagnostics to underserved communities. But responsible adoption requires addressing bias, ensuring explainability, integrating seamlessly into clinical workflows, and maintaining the irreplaceable role of physician judgment. The future isn't AI replacing radiologists — it's radiologists augmented by AI, able to focus their expertise on the most challenging cases while routine screenings are handled faster and more accurately than ever before.</p>
<p style="background:rgba(239,83,80,.08);border-left:3px solid #ef5350;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(239,83,80,.05);border-radius:14px;border:1px solid rgba(239,83,80,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-drug-discovery.html" style="color:#ef5350;text-decoration:none">→ AI Drug Discovery: Shrinking 10-Year Timelines to Months</a></li></ul></div>
"""

# ============================================================
# ARTICLE 4: article-drug-discovery.html
# ============================================================
DRUG_DISCOVERY = """
<h2 id="intro">From 10 Years to 18 Months: The Drug Development Revolution</h2>
<p>Developing a new drug traditionaly takes 10-15 years and costs an average of $2.6 bilion, with a 90% failure rate in clinical trials. These numbers have constrained pharmaceutical innovation for decades — only diseases affecting large patient populations (and promising large profits) attract R&D investment. But artificial intelligence is fundamentally reshaping this calculus. In 2024, Insilico Medicine's AI-discovered drug for idiopathic pulmonary fibrosis entered Phase II clinical trials just 30 months after initial discovery — a process that historically would have taken 4-6 years to reach the same milestone. The message is clear: AI doesn't just speed up drug discovery; it makes previously uneconomical targets viable. For rare disease research, this is nothing short of revolutionary.</p>

<h2 id="how-ai-helps">Where AI Adds Value in the Drug Pipeline</h2>
<h3 id="target-discovery">Target Identification: Finding the Needle in the Haystack</h3>
<p>The human genome contains approximately 20,000 protein-coding genes, but only a fraction are "druggable" — meaning small molecules or biologics can effectively modulate their function. AI systems analyze genomic databases to identify gene-disease associations from GWAS studies, biobanks, and published literature. DeepMind's AlphaFold2 predicted structures for nearly all known proteins, dramatically expanding the druggable target space by revealing binding pockets and allosteric sites that weren't previously known. Pathway analysis maps disease mechanisms to identify which protein to target for maximum therapeutic effect with minimum side effects. Atomwise claims their screening platform can evaluate 10-20 milion compounds per target per day — compared to 1,000-2,000 per day using traditional high-throughput screening.</p>

<h3 id="molecule-design">Molecule Design: Generating Novel Compounds</h3>
<p>Generative AI models are designing molecules that have never existed in nature. Generative Adversarial Networks (GANs) create novel molecular structures optimized for binding affinity, solubility, and synthesizability. Diffusion models, inspired by image generation, can "hallucinate" drug-like molecules with desired properties. Reinforcement learning optimizes molecules against multiple objectives simultaneously — potency plus safety plus manufacturability. Recursion Pharmaceuticals combines automated microscopy with AI to observe how cells respond to compounds at scale, generating massive phenotypic datasets that inform molecule design decisions. Their "cellartry" approach has produced over 50 therapeutic programs across oncology, immunology, and infectious disease.</p>

<h3 id="clinical-trials">Clinical Trial Optimization</h3>
<p>Even after a drug candidate is identified, AI accelerates the expensive clinical trial phases. Patient recruitment uses NLP to analyze EHRs and identify eligible trial participants, reducing enrollment time by 30-50%. Traditional recruitment can take 18-24 months; AI-assisted recruitment can cut this to 6-12 months. Site selection predicts which trial sites will enroll fastest and retain patients best. Real-time adverse event detection uses pattern recognition across trial data to identify safety signals earlier. And Bayesian adaptive designs adjust dosing mid-trial based on accumulating results, reducing required sample sizes and speeding time-to-approval.</p>

<h2 id="success-stories">Success Stories and Real Results</h2>
<h3 id="insilico">Insilico Medicine: From AI to Phase II in 30 Months</h3>
<p>Insilico's end-to-end AI platform identified a novel target for idiopathic pulmonary fibrosis (IPF), generated a molecule against it, and advanced it through preclinical testing — all within 18 months. The resulting compound, INS018_055, entered Phase II trials in February 2024. CEO Alex Zhavoronkov estimates the total cost at under $2.6 milion, compared to the industry average of $400+ milion for reaching Phase II. Insilico now has 10+ clinical-stage assets in its pipeline, all discovered and developed using AI. Their approach emphasizes "generative biology" — using AI not just to design molecules but to understand disease biology from first principles.</p>

<h3 id="alphafold">AlphaFold: Unlocking Protein Structures</h3>
<p>DeepMind's AlphaFold2 solved the 50-year grand challenge of protein structure prediction. By 2025, AlphaFold had predicted structures for over 200 milion proteins — virtually every known protein. This structural database has become foundational for drug discovery, enabling structure-based drug design for targets that previously lacked experimental structures. A 2025 study in Science found that structure-based virtual screening using AlphaFold predictions achieved 78% of the performance of screening with experimental structures — a remarkable result that democratizes structure-based drug design for thousands of targets.</p>

<h3 id="exscientia">Exscientia: AI-Designed Drugs Entering Trials</h3>
<p>UK-based Exscientia has multiple AI-designed drug candidates in clinical trials. Their collaboration with Sumitomo Dainippon produced an OCD drug candidate discovered in just 12 months (compared to the typical 4-5 years), now in Phase I trials. Their approach emphasizes "patient-first" design — optimizing not just for potency but for properties that matter to actual patients: oral bioavailability, minimal drug-drug interactions, and flat dosing regimens. Exscientia went public in 2021 at a $2.6 bilion valuation, though the stock has since declined as the sector grapples with clinical validation challenges.</p>

<h2 id="limitations">Limitations and Skepticism</h2>
<p>Despite the excitement, important caveats remain. The "Valley of Death": many AI-discovered compounds look great in silico but fail in wet lab experiments. Computational predictions don't always translate to biological reality — proteins move, membranes are complex, and biological systems have feedback loops that static models miss. As of 2026, no fully AI-discovered drug has received FDA approval. The pipeline is promising but unproven at the finish line. Data quality issues persist: AI models are only as good as their training data, and published scientific literature contains reproducibility issues that propagate into AI training sets. And intellectual property questions about inventorship for AI-generated inventions remain legally unresolved in most jurisdictions.</p>

<h2 id="future">What's Next</h2>
<p>Three trends will define the next era of AI drug discovery. End-to-end automation: fully autonomous labs (like those being built by Recursion and Tempus) where AI designs molecules, robots synthesize them, and automated assays test them — with minimal human intervention. Multi-target drugs: AI excels at polypharmacology — designing single molecules that hit multiple disease targets simultaneously, potentially addressing complex diseases like Alzheimer's that single-target drugs have failed to treat. And personalized medicine integration: combining AI drug discovery with patient genomic profiles to develop individualized therapies — the ultimate precision medicine vision.</p>

<h2 id="conclusion">Conclusion</h2>
<p>AI drug discovery is the most transformative application of artificial intelligence in healthcare — and arguably in any industry. It promises to cut development timelines by 70-80%, reduce costs by 90%, and open therapeutic areas that were previously economically unviable. But the technology is still young. The true test will come in the next 3-5 years as the current wave of AI-discovered candidates progresses through clinical trials. If even a fraction succeed, we'll witness a fundamental restructuring of the pharmaceutical industry — one where AI doesn't just assist researchers, but leads the way.</p>
<p style="background:rgba(239,83,80,.08);border-left:3px solid #ef5350;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(239,83,80,.05);border-radius:14px;border:1px solid rgba(239,83,80,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-medical-imaging.html" style="color:#ef5350;text-decoration:none">→ AI in Medical Imaging: From Research Labs to Clinical Practice</a></li></ul></div>
"""

# ============================================================
# ARTICLE 5: article-contract-review.html
# ============================================================
CONTRACT_REVIEW = """
<h2 id="intro">The Document Problem That Costs Bilions</h2>
<p>A typical merger or acquisition involves reviewing 20,000-100,000 contracts. Corporate legal teams spend months — sometimes years — reading through lease agreements, employment contracts, supplier terms, and intellectual property licenses to identify risks. At bilng rates of $300-800 per hour for senior associates, due diligence can cost milions. And despite this investment, human reviewers miss things — studies suggest contract review error rates range from 10-30%, with missed clauses leading to post-acquisition liabilities that average $4.2 bilion per year across M&A deals globaly. Artificial inteligence is changing this equation dramatically. Kira Systems, acquired by Litera in 2023 for an estimated $500 milion, pioneered machine learning for contract analysis. Their technology can review a typical M&A document set in hours rather than weeks, with accuracy that matches or exceeds junior associates. Lawgeex reports their AI reduces contract review time by 92% while cutting costs by 80%. The legal industry's initial skepticism is giving way to adoption — 78% of Am Law 100 firms now use some form of AI contract analysis, according to the 2025 Legal Technology Survey.</p>

<h2 id="how-it-works">How AI Contract Review Actually Works</h2>
<h3 id="nlp-extraction">Natural Language Processing for Legal Text</h3>
<p>Legal documents follow predictable patterns — defined terms, recitals, representations, covenants, indemnification clauses. AI systems exploit this structure. Entity recognition identifies parties, dates, monetary amounts, governing law jurisdictions, and key contractual terms. Clause classification categorizes every provision into types (termination, change of control, confidentiality, IP assignment, etc.). Risk flagging highlights unusual, missing, or unfavorable clauses compared to market standards. And comparison analysis identifies inconsistencies across a contract portfolio — for example, different termination rights across subsidiary companies that create legal exposure.</p>

<h3 id="tech-stack">The Technology Stack</h3>
<p>Leading platforms combine multiple AI approaches. Transformer-based NLP: fine-tuned BERT and RoBERTa models trained on milions of annotated legal documents achieve state-of-the-art extraction accuracy (>96% for common clause types). Computer vision: some systems analyze scanned PDFs and images of contracts, handling the reality that many legal documents exist only as paper or poor-quality scans. And knowledge graphs: mapping relationships between contracts, entities, and obligations across an organization's entire document corpus, enabling queries like "show me all contracts that automaticaly renew in the next 90 days."</p>

<h2 id="market-leaders">Market Leaders and Their Approaches</h2>
<h3 id="kira">Kira Systems (Litera): The Pioneer</h3>
<p>Kira's machine learning engine learns from human annotations — lawyers highlight relevant provisions in sample documents, and the system generalizes to find similar language across thousands of other contracts. Their library covers 1,400+ provision types out-of-the-box, and clients can train custom extractors for niche requirements. Major law firms including Latham & Watkins, Clifford Chance, and Allen & Overy use Kira for M&A due diligence, lease abstraction, and regulatory compliance reviews. A 2024 case study by Latham & Watkins found that Kira reduced document review time by 73% in a complex cross-border acquisition involving 45,000+ contracts.</p>

<h3 id="luminance">Luminance: The Cambridge Spinout</h3>
<p>Founded by mathematicians from Cambridge University, Luminance takes a different approach. Their proprietary AI doesn't just extract text — it understands legal concepts and their implications. Luminance's "Legal Language Model" can identify not just what a clause says, but whether it's market-standard, favorable, or problematic given the specific deal context. They've raised over $120 milion and count PwC, Deloitte, and Baker McKenzie among their clients. Luminance's "early case assessment" feature for litigation uses AI to analyze thousands of documents and predict case strength — helping legal teams decide whether to settle or litigate.</p>

<h3 id="lawgeex">Lawgeex: Speed at Scale</h3>
<p>Lawgeex focuses specifically on contract review efficiency. Their benchmark study showed their AI completed review of 20 NDAs with 94% accuracy in 4.2 minutes — compared to 92 minutes for a group of experienced lawyers. The implication isn't that AI replaces lawyers; it's that lawyers can focus their time on strategic advice rather than mechanical review. Lawgeex was acquired by DocuSign in 2024 for $165 milion, signaling the strategic importance of contract AI to the broader agreement workflow ecosystem.</p>

<h2 id="use-cases">Beyond M&A: Other Use Cases</h2>
<p>AI contract review extends far beyond due diligence. Lease abstraction: real estate companies manage portfolios of 10,000+ leases; AI extracts key terms into searchable databases. Regulatory compliance: financial services firms use AI to ensure contracts contain required regulatory provisions (GDPR clauses, SOC2 requirements, FINRA compliance). Insurance policy review: insurers analyze policy documents to assess coverage gaps. Procurement: enterprises review supplier contracts to ensure compliance with corporate policies. And contract lifecycle management: AI tracks obligations, renewal dates, and compliance requirements across an organization's entire contract portfolio, preventing costly oversights.</p>

<h2 id="challenges">Challenges and Limitations</h2>
<p>AI struggles with nuance and context — ambiguous language, implied terms, and contextual interpretation that experienced lawyers handle intuitively. Data privacy is a concern: contract data contains confidential business information, trade secrets, and personal data. On-premise deployments and strict access controls are essential. Integration complexity with existing document management systems (DocuSign, iManage, NetDocuments) requires technical investment and often custom development. Change management is perhaps the biggest barrier: lawyers trained in traditional methods may resist AI adoption. Successful implementations include comprehensive training and change management programs. And ethical concerns about liability when AI misses a material clause are stil evolving in bar association guidelines and case law.</p>

<h2 id="future">Future Directions</h2>
<p>The next generation of legal AI will move beyond extraction to generation and reasoning. Contract drafting: AI that drafts contract language based on negotiated term sheets, ensuring consistency with precedent libraries. Obligation management: automaticaly tracking deadlines, renewals, and obligations extracted from signed contracts. Negotiation support: suggesting counterproposals based on market data and the specific counterparty's negotiation history. And predictive analytics: assessing litigation risk based on contract language patterns correlated with historical dispute outcomes. The legal profession is conservatism by design — and that's appropriate for an industry that manages society's most important commitments. But the efficiency gains are too large to ignore indefinitely.</p>

<h2 id="conclusion">Conclusion</h2>
<p>AI contract review has graduated from experimental technology to essential infrastructure for modern legal practice. The value proposition is compelling: faster reviews, lower costs, fewer errors, and — critically — freeing lawyers to do the high-value work that drew them to the profession. But AI is a tool, not a replacement. The most effective legal teams pair AI efficiency with human judgment, using machines to handle volume and pattern recognition while attorneys provide strategic counsel, negotiate nuance, and take professional responsibility for outcomes. As the technology matures, the dividing line between "AI tasks" and "lawyer tasks" will continue shifting — always toward higher-value human work.</p>
<p style="background:rgba(129,199,132,.08);border-left:3px solid #81c784;padding:12px 16px;margin-top:30px;font-size:.85rem;color:#9898a8"><em>This article was researched and written with AI assistance, then reviewed and fact-checked by the AI Verticals editorial team. Last updated: June 2026.</em></p>
<div class="related-articles" style="margin-top:32px;padding:24px;background:rgba(129,199,132,.05);border-radius:14px;border:1px solid rgba(129,199,132,.12)"><h3 style="color:#e8e8f0;margin-bottom:16px;font-size:1.1rem">Related Reading</h3><ul style="list-style:none;padding:0"><li style="margin-bottom:10px"><a href="/en/articles/article-deepfake-detect.html" style="color:#81c784;text-decoration:none">→ Deepfake Detection: Authenticating Reality in the Age of Synthetic Media</a></li></ul></div>
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
    import re
    clean = re.sub(r"<[^>]+>", " ", html_fragment)
    return len(clean.split())


def main():
    import re
    articles = [
        ("article-medical-imaging.html", MEDICAL_IMAGING),
        ("article-drug-discovery.html", DRUG_DISCOVERY),
        ("article-contract-review.html", CONTRACT_REVIEW),
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
