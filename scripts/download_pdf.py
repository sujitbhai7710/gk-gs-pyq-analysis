#!/usr/bin/env python3
"""Download GK/GS PYQ PDF from Google Drive."""
import gdown
import os

FILE_ID = "1no_Hvs2e3aBy-VrHvecGiYZixGHVuUUw"
OUTPUT = "/home/z/my-project/download/gk_gs_pyq.pdf"

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

# Try direct download
url = f"https://drive.google.com/uc?id={FILE_ID}"
print(f"Downloading from: {url}")
try:
    gdown.download(url, OUTPUT, quiet=False)
except Exception as e:
    print(f"First attempt failed: {e}")
    # Try with fuzzy URL
    url2 = f"https://drive.google.com/file/d/{FILE_ID}/view"
    print(f"Trying fuzzy: {url2}")
    gdown.download(url2, OUTPUT, quiet=False, fuzzy=True)

if os.path.exists(OUTPUT):
    size_mb = os.path.getsize(OUTPUT) / (1024 * 1024)
    print(f"\nDownloaded: {OUTPUT}")
    print(f"Size: {size_mb:.2f} MB")
else:
    print("Download failed!")
