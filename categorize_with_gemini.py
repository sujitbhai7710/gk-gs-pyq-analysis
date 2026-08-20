#!/usr/bin/env python3
"""
Use Gemini to categorize each question into subject + sub-topic AND
extract the correct answer.

For each question, sends the question text + options to Gemini Flash and asks:
1. Which subject does this belong to?
2. Which sub-topic (from a fixed list)?
3. What is the correct answer (option A/B/C/D)?

Outputs to categorized_with_answers.json
"""
import os
import sys
import json
import time
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: Set GEMINI_API_KEY env var")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

INPUT = sys.argv[1] if len(sys.argv) > 1 else "questions.json"
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else "categorized_with_answers.json"

# Fixed taxonomy - subjects and their sub-topics
TAXONOMY = {
    "History": [
        "Prehistoric Period & Indus Valley Civilization",
        "Vedic Age & Aryan Society",
        "Mahajanapadas, Buddhism & Jainism",
        "Mauryan Empire",
        "Post-Mauryan Period (Shungas, Kushanas, Sakas, Indo-Greeks, Satavahanas)",
        "Gupta & Post-Gupta Period (incl. Vardhana / Harsha)",
        "Southern & Deccan Dynasties (Pallava, Chola, Pandya, Chalukya, Rashtrakuta)",
        "Early Medieval India & Rajput Period",
        "Delhi Sultanate",
        "Vijayanagara & Bahmani Empires",
        "Mughal Empire",
        "Maratha, Sikh & Other Regional Powers",
        "Bhakti & Sufi Movements",
        "Advent of Europeans & Establishment of British Rule",
        "British Acts, Policies & Land Revenue Systems",
        "Governor-Generals & Viceroys",
        "Revolt of 1857",
        "Socio-Religious Reform Movements",
        "Indian National Congress & Early Nationalist Phase",
        "Revolutionary Movements",
        "Gandhian Era & Mass Movements",
        "Independence, Partition & Post-Independence India",
        "World History & Miscellaneous",
    ],
    "Geography": [
        "Physical Geography (Geomorphology)",
        "Indian Geography (Physiography)",
        "Indian Rivers & Drainage System",
        "Climate, Monsoon & Weather",
        "Indian Soils & Natural Vegetation",
        "Indian Agriculture & Crops",
        "Indian Minerals, Energy & Industries",
        "Indian Transport & Communication",
        "World Geography (Continents, Countries, Capitals)",
        "Map Work & Geographical Features",
        "Environmental Geography & Ecology",
    ],
    "Polity": [
        "Making of the Indian Constitution",
        "Salient Features of the Constitution",
        "Fundamental Rights",
        "Directive Principles of State Policy (DPSP)",
        "Fundamental Duties",
        "Union & State Executive (President, PM, Governor)",
        "Parliament & State Legislature",
        "Judiciary (Supreme Court & High Courts)",
        "Constitutional, Statutory & Non-Statutory Bodies",
        "Federalism & Centre-State Relations",
        "Local Government & Panchayati Raj",
        "Constitutional Amendments",
        "Indian Political System & Parties",
        "Welfare Schemes & Government Policies",
        "New Criminal Laws (BNS, BNSS, BSA)",
    ],
    "Economics": [
        "Basics of Indian Economy",
        "Banking & Monetary System",
        "Public Finance & Budget",
        "Inflation & Price Index",
        "Money & Capital Market",
        "International Trade & Organizations",
        "Agriculture, Industry & Service Sectors",
        "Population, Poverty & Unemployment",
    ],
    "General Science": [
        "Physics - Mechanics & Motion",
        "Physics - Light, Sound & Waves",
        "Physics - Heat, Electricity & Magnetism",
        "Physics - Modern Physics & Nuclear",
        "Chemistry - Matter & Atomic Structure",
        "Chemistry - Chemical Bonding & Reactions",
        "Chemistry - Industrial & Organic Chemistry",
        "Biology - Cell & Genetics",
        "Biology - Plant Physiology",
        "Biology - Human Physiology",
        "Biology - Health, Disease & Nutrition",
        "Biology - Ecology & Environment",
    ],
    "Static GK": [
        "Books & Authors",
        "Awards & Honours",
        "Sports & Games",
        "Festivals & Fairs of India",
        "Indian Classical Dance Forms",
        "Indian Folk Dances & Martial Arts",
        "Indian Music (Hindustani & Carnatic)",
        "Indian Musical Instruments",
        "Temple Architecture & Sculpture",
        "Indo-Islamic Architecture",
        "Modern Architecture & Monuments",
        "Paintings & Art Forms",
        "Important Days & Dates",
        "International Organizations & Headquarters",
        "National Symbols & Insignia",
        "Indian Railways, Metro & Transport",
        "Space & Defence",
        "Science & Technology Current Developments",
    ],
    "Current Affairs": [
        "National Affairs & Government Schemes",
        "International Affairs & Treaties",
        "Economy & Business Current",
        "Sports Current Affairs",
        "Awards & Honours Current",
        "Persons in News & Obituaries",
        "Defence & Space Current",
        "Reports, Indices & Rankings",
    ],
}

