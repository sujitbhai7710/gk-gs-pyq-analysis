#!/usr/bin/env python3
"""
Generate all HTML pages for the multi-page GK GS Analysis website.
- index.html: Landing page with overview
- <subject>.html: One page per subject with sub-topics and questions
- about.html: About/methodology page
"""
import json
import os
import re
import html

DATA_FILE = "/home/z/my-project/website/data.json"
OUT_DIR = "/home/z/my-project/website"

# Subject file name mapping
SUBJECT_FILES = {
    "History": "history",
    "Geography": "geography",
    "Polity": "polity",
    "Economics": "economics",
    "General Science": "science",
    "Static GK": "static-gk",
    "Current Affairs": "current-affairs",
    "Uncategorized": "uncategorized",
}

def slugify(s):
    """Convert to HTML-safe identifier."""
    return re.sub(r'[^a-zA-Z0-9]+', '-', s.lower()).strip('-')

def esc(text):
    """HTML escape."""
    return html.escape(str(text) if text else '')

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def nav_links(active=None):
    """Generate navigation HTML."""
    data = load_data()
    links = []
    links.append(f'<li><a href="index.html" class="{("active" if active=="home" else "")}">Home</a></li>')
    for subject in data['subject_order']:
        if subject in SUBJECT_FILES:
            fname = SUBJECT_FILES[subject]
            cls = 'active' if active == fname else ''
            links.append(f'<li><a href="{fname}.html" class="{cls}">{esc(subject)}</a></li>')
    links.append(f'<li><a href="about.html" class="{("active" if active=="about" else "")}">About</a></li>')
    return '\n'.join(links)

def footer_html():
    return """<footer class="footer">
  <div class="footer-content">
    <div class="footer-section">
      <h4>GK GS Analysis</h4>
      <a href="index.html">Home</a>
      <a href="about.html">About this Project</a>
    </div>
    <div class="footer-section">
      <h4>Subjects</h4>
      <a href="history.html">History</a>
      <a href="geography.html">Geography</a>
      <a href="polity.html">Polity</a>
      <a href="economics.html">Economics</a>
    </div>
    <div class="footer-section">
      <h4>More Subjects</h4>
      <a href="science.html">General Science</a>
      <a href="static-gk.html">Static GK</a>
      <a href="current-affairs.html">Current Affairs</a>
    </div>
    <div class="footer-section">
      <h4>Source</h4>
      <p style="font-size:0.85rem; color:rgba(255,255,255,0.7);">SSC CGL Tier 1<br>General Awareness<br>Sep-Oct 2025</p>
    </div>
  </div>
  <div class="footer-bottom">
    Generated from official SSC CGL Tier 1 question papers &middot; Analysis for educational purposes only
  </div>
</footer>"""

def navbar_html(active=None):
    return f"""<nav class="navbar">
  <div class="nav-container">
    <a href="index.html" class="nav-logo">
      <div class="nav-logo-icon">📚</div>
      <span>GK GS Analysis</span>
    </a>
    <button class="mobile-menu-btn" onclick="toggleMobileMenu()">☰</button>
    <ul class="nav-links">
      {nav_links(active)}
    </ul>
  </div>
</nav>"""

# ============== INDEX PAGE ==============
def generate_index(data):
    total_q = data['metadata']['total_questions']
    total_sub = data['metadata']['total_subtopics']
    total_subjects = data['metadata']['total_subjects']
    
    # Build subject cards
    cards = []
    for subject in data['subject_order']:
        if subject not in data['subjects']:
            continue
        sd = data['subjects'][subject]
        meta = sd['meta']
        fname = SUBJECT_FILES.get(subject, slugify(subject))
        
        cards.append(f"""<a href="{fname}.html" class="subject-card" style="--card-color: {meta['color']}; --card-gradient: {meta['gradient']};">
  <div class="subject-card-header">
    <div class="subject-icon">{meta['icon']}</div>
    <div class="subject-count">{sd['total_questions']} Qs</div>
  </div>
  <h3>{esc(subject)}</h3>
  <p>{esc(meta['description'])}</p>
  <div class="subject-card-meta">
    <span>📊 {sd['subtopic_count']} sub-topics</span>
    <span>📝 {sd['total_questions']} questions</span>
  </div>
</a>""")
    
    cards_html = '\n'.join(cards)
    
    # Subject distribution for chart
    chart_labels = []
    chart_data = []
    chart_colors = []
    for subject in data['subject_order']:
        if subject not in data['subjects']:
            continue
        sd = data['subjects'][subject]
        chart_labels.append(subject)
        chart_data.append(sd['total_questions'])
        chart_colors.append(sd['meta']['color'])
    
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GK GS Analysis &middot; SSC CGL Tier 1 (2025) Question Bank</title>
<meta name="description" content="Comprehensive analysis of {total_q} General Awareness questions from SSC CGL Tier 1 (Sep-Oct 2025) - Categorized by subject and sub-topic with full question bank.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
{navbar_html('home')}

