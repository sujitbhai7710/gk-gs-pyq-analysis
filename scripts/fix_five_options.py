#!/usr/bin/env python3
"""Fix questions with 5+ options: remove garbled ones, keep first 4 valid."""
import json
import re
import sys
sys.path.insert(0, '/home/z/my-project/scripts')
from cleanup_questions import is_option_garbled

INPUT = "/home/z/my-project/data/categorized_v4.json"
OUTPUT = "/home/z/my-project/data/categorized_v4.json"

with open(INPUT, 'r', encoding='utf-8') as f:
    qs = json.load(f)

fixed = 0
for q in qs:
    opts = q.get('options', [])
    if len(opts) > 4:
        # Remove garbled options first
        clean_opts = [o for o in opts if not is_option_garbled(o)]
        if len(clean_opts) >= 4:
            q['options'] = clean_opts[:4]
            fixed += 1
        elif len(clean_opts) > 0:
            # Use what we have
            q['options'] = clean_opts
            fixed += 1
        # else: leave as-is, will be cleaned by LLM later

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(qs, f, indent=2, ensure_ascii=False)

print(f"Fixed {fixed} questions with 5+ options")

# Verify
five_plus = sum(1 for q in qs if len(q.get('options',[])) > 4)
print(f"Still 5+ options: {five_plus}")
