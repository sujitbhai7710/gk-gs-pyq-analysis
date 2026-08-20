#!/usr/bin/env python3
"""Examine uncategorized and possibly miscategorized questions to improve taxonomy."""
import json

with open('/home/z/my-project/data/categorized_questions.json', 'r', encoding='utf-8') as f:
    qs = json.load(f)

print("=" * 80)
print("UNCATEGORIZED QUESTIONS (sample 15):")
print("=" * 80)
uncat = [q for q in qs if q['subject'] == 'Uncategorized']
for q in uncat[:15]:
    print(f"\n[Q.No {q['qno']}] {q.get('question','')[:200]}")
    if q.get('options_list'):
        for o in q['options_list'][:2]:
            print(f"  - {o[:80]}")

print("\n\n" + "=" * 80)
print("ECONOMICS > POPULATION questions (verify):")
print("=" * 80)
for q in qs:
    if q.get('subtopic') == 'Population, Poverty & Unemployment':
        print(f"\n[Q.No {q['qno']}] {q.get('question','')[:200]}")
        break

print("\n\n" + "=" * 80)
print("Geography > Indian Minerals questions (verify):")
print("=" * 80)
count = 0
for q in qs:
    if q.get('subtopic') == 'Indian Minerals, Energy & Industries':
        print(f"\n[Q.No {q['qno']}] {q.get('question','')[:200]}")
        count += 1
        if count >= 5:
            break
