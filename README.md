# Road Trip Planner — ADK Agent with MCP

An AI road trip planner built with **Google ADK**, connecting **BigQuery** and 
**Google Maps MCP** to generate precise, hour-by-hour itineraries personalised 
to the user's vehicle and departure time.

---

## What It Does

**Input:** "I'm driving a Tesla Model Y from Toronto to Montreal on July 5th, leaving at 8am."

**Output:** A complete itinerary with exact clock times, named charging stops 
(with kW, stall count, charge duration), specific restaurants near each stop 
timed to actual meal hours, fuel/charge math shown, and a Maps link.

---

## Architecture

```
User Query
    │
    ▼
ADK LlmAgent (Gemini 2.0 Flash)
    │
    ├── BigQuery MCP
    │     vehicles table          ← fuel efficiency, tank size, EV range,
    │                                charge time, compatible networks
    │     charging_stations table ← charger network, kW, stalls, wait time
    │
    └── Google Maps MCP
          Route distance + drive time
          Restaurants near each stop (live, with hours + ratings)
          Gas stations along the highway
          Attractions and landmarks
          Map links
```

**Why BigQuery for only two tables?**

Google Maps can handle routes, restaurants, gas stations, and attractions live — 
that data is richer and always current from Maps. BigQuery fills the two gaps 
Maps cannot:

| Data | Why Maps cannot provide it |
|---|---|
| Vehicle fuel consumption (L/100km) | Maps has no vehicle database |
| Tank capacity | Maps has no vehicle database |
| EV rated range | Maps has no vehicle database |
| Charger power output (kW) | Maps shows pins, not specs |
| Charger connector type (CCS vs Tesla) | Maps does not expose this |
| Number of stalls / typical wait | Maps does not expose this |

The difference between a 50kW FLO stop and a 250kW Tesla Supercharger is 
45 minutes on an itinerary. That data lives in BigQuery.

---

## Project Structure

```
road_trip_agent/
├── mcp_road_trip_app/
│   ├── __init__.py
│   ├── agent.py          # LlmAgent definition + planning prompt
│   └── tools.py          # Maps and BigQuery MCP toolset builders
├── data/
│   ├── generate_datasets.py    # Run this to regenerate CSVs
│   ├── vehicles.csv            # 51 vehicles (gasoline, hybrid, PHEV, EV)
│   └── charging_stations.csv  # 40 EV charging stations across ON/QC corridors
├── scripts/
│   ├── setup_env.sh            # Enable APIs, write .env
│   ├── setup_bigquery.sh       # Load CSVs into BigQuery
│   └── deploy_cloudrun.sh      # Build and deploy to Cloud Run
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Setup

### 1. Clone and open in Cloud Shell
```bash
git clone <your-repo-url>
cd road_trip_agent
```

### 2. Enable APIs and configure environment
```bash
bash scripts/setup_env.sh
```
Open `.env` and paste your Maps API key (requires Maps JavaScript API + Places API).

### 3. Load data into BigQuery
```bash
bash scripts/setup_bigquery.sh
```

### 4. Run locally
```bash
pip install -r requirements.txt
adk web mcp_road_trip_app
```

### 5. Deploy to Cloud Run
```bash
bash scripts/deploy_cloudrun.sh
```

---

## Example Prompts

```
I'm driving a Tesla Model Y from Toronto to Montreal on July 5th, 
leaving at 8am. Plan my trip.

Going from Ottawa to Toronto tomorrow in a Honda CR-V, leaving at 7am.
I want to stop for a proper lunch somewhere along the way.

Road trip in a Hyundai IONIQ 5 from Toronto to Quebec City next Saturday, 
departing 6am. What does the charging plan look like?

Taking my Ford F-150 from Montreal to Niagara Falls on a Sunday in October,
leaving after breakfast around 9am.
```

---

## Datasets

| Table | Rows | What it contains |
|---|---|---|
| vehicles | 51 | Make/model/year with fuel efficiency, tank size, EV range, charge time, compatible networks |
| charging_stations | 40 | EV chargers across Toronto–Montreal, Toronto–Ottawa, Montreal–Quebec City, and Niagara/Muskoka corridors — with network, kW, stalls, and wait time |
