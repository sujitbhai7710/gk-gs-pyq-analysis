#!/usr/bin/env python3
"""OCR pages in batches - synchronous, smaller chunks."""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import sys
import time
import gc

PDF = "/home/z/my-project/download/gk_gs_pyq.pdf"
OUT_DIR = "/home/z/my-project/data/ocr_pages"
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 150

def ocr_page(page_idx, doc):
    out_path = f"{OUT_DIR}/page_{page_idx+1:04d}.txt"
    if os.path.exists(out_path) and os.path.getsize(out_path) > 50:
        return "skipped"
    
    try:
        page = doc[page_idx]
        mat = fitz.Matrix(DPI/72, DPI/72)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        text = pytesseract.image_to_string(img, lang='eng', config='--oem 1 --psm 6')
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        # Cleanup
        img.close()
        del pix, img_data, img
        return "done"
    except Exception as e:
        return f"error: {e}"

def main():
    start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    end_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    
    doc = fitz.open(PDF)
    total = doc.page_count
    end_idx = min(end_idx, total)
    
    print(f"OCR pages {start_idx+1} to {end_idx} (of {total})")
    start = time.time()
    done = 0
    
    for i in range(start_idx, end_idx):
        status = ocr_page(i, doc)
        done += 1
        if done % 5 == 0 or 'error' in status:
            elapsed = time.time() - start
            print(f"  [{done}/{end_idx-start_idx}] page {i+1}: {status} ({elapsed:.0f}s)", flush=True)
        # Force GC
        if done % 10 == 0:
            gc.collect()
    
    doc.close()
    elapsed = time.time() - start
    print(f"Done! {done} pages in {elapsed:.1f}s")

if __name__ == "__main__":
    main()