<section class="hero">
  <div class="hero-content">
    <div class="hero-badge">
      <span>📅</span> SSC CGL Tier 1 &middot; September-October 2025
    </div>
    <h1>GK GS Previous Year<br>Question Analysis</h1>
    <p>A comprehensive, fully-categorized analysis of {total_q} General Awareness (GK/GS) questions from the SSC CGL Tier 1 examination. Every question is classified by subject and sub-topic, with the full question text and all options preserved.</p>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="hero-stat-num">{total_q}</div>
        <div class="hero-stat-label">Total Questions</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-num">{total_subjects}</div>
        <div class="hero-stat-label">Subjects</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-num">{total_sub}</div>
        <div class="hero-stat-label">Sub-topics</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-num">~80</div>
        <div class="hero-stat-label">Exam Shifts</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-title">Subject Distribution</h2>
  <p class="section-subtitle">Distribution of all {total_q} questions across major subjects. Click any subject to dive deeper.</p>
  
  <div class="chart-container">
    <h3 class="chart-title">Questions by Subject</h3>
    <p class="chart-subtitle">Total count of questions in each major subject area</p>
    <div class="chart-wrapper">
      <canvas id="subjectChart"></canvas>
    </div>
  </div>

  <div class="chart-container">
    <h3 class="chart-title">Subject Share (Percentage)</h3>
    <p class="chart-subtitle">Relative weight of each subject in the SSC CGL General Awareness section</p>
    <div class="chart-wrapper" style="height: 380px;">
      <canvas id="subjectDonut"></canvas>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-title">Explore by Subject</h2>
  <p class="section-subtitle">Click any subject card to view detailed sub-topic breakdown and all questions</p>
  <div class="subject-grid">
{cards_html}
  </div>
</section>

<section class="section">
  <h2 class="section-title">How to Use This Resource</h2>
  <p class="section-subtitle">Maximize your SSC CGL preparation with this structured PYQ analysis</p>
  <div class="subject-grid">
    <div class="subject-card" style="--card-color: #1e3a8a; --card-gradient: linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%);">
      <div class="subject-card-header">
        <div class="subject-icon">🎯</div>
      </div>
      <h3>Identify High-Weight Topics</h3>
      <p>See which sub-topics (e.g. Mughal Empire, Mauryan Empire, Indian Dance Forms) get the most questions, so you can prioritize your study.</p>
    </div>
    <div class="subject-card" style="--card-color: #059669; --card-gradient: linear-gradient(135deg, #059669 0%, #064e3b 100%);">
      <div class="subject-card-header">
        <div class="subject-icon">📖</div>
      </div>
      <h3>Practice Real Questions</h3>
      <p>Every question is shown with all four options - just like the real exam. Use them for quick revision and self-testing.</p>
    </div>
    <div class="subject-card" style="--card-color: #d97706; --card-gradient: linear-gradient(135deg, #d97706 0%, #78350f 100%);">
      <div class="subject-card-header">
        <div class="subject-icon">🔍</div>
      </div>
      <h3>Track Pattern Shifts</h3>
      <p>The SSC CGL 2025 pattern emphasises art & culture, schemes, and sports current affairs. Spot the trend here.</p>
    </div>
    <div class="subject-card" style="--card-color: #be185d; --card-gradient: linear-gradient(135deg, #be185d 0%, #500724 100%);">
      <div class="subject-card-header">
        <div class="subject-icon">📊</div>
      </div>
      <h3>Visual Analytics</h3>
      <p>Interactive charts make it easy to see the relative importance of each subject and sub-topic at a glance.</p>
    </div>
  </div>
