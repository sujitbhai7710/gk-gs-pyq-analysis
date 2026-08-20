#!/usr/bin/env python3
"""Extract images from a sample page to understand structure."""
import pdfplumber
import os
from PIL import Image
import io

PDF = "/home/z/my-project/download/gk_gs_pyq.pdf"
OUT = "/home/z/my-project/data/sample_images"
os.makedirs(OUT, exist_ok=True)

# Try using PyMuPDF (fitz) which is faster and better for image extraction
import fitz  # PyMuPDF

doc = fitz.open(PDF)
print(f"Total pages: {doc.page_count}")

# Extract images from page 2 (index 1) which had 17 images
for page_idx in [1, 2, 25]:
    page = doc[page_idx]
    images = page.get_images(full=True)
    print(f"\nPage {page_idx+1}: {len(images)} images")
    
    for img_idx, img in enumerate(images[:5]):  # First 5 only
        xref = img[0]
        try:
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save image
            img_path = f"{OUT}/page{page_idx+1}_img{img_idx+1}.{image_ext}"
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            
            # Get dimensions
            img_pil = Image.open(io.BytesIO(image_bytes))
            print(f"  Image {img_idx+1}: {img_pil.size}, ext={image_ext}, size={len(image_bytes)} bytes")
        except Exception as e:
            print(f"  Image {img_idx+1}: ERROR - {e}")

doc.close()
