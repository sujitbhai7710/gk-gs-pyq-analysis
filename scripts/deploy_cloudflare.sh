#!/usr/bin/env bash
# Deploy all files to Cloudflare Pages via wrangler (recommended method)
# Usage: CLOUDFLARE_API_TOKEN=xxx CLOUDFLARE_ACCOUNT_ID=yyy ./deploy_cloudflare.sh
set -e

: "${CLOUDFLARE_API_TOKEN:?Need to set CLOUDFLARE_API_TOKEN}"
: "${CLOUDFLARE_ACCOUNT_ID:?Need to set CLOUDFLARE_ACCOUNT_ID}"

PROJECT="${CLOUDFLARE_PROJECT_NAME:-gk-gs-pyq-analysis}"
DEPLOY_DIR="${DEPLOY_DIR:-/tmp/website_deploy}"

if [ ! -d "$DEPLOY_DIR" ]; then
    echo "ERROR: Deploy directory $DEPLOY_DIR not found"
    exit 1
fi

echo "Deploying from $DEPLOY_DIR to Cloudflare Pages project: $PROJECT"
cd "$DEPLOY_DIR"

npx -y wrangler@latest pages deploy . \
    --project-name="$PROJECT" \
    --branch=main

echo ""
echo "✓ Deployment complete!"
echo "Production URL: https://$PROJECT.pages.dev/"
