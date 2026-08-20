# GK GS Previous Year Question Analysis

A comprehensive, fully-categorized analysis of **965 General Awareness (GK/GS) questions** from the **SSC CGL Tier 1 examination (September-October 2025)**.

## 📊 What's Inside

- **965 unique questions** extracted from official SSC CGL Tier 1 papers
- **8 major subjects** (History, Geography, Polity, Economics, General Science, Static GK, Current Affairs)
- **82 sub-topics** (e.g., Mauryan Empire, Mughal Empire, Indian Dance Forms, Festivals, Banking, etc.)
- Each question preserved with full text and 4 options
- Interactive charts for visual analysis
- Searchable, expandable sub-topic sections

## 🎯 Subjects Covered

| Subject | Questions | Sub-topics |
|---------|-----------|------------|
| History | 209 | 25 |
| Geography | 199 | 11 |
| Static GK | 187 | 8 |
| Polity | 116 | 12 |
| Current Affairs | 105 | 7 |
| General Science | 74 | 11 |
| Economics | 63 | 7 |

## 📁 Project Structure

```
website/
├── index.html              # Landing page with overview & charts
├── history.html            # History subject page (209 Qs)
├── geography.html          # Geography page (199 Qs)
├── polity.html             # Polity page (116 Qs)
├── economics.html          # Economics page (63 Qs)
├── science.html            # General Science page (74 Qs)
├── static-gk.html          # Static GK page (187 Qs)
├── current-affairs.html    # Current Affairs page (105 Qs)
├── uncategorized.html      # Uncategorized (12 Qs)
├── about.html              # About / methodology
├── styles.css              # Shared styles
├── app.js                  # Shared JS (charts, search, expand/collapse)
└── data.json               # Full structured data (965 Qs)
```

## 🔧 How It Was Built

1. **Source PDF**: Official SSC CGL Tier 1 question paper (488 pages, bilingual)
2. **OCR**: Tesseract OCR (English) on each page rendered at 150 DPI
3. **Parsing**: Custom Python parser extracted Q.No, English question text, and 4 options
4. **Categorization**: Keyword-based taxonomy matching across 82 sub-topics
5. **Website Generation**: Python script generates static HTML from JSON data

## 🚀 Deployment

Static site deployed on Cloudflare Pages.

## ⚠️ Notes

- Only English version of questions is included (Hindi filtered out)
- OCR may introduce minor typos in question text
- Categorization is heuristic - a small percentage may be misclassified
- Questions are deduplicated by Q.No + first 100 chars of question text

## 📜 License

For educational purposes only. Original question papers © SSC.
