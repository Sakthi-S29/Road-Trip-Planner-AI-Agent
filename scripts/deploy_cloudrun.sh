#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# deploy_cloudrun.sh
# Builds and deploys the Road Trip Planner agent to Cloud Run
# Usage: bash scripts/deploy_cloudrun.sh
# ─────────────────────────────────────────────────────────────────────────────

set -e

source .env

PROJECT_ID=${GOOGLE_CLOUD_PROJECT}
REGION=${GOOGLE_CLOUD_REGION:-us-central1}
SERVICE_NAME="road-trip-planner"
IMAGE="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "Deploying $SERVICE_NAME to Cloud Run"
echo "Project: $PROJECT_ID | Region: $REGION"
echo ""

# ── Build container ───────────────────────────────────────────────────────────
echo "Building Docker image..."
gcloud builds submit \
  --tag "$IMAGE" \
  --project "$PROJECT_ID"

echo "Image built: $IMAGE"
echo ""

# ── Deploy to Cloud Run ───────────────────────────────────────────────────────
echo "Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,MAPS_API_KEY=$MAPS_API_KEY" \
  --project "$PROJECT_ID"

echo ""
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --format "value(status.url)")

echo "Deployment complete!"
echo "Service URL: $SERVICE_URL"
echo ""
echo "Test it:"
echo "  curl -X POST $SERVICE_URL/run \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"message\": \"I am driving a Tesla Model Y from Toronto to Montreal on December 25th, leaving at 8am. Plan my trip.\"}'"
