"""
PDF Vision OCR using Google Gemini Flash.

This script reads a multi-page bilingual (English+Hindi) PDF page-by-page,
sends each rendered page image to Gemini Flash, and extracts ONLY the English
text - skipping Hindi, watermarks (e.g. www.XamToppr.com), and noise.

Memory-safe: processes pages in batches of 10.
Output: final_output.txt with structured Markdown per page.

Usage:
    GEMINI_API_KEY=your_key python process_pdf.py [input.pdf] [output.txt]

Environment variables:
    GEMINI_API_KEY   (required) Google AI Studio API key
    PDF_FILE         (optional) Path to input PDF, default: input.pdf
    OUTPUT_FILE      (optional) Path to output text, default: final_output.txt
    BATCH_SIZE       (optional) Pages per batch, default: 10
    DPI              (optional) Render DPI, default: 150
    START_PAGE       (optional) Start from this page (1-indexed), default: 1
    END_PAGE         (optional) Stop at this page, default: last page
"""
import os
import sys
import time
import pypdf
from google import genai
from pdf2image import convert_from_path
from PIL import Image

# --- Configuration ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY secret is missing! Set it in GitHub Actions secrets or env.")

PDF_FILE = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PDF_FILE", "input.pdf")
OUTPUT_FILE = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("OUTPUT_FILE", "final_output.txt")
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "10"))
DPI = int(os.environ.get("DPI", "150"))
START_PAGE = int(os.environ.get("START_PAGE", "1"))
END_PAGE = int(os.environ.get("END_PAGE", "0"))  # 0 = last page

# Initialize Gemini Client
client = genai.Client(api_key=API_KEY)

OCR_PROMPT = (
    "You are an expert OCR system. Extract ONLY the English text from this image page. "
    "Do NOT extract any Hindi/Devanagari script. "
    "Ignore watermarks like 'www.XamToppr.com', 'cbexams.com' URLs, and page headers/footers. "
    "Preserve the original structure exactly: Question Numbers (e.g., 'Q.No: 27'), "
    "Statement numbering (1., 2., 3.), all four answer options on separate lines, "
    "and any 'Not Answered' markers. "
    "Output ONLY the extracted English text - no introduction, no explanation, no commentary."
)


def extract_english_from_image(img):
    """
    Send page image to Gemini Flash to extract ONLY English text.
    Skips Hindi, watermarks, and header/footer noise.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[OCR_PROMPT, img]
    )
    return response.text.strip()


def process_pdf():
    # Get total page count
    reader = pypdf.PdfReader(PDF_FILE)
    total_pages = len(reader.pages)
    end_page = END_PAGE if END_PAGE > 0 else total_pages
    print(f"Total pages in PDF: {total_pages}")
    print(f"Processing range: {START_PAGE} to {end_page}")
    print(f"Batch size: {BATCH_SIZE}, DPI: {DPI}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        out_f.write(f"=== OCR EXTRACTION RESULT ({total_pages} PAGES) ===\n")
        out_f.write(f"=== Source: {PDF_FILE} ===\n")
        out_f.write(f"=== Tool: Google Gemini Flash ===\n\n")

        for start_page in range(START_PAGE, end_page + 1, BATCH_SIZE):
            batch_end = min(start_page + BATCH_SIZE - 1, end_page)
            print(f"\n[Batch] Processing pages {start_page} to {batch_end}...", flush=True)

            try:
                images = convert_from_path(
                    PDF_FILE,
                    first_page=start_page,
                    last_page=batch_end,
                    dpi=DPI
                )
            except Exception as e:
                print(f"  [ERROR] Failed to render batch {start_page}-{batch_end}: {e}")
                for p in range(start_page, batch_end + 1):
                    out_f.write(f"--- PAGE {p} [FAILED TO RENDER] ---\n\n")
                out_f.flush()
                continue

            for i, img in enumerate(images):
                page_num = start_page + i
                if page_num > end_page:
                    break
                print(f"  -> Page {page_num}/{end_page}...", flush=True)

                try:
                    text = extract_english_from_image(img)
                    out_f.write(f"--- PAGE {page_num} ---\n")
                    out_f.write(text + "\n\n")
                    out_f.flush()
                except Exception as e:
                    print(f"  [ERROR] Page {page_num}: {e}")
                    out_f.write(f"--- PAGE {page_num} [FAILED: {e}] ---\n\n")
                    out_f.flush()

                # Rate limit safety
                time.sleep(1)

    print(f"\n✓ Complete! Output saved to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    process_pdf()