</section>

{footer_html()}

<script src="app.js"></script>
<script>
  const labels = {json.dumps(chart_labels)};
  const counts = {json.dumps(chart_data)};
  const colors = {json.dumps(chart_colors)};
  renderSubjectChart('subjectChart', labels, counts, colors);
  renderDonutChart('subjectDonut', labels, counts, colors);
</script>
</body>
</html>"""
    return page


# ============== SUBJECT PAGE ==============
def generate_subject_page(data, subject_name):
    if subject_name not in data['subjects']:
        return None
    
    sd = data['subjects'][subject_name]
    meta = sd['meta']
    fname = SUBJECT_FILES.get(subject_name, slugify(subject_name))
    
    # Build sub-topic sections
    subtopic_sections = []
    chart_labels = []
    chart_data = []
    
    for i, sub in enumerate(sd['subtopics'], 1):
        sub_id = f"sub-{i}"
        chart_labels.append(sub['name'])
        chart_data.append(sub['count'])
        
        # Build question cards
        q_cards = []
        for q in sub['questions']:
            opts_html = ""
            if q['options']:
                opt_items = []
                letters = ['A', 'B', 'C', 'D', 'E']
                for j, opt in enumerate(q['options'][:4]):
                    letter = letters[j] if j < len(letters) else str(j+1)
                    opt_items.append(f'<li><span class="option-letter">{letter}.</span><span>{esc(opt)}</span></li>')
                opts_html = f'<ul class="question-options">{"".join(opt_items)}</ul>'
            
            shift_text = esc(q.get('shift', ''))[:80]
            q_cards.append(f"""<div class="question-card">
  <div class="question-header">
    <span class="question-num">Q.{q['qno']}</span>
    <span class="question-shift">{shift_text}</span>
  </div>
  <div class="question-text">{esc(q['question'])}</div>
  {opts_html}
</div>""")
        
        questions_html = '\n'.join(q_cards)
        
        # Auto-expand first 3 subtopics
        expanded_class = 'expanded' if i <= 3 else ''
        
        subtopic_sections.append(f"""<div class="subtopic-section {expanded_class}" id="{sub_id}" style="--subject-color: {meta['color']};">
  <div class="subtopic-header" onclick="toggleSubtopic('{sub_id}')">
    <div class="subtopic-title-row">
      <div class="subtopic-number">{i}</div>
      <div class="subtopic-title">{esc(sub['name'])}</div>
    </div>
    <div class="subtopic-meta">
      <span class="subtopic-count">{sub['count']} Qs</span>
      <button class="subtopic-toggle" aria-label="Toggle">▼</button>
    </div>
  </div>
  <div class="subtopic-body">
    {questions_html if questions_html else '<p style="color: var(--text-muted); font-style: italic;">No questions extracted for this sub-topic.</p>'}
  </div>
