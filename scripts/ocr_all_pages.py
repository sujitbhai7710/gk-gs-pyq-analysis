#!/usr/bin/env python3
"""
Full PDF OCR pipeline - renders all pages and OCRs them in parallel.
Saves per-page text to /home/z/my-project/data/ocr_pages/page_NNNN.txt
"""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

PDF = "/home/z/my-project/download/gk_gs_pyq.pdf"
OUT_DIR = "/home/z/my-project/data/ocr_pages"
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 150  # Lower DPI for speed, still readable for OCR
N_WORKERS = 2  # Match CPU count

def ocr_page(args):
    page_idx, pdf_path = args
    out_path = f"{OUT_DIR}/page_{page_idx+1:04d}.txt"
    # Skip if already done
    if os.path.exists(out_path) and os.path.getsize(out_path) > 50:
        return page_idx, "skipped"
    
    try:
        doc = fitz.open(pdf_path)
        page = doc[page_idx]
        mat = fitz.Matrix(DPI/72, DPI/72)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # OCR with English only, LSTM engine, sparse text mode
        text = pytesseract.image_to_string(img, lang='eng', 
                                            config='--oem 1 --psm 6')
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        doc.close()
        return page_idx, "done"
    except Exception as e:
        return page_idx, f"error: {e}"

def main():
    doc = fitz.open(PDF)
    total_pages = doc.page_count
    doc.close()
    print(f"Total pages to OCR: {total_pages}")
    
    # Check how many already done
    done = 0
    for i in range(total_pages):
        p = f"{OUT_DIR}/page_{i+1:04d}.txt"
        if os.path.exists(p) and os.path.getsize(p) > 50:
            done += 1
    print(f"Already done: {done}, remaining: {total_pages - done}")
    
    if done == total_pages:
        print("All pages already OCR'd!")
        return
    
    # Build task list (only undone pages)
    tasks = [(i, PDF) for i in range(total_pages) 
             if not (os.path.exists(f"{OUT_DIR}/page_{i+1:04d}.txt") 
                     and os.path.getsize(f"{OUT_DIR}/page_{i+1:04d}.txt") > 50)]
    
    print(f"Processing {len(tasks)} pages with {N_WORKERS} workers...")
    start = time.time()
    
    completed = 0
    with ProcessPoolExecutor(max_workers=N_WORKERS) as executor:
        futures = {executor.submit(ocr_page, t): t[0] for t in tasks}
        for future in as_completed(futures):
            page_idx, status = future.result()
            completed += 1
            if completed % 10 == 0 or status.startswith("error"):
                elapsed = time.time() - start
                rate = completed / elapsed if elapsed > 0 else 0
                eta = (len(tasks) - completed) / rate if rate > 0 else 0
                print(f"  [{completed}/{len(tasks)}] page {page_idx+1}: {status} "
                      f"({rate:.1f} pg/s, ETA {eta:.0f}s)")
    
    elapsed = time.time() - start
    print(f"\nDone! Processed {completed} pages in {elapsed:.1f}s")

if __name__ == "__main__":
    main()
