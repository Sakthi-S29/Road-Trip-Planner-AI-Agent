#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# setup_bigquery.sh — Creates BigQuery dataset and loads the two source tables
#
# Why only two tables?
#   vehicles          — Vehicle fuel efficiency and EV range data.
#                       Maps has no knowledge of this.
#   charging_stations — Charger network, power (kW), stalls, wait time.
#                       Maps shows pins but not the specs that determine
#                       how long you actually stop.
#
#   Routes, restaurants, gas stations, and attractions are served live
#   by Google Maps MCP — no static dataset needed or wanted.
# ─────────────────────────────────────────────────────────────────────────────

set -e

PROJECT_ID=$(gcloud config get-value project)
DATASET="mcp_road_trip"
REGION="US"
DATA_DIR="data"

echo "Project  : $PROJECT_ID"
echo "Dataset  : $DATASET"
echo ""

# ── Create dataset ─────────────────────────────────────────────────────────
echo "Creating BigQuery dataset..."
bq --location=$REGION mk --dataset \
  --description "Road Trip Planner – vehicle specs and EV charging data" \
  "$PROJECT_ID:$DATASET" 2>/dev/null || echo "Dataset already exists – skipping"

# ── Load tables ────────────────────────────────────────────────────────────
for TABLE in vehicles charging_stations; do
  echo ""
  echo "Loading $TABLE..."
  bq load \
    --autodetect \
    --source_format=CSV \
    --skip_leading_rows=1 \
    --replace \
    "$PROJECT_ID:$DATASET.$TABLE" \
    "$DATA_DIR/$TABLE.csv"
  echo "$TABLE loaded."
done

echo ""
echo "Verifying row counts:"
for TABLE in vehicles charging_stations; do
  COUNT=$(bq query --nouse_legacy_sql --format=csv \
    "SELECT COUNT(*) FROM \`$PROJECT_ID.$DATASET.$TABLE\`" 2>/dev/null | tail -1)
  echo "  $TABLE: $COUNT rows"
done

echo ""
echo "BigQuery setup complete."
