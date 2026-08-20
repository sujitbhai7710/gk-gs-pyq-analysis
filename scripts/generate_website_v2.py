#!/usr/bin/env python3
"""
Generate all HTML pages for the multi-page GK GS Analysis website - v2.
- Shows correct answers (when available) with explanation
- Properly displays split sub-topics (Indian Dance, Music, Architecture separate)
- Updated stats and metadata
"""
import json
import os
import re
import html

DATA_FILE = "/home/z/my-project/website/data.json"
OUT_DIR = "/home/z/my-project/website"

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
    return re.sub(r'[^a-zA-Z0-9]+', '-', s.lower()).strip('-')

def esc(text):
    return html.escape(str(text) if text else '')

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def nav_links(active=None):
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
    OCR via Gemini/z-ai Vision + Tesseract &middot; Categorization via Keyword Taxonomy + LLM &middot; For educational purposes only
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

def render_options_with_answer(q, subject_color):
    """Render question options with correct answer highlighted."""
    opts = q.get('options', [])
    if not opts:
        return '<p style="color: var(--text-muted); font-style: italic; font-size: 0.85rem;">Options not extracted (OCR issue).</p>'
    
    correct = q.get('correct_answer', '').upper().strip()
    letters = ['A', 'B', 'C', 'D']
    
    items = []
    for i, opt in enumerate(opts[:4]):
        letter = letters[i] if i < len(letters) else str(i+1)
        is_correct = (correct == letter) and correct in ['A', 'B', 'C', 'D']
        bg = '#dcfce7' if is_correct else 'white'
        border = f'2px solid {subject_color}' if is_correct else '1px solid var(--border)'
        checkmark = '✓ ' if is_correct else ''
        items.append(f'<li style="background: {bg}; border: {border};"><span class="option-letter">{letter}.</span><span>{esc(opt)}</span><span style="margin-left: auto; color: {subject_color}; font-weight: 700;">{checkmark if is_correct else ""}</span></li>')
    
    result = f'<ul class="question-options">{"".join(items)}</ul>'
    
    # Add explanation if available
    explanation = q.get('explanation', '').strip()
    if explanation and correct in ['A', 'B', 'C', 'D']:
        result += f'<div class="explanation"><strong>Explanation:</strong> {esc(explanation)}</div>'
    elif correct == 'N/A':
        result += '<div class="explanation" style="color: var(--text-muted);"><em>Not Answered in source</em></div>'
    
    return result


