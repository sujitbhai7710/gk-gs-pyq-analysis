#!/usr/bin/env python3
"""
Build comprehensive website data from categorized questions.
Generates a single JSON file that the website will load.
"""
import json
import os
from collections import defaultdict, Counter

INPUT = "/home/z/my-project/data/categorized_questions.json"
OUTPUT = "/home/z/my-project/website/data.json"

# Subject ordering and metadata
SUBJECT_META = {
    "History": {
        "icon": "🏛️",
        "color": "#dc2626",
        "gradient": "linear-gradient(135deg, #dc2626 0%, #991b1b 100%)",
        "description": "Ancient, Medieval, Modern Indian History & World History"
    },
    "Geography": {
        "icon": "🌍",
        "color": "#059669",
        "gradient": "linear-gradient(135deg, #059669 0%, #065f46 100%)",
        "description": "Physical, Indian & World Geography"
    },
    "Polity": {
        "icon": "⚖️",
        "color": "#7c3aed",
        "gradient": "linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%)",
        "description": "Constitution, Parliament, Judiciary & Governance"
    },
    "Economics": {
        "icon": "💰",
        "color": "#d97706",
        "gradient": "linear-gradient(135deg, #d97706 0%, #92400e 100%)",
        "description": "Indian Economy, Banking, Budget & Finance"
    },
    "General Science": {
        "icon": "🔬",
        "color": "#0891b2",
        "gradient": "linear-gradient(135deg, #0891b2 0%, #155e75 100%)",
        "description": "Physics, Chemistry & Biology"
    },
    "Static GK": {
        "icon": "📚",
        "color": "#be185d",
        "gradient": "linear-gradient(135deg, #be185d 0%, #831843 100%)",
        "description": "Books, Sports, Awards, Festivals, Dance, Music & More"
    },
    "Current Affairs": {
        "icon": "📰",
        "color": "#1d4ed8",
        "gradient": "linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%)",
        "description": "Recent Events, Schemes, Sports, Awards & Rankings"
    }
}


def main():
    with open(INPUT, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Loaded {len(questions)} questions")
    
    # Build structure: subject -> subtopic -> [questions]
    structure = defaultdict(lambda: defaultdict(list))
    
    for q in questions:
        subject = q.get('subject', 'Uncategorized')
        subtopic = q.get('subtopic', 'Uncategorized')
        
        # Clean question object
        clean_q = {
            'qno': q.get('qno'),
            'question': q.get('question', '').strip(),
            'options': q.get('options_list', []),
            'answered': q.get('answered', True),
            'shift': q.get('shift', ''),
            'page': q.get('page', 0),
            'matched_keywords': q.get('matched_keywords', [])
        }
        
        # Filter out empty options
        clean_q['options'] = [o for o in clean_q['options'] if o and len(o) < 250]
        
        structure[subject][subtopic].append(clean_q)
    
    # Build final data structure
    website_data = {
        'metadata': {
            'total_questions': len(questions),
            'total_subjects': len(structure),
            'total_subtopics': sum(len(subs) for subs in structure.values()),
            'source': 'SSC CGL Tier 1 (Sep-Oct 2025) - General Awareness',
            'exam': 'SSC CGL 2025',
            'note': 'Questions extracted from official SSC CGL Tier 1 question papers (Sep-Oct 2025). Only English version included.'
        },
        'subjects': {},
        'subject_order': list(SUBJECT_META.keys()) + (['Uncategorized'] if 'Uncategorized' in structure else [])
    }
    
    # Add metadata for Uncategorized if present
    if 'Uncategorized' in structure:
        SUBJECT_META['Uncategorized'] = {
            "icon": "❓",
            "color": "#6b7280",
            "gradient": "linear-gradient(135deg, #6b7280 0%, #374151 100%)",
            "description": "Questions that could not be auto-categorized"
        }
    
    # Build subject data
    for subject, subtopics in structure.items():
        meta = SUBJECT_META.get(subject, {
            "icon": "📋",
            "color": "#6b7280",
            "gradient": "linear-gradient(135deg, #6b7280 0%, #374151 100%)",
            "description": ""
        })
        
        subject_questions = sum(len(qs) for qs in subtopics.values())
        
        # Sort subtopics by question count (desc)
        subtopic_list = []
        for subtopic, qs in sorted(subtopics.items(), key=lambda x: -len(x[1])):
            subtopic_list.append({
                'name': subtopic,
                'count': len(qs),
                'questions': qs
            })
        
        website_data['subjects'][subject] = {
            'meta': meta,
            'total_questions': subject_questions,
            'subtopic_count': len(subtopics),
            'subtopics': subtopic_list
        }
    
    # Save
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(website_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nWebsite data saved to: {OUTPUT}")
    print(f"File size: {os.path.getsize(OUTPUT) / 1024:.1f} KB")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"WEBSITE DATA SUMMARY")
    print(f"{'='*60}")
    print(f"Total Questions: {website_data['metadata']['total_questions']}")
    print(f"Total Subjects: {website_data['metadata']['total_subjects']}")
    print(f"Total Sub-topics: {website_data['metadata']['total_subtopics']}")
    print(f"\nSubject Distribution:")
    for subject in website_data['subject_order']:
        if subject in website_data['subjects']:
            sd = website_data['subjects'][subject]
            print(f"  {subject}: {sd['total_questions']} questions, {sd['subtopic_count']} sub-topics")


if __name__ == "__main__":
    main()
