# WindScope

**Day-Ahead Wind Generation Forecast Analytics for UK Energy Buyers**

WindScope is a full-stack analytics dashboard designed to help a UK energy utility's day-ahead electricity buying team compare forecast wind generation with actual generation and evaluate forecast accuracy.

## Features

- UK national wind generation forecast and actual data sourced from the Elexon BMRS API.
- Interactive chart comparing hourly forecast and actual generation.
- Accuracy metrics: Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and forecast bias.
- January 2026 analysis window.
- FastAPI backend and React frontend.
- Docker support planned / in progress.

## Technology Stack

- **Frontend:** React, Vite, Tailwind CSS, shadcn/ui, Recharts
- **Backend:** Python, FastAPI, Pandas, HTTPX
- **Data source:** Elexon BMRS API
- **Deployment:** To be added after deployment

## Data Sources

WindScope uses Elexon's API for:

- **Actual generation:** `FUELHH`, filtered to the `WIND` fuel type.
- **Forecast generation:** `WINDFOR` historical wind forecast records.

Official API documentation:
- [FUELHH dataset](https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/FUELHH/stream)
- [WINDFOR dataset](https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/WINDFOR/stream)

## Forecast Evaluation Methodology

The current prototype uses a **10:00 UTC cutoff on the day before delivery** as an assumed day-ahead decision time.

1. Retrieve historical wind forecast publications available by the assumed cutoff.
2. Select the latest eligible forecast for each delivery timestamp.
3. Retrieve actual wind generation.
4. Aggregate half-hourly actual readings into hourly averages.
5. Match forecasts and actuals by UTC delivery timestamp.
6. Calculate forecast errors as:

   `Error = Forecast - Actual`

Metrics:

- **MAE:** Mean absolute error, in MW.
- **RMSE:** Root mean square error, in MW.
- **Bias:** Mean forecast error, in MW. Positive bias means forecasts exceed actual generation on average.

The cutoff time is an assumption and should be confirmed against the customer's intended purchasing decision time before operational use. The current implementation is a prototype, not a trading recommendation.

## January 2026 Results

The current API returns the following metrics for 1–31 January 2026:

| Metric | Value |
|---|---:|
| MAE | 2,122.81 MW |
| RMSE | 2,616.69 MW |
| Bias | +1,840.30 MW |
| Matched hourly intervals | 744 |
| Missing forecasts | 0 |

These values are results from the current implementation and its stated cutoff assumption. They should be revalidated if the data-selection methodology or cutoff changes.

## Project Structure

```text
windscope/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── data/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── data_service.py
│   ├── requirements.txt
│   └── check_forecast.py
└── README.md
```

Additional diagnostic scripts may be present in the backend folder.

## Run Locally

### Requirements

- Node.js and npm
- Python 3.11 or a compatible supported version
- Internet access to retrieve Elexon API data

### 1. Start the backend

Open a terminal in the project root:

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Backend API: `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

### 2. Start the frontend

Open a second terminal:

```bat
cd frontend
npm install
npm run dev
```

Open the local frontend URL printed by Vite, normally `http://localhost:5173`.

### API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Backend health check |
| `GET /api/overview?date=2026-01-01` | Daily generation data and metrics |
| `GET /api/accuracy?start_date=2026-01-01&end_date=2026-01-31` | Accuracy metrics for a date range |
| `GET /api/forecasts?date=2026-01-01` | Forecast and actual records for a delivery day |

The prototype currently restricts analysis to January 2026.

## Deployment

Deployment URL: **To be added after successful deployment.**

## AI Use Disclosure

AI assistance was used during development for code drafting, debugging, API integration guidance, data validation steps, and documentation preparation. The project was tested locally, and the data-selection and evaluation assumptions are documented above.

## Limitations and Future Improvements

- Confirm the day-ahead purchasing decision cutoff with the intended customer.
- Validate the forecast product and delivery-period semantics against Elexon's documentation.
- Add automated tests for API parsing, timestamp alignment, and accuracy calculations.
- Improve error handling and caching for API requests.
- Complete and test Docker configuration.
- Deploy the frontend and backend and document the live URLs.
