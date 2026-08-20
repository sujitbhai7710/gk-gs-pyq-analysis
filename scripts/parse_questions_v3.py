#!/usr/bin/env python3
"""
Parse merged OCR output into structured questions.
Uses improved parser that handles both VLM and Tesseract output formats.
"""
import os
import re
import sys
import json
import glob

OCR_DIR = "/home/z/my-project/data/ocr_merged"
OUTPUT = "/home/z/my-project/data/questions_v3.json"


def extract_questions_from_page(page_num, text):
    """Extract questions from a single page's text."""
    lines = text.split('\n')
    
    questions = []
    current_q = None
    q_pattern = re.compile(r'^[QO]\.?\s*No\s*[:\-]?\s*(\d+)', re.IGNORECASE)
    
    for line in lines:
        stripped = line.strip()
        # Skip source header
        if stripped.startswith('[SOURCE:'):
            continue
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


def is_english_line(line):
    """Check if a line is English (vs Hindi garbled)."""
    if not line or len(line.strip()) < 2:
        return False
    line = line.strip()
    # Reject if contains Devanagari
    for c in line:
        if '\u0900' <= c <= '\u097F':
            return False
    ascii_chars = sum(1 for c in line if ord(c) < 128)
    if len(line) > 0 and ascii_chars / len(line) < 0.95:
        return False
    words = re.findall(r'[a-zA-Z]{2,}', line)
    if not words:
        return False
    letters = [c for c in line.lower() if c.isalpha()]
    if not letters:
        return False
    vowels = sum(1 for c in letters if c in 'aeiou')
    vowel_ratio = vowels / len(letters)
    
    ENGLISH_WORDS = set("the is are was were be been being am a an of in on at to for from by with as into through during before after above below up down out off over under again further then once here there when where why how all any both each few more most other some such no nor not only own same so than too very can will just should now and or but if because until while about against between within without which who whom whose what this that these those i you he she it we they them his her its our their my your his hers ours theirs me him us has had have do does did doing would should could ought may might must shall will can cannot king kingdom dynasty empire war battle treaty policy act amendment constitution parliament president prime minister governor general assembly council court state country city river mountain sea ocean lake desert forest capital science physics chemistry biology botany zoology geology astronomy history geography polity economics india indian world global national international federal unitary central state local government music dance festival temple architecture sculpture painting literature book author poet poetry which following statements correct incorrect considered according given below above about with from into first second third fourth option pair matched related associated founded established started introduced person place name type kind category group belongs known called defined describes reflects refers read consider fill blank choose find select identify explain describe only both neither either none all true false correct wrong answered who whom whose which what where when why how many much long far high low according based following given below read consider".split())
    
    word_set = set(w.lower() for w in words)
    common_count = sum(1 for w in word_set if w in ENGLISH_WORDS)
    STRONG_ENGLISH = set("the is are was were a an of in on at to for from by with and or but if when where which who whom what this that these those he she it we they them his her its their my your has had have do does did can will should would could about into through during".split())
    strong_count = sum(1 for w in word_set if w in STRONG_ENGLISH)
    
    if strong_count >= 1:
        return True
    if common_count >= 1 and vowel_ratio >= 0.25:
        return True
    if len(words) <= 6 and vowel_ratio >= 0.25:
        cap_words = [w for w in words if w[0].isupper()]
        if len(cap_words) >= 1:
            max_consec_cons = 0
            current = 0
            for c in line.lower():
                if c.isalpha() and c not in 'aeiou':
                    current += 1
                    max_consec_cons = max(max_consec_cons, current)
                else:
                    current = 0
            if max_consec_cons <= 4:
                return True
    return False


def split_question_and_options(q):
    """Split question lines into question text and 4 options.
    
    Improved: filters out Hindi/garbled lines first, then identifies options.
    """
    if not q['lines']:
        return '', []
    
    # Filter to English-only lines
    english_lines = []
    for line in q['lines']:
        if is_english_line(line):
            english_lines.append(line)
    
    if not english_lines:
        return '', []
    
    # Identify option-like lines
    line_types = []
    for line in english_lines:
        is_option = True
        if len(line) > 250:
            is_option = False
        if line.endswith('?') or line.endswith(':'):
            is_option = False
        if line.startswith('Assertion') or line.startswith('Reason'):
            is_option = False
        if line.startswith('Statement'):
            is_option = False
        if line.lower().startswith(('consider the following', 'read the', 'which of', 'fill in', 'according to')):
            is_option = False
        if line.lower().startswith('in ') and len(line) > 80:
            is_option = False
        line_types.append(is_option)
    
    # Find last contiguous option block
    option_start = len(english_lines)
    for i in range(len(english_lines)-1, -1, -1):
        if line_types[i]:
            option_start = i
        else:
            break
    
    option_block = english_lines[option_start:]
    
    if len(option_block) < 2 or len(option_block) > 6:
        if len(english_lines) >= 4:
            candidate = english_lines[-4:]
            if all(len(c) < 250 and not c.endswith('?') and not c.endswith(':') for c in candidate):
                option_start = len(english_lines) - 4
                option_block = candidate
    
    question_lines = english_lines[:option_start]
    question_text = ' '.join(question_lines).strip()
    
    options = [opt.strip() for opt in option_block if opt.strip() and len(opt.strip()) <= 300]
    
    return question_text, options


def main():
    page_files = sorted(glob.glob(f"{OCR_DIR}/page_*.txt"))
    print(f"Found {len(page_files)} OCR'd pages")
    
    all_questions = []
    
    for pf in page_files:
        page_num = int(re.search(r'page_(\d+)', pf).group(1))
        with open(pf, 'r', encoding='utf-8') as f:
            text = f.read()
        
        questions = extract_questions_from_page(page_num, text)
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
        if not qtext or len(qtext) < 20:
            continue
        key = (q['qno'], qtext)
        if key in seen:
            continue
        seen.add(key)
        unique.append(q)
    
    print(f"After dedup: {len(unique)} unique questions")
    
    # Stats
    no_opts = sum(1 for q in unique if not q.get('options'))
    print(f"Questions with no options: {no_opts}")
    has_4_opts = sum(1 for q in unique if len(q.get('options', [])) == 4)
    print(f"Questions with 4 options: {has_4_opts}")
    
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to: {OUTPUT}")


if __name__ == "__main__":
    main()
