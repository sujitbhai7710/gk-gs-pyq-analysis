#!/usr/bin/env python3
"""
Batched LLM answer extraction - processes 5 questions per LLM call
to reduce total API calls and stay under rate limits.
"""
import json
import os
import sys
import time
import subprocess
import re

INPUT = "/home/z/my-project/data/categorized_v3.json"


def call_zai_chat(prompt, max_retries=5):
    """Call z-ai chat with aggressive retry on rate limit."""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['z-ai', 'chat', '--prompt', prompt, '--output', '/tmp/chat_batch.json'],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode != 0:
                stderr = result.stderr or ''
                if '429' in stderr:
                    # Wait 2 min, then 5 min, then 10 min, then 20 min
                    wait_times = [120, 300, 600, 1200, 1800]
                    wait = wait_times[min(attempt, len(wait_times)-1)]
                    print(f"    [429 rate limited, waiting {wait}s]", flush=True)
                    time.sleep(wait)
                    continue
                time.sleep(10)
                continue
            with open('/tmp/chat_batch.json', 'r') as f:
                data = json.load(f)
            choices = data.get('choices', [])
            if choices:
                return choices[0].get('message', {}).get('content', '').strip()
        except subprocess.TimeoutExpired:
            print(f"    [timeout, retry {attempt+1}]", flush=True)
            time.sleep(10)
        except Exception as e:
            print(f"    [error: {e}]", flush=True)
            time.sleep(10)
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
    # Try to find JSON array
    try:
        return json.loads(text)
    except:
        # Try to find a JSON array in text
        m = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except:
                pass
        return None


def process_batch(batch):
    """Process a batch of 5 questions in one LLM call."""
    questions_text = ""
    actual_qnos = []
    for i, q in enumerate(batch):
        qno = q.get('qno')
        actual_qnos.append(qno)
        qtext = q.get('question', '').strip()
        options = q.get('options', [])
        opts_text = ""
        letters = ['A', 'B', 'C', 'D']
        for j, opt in enumerate(options[:4]):
            letter = letters[j] if j < len(letters) else str(j+1)
            opts_text += f"{letter}. {opt}\n"
        if not opts_text:
            opts_text = "(no options)"
        if not q.get('answered', True):
            opts_text = "Not Answered\n" + opts_text
        questions_text += f"\n--- Question {i+1} (Q.No: {qno}) ---\nQ: {qtext}\nOptions:\n{opts_text}\n"
    
    prompt = f"""You are an expert at SSC CGL General Awareness. Analyze these {len(batch)} questions and return ONLY a JSON array (no other text).

For each question, return an object with the EXACT qno from above:
{{"qno": <number>, "correct_answer": "<A/B/C/D or N/A>", "explanation": "<brief 1-sentence explanation>"}}

Questions:
{questions_text}

Return ONLY a JSON array like:
[{{"qno": {actual_qnos[0]}, "correct_answer": "A", "explanation": "..."}}, ...]

No code fences, no markdown, no intro - just the JSON array."""
    
    response = call_zai_chat(prompt)
    if not response:
        return None
    parsed = parse_json_response(response)
    if parsed and isinstance(parsed, list):
        # Verify qnos match
        return parsed
    return None


def main():
    with open(INPUT, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # Find questions without correct_answer
    no_answer = [q for q in questions if not q.get('correct_answer')]
    print(f"Loaded {len(questions)} questions, {len(no_answer)} without answer", flush=True)
    
    if not no_answer:
        print("All questions already have answers!")
        return
    
    # Process in batches of 3 (smaller to avoid token limits)
    batch_size = 3
    completed = 0
    failed = 0
    start = time.time()
    
    for i in range(0, len(no_answer), batch_size):
        batch = no_answer[i:i+batch_size]
        results = process_batch(batch)
        
        if results and isinstance(results, list):
            # Map results back to questions by qno
            for r in results:
                qno = r.get('qno')
                for q in batch:
                    if q['qno'] == qno:
                        q['correct_answer'] = r.get('correct_answer', '')
                        q['explanation'] = r.get('explanation', '')
                        break
            completed += len(results)
        else:
            failed += len(batch)
        
        # Save progress every 2 batches
        if (i // batch_size) % 2 == 0:
            with open(INPUT, 'w', encoding='utf-8') as f:
                json.dump(questions, f, indent=2, ensure_ascii=False)
            elapsed = time.time() - start
            done = i + len(batch)
            rate = done / elapsed if elapsed > 0 else 0
            eta = (len(no_answer) - done) / rate if rate > 0 else 0
            with_ans = sum(1 for q in questions if q.get('correct_answer'))
            print(f"  [{done}/{len(no_answer)}] {rate:.1f} q/s, ETA {eta:.0f}s, total with answers: {with_ans}", flush=True)
        
        # Rate limit: wait between batches
        time.sleep(3)
    
    # Final save
    with open(INPUT, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    elapsed = time.time() - start
    with_ans = sum(1 for q in questions if q.get('correct_answer'))
    print(f"\n✓ Done! {completed} answers extracted in {elapsed:.0f}s")
    print(f"Total with answers: {with_ans}/{len(questions)}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
