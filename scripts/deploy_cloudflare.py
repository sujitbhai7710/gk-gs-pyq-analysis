#!/usr/bin/env python3
"""
Deploy website to Cloudflare Pages using Direct Upload API.
Properly builds manifest with SHA-256 hashes for each file.
"""
import os
import hashlib
import json
import requests
import sys

# Read credentials from environment variables
CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ACCT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
PROJECT = os.environ.get("CLOUDFLARE_PROJECT_NAME", "gk-gs-pyq-analysis")
DEPLOY_DIR = "/tmp/website_deploy"

if not CF_TOKEN or not ACCT_ID:
    print("ERROR: Set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID env vars")
    sys.exit(1)

def get_file_hash(filepath):
    """Get SHA-256 hash of file content (hex)."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    if not os.path.isdir(DEPLOY_DIR):
        print(f"ERROR: {DEPLOY_DIR} not found")
        sys.exit(1)
    
    # Collect all files
    files_to_upload = []
    for root, dirs, files in os.walk(DEPLOY_DIR):
        for fname in files:
            if fname.startswith('.'):
                continue
            filepath = os.path.join(root, fname)
            relpath = os.path.relpath(filepath, DEPLOY_DIR)
            # Use forward slashes for Cloudflare
            relpath = relpath.replace(os.sep, '/')
            files_to_upload.append((relpath, filepath))
    
    print(f"Found {len(files_to_upload)} files to upload")
    
    # Build manifest: { "path/to/file": "sha256-hash" }
    # Cloudflare expects NO leading slash in manifest keys
    manifest = {}
    file_hashes = {}
    for relpath, filepath in files_to_upload:
        file_hash = get_file_hash(filepath)
        # Cloudflare expects hash with "/" prefix for paths
        manifest[relpath] = file_hash
        file_hashes[relpath] = file_hash
        size_kb = os.path.getsize(filepath) / 1024
        print(f"  {relpath}: {size_kb:.1f} KB, sha256={file_hash[:16]}...")
    
    # Prepare multipart form data
    # Cloudflare API expects:
    # - "manifest" field: JSON string of {"path": "hash"} mapping
    # - One field per file with key=path, value=file content
    
    files_payload = []
    files_payload.append(('manifest', (None, json.dumps(manifest), 'application/json')))
    
    for relpath, filepath in files_to_upload:
        # Key must match manifest key (no leading /)
        files_payload.append((relpath, (relpath, open(filepath, 'rb'), 'application/octet-stream')))
    
    print(f"\nUploading {len(files_to_upload)} files to Cloudflare Pages...")
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCT_ID}/pages/projects/{PROJECT}/deployments"
    headers = {"Authorization": f"Bearer {CF_TOKEN}"}
    
    response = requests.post(url, headers=headers, files=files_payload, timeout=300)
    
    print(f"\nHTTP Status: {response.status_code}")
    
    try:
        result = response.json()
    except:
        print(f"Response: {response.text[:1000]}")
        return
    
    if result.get('success'):
        deployment = result['result']
        print(f"\n✓ DEPLOYMENT SUCCESSFUL!")
        print(f"  Deployment ID: {deployment.get('id')}")
        print(f"  URL: https://{deployment.get('url', '').replace('https://', '')}")
        print(f"  Environment: {deployment.get('environment')}")
        print(f"\n  Production URL: https://{PROJECT}.pages.dev")
        
        # Save deployment info
        with open('/home/z/my-project/data/deployment_info.json', 'w') as f:
            json.dump(deployment, f, indent=2)
    else:
        print(f"\n✗ DEPLOYMENT FAILED")
        print(f"Errors: {json.dumps(result.get('errors', []), indent=2)}")

if __name__ == "__main__":
    main()
