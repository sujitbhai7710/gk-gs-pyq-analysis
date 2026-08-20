#!/usr/bin/env python3
"""
Re-parse OCR text to extract missing options.
Many "problematic" questions actually have all 4 options in the source OCR
but the parser missed them. This script re-extracts options from raw OCR.

Strategy:
1. For each problematic question, look at the source OCR page
2. Find the Q.No marker, then extract ALL lines until the next Q.No
3. Filter to English-only lines
4. Identify the 4 options (short lines after the question)
"""
import os
import re
import sys
import json
import glob

OCR_DIR = "/home/z/my-project/data/ocr_merged"
INPUT = "/home/z/my-project/data/categorized_v3.json"
OUTPUT = "/home/z/my-project/data/categorized_v4.json"


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
    words = re.findall(r'[a-zA-Z]+', line)
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
    if len(words) <= 8 and vowel_ratio >= 0.25:
        cap_words = [w for w in words if w[0].isupper()]
        if len(cap_words) >= 1:
            # Check for garbled patterns
            max_consec_cons = 0
            current = 0
            for c in line.lower():
                if c.isalpha() and c not in 'aeiou':
                    current += 1
                    max_consec_cons = max(max_consec_cons, current)
                else:
                    current = 0
            if max_consec_cons <= 5:
                return True
    return False


def extract_all_text_for_qno(page_text, target_qno):
    """Extract all text between Q.No: target_qno and the next Q.No."""
    lines = page_text.split('\n')
    q_pattern = re.compile(r'^[QO]\.?\s*No\s*[:\-]?\s*(\d+)', re.IGNORECASE)
    
    capturing = False
    collected_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('[SOURCE:'):
            continue
        m = q_pattern.match(stripped)
        if m:
            qnum = int(m.group(1))
            if qnum == target_qno:
                capturing = True
                # Add the rest of the line after Q.No: N
                rest = stripped[m.end():].strip()
                rest = re.sub(r'^[\s:\-]+', '', rest)
                if rest:
                    collected_lines.append(rest)
                continue
            elif capturing:
                # Next question started
                break
        elif capturing:
            if not stripped:
                continue
            if stripped == 'Not Answered':
                continue
            if 'XamToppr' in stripped or 'www.' in stripped:
                continue
            if 'cbexams.com' in stripped:
                continue
            if stripped.startswith('Click Here'):
                continue
            collected_lines.append(stripped)
    
    return collected_lines


def split_question_and_options_better(lines):
    """Better splitter: identify options as the last 4 short non-question lines."""
    if not lines:
        return '', []
    
    # Filter to English only
    english_lines = [l for l in lines if is_english_line(l)]
    if not english_lines:
        return '', []
    
    # Classify each line
    line_types = []  # 'question', 'option', 'statement'
    for line in english_lines:
        ltype = 'option'  # default
        if len(line) > 250:
            ltype = 'question'
        elif line.endswith('?') or line.endswith(':'):
            ltype = 'question'
        elif line.startswith('Assertion') or line.startswith('Reason'):
            ltype = 'question'
        elif line.startswith('Statement'):
            ltype = 'statement'
        elif line.lower().startswith(('consider the following', 'read the', 'which of', 'fill in', 'according to')):
            ltype = 'question'
        elif line.lower().startswith('in ') and len(line) > 80:
            ltype = 'question'
        elif re.match(r'^\d+\)', line) or re.match(r'^\d+\.', line):
            ltype = 'statement'
        line_types.append(ltype)
    
    # Find the last contiguous block of option-like lines (length 3-5)
    # Scan from end
    option_start = len(english_lines)
    option_count = 0
    for i in range(len(english_lines)-1, -1, -1):
        if line_types[i] == 'option':
            option_start = i
            option_count += 1
            if option_count >= 4:
                break
        else:
            if option_count >= 3:
                # We have at least 3 options, stop here
                break
            option_start = len(english_lines)
            option_count = 0
    
    if option_count < 2:
        # Couldn't find options - try taking last 4 lines
        if len(english_lines) >= 4:
            option_start = len(english_lines) - 4
        else:
            option_start = len(english_lines)
    
    option_block = english_lines[option_start:]
    question_lines = english_lines[:option_start]
    
    # Clean options
    options = []
    for opt in option_block:
        opt = opt.strip()
        if opt and 3 <= len(opt) <= 300:
            options.append(opt)
    
    # Take exactly 4
    if len(options) > 4:
        options = options[-4:]
    
    question_text = ' '.join(question_lines).strip()
    return question_text, options


def main():
    with open(INPUT, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Loaded {len(questions)} questions")
    
    # Find problematic questions
    from cleanup_questions import is_question_problematic
    problematic_indices = []
    for i, q in enumerate(questions):
        if is_question_problematic(q):
            problematic_indices.append(i)
    
    print(f"Problematic: {len(problematic_indices)}")
    
    # For each problematic question, try to re-parse from OCR
    fixed = 0
    still_bad = 0
    
    for idx in problematic_indices:
        q = questions[idx]
        page_num = q.get('page', 0)
        qno = q.get('qno', 0)
        
        # Load OCR for this page
        ocr_path = f"{OCR_DIR}/page_{page_num:04d}.txt"
        if not os.path.exists(ocr_path):
            still_bad += 1
            continue
        
        with open(ocr_path, 'r', encoding='utf-8') as f:
            page_text = f.read()
        
        # Extract all lines for this Q.No
        all_lines = extract_all_text_for_qno(page_text, qno)
        
        # Re-parse
        new_qtext, new_opts = split_question_and_options_better(all_lines)
        
        # Check if new parse is better
        if len(new_opts) == 4 and all(3 <= len(o) <= 250 for o in new_opts):
            # Better! Use new parse
            if new_qtext and len(new_qtext) > len(q.get('question', '')):
                q['question'] = new_qtext
            q['options'] = new_opts
            q['reparsed'] = True
            fixed += 1
        elif len(new_opts) > len(q.get('options', [])):
            # Partial improvement
            q['options'] = new_opts
            q['reparsed'] = True
            fixed += 1
        else:
            still_bad += 1
    
    print(f"Fixed by re-parsing: {fixed}")
    print(f"Still problematic: {still_bad}")
    
    # Save
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    # Final stats
    prob_after = sum(1 for q in questions if is_question_problematic(q))
    print(f"\nProblematic before: {len(problematic_indices)}")
    print(f"Problematic after: {prob_after}")
    print(f"Saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
