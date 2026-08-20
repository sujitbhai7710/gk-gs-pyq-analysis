#!/usr/bin/env python3
"""
Continue LLM categorization in background - extract more correct answers.
Loads existing progress and only processes questions without answers.
"""
import json
import os
import sys
import time
import subprocess
import re

INPUT = "/home/z/my-project/data/categorized_v3.json"
PROGRESS_FILE = "/home/z/my-project/data/categorized_v3.json"  # Same file


def call_zai_chat(prompt, max_retries=2):
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['z-ai', 'chat', '--prompt', prompt, '--output', '/tmp/chat_out.json'],
                capture_output=True, text=True, timeout=90
            )
            if result.returncode != 0:
                if '429' in (result.stderr or ''):
                    time.sleep(60 * (attempt + 1))  # Wait 1 min, then 2 min
                    continue
                time.sleep(5)
                continue
            with open('/tmp/chat_out.json', 'r') as f:
                data = json.load(f)
            choices = data.get('choices', [])
            if choices:
                return choices[0].get('message', {}).get('content', '').strip()
        except:
            time.sleep(3)
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
    m = re.search(r'\{[^{}]*\}', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except:
            pass
    try:
        return json.loads(text)
    except:
        return None


def categorize_with_llm(q):
    qtext = q.get('question', '').strip()
    options = q.get('options', [])
    if not qtext:
        return None
    
    opts_text = ""
    letters = ['A', 'B', 'C', 'D']
    for i, opt in enumerate(options[:4]):
        letter = letters[i] if i < len(letters) else str(i+1)
        opts_text += f"{letter}. {opt}\n"
    if not opts_text:
        opts_text = "(no options)"
    if not q.get('answered', True):
        opts_text = "Not Answered\n" + opts_text
    
    prompt = f"""Analyze this SSC CGL General Awareness question and return ONLY a JSON object.

QUESTION: {qtext}

OPTIONS:
{opts_text}

Return JSON with these fields:
- "subject": one of History, Geography, Polity, Economics, General Science, Static GK, Current Affairs
- "subtopic": specific sub-topic (use "Indian Classical Dance Forms" for classical dance, "Indian Music (Hindustani & Carnatic)" for music, "Indian Musical Instruments" for instruments, "Temple Architecture & Sculpture" for temples/caves, "Indo-Islamic Architecture" for mosques/tombs, "Mughal Empire" for Mughal history, "Sports Current Affairs" for 2024-25 sports events, "Sports & Games" for sports rules/terms)
- "correct_answer": letter A/B/C/D of correct option, or "N/A" if "Not Answered"
- "explanation": brief 1-sentence explanation

Return only JSON, no other text."""
    
    response = call_zai_chat(prompt)
    if not response:
        return None
    return parse_json_response(response)


def main():
    with open(INPUT, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # Find questions without correct_answer
    no_answer = [q for q in questions if not q.get('correct_answer')]
    print(f"Loaded {len(questions)} questions, {len(no_answer)} without answer", flush=True)
    
    if not no_answer:
        print("All questions already have answers!")
        return
    
    # Process one at a time with 2s delay
    completed = 0
    failed = 0
    start = time.time()
    
    for i, q in enumerate(no_answer):
        cat = categorize_with_llm(q)
        if cat:
            # Don't overwrite keyword categorization, just add answer
            q['correct_answer'] = cat.get('correct_answer', '')
            q['explanation'] = cat.get('explanation', '')
            # But DO update subject/subtopic if currently Uncategorized
            if q.get('subject') == 'Uncategorized':
                q['subject'] = cat.get('subject', 'Uncategorized')
                q['subtopic'] = cat.get('subtopic', 'Uncategorized')
            completed += 1
        else:
            failed += 1
        
        # Save progress every 5 questions
        if (i+1) % 5 == 0:
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(questions, f, indent=2, ensure_ascii=False)
            elapsed = time.time() - start
            rate = (i+1) / elapsed if elapsed > 0 else 0
            eta = (len(no_answer) - i - 1) / rate if rate > 0 else 0
            print(f"  [{i+1}/{len(no_answer)}] {rate:.1f} q/s, ETA {eta:.0f}s, failed={failed}", flush=True)
        
        # Rate limit
        time.sleep(2)
    
    # Final save
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    elapsed = time.time() - start
    print(f"\n✓ Done! {completed} answers extracted in {elapsed:.0f}s, failed={failed}")


if __name__ == "__main__":
    main()