</div>""")
    
    sections_html = '\n'.join(subtopic_sections)
    
    # Top 10 subtopics for chart (to keep it readable)
    top_n = 12
    chart_labels_top = chart_labels[:top_n]
    chart_data_top = chart_data[:top_n]
    
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(subject_name)} &middot; GK GS Analysis &middot; SSC CGL 2025</title>
<meta name="description" content="Detailed analysis of {sd['total_questions']} {esc(subject_name)} questions from SSC CGL Tier 1 (2025), broken into {sd['subtopic_count']} sub-topics with full question text and options.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
{navbar_html(fname)}

<section class="subject-hero" style="--subject-gradient: {meta['gradient']};">
  <div class="subject-hero-content">
    <div class="subject-hero-icon">{meta['icon']}</div>
    <div class="subject-hero-text">
      <h1>{esc(subject_name)}</h1>
      <p>{esc(meta['description'])}</p>
      <div class="subject-hero-stats">
        <div class="subject-hero-stat">
          <div class="subject-hero-stat-num">{sd['total_questions']}</div>
          <div class="subject-hero-stat-label">Total Questions</div>
        </div>
        <div class="subject-hero-stat">
          <div class="subject-hero-stat-num">{sd['subtopic_count']}</div>
          <div class="subject-hero-stat-label">Sub-topics</div>
        </div>
        <div class="subject-hero-stat">
          <div class="subject-hero-stat-num">{(sd['total_questions']*100)//data['metadata']['total_questions']}%</div>
          <div class="subject-hero-stat-label">Of All Questions</div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="breadcrumb">
  <a href="index.html">Home</a>
  <span class="breadcrumb-sep">›</span>
  <span>{esc(subject_name)}</span>
</div>

<section class="section" style="padding-top: 1.5rem;">
  <div style="display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
    <input type="text" id="searchInput" placeholder="🔍 Search questions in {esc(subject_name)}..." 
           style="flex: 1; min-width: 250px; padding: 0.75rem 1rem; border: 1px solid var(--border); border-radius: var(--radius-sm); font-size: 0.95rem; font-family: inherit;"
           oninput="searchQuestions('searchInput', 'subtopicsContainer')">
    <button onclick="expandAll()" style="padding: 0.75rem 1.25rem; background: {meta['color']}; color: white; border: none; border-radius: var(--radius-sm); cursor: pointer; font-weight: 600; font-size: 0.9rem;">Expand All</button>
    <button onclick="collapseAll()" style="padding: 0.75rem 1.25rem; background: white; color: var(--text); border: 1px solid var(--border); border-radius: var(--radius-sm); cursor: pointer; font-weight: 600; font-size: 0.9rem;">Collapse All</button>
  </div>

  <div class="chart-container">
    <h3 class="chart-title">Sub-topic Distribution</h3>
    <p class="chart-subtitle">Top {len(chart_labels_top)} sub-topics by question count in {esc(subject_name)}</p>
    <div class="chart-wrapper" style="height: {max(300, len(chart_labels_top)*35)}px;">
      <canvas id="subtopicChart"></canvas>
    </div>
  </div>

  <h2 class="section-title" style="font-size: 1.5rem;">All Sub-topics &amp; Questions</h2>
  <p class="section-subtitle">Click any sub-topic to expand and view all its questions</p>

  <div id="subtopicsContainer">
{sections_html}
  </div>
</section>

{footer_html()}

<script src="app.js"></script>
<script>
  const labels = {json.dumps(chart_labels_top)};
  const counts = {json.dumps(chart_data_top)};
  const color = "{meta['color']}";
  renderSubtopicChart('subtopicChart', labels, counts, color);
</script>
</body>
</html>"""
    return page


# ============== ABOUT PAGE ==============
def generate_about_page(data):
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About &middot; GK GS Analysis</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
{navbar_html('about')}

<section class="hero" style="padding: 3rem 1.5rem 4rem;">
  <div class="hero-content">
    <div class="hero-badge"><span>ℹ️</span> About</div>
    <h1>About This Project</h1>
    <p>A data-driven analysis of SSC CGL Tier 1 General Awareness questions, organized for smart preparation.</p>
  </div>
</section>

<section class="section">
  <h2 class="section-title">Overview</h2>
  <p style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 1.5rem;">
    This website presents a structured analysis of {data['metadata']['total_questions']} General Awareness (GK/GS) questions 
    from the SSC CGL Tier 1 examination held in September-October 2025. Every question has been categorized 
    into one of {data['metadata']['total_subjects']} major subjects and further classified into {data['metadata']['total_subtopics']} 
    sub-topics, giving you a granular view of what SSC actually asks.
  </p>

  <h2 class="section-title" style="margin-top: 2.5rem;">Methodology</h2>
  <p style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 1rem;">
    The analysis was performed in the following steps:
  </p>
  <ol style="font-size: 1rem; color: var(--text); margin-left: 1.5rem; line-height: 2;">
    <li><strong>Source PDF:</strong> The official SSC CGL Tier 1 question paper PDF (488 pages, bilingual English/Hindi) was downloaded from Google Drive.</li>
    <li><strong>OCR Extraction:</strong> Each page was rendered at 150 DPI and processed with Tesseract OCR (English language mode) to extract text. Hindi text was filtered out automatically.</li>
    <li><strong>Question Parsing:</strong> A custom parser identified question blocks (Q.No markers), extracted the English question text, and isolated the four options from surrounding translated text.</li>
    <li><strong>Subject Categorization:</strong> Each question was matched against a taxonomy of {data['metadata']['total_subtopics']} sub-topics across {data['metadata']['total_subjects']} subjects using keyword-based scoring. The best-matching sub-topic was assigned to each question.</li>
    <li><strong>Website Generation:</strong> A multi-page static website was generated with interactive charts, expandable sub-topic sections, and full question listings.</li>
  </ol>

  <h2 class="section-title" style="margin-top: 2.5rem;">Taxonomy</h2>
  <p style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 1rem;">
    The categorization taxonomy covers the standard SSC CGL General Awareness syllabus:
  </p>
  <div class="subject-grid" style="margin-top: 1.5rem;">
