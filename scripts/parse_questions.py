#!/usr/bin/env python3
"""
Improved parser - better English/Hindi filtering and option extraction.
"""
import os
import re
import json
import glob

OCR_DIR = "/home/z/my-project/data/ocr_pages"
OUTPUT = "/home/z/my-project/data/all_questions.json"

# Common English words - if a line contains one of these AND has reasonable
# vowel ratio, it's likely English
ENGLISH_WORDS = set("""
the is are was were be been being am a an of in on at to for from by with as into through during before after
above below up down out off over under again further then once here there when where why how all any both each
few more most other some such no nor not only own same so than too very can will just should now and or but if
because until while about against between within without which who whom whose what this that these those i you
he she it we they them his her its our their my your his hers ours theirs me him us
has had have do does did doing would should could ought may might must shall will can cannot
king kingdom dynasty empire war battle treaty policy act amendment constitution parliament president prime minister
governor general assembly council court state country city river mountain sea ocean lake desert forest capital
science physics chemistry biology botany zoology geology astronomy history geography polity economics
india indian world global national international federal unitary central state local government
music dance festival temple architecture sculpture painting literature book author poet poetry
which following statements correct incorrect considered according given below above about with from into
first second third fourth option pair matched related associated founded established started introduced
person place name type kind category group belongs known called defined describes reflects refers
read consider fill blank choose find select identify explain describe
only both neither either none all true false correct wrong answered
indus valley civilization vedic age mahajanapadas buddhism jainism mauryan gupta mughal delhi sultanate
vijayanagara bahmani maratha sikh bhakti sufi british europeans revolt reform congress gandhian independence
physical indian climate rivers soils agriculture minerals transport world map environmental
making features fundamental rights duties directive principles union parliament judiciary bodies
federalism local amendments political parties welfare
basics banking public inflation money international agriculture population
physics chemistry biology cell plant human health ecology
books authors awards sports festivals dance music temple paintings days organizations symbols railways space
national international economy sports awards persons defence reports
""".split())

# Strong English indicators (very common words that almost always indicate English)
STRONG_ENGLISH = set("the is are was were a an of in on at to for from by with and or but if when where which who whom what this that these those he she it we they them his her its their my your has had have do does did can will should would could about into through during".split())

def is_english_line(line):
    """Determine if a line is proper English (vs garbled Hindi OCR)."""
    line = line.strip()
    if not line or len(line) < 2:
        return False
    
    # Skip lines with too many non-ASCII chars
    ascii_chars = sum(1 for c in line if ord(c) < 128)
    if len(line) > 0 and ascii_chars / len(line) < 0.95:
        return False
    
    # Get words
    words = re.findall(r'[a-zA-Z]+', line)
    if len(words) == 0:
        return False
    
    # Vowel ratio check
    letters = [c for c in line.lower() if c.isalpha()]
    if len(letters) == 0:
        return False
    vowels = sum(1 for c in letters if c in 'aeiou')
    vowel_ratio = vowels / len(letters)
    
    # Check for strong English words
    word_set = set(w.lower() for w in words)
    strong_count = sum(1 for w in word_set if w in STRONG_ENGLISH)
    common_count = sum(1 for w in word_set if w in ENGLISH_WORDS)
    
    # Strong English indicator: at least one strong English word
    if strong_count >= 1:
        return True
    
    # Common English words (less common)
    if common_count >= 1 and vowel_ratio >= 0.2:
        return True
    
    # For short lines (likely options like "Tokyo", "Tishra"), check:
    # - 1-4 words
    # - Each word starts with capital OR is all lowercase alphabetic
    # - Reasonable vowel ratio
    if len(words) <= 6 and vowel_ratio >= 0.25:
        # Check if it looks like a list of proper nouns or technical terms
        cap_words = [w for w in words if w[0].isupper()]
        if len(cap_words) >= 1 and len(words) <= 4:
            # Check for garbled patterns: random letter combinations
            # Garbled text often has unusual bigrams like 'aa', 'ee', etc.
            unusual = 0
            for i in range(len(line)-1):
                if line[i:i+2].lower() in ('aa', 'uu', 'ii') and i > 0 and not line[i-1].isupper():
                    unusual += 1
            if unusual > 2:
                return False
            return True
    
    # Garbled text - return False
    return False


def extract_questions_from_page(text):
    """Extract questions from a single page's OCR text."""
    lines = text.split('\n')
    
    questions = []
    current_q = None
    q_pattern = re.compile(r'^[QO]\.?\s*No\s*[:\-]?\s*(\d+)', re.IGNORECASE)
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = q_pattern.match(stripped)
        if m:
            if current_q:
                questions.append(current_q)
            
            qnum = int(m.group(1))
            rest = stripped[m.end():].strip()
            # Remove leading colons/spacing
            rest = re.sub(r'^[\s:\-]+', '', rest)
            
            current_q = {
                'qno': qnum,
                'all_lines': [rest] if rest else [],
                'english_lines': [],
                'answered': True,
            }
        elif current_q is not None:
            if not stripped:
                continue
            if stripped == 'Not Answered':
                current_q['answered'] = False
                continue
            if stripped.startswith('www.') or stripped.startswith('https://'):
                continue
            if stripped.startswith('Click Here'):
                continue
            if 'cbexams.com' in stripped and len(stripped) < 200:
                continue
            current_q['all_lines'].append(stripped)
    
    if current_q:
        questions.append(current_q)
    
    # Filter English lines
    for q in questions:
        for line in q['all_lines']:
            if is_english_line(line):
                q['english_lines'].append(line)
    
    return questions


