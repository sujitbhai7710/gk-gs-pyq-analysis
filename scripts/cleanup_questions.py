#!/usr/bin/env python3
"""
Clean up problematic questions using LLM.

For each question with <4 options or weird/short options:
1. Send the question text + existing (broken) options to LLM
2. LLM returns the 4 correct options for this SSC CGL question
3. Also re-cleans the question text if needed

Saves progress every 5 questions to handle rate limits.
"""
import json
import os
import sys
import time
import subprocess
import re

INPUT = "/home/z/my-project/data/categorized_v4.json"
PROGRESS_FILE = "/home/z/my-project/data/cleanup_progress_v4.json"


def call_zai_chat(prompt, max_retries=3):
    """Call z-ai chat with retry on rate limit."""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['z-ai', 'chat', '--prompt', prompt, '--output', '/tmp/chat_clean.json'],
                capture_output=True, text=True, timeout=90
            )
            if result.returncode != 0:
                stderr = result.stderr or ''
                if '429' in stderr:
                    wait_times = [60, 180, 600]
                    wait = wait_times[min(attempt, len(wait_times)-1)]
                    print(f"    [429, wait {wait}s]", flush=True)
                    time.sleep(wait)
                    continue
                time.sleep(10)
                continue
            with open('/tmp/chat_clean.json', 'r') as f:
                data = json.load(f)
            choices = data.get('choices', [])
            if choices:
                return choices[0].get('message', {}).get('content', '').strip()
        except:
            time.sleep(5)
    return None


def parse_json_response(text):
    if not text:
        return None
    text = text.strip()
    if text.startswith('```'):
        lines = text.split('\n')
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        text = '\n'.join(lines)
    # Try JSON parse
    try:
        return json.loads(text)
    except:
        pass
    # Find JSON object
    m = re.search(r'\{[^{}]*\}', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except:
            pass
    return None


def is_option_garbled(opt):
    """Check if an option looks garbled or too short."""
    if not opt or len(opt) < 4:
        return True
    if len(opt) > 250:
        return True
    # Check vowel ratio
    letters = [c for c in opt.lower() if c.isalpha()]
    if not letters:
        return True
    vowels = sum(1 for c in letters if c in 'aeiou')
    vr = vowels / len(letters)
    if vr < 0.15:
        return True
    return False


def is_question_problematic(q):
    """Check if a question needs cleanup."""
    opts = q.get('options', [])
    if len(opts) != 4:
        return True
    for opt in opts:
        if is_option_garbled(opt):
            return True
    return False


def clean_question_with_llm(q):
    """Use LLM to re-extract clean question text + 4 valid options."""
    qtext = q.get('question', '').strip()
    bad_opts = q.get('options', [])
    
    # Build context with what we have
    opts_text = ""
    letters = ['A', 'B', 'C', 'D']
    for i, opt in enumerate(bad_opts[:4]):
        letter = letters[i] if i < len(letters) else str(i+1)
        opts_text += f"{letter}. {opt}\n"
    if not opts_text:
        opts_text = "(no options extracted - OCR failed)"
    
    prompt = f"""You are an expert at SSC CGL General Awareness questions. I have a question with broken/incomplete options (OCR errors). Reconstruct the 4 correct options.

QUESTION TEXT (may be incomplete):
{qtext}

EXISTING OPTIONS (some may be garbled or missing):
{opts_text}

Based on the question topic and any partial options, provide the 4 correct multiple-choice options that SSC would typically use for this question. The options should be:
- 4 distinct, plausible options (one correct + 3 distractors)
- Each option 5-150 characters
- Real, factual content (not made up)
- Match SSC CGL exam style

Return ONLY a JSON object (no other text, no markdown):
{{"question": "<cleaned complete question text>", "options": ["opt1", "opt2", "opt3", "opt4"], "correct_answer": "<A/B/C/D>", "explanation": "<1 sentence>"}}

If the question text is already complete, return it as-is. If you can identify the correct answer, include it."""
    
    response = call_zai_chat(prompt)
    if not response:
        return None
    return parse_json_response(response)


def main():
    with open(INPUT, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # Find all problematic questions
    problematic = [(i, q) for i, q in enumerate(questions) if is_question_problematic(q)]
    print(f"Loaded {len(questions)} questions", flush=True)
    print(f"Problematic: {len(problematic)}", flush=True)
    
    if not problematic:
        print("All questions are clean!")
        return
    
    # Load progress
    cleaned_indices = set()
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE) as f:
                cleaned_questions = json.load(f)
            # Mark already-cleaned questions
            for cq in cleaned_questions:
                if 'original_qno' in cq and 'original_page' in cq:
                    cleaned_indices.add((cq.get('original_qno'), cq.get('original_page')))
            print(f"Already cleaned: {len(cleaned_indices)}")
        except:
            cleaned_questions = []
    else:
        cleaned_questions = []
    
    # Process each problematic question
    completed = 0
    failed = 0
    start = time.time()
    save_counter = 0
    
    for idx, (i, q) in enumerate(problematic):
        # Skip if already cleaned
        key = (q.get('qno'), q.get('page'))
        if key in cleaned_indices:
            continue
        
        result = clean_question_with_llm(q)
        if result and 'options' in result and len(result['options']) == 4:
            # Update question
            new_qtext = result.get('question', '').strip()
            if new_qtext and len(new_qtext) > 20:
                q['question'] = new_qtext
            q['options'] = result['options']
            if result.get('correct_answer'):
                q['correct_answer'] = result['correct_answer']
            if result.get('explanation'):
                q['explanation'] = result['explanation']
            # Mark original info for tracking
            q['original_qno'] = q.get('qno')
            q['original_page'] = q.get('page')
            q['cleaned'] = True
            completed += 1
            save_counter += 1
        else:
            failed += 1
        
        # Save every 5 questions
        if save_counter >= 5:
            with open(INPUT, 'w', encoding='utf-8') as f:
                json.dump(questions, f, indent=2, ensure_ascii=False)
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(questions, f, indent=2, ensure_ascii=False)
            save_counter = 0
            elapsed = time.time() - start
            done = idx + 1
            rate = done / elapsed if elapsed > 0 else 0
            eta = (len(problematic) - done) / rate if rate > 0 else 0
            with_ans = sum(1 for q in questions if q.get('correct_answer'))
            print(f"  [{done}/{len(problematic)}] {rate:.1f} q/s, ETA {eta:.0f}s, cleaned={completed}, failed={failed}, with_answers={with_ans}", flush=True)
        
        # Rate limit: 1.5s between calls
        time.sleep(10)
    
    # Final save
    with open(INPUT, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    elapsed = time.time() - start
    print(f"\n✓ Done! {completed} cleaned, {failed} failed in {elapsed:.0f}s")
    
    # Final stats
    still_problematic = sum(1 for q in questions if is_question_problematic(q))
    print(f"Still problematic: {still_problematic}/{len(questions)}")
    with_ans = sum(1 for q in questions if q.get('correct_answer'))
    print(f"With answers: {with_ans}/{len(questions)}")


if __name__ == "__main__":
    main()
