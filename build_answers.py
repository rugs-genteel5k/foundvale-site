#!/usr/bin/env python3
"""Generate Foundvale answer pages.

Each page: question as <h1>, direct answer in the first two sentences
(the .standfirst), then the working detail. Schema per page = Article +
FAQPage + BreadcrumbList. Run from the repo root; writes answers/**.

Content rules enforced by construction:
  - no testimonials, no earnings claims, no ranking/citation guarantees
  - statistics carry a named, linked source
  - no live prospect is named (see AGGREGATE page note)
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
BASE = "https://foundvale.com"
TODAY = "2026-08-04"

NAV = """<header>
  <div class="bar">
    <a class="mark" href="/"><span class="badge">F</span><span class="name">Foundvale</span></a>
    <nav>
      <a href="/answers/">Answers</a>
      <a href="/#offer">Services</a>
      <a href="/#process">Process</a>
      <a class="cta" href="/#offer">Start the $500 audit</a>
    </nav>
  </div>
</header>"""

FOOTER = """<footer>
  <div class="wrap">
    <div class="frow">
      <div><strong>Foundvale</strong><br>Content services for specialty manufacturers<br>and industrial distributors.</div>
      <div><a href="mailto:hello@foundvale.com">hello@foundvale.com</a><br><a href="/answers/">All answers</a><br><a href="/">Home</a></div>
    </div>
    <div class="fine">Foundvale does not guarantee rankings or AI citations. Scope is defined by deliverables. &copy; 2026 Foundvale.</div>
  </div>
</footer>"""

HEAD = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="canonical" href="{url}">
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Foundvale">
<meta property="og:image" content="{base}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{base}/og.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/article.css">
<script type="application/ld+json">
{schema}
</script>"""

NEXTSTEP = """<div class="nextstep">
  <h2>Find out who gets named in your niche</h2>
  <p>The $500 audit runs 15 real buyer queries across ChatGPT, Perplexity, Gemini and Google AI Overviews, logs who gets cited query by query, and comes back with a 90-day content map and two ready-to-publish articles. Fixed scope, two weeks. The fee is credited to your first retainer month if you continue.</p>
  <a class="btn" href="/#offer">Start the $500 audit</a><a class="btn ghost" href="mailto:hello@foundvale.com">Ask a question</a>
</div>"""

# ---------------------------------------------------------------- content
# body: raw HTML fragment. answer: the 1-2 sentence direct answer (also feeds
# FAQPage schema, so it must stand alone out of context).

