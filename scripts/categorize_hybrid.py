#!/usr/bin/env python3
"""
Hybrid categorization:
1. Use refined v2 taxonomy (keyword-based) for fast bulk categorization - splits merged topics
2. Use LLM (z-ai chat) only for uncategorized questions
"""
import json
import re
import os
import sys
import time
import subprocess
from collections import Counter

sys.path.insert(0, '/home/z/my-project/scripts')
from taxonomy_v2 import TAXONOMY

INPUT = "/home/z/my-project/data/questions_v3.json"
OUTPUT = "/home/z/my-project/data/categorized_v3.json"


def count_keyword_matches(text, keywords):
    text_lower = text.lower()
    score = 0
    matched = []
    for kw in keywords:
        kw_lower = kw.lower()
        if re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower):
            score += 1
            matched.append(kw)
    return score, matched


def categorize_with_keywords(q):
    """Keyword-based categorization using refined v2 taxonomy."""
    qtext = q.get('question', '')
    options = ' '.join(q.get('options', []))
    full_text = qtext + ' ' + options
    
    if not qtext or len(qtext) < 10:
        return "Uncategorized", "Uncategorized", 0, []
    
    best_subject = "Uncategorized"
    best_subtopic = "Uncategorized"
    best_score = 0
    best_matched = []
    
    years_recent = re.findall(r'\b(2024|2025|2026)\b', full_text)
    recent_year_bonus = len(years_recent) * 2
    
    for subject, subtopics in TAXONOMY.items():
        for subtopic, keywords in subtopics.items():
            score, matched = count_keyword_matches(full_text, keywords)
            if subject == "Current Affairs" and recent_year_bonus > 0:
                score += recent_year_bonus
            if score > best_score:
                best_score = score
                best_subject = subject
                best_subtopic = subtopic
                best_matched = matched
    
    # Fallback heuristics
    if best_score == 0:
        full_lower = full_text.lower()
        if any(w in full_lower for w in ['river', 'mountain', 'climate', 'country', 'capital', 'state', 'sea', 'ocean', 'continent']):
            return "Geography", "World Geography (Continents, Countries, Capitals)", 1, []
        if any(w in full_lower for w in ['prime minister', 'parliament', 'constitution', 'amendment', 'article', 'lok sabha', 'rajya sabha']):
            return "Polity", "Parliament & State Legislature", 1, []
        if any(w in full_lower for w in ['ancient', 'medieval', 'empire', 'dynasty', 'king', 'queen', 'period', 'century']):
            return "History", "World History & Miscellaneous", 1, []
        if any(w in full_lower for w in ['bank', 'rate', 'inflation', 'gdp', 'economic', 'finance', 'rupee']):
            return "Economics", "Banking & Monetary System", 1, []
        if any(w in full_lower for w in ['sport', 'player', 'team', 'championship', 'tournament', 'medal', 'olympic']):
            return "Static GK", "Sports & Games", 1, []
        if any(w in full_lower for w in ['festival', 'dance', 'music', 'song', 'celebration', 'fair']):
            return "Static GK", "Festivals & Fairs of India", 1, []
        if any(w in full_lower for w in ['book', 'author', 'novel', 'poem', 'written', 'literary']):
            return "Static GK", "Books & Authors", 1, []
        if any(w in full_lower for w in ['award', 'prize', 'honour', 'padma', 'nobel']):
            return "Static GK", "Awards & Honours", 1, []
        if any(w in full_lower for w in ['cell', 'tissue', 'organ', 'plant', 'animal', 'human body', 'disease', 'blood']):
            return "General Science", "Biology - Human Physiology", 1, []
        if any(w in full_lower for w in ['atom', 'molecule', 'chemical', 'reaction', 'acid', 'base']):
            return "General Science", "Chemistry - Matter & Atomic Structure", 1, []
        if any(w in full_lower for w in ['force', 'energy', 'light', 'sound', 'electricity', 'magnet']):
            return "General Science", "Physics - Mechanics & Motion", 1, []
        if any(w in full_lower for w in ['temple', 'cave', 'sculpture', 'architecture', 'pillar', 'stupa']):
            return "Static GK", "Temple Architecture & Sculpture", 1, []
        if any(w in full_lower for w in ['2024', '2025', '2026', 'recently', 'latest']):
            return "Current Affairs", "National Affairs & Government Schemes", 1, []
        return "Uncategorized", "Uncategorized", 0, []
    
    return best_subject, best_subtopic, best_score, best_matched