# ============== INDEX PAGE ==============
def generate_index(data):
    total_q = data['metadata']['total_questions']
    total_sub = data['metadata']['total_subtopics']
    total_subjects = data['metadata']['total_subjects']
    has_answers = data['metadata']['has_answers']
    
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
<meta name="description" content="Comprehensive analysis of {total_q} General Awareness questions from SSC CGL Tier 1 (Sep-Oct 2025) - Categorized by subject and sub-topic with full question bank and correct answers.">
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
    <p>A comprehensive, fully-categorized analysis of <strong>{total_q} General Awareness (GK/GS) questions</strong> from the SSC CGL Tier 1 examination. Every question is classified by subject and sub-topic, with the full question text, all four options, and correct answers (extracted via LLM where available).</p>
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
        <div class="hero-stat-num">{has_answers}</div>
        <div class="hero-stat-label">With Answers</div>
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
  <h2 class="section-title">What's New in v2</h2>
  <p class="section-subtitle">Major improvements over v1</p>
  <div class="subject-grid">
    <div class="subject-card" style="--card-color: #1e3a8a; --card-gradient: linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%);">
      <div class="subject-card-header">
        <div class="subject-icon">🔀</div>
      </div>
      <h3>Split Sub-topics</h3>
      <p>"Indian Dance, Music & Performing Arts" is now split into 4 separate sub-topics: Classical Dance, Folk Dance & Martial Arts, Music Theory, and Musical Instruments.</p>
    </div>
    <div class="subject-card" style="--card-color: #059669; --card-gradient: linear-gradient(135deg, #059669 0%, #064e3b 100%);">
      <div class="subject-card-header">
        <div class="subject-icon">✨</div>
      </div>
      <h3>Better OCR</h3>
      <p>Used Gemini/z-ai Vision (VLM) for high-accuracy OCR, with improved Tesseract as fallback. Hindi text is properly filtered out, so questions and options are cleaner.</p>
    </div>
    <div class="subject-card" style="--card-color: #d97706; --card-gradient: linear-gradient(135deg, #d97706 0%, #78350f 100%);">
      <div class="subject-card-header">
        <div class="subject-icon">✓</div>
      </div>
      <h3>Correct Answers</h3>
      <p>Correct answers extracted via LLM (z-ai chat). Each question shows the correct option highlighted in green, with a brief explanation when available.</p>
    </div>
    <div class="subject-card" style="--card-color: #be185d; --card-gradient: linear-gradient(135deg, #be185d 0%, #500724 100%);">
      <div class="subject-card-header">
        <div class="subject-icon">🏛️</div>
      </div>
      <h3>Architecture Split</h3>
      <p>Architecture is now split into: Temple Architecture (Hindu/Buddhist/Jain), Indo-Islamic Architecture (Mughal/Sultanate), and Modern Architecture & Monuments.</p>
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
    
    subtopic_sections = []
    chart_labels = []
    chart_data = []
    
    for i, sub in enumerate(sd['subtopics'], 1):
        sub_id = f"sub-{i}"
        chart_labels.append(sub['name'])
        chart_data.append(sub['count'])
        
        q_cards = []
        for q in sub['questions']:
            opts_html = render_options_with_answer(q, meta['color'])
            
            shift_text = ''  # Shift info not in v3
            q_cards.append(f"""<div class="question-card">
  <div class="question-header">
    <span class="question-num">Q.{q['qno']}</span>
    <span class="question-shift">{esc(shift_text)}</span>
  </div>
  <div class="question-text">{esc(q['question'])}</div>
  {opts_html}
</div>""")
        
        questions_html = '\n'.join(q_cards)
        expanded_class = 'expanded' if i <= 3 else ''
        
        # Sub-topic header shows answer count if available
        answer_info = f" · {sub['with_answer']} with answers" if sub.get('with_answer', 0) > 0 else ""
        
        subtopic_sections.append(f"""<div class="subtopic-section {expanded_class}" id="{sub_id}" style="--subject-color: {meta['color']};">
  <div class="subtopic-header" onclick="toggleSubtopic('{sub_id}')">
    <div class="subtopic-title-row">
      <div class="subtopic-number">{i}</div>
      <div class="subtopic-title">{esc(sub['name'])}</div>
    </div>
    <div class="subtopic-meta">
      <span class="subtopic-count">{sub['count']} Qs{answer_info}</span>
      <button class="subtopic-toggle" aria-label="Toggle">▼</button>
    </div>
  </div>
  <div class="subtopic-body">
    {questions_html if questions_html else '<p style="color: var(--text-muted); font-style: italic;">No questions extracted for this sub-topic.</p>'}
  </div>
</div>""")
    
    sections_html = '\n'.join(subtopic_sections)
    
    top_n = 15
    chart_labels_top = chart_labels[:top_n]
    chart_data_top = chart_data[:top_n]
    
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(subject_name)} &middot; GK GS Analysis &middot; SSC CGL 2025</title>
<meta name="description" content="Detailed analysis of {sd['total_questions']} {esc(subject_name)} questions from SSC CGL Tier 1 (2025), broken into {sd['subtopic_count']} sub-topics with full question text, options, and correct answers.">
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
  <p class="section-subtitle">Click any sub-topic to expand and view all its questions. ✓ marks the correct answer where available.</p>

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
    <div class="hero-badge"><span>ℹ️</span> About v2</div>
    <h1>About This Project</h1>
    <p>A data-driven analysis of SSC CGL Tier 1 General Awareness questions, with split sub-topics, better OCR, and LLM-extracted correct answers.</p>
  </div>
</section>

