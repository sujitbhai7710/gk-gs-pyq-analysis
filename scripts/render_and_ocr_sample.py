#!/usr/bin/env python3
"""Render one PDF page as high-res image and OCR it."""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

PDF = "/home/z/my-project/download/gk_gs_pyq.pdf"
OUT = "/home/z/my-project/data/page_renders"
os.makedirs(OUT, exist_ok=True)

doc = fitz.open(PDF)

# Render page 2 (index 1) at high DPI
for page_idx in [1, 2, 25]:
    page = doc[page_idx]
    # High resolution: 300 DPI (default is 72)
    mat = fitz.Matrix(300/72, 300/72)
    pix = page.get_pixmap(matrix=mat)
    
    img_path = f"{OUT}/page_{page_idx+1}.png"
    pix.save(img_path)
    print(f"Page {page_idx+1}: rendered to {img_path} ({pix.width}x{pix.height})")
    
    # OCR the rendered image
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    print(f"\n----- OCR TEXT (page {page_idx+1}) -----")
    print(text)
    print("=" * 80)

doc.close()
