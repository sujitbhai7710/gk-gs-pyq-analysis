"""
Parse Gemini OCR output (final_output.txt) into structured JSON of questions.

Each question has:
    - qno: int
    - question: str (English text only)
    - options: list[str] (4 options)
    - answered: bool (False if "Not Answered")
    - page: int
    - shift: str (exam shift info, if detected)

Usage:
    python parse_questions.py [final_output.txt] [questions.json]
"""
import os
import re
import sys
import json

INPUT = sys.argv[1] if len(sys.argv) > 1 else "final_output.txt"
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else "questions.json"


def parse_pages(text):
    """Split text into pages using --- PAGE N --- markers."""
    pages = {}
    # Match "--- PAGE 12 ---" or "--- PAGE 12 [FAILED...] ---"
    pattern = re.compile(r'^---\s*PAGE\s+(\d+)(?:\s*\[[^\]]*\])?\s*---\s*$', re.MULTILINE)
    
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        page_num = int(m.group(1))
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        page_text = text[start:end].strip()
        pages[page_num] = page_text
    
    return pages


def extract_questions_from_page(page_num, page_text):
    """Extract questions from a single page's text."""
    lines = page_text.split('\n')
    
    questions = []
    current_q = None
    q_pattern = re.compile(r'^[QO]\.?\s*No\s*[:\-]?\s*(\d+)', re.IGNORECASE)
    
    for line in lines:
        stripped = line.strip()
        m = q_pattern.match(stripped)
        if m:
            if current_q:
                questions.append(current_q)
            
            qnum = int(m.group(1))
            rest = stripped[m.end():].strip()
            rest = re.sub(r'^[\s:\-]+', '', rest)
            
            current_q = {
                'qno': qnum,
                'page': page_num,
                'lines': [rest] if rest else [],
                'answered': True,
            }
        elif current_q is not None:
            if not stripped:
                continue
            if stripped == 'Not Answered':
                current_q['answered'] = False
                continue
            if 'XamToppr' in stripped or 'www.' in stripped:
                continue
            if 'cbexams.com' in stripped:
                continue
            if stripped.startswith('Click Here'):
                continue
            current_q['lines'].append(stripped)
    
    if current_q:
        questions.append(current_q)
    
    return questions


def split_question_and_options(q):
    """Split question lines into question text and 4 options."""
    lines = q['lines']
    if not lines:
        return '', []
    
    # Identify option-like lines
    line_types = []
    for line in lines:
        is_option = True
        if len(line) > 200:
            is_option = False
        if line.endswith('?') or line.endswith(':'):
            is_option = False
        if line.startswith('Assertion') or line.startswith('Reason'):
            is_option = False
        if line.startswith('Statement'):
            is_option = False
        if line.lower().startswith(('consider the following', 'read the', 'which of', 'fill in', 'in ', 'according to')):
            is_option = False
        line_types.append(is_option)
    
    # Find last contiguous option block
    option_start = len(lines)
    for i in range(len(lines)-1, -1, -1):
        if line_types[i]:
            option_start = i
        else:
            break
    
    option_block = lines[option_start:]
    
    if len(option_block) < 2 or len(option_block) > 6:
        if len(lines) >= 4:
            candidate = lines[-4:]
            if all(len(c) < 200 and not c.endswith('?') and not c.endswith(':') for c in candidate):
                option_start = len(lines) - 4
                option_block = candidate
    
    question_lines = lines[:option_start]
    question_text = ' '.join(question_lines).strip()
    
    # Clean options
    options = [opt.strip() for opt in option_block if opt.strip() and len(opt.strip()) <= 250]
    
    return question_text, options


def main():
    if not os.path.exists(INPUT):
        print(f"ERROR: {INPUT} not found")
        sys.exit(1)
    
    with open(INPUT, 'r', encoding='utf-8') as f:
        text = f.read()
    
    pages = parse_pages(text)
    print(f"Parsed {len(pages)} pages")
    
    all_questions = []
    for page_num in sorted(pages.keys()):
        page_text = pages[page_num]
        questions = extract_questions_from_page(page_num, page_text)
        for q in questions:
            qtext, opts = split_question_and_options(q)
            q['question'] = qtext
            q['options'] = opts
            del q['lines']
            all_questions.append(q)
    
    print(f"Extracted {len(all_questions)} raw questions")
    
    # Dedupe by (qno, first 100 chars of question)
    seen = set()
    unique = []
    for q in all_questions:
        qtext = q['question'].strip()[:100]
        if not qtext:
            continue
        key = (q['qno'], qtext)
        if key in seen:
            continue
        seen.add(key)
        unique.append(q)
    
    print(f"After dedup: {len(unique)} unique questions")
    
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