def split_question_and_options(q):
    """Split english_lines into question text and options.
    
    Strategy: 
    1. Identify option-like lines (short, no ? or :, often capitalized)
    2. The last contiguous block of 3-5 short lines = options
    3. Everything before = question
    """
    if not q['english_lines']:
        return '', []
    
    lines = [l.strip() for l in q['english_lines'] if l.strip()]
    if not lines:
        return '', []
    
    # Classify each line as option-like or question-like
    # Option-like: short (<120 chars), doesn't end with ? or :,
    # doesn't start with "Assertion" or "Reason" or "Statement"
    line_types = []
    for i, line in enumerate(lines):
        is_option = True
        if len(line) > 150:
            is_option = False
        if line.endswith('?'):
            is_option = False
        if line.endswith(':'):
            is_option = False
        if line.startswith('Assertion'):
            is_option = False
        if line.startswith('Reason'):
            is_option = False
        if line.startswith('Statement'):
            is_option = False
        if line.lower().startswith('consider the following'):
            is_option = False
        if line.lower().startswith('read the'):
            is_option = False
        if line.lower().startswith('which of'):
            is_option = False
        if line.lower().startswith('fill in'):
            is_option = False
        if line.lower().startswith('in '):
            # Could be question continuation like "In Carnatic music..."
            # Only treat as option if very short
            if len(line) > 80:
                is_option = False
        line_types.append(is_option)
    
    # Find the last contiguous block of option-like lines
    # Scan from end, find the first non-option line
    option_start = len(lines)
    for i in range(len(lines)-1, -1, -1):
        if line_types[i]:
            option_start = i
        else:
            break
    
    # Now check: is the option block at least 2 lines and at most 6?
    option_block = lines[option_start:]
    if len(option_block) < 2 or len(option_block) > 6:
        # Try a different heuristic: take last 4 lines
        # But only if they look like options
        if len(lines) >= 4:
            candidate = lines[-4:]
            if all(len(c) < 150 and not c.endswith('?') and not c.endswith(':') for c in candidate):
                option_start = len(lines) - 4
                option_block = candidate
            else:
                # Just take whatever option-like lines exist
                option_indices = [i for i, t in enumerate(line_types) if t]
                if option_indices:
                    # Find contiguous block at end
                    last_idx = option_indices[-1]
                    first_in_block = last_idx
                    for j in range(last_idx, -1, -1):
                        if line_types[j]:
                            first_in_block = j
                        else:
                            break
                    option_start = first_in_block
                    option_block = lines[option_start:]
                else:
                    option_start = len(lines)
                    option_block = []
    
    question_lines = lines[:option_start]
    option_lines = option_block
    
    # Clean up options
    clean_options = []
    for opt in option_lines:
        opt = opt.strip()
        if opt and len(opt) <= 200:
            clean_options.append(opt)
    
    question_text = ' '.join(question_lines).strip()
    return question_text, clean_options


def main():
    page_files = sorted(glob.glob(f"{OCR_DIR}/page_*.txt"))
    print(f"Found {len(page_files)} OCR'd pages")
    
    all_questions = []
    shift_count = 0
    current_shift = None
    
    for pf in page_files:
        page_num = int(re.search(r'page_(\d+)', pf).group(1))
        with open(pf, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Detect shift boundaries
        shift_match = re.search(r'Shift[-\s]*(\d+)', text)
        date_match = re.search(r'Test Date\s*:\s*([\d/\-]+\s+\w+\s+\d+)', text)
        time_match = re.search(r'Test Time and Shift\s*:\s*([^\n]+)', text)
        
        if shift_match and date_match:
            time_str = time_match.group(1).strip() if time_match else ''
            shift_id = f"Shift {shift_match.group(1)} - {date_match.group(1)} {time_str}"
            current_shift = shift_id
        
        questions = extract_questions_from_page(text)
        for q in questions:
            q['page'] = page_num
            q['shift'] = current_shift or f"Shift {shift_count}"
            qtext, opts = split_question_and_options(q)
            q['question'] = qtext
            q['options_list'] = opts
            # Clean up
            del q['all_lines']
            all_questions.append(q)
    
    print(f"Total raw questions extracted: {len(all_questions)}")
    
    # Deduplicate by (qno, question text first 100 chars)
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
    
    print(f"After dedup (with non-empty question): {len(unique)}")
    
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
