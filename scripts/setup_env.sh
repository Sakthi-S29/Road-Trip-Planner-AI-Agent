#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# setup_env.sh
# Enables required GCP APIs and writes the .env file
# Usage: bash scripts/setup_env.sh
# ─────────────────────────────────────────────────────────────────────────────

set -e

PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"

echo "Setting up environment for project: $PROJECT_ID"
echo ""

# ── Enable required APIs ──────────────────────────────────────────────────────
echo "Enabling required GCP APIs..."
gcloud services enable \
  bigquery.googleapis.com \
  bigquerystorage.googleapis.com \
  maps-backend.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  --project="$PROJECT_ID"

echo "APIs enabled."
echo ""

# ── Write .env file ───────────────────────────────────────────────────────────
echo "Writing .env file..."
cat > .env << EOF
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_CLOUD_REGION=$REGION

# Paste your Maps API key here (must have Maps JavaScript API enabled)
# Get it from: https://console.cloud.google.com/apis/credentials
MAPS_API_KEY=YOUR_MAPS_API_KEY_HERE
EOF

echo ".env file written."
echo ""
echo "ACTION REQUIRED: Open .env and replace YOUR_MAPS_API_KEY_HERE with your actual key."
echo ""
echo "Environment setup complete!"