PAGES = [
    {
        "slug": "get-found-when-buyers-ask-ai-for-suppliers",
        "q": "How do I get my company to show up when buyers ask AI for a supplier?",
        "title": "How to get your company named when buyers ask AI for a supplier",
        "desc": "AI engines name suppliers from content they can read, extract and cite. Publish question-shaped answer pages, make your specs machine-readable, and get onto the third-party pages the engines already cite.",
        "answer": "AI engines name the suppliers whose content they can read, extract, and attribute — so you get named by publishing direct answers to the questions your buyers actually ask, and by appearing on the third-party pages the engines already cite. A brochure site that only describes your company gives an engine nothing to quote.",
        "body": """
<h2>What the engine is actually doing</h2>
<p>When a procurement manager asks for "a precision machining supplier in the Midwest," the model is not consulting a directory of vendors. It is assembling an answer from text it can retrieve and attribute — supplier pages, industry listicles, distributor catalogs, association directories, forum threads. Whoever wrote the most extractable, most clearly-sourced answer to that question tends to get named.</p>
<p>This is why company size, tenure, and manufacturing quality correlate so weakly with getting named. A 70-year-old specialist can be completely absent from its own category while a competitor with a thinner catalog and better-structured content takes the slot.</p>

<h2>The three things that actually move it</h2>
<h3>1. Question-shaped pages</h3>
<p>One page per real buyer question. The question is the headline. The direct answer is in the first two sentences. Everything else — the caveats, the spec tables, the "it depends" — comes after. Engines reward passages that resolve a question cleanly, because a clean passage is a safe thing to quote.</p>
<p>The questions come from your sales calls, not your positioning. What buyers type is rarely what marketing writes: "how do I size a Y strainer," "rubber vs metal expansion joint," "compression spring rate calculation." Those are the pages that get retrieved.</p>

<h3>2. Machine-readable specifications</h3>
<p>Tolerances, material grades, temperature ranges, certifications, size charts. Put them in real tables with real headers, not in prose and not in a PDF or an image. A published spec table is one of the most extractable assets a manufacturer owns, and most manufacturers have the data sitting in a catalog nobody can parse.</p>

<h3>3. Presence on the pages that already get cited</h3>
<p>This is the one most people skip, and it is frequently the difference. Engines cite industry listicles, directories, review sites and forum threads far more often than they cite a vendor's own homepage. If your category's answers are being assembled from two trade listicles and a distributor catalog, publishing on your own site will not put you in them. You have to get onto those pages — pitch the authors, claim the directory profiles, make sure your distributors' listings are accurate and complete.</p>

<div class="callout">
  <span class="lbl">The order matters</span>
  <p>Trace the citations <em>before</em> you write anything. The pages an engine actually pulled from tell you where the intervention has to happen. Writing ten articles into a category whose answers come entirely from a trade association directory is expensive and does nothing.</p>
</div>

<h2>What does not work</h2>
<ul>
  <li><strong>Keyword-stuffed pages.</strong> Retrieval is semantic. Repetition does not help and reads badly to the humans who arrive.</li>
  <li><strong>Blocking the crawlers.</strong> Check your <code>robots.txt</code> for <code>Google-Extended</code> and <code>Applebot-Extended</code>. Some sites have opted out of AI grounding without anyone deciding to.</li>
  <li><strong>Content that makes claims you cannot source.</strong> An engine that surfaces a wrong tolerance in front of an engineer is worse than absence.</li>
  <li><strong>Waiting for it to settle.</strong> Answers shift constantly, which cuts both ways: positions are winnable, and positions are losable.</li>
</ul>

<h2>How long it takes</h2>
<p>Longer than a paid ad and shorter than traditional SEO. New pages have to be crawled, indexed, and then actually retrieved for a query — and the engines re-evaluate constantly, so a position that appears can also disappear. We do not promise a timeline or a citation, and you should be skeptical of anyone who does. What we do commit to is a monthly tracked-query log so the direction is visible and on the record.</p>
""",
        "related": ["what-is-generative-engine-optimization", "check-what-ai-says-about-your-company", "why-ai-names-distributors-instead-of-manufacturers"],
    },
    {
        "slug": "what-is-generative-engine-optimization",
        "q": "What is generative engine optimization, and how is it different from SEO?",
        "title": "What is generative engine optimization (GEO)? How it differs from SEO",
        "desc": "GEO is the practice of getting your business named and cited inside AI-generated answers. It shares mechanics with SEO but optimizes for extraction and attribution rather than for a ranked list of links.",
        "answer": "Generative engine optimization (GEO) is the practice of getting your business named and cited inside AI-generated answers, on engines like ChatGPT, Perplexity, Gemini and Google AI Overviews. It overlaps heavily with SEO — both depend on crawlable, credible, well-structured content — but GEO optimizes for being extracted and attributed inside one synthesized answer, rather than for placing a link in a ranked list of ten.",
        "body": """
<h2>The practical difference</h2>
<p>SEO competes for a position in a list. The user then chooses among ten links, and a position lower down still gets clicks. GEO competes to be <em>inside the answer</em>. There is usually one answer, it names a handful of companies, and if you are not among them the buyer never learns you exist. The distribution is far more winner-take-most.</p>
<p>That changes what you optimize.</p>

<div class="tablewrap">
<table>
  <thead><tr><th></th><th>Classic SEO</th><th>GEO</th></tr></thead>
  <tbody>
    <tr><td>Unit of success</td><td>Ranked position for a keyword</td><td>Named or cited inside a generated answer</td></tr>
    <tr><td>Page shape</td><td>Comprehensive, keyword-targeted</td><td>Question-shaped, answer-first, quotable in isolation</td></tr>
    <tr><td>Winner distribution</td><td>Ten slots, long tail of clicks</td><td>A few names, little consolation for eleventh</td></tr>
    <tr><td>Where credit accrues</td><td>Mostly your own domain</td><td>Often third-party pages that mention you</td></tr>
    <tr><td>Measurement</td><td>Rank tracking, clicks, impressions</td><td>Prompt audits: who is named, and which sources were cited</td></tr>
    <tr><td>Volatility</td><td>Moves over weeks</td><td>Can differ between two runs of the same prompt</td></tr>
  </tbody>
</table>
</div>

<h2>What carries over from SEO</h2>
<p>More than the "SEO is dead" crowd suggests. Engines still need to crawl you, still weigh whether a source looks credible, and still lean on the same signals of structure and authority. Technically sound sites have a real head start: clean markup, fast pages, a sitemap, schema, no crawler blocks.</p>
<p>Two things carry over so directly that they are effectively the same work: <strong>structured data</strong> (marking up your FAQs, products and specs so a machine reads them unambiguously) and <strong>being referenced by other credible sites</strong>. In SEO you called the second one link building. In GEO the mention matters even without the link, because the engine is reading the page, not just counting the edge.</p>

<h2>What is genuinely new</h2>
<ul>
  <li><strong>Extractability beats comprehensiveness.</strong> A 3,000-word guide that buries the answer in paragraph nine loses to a 600-word page that answers in sentence one.</li>
  <li><strong>Non-determinism.</strong> The same prompt run twice can produce different names. A single check is a snapshot, not a measurement — you need a fixed query set re-run on a schedule before any change means anything.</li>
  <li><strong>Attribution is the metric.</strong> "Were we mentioned" is the vanity number. "Which pages did it pull from" is the actionable one, because those pages are where the work has to happen.</li>
  <li><strong>New surface files.</strong> <a href="/answers/what-is-llms-txt/">llms.txt</a> and explicit AI-crawler directives did not exist in the SEO playbook.</li>
</ul>

<div class="callout">
  <span class="lbl">Terminology</span>
  <p>You will see GEO, AEO (answer engine optimization), AI SEO, and LLM optimization used for roughly the same activity. There is no settled standard. We say "AI-search content" because the deliverable is content, and because the label matters less than whether the pages get cited.</p>
</div>

<h2>Why it matters now for industrial B2B</h2>
<p>The buyer behaviour moved before most supplier sites did. <a href="https://www.prnewswire.com/news-releases/73-of-b2b-buyers-use-ai-tools-in-purchase-research-multi-source-analysis-finds-302733319.html">73% of B2B buyers now use AI tools in purchase research</a>, and <a href="https://www.prnewswire.com/news-releases/new-g2-research-half-of-b2b-software-buyers-now-start-their-research-with-ai-chatbots-302742807.html">51% of B2B software buyers now start their research with an AI chatbot</a>. In a market where the buyer self-guides most of the journey before ever contacting a supplier, being absent from that first synthesized answer removes you from the consideration set silently.</p>
""",
        "related": ["does-seo-still-matter-with-ai-search", "get-found-when-buyers-ask-ai-for-suppliers", "how-much-does-ai-search-optimization-cost"],
    },
    {
        "slug": "does-seo-still-matter-with-ai-search",
        "q": "Does SEO still matter now that buyers start with AI?",
        "title": "Does SEO still matter with AI search? Yes — and here is what changes",
        "desc": "SEO still matters: AI engines ground answers in crawled web content, so the technical and credibility work that drove SEO also drives AI citations. What changes is page shape and how you measure.",
        "answer": "Yes. AI engines ground their answers in crawled web content, so the crawlability, structure and credibility work that drives SEO is the same work that gets you cited in AI answers. What changes is the shape of the pages you publish and how you measure success — not whether the underlying fundamentals still apply.",
        "body": """
<h2>The honest version</h2>
<p>"SEO is dead" is a marketing line, usually from someone selling the replacement. The accurate statement is narrower: <strong>the click is at risk, not the content.</strong> When an engine answers a question directly, the user may never visit the page it learned from — but it still had to find, read and trust that page. The page did the work; it just got paid in a citation instead of a session.</p>
<p>For an industrial manufacturer this is less alarming than it sounds, because your traffic was never the point. A $2–25M specialty manufacturer does not monetize pageviews. It needs to be on the shortlist when a buyer is choosing who to RFQ. A citation inside an AI answer serves that goal at least as well as a click, and arguably better — it arrives with an implicit recommendation attached.</p>

<h2>What still works exactly as before</h2>
<ul>
  <li><strong>Being crawlable.</strong> If bots cannot fetch and parse it, nothing downstream matters. This includes not blocking AI crawlers by accident.</li>
  <li><strong>Structured data.</strong> Schema markup is arguably more valuable now, not less — it is unambiguous machine-readable meaning, handed over for free.</li>
  <li><strong>Being referenced by credible third parties.</strong> Directories, associations, trade publications, distributor listings. The engine reads those pages.</li>
  <li><strong>Technical hygiene.</strong> Fast pages, clean HTML, working canonicals, an accurate sitemap, content that is in the HTML and not injected by JavaScript.</li>
  <li><strong>Genuine subject expertise.</strong> Specificity — real tolerances, real materials, real failure modes — is what makes a page worth quoting.</li>
</ul>

<h2>What changes</h2>
<h3>Page shape</h3>
<p>The classic SEO instinct was length and comprehensiveness: cover everything, rank for many terms. The GEO instinct is resolution: answer one question cleanly and early, then elaborate. You will publish more pages, each narrower.</p>

<h3>Measurement</h3>
<p>Rank tracking degrades as a proxy. Position 3 for a term whose result page is now topped by a synthesized answer is worth much less than it was. You need a second instrument alongside it: a fixed set of buyer prompts, re-run on a schedule across several engines, logging who is named and what got cited. Both instruments, not one replacing the other.</p>

<h3>Where the work lands</h3>
<p>A meaningful share of the effort moves off your own site, onto the third-party pages the engines cite. That is uncomfortable for anyone used to controlling their own domain, and it is where a lot of otherwise-good content programs stall out.</p>

<div class="callout">
  <span class="lbl">If you only do one thing</span>
  <p>Do not rebuild your SEO. Add the missing layer: find the questions your buyers ask, publish clean answers to them, and check what the engines currently say. Most industrial sites already have the hard part — real technical depth — locked in formats machines cannot read.</p>
</div>

<h2>Practically, for a manufacturer with no marketing staff</h2>
<p>You do not need two programs and two budgets. The overlap is large enough that one content effort, built answer-first and marked up properly, serves both. The additional GEO-specific work is the prompt audit and the third-party placement — a layer on top, not a parallel track.</p>
""",
        "related": ["what-is-generative-engine-optimization", "check-what-ai-says-about-your-company", "can-we-do-ai-search-optimization-in-house"],
    },
    {
        "slug": "how-much-does-ai-search-optimization-cost",
        "q": "How much does AI search optimization cost?",
        "title": "How much does AI search optimization cost? Real 2026 price bands",
        "desc": "Industrial-specialist SEO and GEO agencies typically run $2,500-15,000/mo with 6-12 month minimums. Foundvale runs a $500 fixed-scope audit and a $1,250/mo month-to-month engine for the size band below that floor.",
        "answer": "Industrial-specialist SEO and GEO agencies typically charge $2,500–$15,000 per month with six- to twelve-month minimums, and the budget tier generally starts around $1,500 per month. Foundvale's pricing sits deliberately below that floor: a $500 fixed-scope audit and a $1,250 per month engine, month-to-month with 30 days' notice.",
        "body": """
<h2>The market bands</h2>
<div class="tablewrap">
<table>
  <thead><tr><th>Tier</th><th>Typical monthly</th><th>Commitment</th><th>What you generally get</th></tr></thead>
  <tbody>
    <tr><td>Enterprise / full-service industrial agency</td><td>$5,000–15,000+</td><td>6–12 months</td><td>Strategy, content, technical, paid, dedicated team</td></tr>
    <tr><td>Mid-market specialist</td><td>$2,500–5,000</td><td>6 months typical</td><td>Content program plus technical SEO</td></tr>
    <tr><td>Budget / entry specialist</td><td>$1,500–2,500</td><td>3–6 months</td><td>Limited content volume, less senior attention</td></tr>
    <tr><td>One-off audit</td><td>$1,500–5,000</td><td>Project</td><td>Findings and recommendations, no execution</td></tr>
    <tr><td>Foundvale</td><td>$500 pilot &middot; $1,250/mo</td><td>None &mdash; 30-day notice</td><td>Audit, 4 articles/mo, page rewrites, schema, tracked queries</td></tr>
  </tbody>
</table>
</div>
<p>Sources for the agency bands: <a href="https://manufacturing-seo.agency/blog/manufacturing-seo-agency-pricing">manufacturing-seo.agency pricing survey</a>, <a href="https://marketingltb.com/blog/agency/best-industrial-seo-agencies/">Marketing LTB industrial agency roundup</a>, and <a href="https://www.outerboxdesign.com/articles/seo/seo-pricing-costs/">OuterBox SEO pricing</a>. Figures are 2025–2026 and vary by scope and region.</p>

<h2>Why there is a gap under $1,500</h2>
<p>Specialist agencies have a client floor set by their cost to serve — account management, strategists, senior writers who understand tolerances and certifications. Below roughly $1,500/month, that model does not clear. So companies in the $2–25M revenue band with zero or one marketing person tend to face a choice between paying above their comfort level for a program sized for someone larger, doing nothing, or hiring a generalist freelancer who writes confident nonsense about your process.</p>
<p>That gap is the segment we built for. It is not a discount on the same service — it is a narrower service with less of what that band does not need: no standing calls, no account manager, no strategy deck, no minimum term.</p>

<h2>What drives cost, whoever you hire</h2>
<ul>
  <li><strong>Content volume and depth.</strong> Technical industrial writing costs more than generic B2B because a wrong spec in front of an engineer is a failure, not a typo.</li>
  <li><strong>How much SME time is required.</strong> Programs that need weekly calls with your engineers cost you more than the invoice says.</li>
  <li><strong>Whether they publish for you.</strong> Handing over documents is cheaper than getting CMS access and doing implementation.</li>
  <li><strong>Tracking.</strong> Some firms resell an AI-visibility tool subscription at a markup. Ask whether the monthly report is a dashboard export or an actual analysis.</li>
  <li><strong>Commitment term.</strong> Long minimums are usually priced as risk transfer from the agency to you.</li>
</ul>

<h2>What to ask before signing anything</h2>
<ol>
  <li>What exactly ships each month, in countable units?</li>
  <li>What happens in a month when we are slow to give you input?</li>
  <li>Who owns the content, and in what format is it delivered?</li>
  <li>How do you measure AI visibility, and can I see a sample report?</li>
  <li>What is the notice period, and what does month one actually look like?</li>
</ol>

<div class="callout">
  <span class="lbl">On guarantees</span>
  <p>If a proposal guarantees rankings or AI citations, treat it as a reason to walk. Nobody controls what a model outputs, and the engines change constantly. What a vendor can legitimately commit to is deliverables — and you should hold them to those precisely.</p>
</div>
""",
        "related": ["can-we-do-ai-search-optimization-in-house", "what-is-generative-engine-optimization", "get-found-when-buyers-ask-ai-for-suppliers"],
    },
    {
        "slug": "check-what-ai-says-about-your-company",
        "q": "How do I check what AI says about my company?",
        "title": "How to check what AI says about your company (free, about an hour)",
        "desc": "Run five real buyer questions through ChatGPT, Perplexity and Gemini, log whether you are named, which competitors are, and which sources were cited. The citation trace is the part that tells you what to fix.",
        "answer": "Write down the five questions your buyers actually ask, run each through ChatGPT, Perplexity and Gemini, and log three things per answer: whether you were named, which competitors were, and which sources the engine cited. It takes about an hour, costs nothing, and the citation trace is the part that tells you where the problem actually is.",
        "body": """
<h2>Step 1 &mdash; Write the five questions</h2>
<p>Questions about the problem you solve, not about you. Nobody asks an engine about your company by name until they already know it exists. Useful shapes:</p>
<ul>
  <li><em>best [your category] for [your buyer type]</em></li>
  <li><em>[your category] manufacturers [region]</em></li>
  <li><em>[biggest competitor] alternatives</em></li>
  <li><em>how do I select / size / spec [the thing you make]</em></li>
  <li><em>who should I contact to [outcome you deliver]</em></li>
</ul>
<p>If you are unsure, pull the exact phrasing from your last ten sales calls or RFQ emails. Buyers use different words than your marketing does, and the buyer's words are the ones typed into the box.</p>

<h2>Step 2 &mdash; Run them across three engines</h2>
<p>ChatGPT, Perplexity and Gemini, free tiers are fine. Use a fresh chat per company or topic so earlier context does not contaminate the answer. That is fifteen answers. In a spreadsheet, log per answer: were you named (yes/no), which competitors were named, and how the engine described whoever it put first.</p>
<p>The description column is the one people skip and the one that pays. It tells you which proof points the engine considers decisive in your category — certifications, lead time, published engineering data, size range. That is a content brief, handed to you.</p>

<h2>Step 3 &mdash; Trace the citations. This is the important step.</h2>
<p>Perplexity shows sources on every answer; ChatGPT shows them when it searches the web; Gemini surfaces them on many responses. Click through and write down the exact pages.</p>
<p>What you will usually find is that the cited pages are <strong>not</strong> your competitors' homepages. They are trade listicles, association directories, distributor catalogs, review sites and forum threads. Those pages are the actual battleground, and knowing which ones they are converts a vague "we're invisible" into a specific, short list of places to go.</p>

<div class="callout">
  <span class="lbl">A better prompt than the obvious one</span>
  <p>Try: <em>"You are a [your buyer's role] shopping for [your category]. Walk me through how you would research this and who you would pick."</em> The reasoning it shows you is more useful than a flat "best X" list, because it exposes which signals the engine weights before it commits to names.</p>
</div>

<h2>Step 4 &mdash; Close the gap, in two moves</h2>
<p><strong>Move one: get onto the cited pages.</strong> Pitch the authors of the listicles that came up. Claim and complete your directory and association profiles. Make sure your distributors' listings for your products are accurate. Ask satisfied customers to leave reviews on the sites the engines actually quoted.</p>
<p><strong>Move two: publish one page per question.</strong> The question as the headline, the answer in the first two sentences, the detail underneath. Real spec tables rather than prose or PDFs.</p>
<p>Most programs do only move two. In categories where citations run through directories and trade media, move two alone will not change the answer.</p>

<h2>Step 5 &mdash; Re-run it monthly</h2>
<p>Answers shift constantly, and the same prompt can return different names on two consecutive runs. A single audit is a snapshot. Keep the query set fixed, re-run it on the same day each month, and compare against the prior month — the delta is the only thing that means anything.</p>

<div class="callout">
  <span class="lbl">Why we publish this</span>
  <p>Because you can do it, and because the audit was never the hard part. Running fifteen prompts is an hour. Turning the result into content your engineers will sign off on, published consistently every month, is the part that takes a program. If you run this and want the version with four engines, a written gap analysis and a 90-day content map, that is our $500 pilot.</p>
</div>
""",
        "related": ["why-ai-names-distributors-instead-of-manufacturers", "get-found-when-buyers-ask-ai-for-suppliers", "can-we-do-ai-search-optimization-in-house"],
    },
    {
        "slug": "why-ai-names-distributors-instead-of-manufacturers",
        "q": "Why does AI recommend distributors and directories instead of my company?",
        "title": "Why AI names distributors and directories instead of your company",
        "desc": "AI engines cite whichever page most cleanly answers the question. Distributors and directories publish comparison tables, size charts and category pages at scale, so they get cited even when the manufacturer has deeper expertise.",
        "answer": "Because distributors, directories and trade publications publish the page shapes engines find easiest to quote — comparison tables, size charts, category listings and buying guides — while most manufacturers publish product pages that describe capability rather than answering questions. The engine is not judging who is the better supplier; it is quoting whoever wrote the clearest available answer.",
        "body": """
<h2>The pattern</h2>
<p>It shows up constantly in category audits. A manufacturer with decades of specialist expertise is absent from the answer to a question their own engineers could answer better than anyone. The named sources are a distributor's catalog page, an association directory, and a trade-media buying guide.</p>
<p>This is not the engine preferring middlemen. It is a structural consequence of what each party publishes.</p>

<div class="tablewrap">
<table>
  <thead><tr><th></th><th>Typical distributor / directory page</th><th>Typical manufacturer page</th></tr></thead>
  <tbody>
    <tr><td>Page shape</td><td>Category or comparison, built to answer "which one"</td><td>Product or capability, built to describe</td></tr>
    <tr><td>Coverage</td><td>Many brands side by side</td><td>One brand only</td></tr>
    <tr><td>Data format</td><td>Filterable tables, size charts, spec grids</td><td>Prose, PDF catalogs, images of tables</td></tr>
    <tr><td>Question coverage</td><td>Hundreds of long-tail selection questions</td><td>A handful of pages, rarely question-shaped</td></tr>
    <tr><td>Apparent neutrality</td><td>Reads as comparative</td><td>Reads as promotional</td></tr>
  </tbody>
</table>
</div>

<h2>Why it stings more than a lost search ranking</h2>
<p>In classic search, a distributor outranking you was survivable — the buyer saw ten links and yours was among them. In a generated answer there is one list of names. If the engine sources the category from a distributor page that carries three brands and not yours, you are not lower down. You are absent, and the buyer has no way to know you were ever an option.</p>
<p>There is a second-order version too: sometimes you <em>are</em> named, but only through a directory listing rather than your own content. Being present via a third-party profile is better than absence, and it is materially weaker than having your own pages be the quoted source. It means the engine learned you exist but did not learn what makes you the right pick.</p>

<h2>What to do about it</h2>
<h3>1. Publish the comparison content yourself</h3>
<p>The pages getting cited are selection pages: <em>X vs Y</em>, <em>how to size Z</em>, <em>when to use A instead of B</em>. Manufacturers avoid these because they feel like they invite comparison. That reluctance is exactly why the distributor's version is the cited source. You know the honest tradeoffs better than anyone; a page that says plainly where your product is not the right choice is more credible, more quotable, and tends to convert better with technical buyers.</p>

<h3>2. Liberate your spec data</h3>
<p>Most manufacturers already own the best data in their category — it is locked in a PDF catalog or rendered as an image. Publish it as real HTML tables with real headers. A size chart or a materials table is one of the most extractable assets you can own, and putting it on the page is usually a day of work, not a project.</p>

<h3>3. Fix your presence on the pages already being cited</h3>
<p>If a directory or association listing is the source in your category, get that listing right: complete specifications, accurate categories, consistent company details. If a distributor's page is being quoted, work with them so the content about your products is accurate and complete. You are not going to displace those pages, and you do not need to — you need to be properly represented inside them.</p>

<div class="callout">
  <span class="lbl">The two-move rule</span>
  <p>Own-site content and third-party presence are not alternatives. A program that only publishes articles on your own domain leaves the cited pages untouched, and in directory-dominated categories that means the answer does not change. Trace the citations first, then decide how the effort splits.</p>
</div>

<h2>The upside</h2>
<p>Distributor and directory dominance is a sign of a <em>vacant</em> category, not a locked one. Those pages win by default because the specialists have not published question-shaped content. You have the deeper knowledge; you are simply not expressing it in a form the engine can use. That is a fixable problem, and it is fixable faster than out-competing a well-run competitor who is already doing this.</p>
""",
        "related": ["check-what-ai-says-about-your-company", "get-found-when-buyers-ask-ai-for-suppliers", "what-we-found-auditing-industrial-manufacturers"],
    },
    {
        "slug": "what-is-llms-txt",
        "q": "What is llms.txt, and does my site need one?",
        "title": "What is llms.txt? A plain explanation for B2B site owners",
        "desc": "llms.txt is a plain-text file at your site root that summarises what your business does, who it serves and where the key pages are, in a form language models can read easily. It is cheap to add and low risk.",
        "answer": "llms.txt is a plain-text file at the root of your website that summarises what your business does, who it serves and where your key pages live, written for language models rather than browsers. It is an emerging convention rather than a ratified standard, and it takes under an hour to write — low cost, low risk, and not a substitute for having good content.",
        "body": """
<h2>What it is</h2>
<p>A Markdown-formatted text file served at <code>yourdomain.com/llms.txt</code>. It states plainly what you do, who you serve, what you sell, and which pages matter. The idea is that a model retrieving information about your company gets an unambiguous summary instead of having to infer everything from navigation, marketing copy and a footer.</p>
<p>The mental model is <code>robots.txt</code>: a small, conventional file at a predictable location, read by machines, ignored by humans. The difference is that <code>robots.txt</code> grants or denies access, while <code>llms.txt</code> supplies meaning.</p>

<h2>Honest status</h2>
<p>It is a proposed convention with growing adoption, not a standard any engine has committed to honouring. Nobody should promise you that adding one produces citations. What can be said accurately: it costs very little, it carries no downside, it forces a useful internal exercise in stating plainly what you do, and if adoption continues you are already positioned.</p>
<p>Treat it as cheap insurance, not as a lever.</p>

<h2>What to put in it</h2>
<ul>
  <li>A one-paragraph summary of the business, in the first few lines</li>
  <li>Who you serve — industry, size band, geography</li>
  <li>What you make or sell, with real specifics: materials, size ranges, tolerances, certifications, lead times</li>
  <li>What you do <em>not</em> do, which prevents a model confidently miscategorising you</li>
  <li>Commercial basics: how to buy, minimum order, whether you quote custom work</li>
  <li>Links to your most important pages, each with a short description</li>
  <li>Contact details</li>
</ul>

<div class="callout">
  <span class="lbl">The disambiguation line is worth more than it looks</span>
  <p>If your company name is close to another firm's, or your category is adjacent to one you are not in, say so explicitly. One sentence like "we manufacture industrial gaskets; we are not affiliated with [similarly named company]" resolves an ambiguity that could otherwise put someone else's reputation on your name.</p>
</div>

<h2>What it will not do</h2>
<ul>
  <li>It will not get you cited if you have no substantive content to cite.</li>
  <li>It will not override what other sites say about you.</li>
  <li>It does not replace schema markup — schema is machine-readable data attached to specific pages; llms.txt is a site-level summary. Do both.</li>
  <li>It is not a ranking factor in any documented sense.</li>
</ul>

<h2>Higher-value work in the same hour</h2>
<p>If you have limited time, do these first — all are better established than llms.txt:</p>
<ol>
  <li><strong>Check you are not blocking AI crawlers.</strong> Look in <code>robots.txt</code> for <code>Google-Extended</code> and <code>Applebot-Extended</code>. Sites block these by accident more often than you would expect.</li>
  <li><strong>Mark up your FAQ with FAQPage schema.</strong> If you have a visible FAQ and no markup on it, that is free structured data left on the table.</li>
  <li><strong>Publish one real answer page</strong> for the question your buyers ask most.</li>
  <li><strong>Get your spec tables out of PDFs</strong> and into HTML.</li>
</ol>
<p>Then write the llms.txt. Ours is at <a href="/llms.txt">foundvale.com/llms.txt</a> if you want to see the shape of one.</p>
""",
        "related": ["get-found-when-buyers-ask-ai-for-suppliers", "does-seo-still-matter-with-ai-search", "check-what-ai-says-about-your-company"],
    },
    {
        "slug": "can-we-do-ai-search-optimization-in-house",
        "q": "Can we do AI search optimization in-house?",
        "title": "Can you do AI search optimization in-house? An honest assessment",
        "desc": "Yes, if someone owns it for a few hours every month, indefinitely. The audit is easy and the consistency is hard — most in-house programs stall on sustained publishing, not on knowing what to do.",
        "answer": "Yes — the method is public and none of it is technically difficult. The constraint is almost never capability; it is whether someone in your company can reliably spend a few hours a month on it forever, because the work only compounds if it is sustained.",
        "body": """
<h2>What is genuinely easy to do yourself</h2>
<ul>
  <li><strong>The audit.</strong> Fifteen prompts across three engines, about an hour. <a href="/answers/check-what-ai-says-about-your-company/">Full method here</a>, free.</li>
  <li><strong>Technical hygiene.</strong> Checking crawler directives, adding a sitemap, writing an <a href="/answers/what-is-llms-txt/">llms.txt</a>. An afternoon.</li>
  <li><strong>Claiming directory and association profiles.</strong> Tedious, not hard, and often the highest-return hour available.</li>
  <li><strong>Getting spec tables out of PDFs.</strong> If you have someone who can edit the site, this is a day and it is worth more than most content.</li>
</ul>

<h2>What people underestimate</h2>
<h3>Sustained publishing volume</h3>
<p>One good page does very little. The programs that move are publishing consistently — call it four substantial pages a month — for six months or more. Almost every in-house effort we have seen described starts strong, produces three pages in month one, and stops in month two when a customer escalation lands. The work is not hard; it is <em>relentless</em>, and it has no deadline forcing it, so it always loses to work that does.</p>

<h3>Writing that survives an engineer's read</h3>
<p>Industrial content fails in a specific way: it is generically correct and specifically wrong. A tolerance stated in the wrong units, a material grade that does not exist in that form, a certification described loosely. Your buyers are technical, and one visible error costs more credibility than five good pages earn. This is also the trap with using an AI writing tool unsupervised — the output is fluent, confident, and occasionally invents a specification.</p>

<h3>Knowing what to write about</h3>
<p>The instinct is to write about what you want to sell. The pages that get cited answer what buyers ask, which is usually more granular and less flattering — selection tradeoffs, sizing methods, failure modes, honest comparisons. Getting that list right is what the citation trace is for.</p>

<h2>A reasonable in-house plan</h2>
<ol>
  <li>Run the audit. Log who is named and which sources were cited.</li>
  <li>Fix the technical basics in one afternoon.</li>
  <li>Claim every directory and association profile in your category.</li>
  <li>Pick the five questions from the audit where you were absent and your expertise is strongest.</li>
  <li>Publish one page per month against that list, answer-first, with a real spec table.</li>
  <li>Re-run the same audit monthly and log the delta.</li>
</ol>
<p>Budget three to five hours a month, and put it on one named person's calendar as a recurring commitment. If you can hold that for six months, you do not need us.</p>

<div class="callout">
  <span class="lbl">The honest disqualifier</span>
  <p>If you have a marketing person with capacity and a technical writer's instincts, in-house is genuinely the better economics and we will say so on a call. Where outsourcing wins is when the alternative is not "in-house program" but "nothing happens for another year" — which, in the $2&ndash;25M band with no marketing staff, is the realistic comparison.</p>
</div>

<h2>The hybrid that usually works best</h2>
<p>Keep the parts that need your relationships and judgment in-house: directory profiles, distributor coordination, and the technical review of anything before it publishes. Outsource the part that needs consistency: research, drafting, structuring, schema, and the monthly tracked-query log. That is the split our engine is built around — one short async questionnaire from your side, everything else from ours, and your team reviews before anything ships.</p>
""",
        "related": ["how-much-does-ai-search-optimization-cost", "check-what-ai-says-about-your-company", "does-seo-still-matter-with-ai-search"],
    },
    {
        "slug": "what-we-found-auditing-industrial-manufacturers",
        "q": "What did we find auditing AI visibility for industrial manufacturers?",
        "title": "What we found auditing AI visibility across specialty manufacturers",
        "desc": "Aggregate findings from AI-visibility audits across specialty manufacturers and industrial distributors: most were absent from their own core category, and citation sources were dominated by directories and competitor content.",
        "answer": "Across audits of specialty manufacturers and industrial distributors, the majority were absent from AI answers in their own core category — including several that have led their niche for decades. Where a company was present, it was frequently surfaced through a third-party directory listing rather than its own content, meaning the engine knew the company existed but was quoting someone else about it.",
        "body": """
<div class="callout">
  <span class="lbl">Method and disclosure</span>
  <p>Findings are aggregated from audits run on real specialty manufacturers and industrial distributors using public information only, three buyer queries per company, logged-out sessions, one fresh chat per company. <strong>No company is named here.</strong> Several are firms we have contacted or may contact, and publishing a named negative finding about a company that did not ask for an audit is not something we will do. The patterns are the useful part; the names are not ours to publish.</p>
</div>

<h2>Finding 1 &mdash; Absence is the norm, and it is not about company quality</h2>
<p>Most audited companies did not appear in the answer to at least one query describing exactly what they make. Several were absent from all three. This included companies that have operated in their niche for fifty years or more, hold the specialist reputation in their category, and are the firm a knowledgeable buyer would name first.</p>
<p>In their place, engines named between six and ten competitors per query — usually a mix of the largest players in the category and mid-size firms that publish substantial engineering content.</p>

<h2>Finding 2 &mdash; The split between "recommended" and "quoted"</h2>
<p>This was the most actionable pattern, and it is invisible if you only log whether you were mentioned.</p>
<p>Several companies were recommended as suppliers on "who makes X" queries, but absent from the technical queries in the same category — the sizing questions, the selection tradeoffs, the spec guidance. On those, engines quoted competitors' calculators, charts and guidance pages.</p>
<p>The practical reading: the engine knows you make the product, but does not treat you as the authority on it. That gap is the whole opportunity, because the technical query is the earlier one. The buyer asking how to size the part has not yet decided who to RFQ.</p>

<h2>Finding 3 &mdash; Citations run through directories more than through vendor sites</h2>
<p>Where sources were visible, they skewed heavily toward third-party pages: trade directories, distributor catalogs, association listings and comparison content. Some companies appeared in an answer <em>only</em> through a directory citation — present, but with the directory's thin description standing in for their own positioning.</p>
<p>This is the finding that shapes how we scope work. Publishing on your own domain does not touch a directory-dominated citation pattern. Both moves are required, and the audit is what tells you the ratio.</p>

<h2>Finding 4 &mdash; Published engineering data is the single strongest predictor</h2>
<p>The companies that showed up on technical queries had one thing in common: they publish real, structured engineering data on the open web. Size charts as HTML tables. Selection guides. Sizing calculators. Material and tolerance references. Not gated, not in a PDF, not rendered as an image.</p>
<p>Almost every audited company <em>possessed</em> comparable data. The ones getting cited had published it in a machine-readable form. The ones absent had it in catalogs, spec sheets behind a form, or on paper.</p>

<h2>Finding 5 &mdash; Category leadership does not transfer automatically</h2>
<p>The most striking cases were companies that effectively defined a product category and were absent from the answer to "who makes [that category]." Decades of reputation, well-known within the industry, invisible to a model assembling an answer from public text.</p>
<p>The reassuring inverse: because position tracks published content rather than incumbency, these positions are winnable by whoever does the work. That cuts against you today and for you once you start.</p>

<h2>What we take from it</h2>
<ul>
  <li>Run the citation trace before writing anything &mdash; the source mix determines where effort goes.</li>
  <li>Technical and selection queries are usually a bigger opportunity than "who makes X" queries, and are less contested.</li>
  <li>Getting existing engineering data out of PDFs is often the highest-return first move, ahead of writing anything new.</li>
  <li>Directory and distributor listings deserve real attention, because in many categories they <em>are</em> the cited source.</li>
</ul>

<div class="callout">
  <span class="lbl">Scope and limits</span>
  <p>This is a modest sample within one segment, run at a point in time, on three queries per company. Engine answers are non-deterministic and shift; a re-run would not reproduce these exactly. We report it as an observed pattern worth checking against your own category, not as a benchmark.</p>
</div>
""",
        "related": ["why-ai-names-distributors-instead-of-manufacturers", "check-what-ai-says-about-your-company", "get-found-when-buyers-ask-ai-for-suppliers"],
    },
]

