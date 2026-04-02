#!/bin/bash
# deploy.sh — Deploy Internet Era to Google Cloud Run
# Usage: ./deploy.sh
# Prerequisites: gcloud CLI installed, authenticated
set -euo pipefail

PROJECT_ID="${GCP_PROJECT_ID:?Error: Set GCP_PROJECT_ID env var. Example: export GCP_PROJECT_ID=internet-era-12345}"
REGION="us-central1"

echo "============================================"
echo "  Deploying Internet Era Backend"
echo "============================================"
echo "  Project: $PROJECT_ID"
echo "  Region: $REGION"
echo "============================================"

# Build and push to Container Registry
echo ""
echo "[1/3] Building Docker image..."
docker build -t "gcr.io/$PROJECT_ID/internet-era:latest" backend/

echo "[2/3] Pushing to Google Container Registry..."
docker push "gcr.io/$PROJECT_ID/internet-era:latest"

echo "[3/3] Deploying to Cloud Run..."
gcloud run deploy internet-era \
  --image "gcr.io/$PROJECT_ID/internet-era:latest" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars "OPENROUTER_API_KEY=$OPENROUTER_API_KEY" \
  --service-account "internet-era@$PROJECT_ID.iam.gserviceaccount.com" \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 50 \
  --timeout 60s \
  --port 8080

SERVICE_URL=$(gcloud run services describe internet-era --platform managed --region "$REGION" --format="value(status.url)")

echo ""
echo "============================================"
echo "  DEPLOYED!"
echo "============================================"
echo "  Backend URL: $SERVICE_URL"
echo ""
echo "  Now update your frontend API_URL:"
echo "  Open static/index.html"
echo "  Change: const API = '/api/analyze';"
echo "  To:     const API = '$SERVICE_URL/analyze';"
echo "============================================"

# Deploy frontend to Cloudflare Pages
echo ""
echo "To deploy frontend to Cloudflare Pages:"
echo "1. Run: npx wrangler pages deploy static --project-name=internet-era"
echo "   (requires Cloudflare CLI: npm install -g wrangler)"
echo "============================================"