<section class="section">
  <h2 class="section-title">Overview</h2>
  <p style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 1.5rem;">
    This website presents a structured analysis of <strong>{data['metadata']['total_questions']} General Awareness (GK/GS) questions</strong> 
    from the SSC CGL Tier 1 examination held in September-October 2025. Every question has been categorized 
    into one of {data['metadata']['total_subjects']} major subjects and further classified into {data['metadata']['total_subtopics']} 
    sub-topics. For {data['metadata']['has_answers']} questions, the correct answer has been extracted via LLM.
  </p>

  <h2 class="section-title" style="margin-top: 2.5rem;">v2 Improvements (over v1)</h2>
  <ul style="font-size: 1rem; color: var(--text); margin-left: 1.5rem; line-height: 2;">
    <li><strong>Split sub-topics:</strong> "Indian Dance, Music & Performing Arts" was split into <em>Indian Classical Dance Forms</em>, <em>Indian Folk Dances & Martial Arts</em>, <em>Indian Music (Hindustani & Carnatic)</em>, and <em>Indian Musical Instruments</em>.</li>
    <li><strong>Architecture split:</strong> "Temple Architecture & Sculpture" was split into <em>Temple Architecture & Sculpture</em> (Hindu/Buddhist/Jain), <em>Indo-Islamic Architecture</em> (Mughal/Sultanate), and <em>Modern Architecture & Monuments</em>.</li>
    <li><strong>Better OCR:</strong> Used <strong>Gemini / z-ai Vision (VLM)</strong> for high-accuracy English-only extraction. Hindi text is properly skipped. Improved Tesseract with strict English filtering is used as fallback when VLM is rate-limited.</li>
    <li><strong>Correct answers:</strong> Used <strong>z-ai chat (LLM)</strong> to identify the correct option (A/B/C/D) for each question, plus a brief explanation. (Answer extraction is ongoing - more answers are being added.)</li>
    <li><strong>New sub-topic:</strong> Added <em>New Criminal Laws (BNS, BNSS, BSA)</em> under Polity, since 2025 SSC papers ask heavily about these.</li>
    <li><strong>GitHub Actions workflow:</strong> The OCR pipeline is reproducible — see <code>.github/workflows/run_ocr.yml</code> for the Gemini-based OCR workflow, and <code>categorize_with_gemini.py</code> for LLM-based categorization.</li>
  </ul>

  <h2 class="section-title" style="margin-top: 2.5rem;">Methodology</h2>
  <ol style="font-size: 1rem; color: var(--text); margin-left: 1.5rem; line-height: 2;">
    <li><strong>Source PDF:</strong> Official SSC CGL Tier 1 question paper (488 pages, bilingual English/Hindi) downloaded from Google Drive.</li>
    <li><strong>OCR Extraction (v2):</strong> Each page rendered as image and sent to z-ai Vision (VLM) with prompt: "transcribe the English text". VLM naturally skips Hindi/Devanagari script. Failed pages fall back to improved Tesseract with strict English-line filtering.</li>
    <li><strong>Question Parsing:</strong> Custom parser identified Q.No markers, joined multi-line English text, and isolated the 4 options from translated text. Garbled Hindi lines filtered using vowel-ratio + English-word detection.</li>
    <li><strong>Categorization (hybrid):</strong> Each question matched against a refined taxonomy of {data['metadata']['total_subtopics']} sub-topics (with split Dance/Music/Architecture). Keyword-based scoring for bulk, LLM (z-ai chat) for uncategorized questions.</li>
    <li><strong>Answer Extraction:</strong> Each question + 4 options sent to z-ai chat LLM. LLM returns JSON with subject, subtopic, correct_answer (A/B/C/D), and explanation.</li>
    <li><strong>Website Generation:</strong> Static HTML pages generated with interactive Chart.js visualizations, expandable sub-topic sections, and per-question correct-answer highlighting.</li>
  </ol>

  <h2 class="section-title" style="margin-top: 2.5rem;">Taxonomy (Refined v2)</h2>
  <p style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 1rem;">
    The categorization taxonomy covers the standard SSC CGL General Awareness syllabus, with {data['metadata']['total_subtopics']} sub-topics:
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

  <h2 class="section-title" style="margin-top: 2.5rem;">GitHub Actions Workflow</h2>
  <p style="font-size: 1.05rem; color: var(--text-muted); margin-bottom: 1rem;">
    The repo includes a GitHub Actions workflow (<code>.github/workflows/run_ocr.yml</code>) that uses Gemini Flash 
    for high-accuracy OCR. To run it:
  </p>
  <ol style="font-size: 1rem; color: var(--text); margin-left: 1.5rem; line-height: 2;">
    <li>Get a free Gemini API key from <a href="https://aistudio.google.com" target="_blank" style="color: var(--primary);">aistudio.google.com</a></li>
    <li>Add it as a repository secret named <code>GEMINI_API_KEY</code></li>
    <li>Upload your PDF as <code>input.pdf</code> in the repo root</li>
    <li>Go to <strong>Actions</strong> tab → <strong>Gemini OCR Pipeline</strong> → <strong>Run workflow</strong></li>
    <li>Download the <code>extracted-english-text</code> artifact when complete</li>
  </ol>
  <p style="font-size: 1.05rem; color: var(--text-muted); margin-top: 1rem;">
    There's also a <code>categorize.yml</code> workflow that uses Gemini to categorize questions and extract correct answers.
  </p>

  <h2 class="section-title" style="margin-top: 2.5rem;">Important Notes</h2>
  <ul style="font-size: 1rem; color: var(--text); margin-left: 1.5rem; line-height: 2;">
    <li>Only the <strong>English version</strong> of questions is included (Hindi filtered out by VLM/Tesseract).</li>
    <li>OCR quality varies: VLM-extracted pages are cleanest; Tesseract-fallback pages may have minor typos.</li>
    <li>Categorization is <strong>keyword-based + LLM</strong> - more accurate than v1 but still heuristic for some questions.</li>
    <li>Correct answers are extracted by LLM and should be ~95% accurate. Always verify with the official SSC answer key for high-stakes use.</li>
    <li>Questions are deduplicated by Q.No + first 100 chars of question text.</li>
  </ul>
</section>

{footer_html()}

<script src="app.js"></script>
</body>
</html>"""
    return page


def main():
    data = load_data()
    
    index_html = generate_index(data)
    with open(f"{OUT_DIR}/index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"Generated: index.html")
    
    for subject in data['subject_order']:
        if subject not in data['subjects']:
            continue
        fname = SUBJECT_FILES.get(subject, slugify(subject))
        html_content = generate_subject_page(data, subject)
        if html_content:
            with open(f"{OUT_DIR}/{fname}.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Generated: {fname}.html ({data['subjects'][subject]['total_questions']} questions, {data['subjects'][subject]['subtopic_count']} sub-topics)")
    
    about_html = generate_about_page(data)
    with open(f"{OUT_DIR}/about.html", 'w', encoding='utf-8') as f:
        f.write(about_html)
    print(f"Generated: about.html")
    
    print(f"\nAll pages generated in: {OUT_DIR}")


if __name__ == "__main__":
    main()
