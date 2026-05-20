# TEAMS - Tiger-AI Effectiveness Assessment & Monitoring System

An analytical dashboard for monitoring Project Tiger conservation efforts across India's 58 tiger reserves.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-purple)

## Features

### Page 1 — National Overview
- Interactive India map with all 58 tiger reserves as bubbles (colored by density, sized by population)
- 4 stat cards: Total Tigers 2022, Growth %, Most Improved, Most At-Risk
- National tiger population trend line (1973–2022) with census annotations

### Page 2 — Reserve Explorer
- Sidebar dropdown to select any reserve
- Population history bar chart (2006–2022)
- Reserve stats: area, state, poaching incidents, conflict count, habitat health
- Status badge: Healthy / At Risk / Underperforming

### Page 3 — Threat Analysis
- Poaching incident bubble map (size = incidents, color = severity)
- Human-tiger conflict heatmap by reserve and year
- Year range slider filter
- Top 10 reserves by poaching incidents

### Page 4 — Habitat Health
- Side-by-side NDVI maps (2015 vs 2022) with reserve highlighting
- Habitat fragmentation score bar chart
- Forest cover trend line (FSI data)

### Page 5 — Predictions
- ARIMA forecast chart (predicted population to 2026 with confidence interval)
- Regression output table showing underperforming reserves
- At-risk reserves flagged with reasons

## Tech Stack
- **Streamlit** — App framework and UI
- **Plotly Express** — All interactive charts
- **Plotly scatter_mapbox** — Maps with carto-positron tiles
- **Pandas** — Data processing
- **NumPy** — Numerical computations

## Project Structure
```
teams-dashboard/
├── .streamlit/
│   └── config.toml          # Dark theme configuration
├── app.py                    # Main entry point (home page)
├── pages/
│   ├── 01_national_overview.py
│   ├── 02_reserve_explorer.py
│   ├── 03_threat_analysis.py
│   ├── 04_habitat_health.py
│   └── 05_predictions.py
├── data/
│   ├── reserves.csv
│   ├── census.csv
│   ├── poaching.csv
│   ├── conflict.csv
│   ├── habitat.csv
│   └── predictions.csv
├── utils/
│   ├── __init__.py
│   ├── data_loader.py        # Cached data loading functions
│   └── map_utils.py          # Map helpers, card components, CSS
├── generate_data.py           # Dummy data generator
├── requirements.txt
└── README.md
```

## Setup

### Local Development
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Cloud
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `app.py` as the main file
4. Deploy — it will auto-install from `requirements.txt`

## Data Format

The app expects CSV files in `/data/` with these exact columns:

| File | Columns |
|------|---------|
| `reserves.csv` | reserve_name, state, latitude, longitude, core_area_km2, buffer_area_km2 |
| `census.csv` | reserve_name, year, population |
| `poaching.csv` | reserve_name, year, incidents, severity |
| `conflict.csv` | reserve_name, year, human_deaths, cattle_kills |
| `habitat.csv` | reserve_name, ndvi_2015, ndvi_2022, fragmentation_score |
| `predictions.csv` | reserve_name, predicted_population, performance_index, at_risk |

Drop real CSVs into the `/data/` folder with matching column names — no code changes needed.

## Design
- **Theme**: Dark mode throughout
- **Primary**: Deep forest green `#1B4332`
- **Accent**: Amber `#F59E0B`
- **Alert**: Red `#EF4444`
- **Typography**: Inter (Google Fonts)
- **Charts**: Plotly only (no matplotlib)

## License
Built for Project Tiger conservation research and analysis.
