#!/usr/bin/env python3
"""Inspect first few pages of the PDF to understand structure."""
import pdfplumber

PDF = "/home/z/my-project/download/gk_gs_pyq.pdf"

with pdfplumber.open(PDF) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    print("=" * 80)
    # Print first 3 pages
    for i in range(min(5, len(pdf.pages))):
        page = pdf.pages[i]
        text = page.extract_text() or ""
        print(f"\n----- PAGE {i+1} -----")
        print(text[:3000])
        print("-" * 80)
