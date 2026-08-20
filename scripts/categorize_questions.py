#!/usr/bin/env python3
"""
Categorize extracted questions using keyword-based taxonomy.
For each question, compute match scores against all sub-topics
and assign subject + sub-topic with highest score.

Output: /home/z/my-project/data/categorized_questions.json
"""
import json
import re
import os
import sys

# Add scripts dir to path
sys.path.insert(0, '/home/z/my-project/scripts')
from taxonomy import TAXONOMY

INPUT = "/home/z/my-project/data/all_questions.json"
OUTPUT = "/home/z/my-project/data/categorized_questions.json"


def normalize_text(text):
    """Lowercase and normalize text for matching."""
    text = text.lower()
    # Replace common OCR errors
    replacements = {
        '|': 'i', 'l': 'l',  # ambiguity - keep as is for now
    }
    return text


def count_keyword_matches(text, keywords):
    """Count how many keywords appear in text."""
    text_lower = text.lower()
    score = 0
    matched_keywords = []
    for kw in keywords:
        kw_lower = kw.lower()
        # Word boundary search
        if re.search(r'\b' + re.escape(kw_lower) + r'\b', text_lower):
            score += 1
            matched_keywords.append(kw)
    return score, matched_keywords


def categorize_question(question_obj):
    """Categorize a single question. Returns (subject, sub_topic, score, matched_kws)."""
    # Combine question + options for matching
    qtext = question_obj.get('question', '')
    options = ' '.join(question_obj.get('options_list', []))
    full_text = qtext + ' ' + options
    
    if not qtext or len(qtext) < 10:
        return "Uncategorized", "Uncategorized", 0, []
    
    best_subject = "Uncategorized"
    best_subtopic = "Uncategorized"
    best_score = 0
    best_matched = []
    
    # Special case: if year 2024/2025 mentioned, likely Current Affairs
    years_recent = re.findall(r'\b(2024|2025|2026)\b', full_text)
    recent_year_bonus = len(years_recent) * 2
    
    # Check each subject and sub-topic
    subject_scores = {}
    for subject, subtopics in TAXONOMY.items():
        subject_total = 0
        for subtopic, keywords in subtopics.items():
            score, matched = count_keyword_matches(full_text, keywords)
            # Bonus for current affairs if recent year mentioned
            if subject == "Current Affairs" and recent_year_bonus > 0:
                score += recent_year_bonus
            if score > best_score:
                best_score = score
                best_subject = subject
                best_subtopic = subtopic
                best_matched = matched
            subject_total += score
        subject_scores[subject] = subject_total
    
    # If no match found, try broader keyword matching
    if best_score == 0:
        full_lower = full_text.lower()
        # Fallback heuristics based on common patterns
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


def main():
    if not os.path.exists(INPUT):
        print(f"ERROR: {INPUT} not found. Run parse_questions.py first.")
        return
    
    with open(INPUT, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Loaded {len(questions)} questions")
    
    categorized = []
    stats = {
        'subjects': {},
        'subtopics': {}
    }
    
    for q in questions:
        subject, subtopic, score, matched = categorize_question(q)
        q['subject'] = subject
        q['subtopic'] = subtopic
        q['match_score'] = score
        q['matched_keywords'] = matched
        
        stats['subjects'][subject] = stats['subjects'].get(subject, 0) + 1
        key = f"{subject} > {subtopic}"
        stats['subtopics'][key] = stats['subtopics'].get(key, 0) + 1
        
        categorized.append(q)
    
    # Save categorized questions
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(categorized, f, indent=2, ensure_ascii=False)
    
    # Save stats
    stats_sorted = {
        'total_questions': len(categorized),
        'subjects': dict(sorted(stats['subjects'].items(), key=lambda x: -x[1])),
        'subtopics': dict(sorted(stats['subtopics'].items(), key=lambda x: -x[1]))
    }
    with open('/home/z/my-project/data/categorization_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats_sorted, f, indent=2, ensure_ascii=False)
    
    print(f"\nCategorized {len(categorized)} questions")
    print(f"\nSubject distribution:")
    for s, c in stats_sorted['subjects'].items():
        print(f"  {s}: {c}")
    
    print(f"\nTop 15 sub-topics:")
    for s, c in list(stats_sorted['subtopics'].items())[:15]:
        print(f"  {s}: {c}")


if __name__ == "__main__":
    main()