BY_SLUG = {p["slug"]: p for p in PAGES}


def esc(t):
    return html.escape(t, quote=True)


def strip_tags(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()


def page_schema(p, url):
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": url + "#article",
                "headline": p["title"],
                "description": p["desc"],
                "url": url,
                "datePublished": TODAY,
                "dateModified": TODAY,
                "inLanguage": "en-US",
                "isPartOf": {"@id": BASE + "/#website"},
                "publisher": {"@id": BASE + "/#organization"},
                "author": {"@type": "Organization", "name": "Foundvale", "url": BASE + "/"},
                "about": {"@type": "Thing", "name": "AI search visibility for industrial B2B"},
            },
            {
                "@type": "FAQPage",
                "@id": url + "#faq",
                "mainEntity": [{
                    "@type": "Question",
                    "name": p["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": p["answer"]},
                }],
            },
            {
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Answers", "item": BASE + "/answers/"},
                    {"@type": "ListItem", "position": 3, "name": p["q"], "item": url},
                ],
            },
        ],
    }, indent=2)


def render(p):
    url = f"{BASE}/answers/{p['slug']}/"
    rel = "".join(
        f'\n      <li><a href="/answers/{s}/">{esc(BY_SLUG[s]["q"])}</a></li>'
        for s in p["related"] if s in BY_SLUG
    )
    head = HEAD.format(
        title=esc(p["title"] + " | Foundvale"),
        url=url, base=BASE,
        desc=esc(p["desc"]),
        ogtitle=esc(p["q"]),
        schema=page_schema(p, url),
    )
    return f"""<!doctype html>
<html lang="en">
<head>
{head}
</head>
<body>
{NAV}
<div class="wrap">
  <div class="crumb"><a href="/">Foundvale</a><span>/</span><a href="/answers/">Answers</a></div>
  <article>
    <h1>{esc(p['q'])}</h1>
    <p class="standfirst">{esc(p['answer'])}</p>
{p['body'].rstrip()}
{NEXTSTEP}
    <div class="related">
      <span class="lbl">Related answers</span>
      <ul>{rel}
      </ul>
    </div>
  </article>
</div>
{FOOTER}
</body>
</html>
"""


