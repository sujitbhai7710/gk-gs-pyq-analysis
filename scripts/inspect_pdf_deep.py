#!/usr/bin/env python3
"""Deep inspection: look at full text per page and check for images."""
import pdfplumber

PDF = "/home/z/my-project/download/gk_gs_pyq.pdf"

with pdfplumber.open(PDF) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    # Check pages 1, 2, 26, 50, 100, 200, 300
    for i in [0, 1, 2, 25, 49, 99, 199, 299, 399, 487]:
        if i >= len(pdf.pages):
            continue
        page = pdf.pages[i]
        text = page.extract_text() or ""
        chars = page.chars
        images = page.images
        print(f"\n===== PAGE {i+1} =====")
        print(f"  chars count: {len(chars)}, images count: {len(images)}")
        print(f"  text length: {len(text)}")
        print(f"  text preview: {text[:1500]!r}")
        print("-" * 80)