def call_zai_chat(prompt, max_retries=2):
    """Call z-ai chat with rate limit handling."""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['z-ai', 'chat', '--prompt', prompt, '--output', '/tmp/chat_out.json'],
                capture_output=True, text=True, timeout=90
            )
            if result.returncode != 0:
                if '429' in (result.stderr or ''):
                    time.sleep(30 * (attempt + 1))
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
    """Use LLM to categorize + extract correct answer."""
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
    print(f"Loaded {len(questions)} questions")
    
    # Step 1: Keyword-based categorization for ALL questions
    print("\nStep 1: Keyword-based categorization (refined v2 taxonomy)...")
    for q in questions:
        subject, subtopic, score, matched = categorize_with_keywords(q)
        q['subject'] = subject
        q['subtopic'] = subtopic
        q['match_score'] = score
        q['matched_keywords'] = matched
    
    # Stats
    subjects = Counter(q['subject'] for q in questions)
    print("\nSubject distribution (after keyword categorization):")
    for s, c in subjects.most_common():
        print(f"  {s}: {c}")
    
    # Find uncategorized
    uncat = [q for q in questions if q['subject'] == 'Uncategorized']
    print(f"\nUncategorized: {len(uncat)}")
    
    # Step 2: Use LLM for uncategorized questions (and to add correct_answer for ALL)
    print(f"\nStep 2: LLM categorization for {len(uncat)} uncategorized questions...")
    print("(Also extracting correct answers for all questions via LLM)")
    
    # First, do LLM for uncategorized
    llm_count = 0
    for i, q in enumerate(uncat):
        if llm_count >= 5:
            print(f"  Pausing LLM after {llm_count} calls to avoid rate limit")
            break
        cat = categorize_with_llm(q)
        if cat:
            q['subject'] = cat.get('subject', 'Uncategorized')
            q['subtopic'] = cat.get('subtopic', 'Uncategorized')
            q['correct_answer'] = cat.get('correct_answer', '')
            q['explanation'] = cat.get('explanation', '')
            llm_count += 1
            print(f"  [{i+1}/{len(uncat)}] Q{q['qno']}: {q['subject']} > {q['subtopic']}", flush=True)
            time.sleep(2)  # Rate limit
    
    # For all OTHER questions, also try to get correct answer via LLM (sample only)
    # This is rate-limited so we'll do a subset
    no_answer = [q for q in questions if not q.get('correct_answer')]
    print(f"\nQuestions without correct_answer: {len(no_answer)}")
    print("(Will extract answers for first 50 questions via LLM)")
    
    for i, q in enumerate(no_answer[:50]):
        if i >= 5:
            print(f"  Pausing LLM after 5 calls")
            break
        cat = categorize_with_llm(q)
        if cat:
            # Don't overwrite keyword categorization, just add answer
            if not q.get('correct_answer'):
                q['correct_answer'] = cat.get('correct_answer', '')
            if not q.get('explanation'):
                q['explanation'] = cat.get('explanation', '')
            print(f"  [{i+1}/50] Q{q['qno']}: answer={q.get('correct_answer')}", flush=True)
            time.sleep(2)
    
    # Final save
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved to: {OUTPUT}")
    
    # Final stats
    print("\n=== FINAL STATS ===")
    subjects = Counter(q['subject'] for q in questions)
    for s, c in subjects.most_common():
        print(f"  {s}: {c}")
    
    print("\nTop 15 sub-topics:")
    subtopics = Counter(q['subtopic'] for q in questions)
    for s, c in subtopics.most_common(15):
        print(f"  {s}: {c}")
    
    with_answer = sum(1 for q in questions if q.get('correct_answer'))
    print(f"\nQuestions with correct_answer: {with_answer}/{len(questions)}")


if __name__ == "__main__":
    main()
