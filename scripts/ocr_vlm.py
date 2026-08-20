#!/usr/bin/env python3
"""
High-accuracy OCR pipeline using z-ai vision CLI (in-house VLM).
Much better than Tesseract for bilingual English/Hindi PDFs.

Renders each PDF page at 200 DPI, sends to z-ai vision model, gets clean English text.
"""
import fitz  # PyMuPDF
import subprocess
import json
import os
import sys
import time
import io
from PIL import Image
import gc

PDF = "/home/z/my-project/download/gk_gs_pyq.pdf"
OUT_DIR = "/home/z/my-project/data/ocr_vlm"
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 100  # Lower DPI to avoid API content filter errors

PROMPT = (
    "Please read this educational exam paper page and transcribe the English text you can see. "
    "This is a study document. Just output the visible English text, preserving the line breaks and numbering."
)


def ocr_page_with_vlm(img_path):
    """Send page image to z-ai vision and return extracted English text."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['z-ai', 'vision', '--prompt', PROMPT, '--image', img_path, '--output', '/tmp/vlm_out.json'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                stderr = result.stderr
                if '429' in stderr:
                    wait = 15 * (attempt + 1)
                    time.sleep(wait)
                    continue
                elif '400' in stderr or 'contentFilter' in stderr:
                    # Image too large - resize
                    from PIL import Image
                    img = Image.open(img_path)
                    if img.width > 1200:
                        ratio = 1200 / img.width
                        new_size = (1200, int(img.height * ratio))
                        img = img.resize(new_size, Image.LANCZOS)
                        img.save(img_path, optimize=True, quality=80)
                    time.sleep(2)
                    # Retry
                    result = subprocess.run(
                        ['z-ai', 'vision', '--prompt', PROMPT, '--image', img_path, '--output', '/tmp/vlm_out.json'],
                        capture_output=True, text=True, timeout=120
                    )
                else:
                    time.sleep(3)
                    continue
            
            if result.returncode == 0:
                with open('/tmp/vlm_out.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                choices = data.get('choices', [])
                if choices:
                    msg = choices[0].get('message', {})
                    content = msg.get('content', '')
                    if isinstance(content, list):
                        text_parts = []
                        for c in content:
                            if isinstance(c, dict) and c.get('type') == 'text':
                                text_parts.append(c.get('text', ''))
                        content = '\n'.join(text_parts)
                    content = content.strip()
                    if content and '[ERROR' not in content:
                        return content
            
            time.sleep(2)
        except subprocess.TimeoutExpired:
            time.sleep(5)
        except Exception as e:
            time.sleep(3)
    
    return f"[FAILED after {max_retries} retries]"


def ocr_page(page_idx, doc):
    """OCR a single page."""
    out_path = f"{OUT_DIR}/page_{page_idx+1:04d}.txt"
    if os.path.exists(out_path) and os.path.getsize(out_path) > 50:
        return "skipped"
    
    # Render page to image
    page = doc[page_idx]
    mat = fitz.Matrix(DPI/72, DPI/72)
    pix = page.get_pixmap(matrix=mat)
    
    # Save as PNG temporarily
    img_path = f"/tmp/vlm_page_{page_idx+1}.png"
    pix.save(img_path)
    
    # OCR with VLM
    text = ocr_page_with_vlm(img_path)
    
    # Save text
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    # Cleanup
    try:
        os.remove(img_path)
    except:
        pass
    del pix
    return "done"


def main():
    start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    end_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    
    doc = fitz.open(PDF)
    total = doc.page_count
    end_idx = min(end_idx, total)
    
    print(f"VLM OCR pages {start_idx+1} to {end_idx} (of {total}) at {DPI} DPI", flush=True)
    start = time.time()
    done = 0
    
    for i in range(start_idx, end_idx):
        status = ocr_page(i, doc)
        done += 1
        if done % 3 == 0 or 'error' in status:
            elapsed = time.time() - start
            rate = done / elapsed if elapsed > 0 else 0
            eta = (end_idx - start_idx - done) / rate if rate > 0 else 0
            print(f"  [{done}/{end_idx-start_idx}] page {i+1}: {status} ({elapsed:.0f}s, ETA {eta:.0f}s)", flush=True)
        if done % 10 == 0:
            gc.collect()
    
    doc.close()
    elapsed = time.time() - start
    print(f"Done! {done} pages in {elapsed:.1f}s ({done/elapsed:.1f} pg/s)")


if __name__ == "__main__":
    main()