"""
    
    for subject in data['subject_order']:
        if subject not in data['subjects']:
            continue
        sd = data['subjects'][subject]
        meta = sd['meta']
        fname = SUBJECT_FILES.get(subject, slugify(subject))
        page += f"""    <a href="{fname}.html" class="subject-card" style="--card-color: {meta['color']}; --card-gradient: {meta['gradient']};">
      <div class="subject-card-header">
        <div class="subject-icon">{meta['icon']}</div>
        <div class="subject-count">{sd['total_questions']} Qs</div>
      </div>
      <h3>{esc(subject)}</h3>
      <p>{esc(meta['description'])}</p>
      <div class="subject-card-meta">
        <span>📊 {sd['subtopic_count']} sub-topics</span>
      </div>
    </a>
"""
    
    page += f"""  </div>

  <h2 class="section-title" style="margin-top: 2.5rem;">Important Notes</h2>
  <ul style="font-size: 1rem; color: var(--text); margin-left: 1.5rem; line-height: 2;">
    <li>Only the <strong>English version</strong> of questions is included (Hindi text filtered out).</li>
    <li>OCR extraction may introduce minor typos in question text; refer to the original PDF for verbatim text.</li>
    <li>Categorization is <strong>keyword-based and heuristic</strong> - a small percentage of questions may be misclassified.</li>
    <li>Questions are deduplicated by question number + first 100 characters, so questions appearing in multiple shifts are counted once.</li>
    <li>"Not Answered" markers from the original PDF are preserved in the data but not displayed prominently.</li>
    <li>Source: SSC CGL Tier 1 General Awareness (PART-B), Q.No 26-50 per shift, ~80 shifts in Sep-Oct 2025.</li>
  </ul>

  <h2 class="section-title" style="margin-top: 2.5rem;">Source File</h2>
  <p style="font-size: 1.05rem; color: var(--text-muted);">
    Original PDF: <a href="https://drive.google.com/file/d/1no_Hvs2e3aBy-VrHvecGiYZixGHVuUUw/view" target="_blank" style="color: var(--primary);">Google Drive link</a><br>
    Total pages: 488 &middot; File size: ~48 MB
  </p>
</section>

{footer_html()}

<script src="app.js"></script>
</body>
</html>"""
    return page


# ============== MAIN ==============
def main():
    data = load_data()
    
    # Generate index
    index_html = generate_index(data)
    with open(f"{OUT_DIR}/index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"Generated: index.html")
    
    # Generate subject pages
    for subject in data['subject_order']:
        if subject not in data['subjects']:
            continue
        fname = SUBJECT_FILES.get(subject, slugify(subject))
        html_content = generate_subject_page(data, subject)
        if html_content:
            with open(f"{OUT_DIR}/{fname}.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Generated: {fname}.html ({data['subjects'][subject]['total_questions']} questions)")
    
    # Generate about page
    about_html = generate_about_page(data)
    with open(f"{OUT_DIR}/about.html", 'w', encoding='utf-8') as f:
        f.write(about_html)
    print(f"Generated: about.html")
    
    print(f"\nAll pages generated in: {OUT_DIR}")
    print(f"Total files: {len(os.listdir(OUT_DIR))}")


if __name__ == "__main__":
    main()
