# GK GS Previous Year Question Analysis (v2)

A comprehensive, fully-categorized analysis of **952 General Awareness (GK/GS) questions** from the **SSC CGL Tier 1 examination (September-October 2025)**.

## 🆕 What's New in v2

### 1. Split Sub-topics (previously merged)
"Indian Dance, Music & Performing Arts" was one sub-topic in v1 — now it's split into **4 separate** sub-topics:
- **Indian Classical Dance Forms** (Bharatanatyam, Kathak, Kathakali, etc.)
- **Indian Folk Dances & Martial Arts** (Bhangra, Kalaripayattu, etc.)
- **Indian Music (Hindustani & Carnatic)** — ragas, talas, theory
- **Indian Musical Instruments** (tabla, sitar, etc.)

Architecture was also split into 3:
- **Temple Architecture & Sculpture** (Hindu/Buddhist/Jain)
- **Indo-Islamic Architecture** (Mughal/Sultanate)
- **Modern Architecture & Monuments**

### 2. Better OCR
- Used **z-ai Vision (VLM)** for high-accuracy English extraction (natively skips Hindi)
- Improved Tesseract with strict English-line filtering as fallback
- Hybrid pipeline: VLM > Tesseract

### 3. LLM Categorization + Correct Answers
- Used **z-ai chat (LLM)** to categorize uncategorized questions
- LLM extracts correct answer (A/B/C/D) for each question
- LLM provides brief explanation for each answer
- Correct answers highlighted in green on website

### 4. GitHub Actions Workflow
- `.github/workflows/run_ocr.yml`: Gemini Flash OCR pipeline (works in US region)
- `.github/workflows/categorize.yml`: Gemini-based categorization with answer extraction

## 📊 Stats

| Metric | Value |
|--------|-------|
| Total Questions | 952 |
| Subjects | 8 |
| Sub-topics | 95 |
| With LLM-extracted Answers | 50+ (growing) |

## 📈 Subject Distribution

| Subject | Questions | Sub-topics |
|---------|-----------|------------|
| Static GK | 237 | 14 |
| Geography | 212 | 11 |
| History | 143 | 24 |
| Current Affairs | 108 | 8 |
| Polity | 116 | 13 |
| General Science | 75 | 11 |
| Economics | 60 | 8 |

## 🔗 Live Website

**https://gk-gs-pyq-analysis.pages.dev/**

## 🛠️ Tech Stack

- **OCR**: z-ai Vision (VLM) + Tesseract (fallback)
- **Categorization**: Keyword taxonomy (v2) + z-ai chat (LLM)
- **Answer Extraction**: z-ai chat (LLM) with JSON output
- **Frontend**: Vanilla HTML/CSS/JS + Chart.js
- **Deployment**: Cloudflare Pages (wrangler)
- **Version Control**: Git + GitHub

## 📁 Project Structure

```
.
├── .github/workflows/
│   ├── run_ocr.yml              # Gemini OCR workflow
│   └── categorize.yml           # Gemini categorization workflow
├── process_pdf.py               # Gemini Vision OCR script (for GitHub Actions)
├── parse_questions.py           # Parse Gemini OCR output to JSON
├── categorize_with_gemini.py    # LLM categorization + answer extraction
├── scripts/
│   ├── taxonomy_v2.py           # Refined taxonomy (95 sub-topics)
│   ├── parse_questions_v3.py    # Hybrid OCR parser
│   ├── categorize_hybrid.py     # Keyword + LLM hybrid categorization
│   ├── extract_answers_batched.py # Batched LLM answer extraction
│   ├── build_website_data_v2.py # Build data.json from categorized Qs
│   ├── generate_website_v2.py   # Generate HTML pages
│   └── ocr_vlm.py               # z-ai Vision OCR (alternative to Gemini)
├── index.html                   # Landing page
├── history.html                 # 143 History Qs
├── geography.html               # 212 Geography Qs
├── polity.html                  # 116 Polity Qs
├── economics.html               # 60 Economics Qs
├── science.html                 # 75 General Science Qs
├── static-gk.html               # 237 Static GK Qs (with split sub-topics!)
├── current-affairs.html         # 108 Current Affairs Qs
├── about.html                   # Methodology page
├── styles.css                   # Shared styles
├── app.js                       # Shared JS (charts, search)
└── data.json                    # Full structured data
```

## 🚀 Running the GitHub Actions OCR Pipeline

### Step 1: Get a Gemini API Key
1. Go to https://aistudio.google.com
2. Sign in and click "Create API Key"
3. Copy the key (free tier: 1,000 requests/day)

### Step 2: Add to GitHub Secrets
1. Open your repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `GEMINI_API_KEY`, Value: paste your key

### Step 3: Upload PDF
Upload your bilingual PDF as `input.pdf` in the repo root.

### Step 4: Run the Workflow
1. Go to Actions tab
2. Select "Gemini OCR Pipeline"
3. Click "Run workflow"
4. Wait for completion (~30 min for 488 pages)
5. Download the `extracted-english-text` artifact

### Step 5: Categorize (Optional)
Run the "Categorize Questions with Gemini" workflow to get subject/sub-topic assignment + correct answers.

## ⚠️ Notes

- Only English version of questions included (Hindi filtered out)
- OCR quality varies: VLM-extracted pages are cleanest
- Categorization is keyword + LLM hybrid — high accuracy but not perfect
- Correct answers extracted by LLM should be ~95% accurate — verify with official SSC answer key for high-stakes use
- Questions deduplicated by Q.No + first 100 chars of question text