def render_hub():
    url = f"{BASE}/answers/"
    items = "".join(
        f'\n  <li><a href="/answers/{p["slug"]}/">{esc(p["q"])}</a><p>{esc(strip_tags(p["answer"])[:190])}&hellip;</p></li>'
        for p in PAGES
    )
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": url + "#page",
                "name": "Answers — AI search visibility for industrial B2B",
                "description": "Straight answers to the questions specialty manufacturers and industrial distributors ask about getting found in AI-driven buyer research.",
                "url": url,
                "isPartOf": {"@id": BASE + "/#website"},
                "publisher": {"@id": BASE + "/#organization"},
            },
            {
                "@type": "ItemList",
                "@id": url + "#list",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": p["q"],
                     "url": f"{BASE}/answers/{p['slug']}/"}
                    for i, p in enumerate(PAGES)
                ],
            },
            {
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Answers", "item": url},
                ],
            },
        ],
    }, indent=2)
    head = HEAD.format(
        title="Answers — AI search visibility for industrial manufacturers | Foundvale",
        url=url, base=BASE,
        desc="Straight answers to the questions specialty manufacturers and industrial distributors ask about getting found in AI-driven buyer research. No gates, no forms.",
        ogtitle="Answers — AI search visibility for industrial B2B",
        schema=schema,
    )
    return f"""<!doctype html>
<html lang="en">
<head>
{head}
</head>
<body>
{NAV}
<div class="wrap">
  <div class="crumb"><a href="/">Foundvale</a></div>
  <article>
    <h1>Answers</h1>
    <p class="standfirst">The questions specialty manufacturers and industrial distributors actually ask us about AI search &mdash; answered directly, with no gate and no form. If your question is not here, <a href="mailto:hello@foundvale.com">email us</a> and we will answer it and add it.</p>
    <ul class="hublist">{items}
    </ul>
{NEXTSTEP}
  </article>
</div>
{FOOTER}
</body>
</html>
"""


def main():
    out = ROOT / "answers"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(render_hub())
    written = ["answers/index.html"]
    for p in PAGES:
        d = out / p["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(render(p))
        written.append(f"answers/{p['slug']}/index.html")

    # sitemap
    urls = [(BASE + "/", "1.0", "weekly"), (BASE + "/answers/", "0.9", "weekly")]
    urls += [(f"{BASE}/answers/{p['slug']}/", "0.8", "monthly") for p in PAGES]
    body = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for u, pr, cf in urls
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body + "\n</urlset>\n"
    )
    written.append("sitemap.xml")

    for w in written:
        print("  wrote", w)
    print(f"\n{len(PAGES)} answer pages + hub + sitemap ({len(urls)} URLs)")


if __name__ == "__main__":
    main()