# Build a flat list of all sub-topics with subject prefix
ALL_SUBTOPICS = []
for subject, subs in TAXONOMY.items():
    for sub in subs:
        ALL_SUBTOPICS.append(f"{subject} > {sub}")

TAXONOMY_TEXT = "\n".join(ALL_SUBTOPICS)


def categorize_question(q):
    """Send a single question to Gemini for categorization + answer extraction."""
    qtext = q.get('question', '').strip()
    options = q.get('options', [])
    
    if not qtext:
        return None
    
    # Build options text
    opts_text = ""
    letters = ['A', 'B', 'C', 'D']
    for i, opt in enumerate(options[:4]):
        letter = letters[i] if i < len(letters) else str(i+1)
        opts_text += f"{letter}. {opt}\n"
    
    prompt = f"""You are an expert at analyzing Indian competitive exam questions (SSC CGL General Awareness).

QUESTION:
{qtext}

OPTIONS:
{opts_text}

TASK: Analyze this question and return a JSON object with EXACTLY these fields:
- "subject": one of {list(TAXONOMY.keys())}
- "subtopic": one of the sub-topics from the taxonomy below (use the sub-topic name only, not the subject prefix)
- "correct_answer": the LETTER (A, B, C, or D) of the correct option, or "Not Answered" if the question was not answered in the source
- "explanation": a brief 1-2 sentence explanation of why the answer is correct

TAXONOMY (subject > sub-topic):
{TAXONOMY_TEXT}

RULES:
1. Pick the MOST specific sub-topic. If a question is about a Mughal emperor, use "Mughal Empire" not "World History".
2. If a question is about a dance form (e.g., Bharatanatyam), use "Indian Classical Dance Forms".
3. If a question is about a musical raga or instrument, use "Indian Music (Hindustani & Carnatic)" or "Indian Musical Instruments".
4. If a question is about a temple or cave, use "Temple Architecture & Sculpture".
5. If a question mentions a 2024/2025 event, person, or scheme, use the appropriate "Current Affairs" sub-topic.
6. If a question is about a sports event from 2024/2025, use "Sports Current Affairs".
7. If a question is about a sports rule or terminology (not a recent event), use "Sports & Games" under Static GK.
8. "Not Answered" means the original question paper showed "Not Answered" - otherwise always pick A/B/C/D.

Return ONLY the JSON object, no other text.
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        text = response.text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
        # Remove any leading "json" identifier
        if text.startswith("json"):
            text = text[4:].strip()
        
        result = json.loads(text)
        return result
    except Exception as e:
        print(f"  [ERROR] Q{q.get('qno')}: {e}")
        return None


def main():
    with open(INPUT, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Loaded {len(questions)} questions")
    
    results = []
    failed = 0
    
    for i, q in enumerate(questions):
        print(f"[{i+1}/{len(questions)}] Q.No {q.get('qno')}...", flush=True)
        
        cat = categorize_question(q)
        if cat:
            q['subject'] = cat.get('subject', 'Uncategorized')
            q['subtopic'] = cat.get('subtopic', 'Uncategorized')
            q['correct_answer'] = cat.get('correct_answer', '')
            q['explanation'] = cat.get('explanation', '')
        else:
            q['subject'] = 'Uncategorized'
            q['subtopic'] = 'Uncategorized'
            q['correct_answer'] = ''
            q['explanation'] = ''
            failed += 1
        
        results.append(q)
        
        # Save progress every 20 questions
        if (i+1) % 20 == 0:
            with open(OUTPUT, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"  Saved progress: {i+1} questions")
        
        # Rate limit
        time.sleep(0.5)
    
    # Final save
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Done! {len(results)} questions categorized")
    print(f"  Failed: {failed}")
    print(f"  Output: {OUTPUT}")


if __name__ == "__main__":
    main()
