# WindScope — Wind Generation Forecast Analysis

WindScope is a full-stack dashboard for analysing UK wind generation forecasts against actual generation. It is designed to help a day-ahead electricity buying team review forecast performance, understand forecast errors, and make more informed procurement decisions.

## Live Demo

- **Frontend:** https://wind-scope-phi.vercel.app/
- **Backend health check:** https://windscope-backend-ajat.onrender.com/api/health
- **January 2026 accuracy API:** https://windscope-backend-ajat.onrender.com/api/accuracy?start_date=2026-01-01&end_date=2026-01-31
- **Demo video:** `ADD_YOUR_UNLISTED_YOUTUBE_VIDEO_URL_HERE`

> The backend is hosted on Render and may take a short time to respond if its service has been idle.

## Features

- Daily overview of actual and forecast wind generation.
- Forecast-versus-actual visualisation.
- Forecast accuracy analysis for January 2026.
- Key metrics: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and bias.
- Python API for retrieving processed data.
- Docker Compose setup for local development and testing.

## Technology Stack

**Frontend**
- React
- Vite
- Tailwind CSS
- shadcn/ui components
- Recharts
- Lucide icons

**Backend**
- Python
- FastAPI
- pandas
- HTTPX

**Deployment and tooling**
- Vercel (frontend)
- Render (backend)
- Docker and Docker Compose
- Elexon BMRS API

## Data Sources

WindScope uses Elexon's BMRS API:

- **FUELHH** — actual generation data, filtered to wind generation: https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/FUELHH/stream
- **WINDFOR** — wind generation forecast data: https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/WINDFOR/stream

The analysis in this assignment is scoped to **January 2026**.

## Metrics and Methodology

- **MAE (Mean Absolute Error):** average absolute difference between forecast and actual generation.
- **RMSE (Root Mean Squared Error):** square root of the average squared forecast error; larger errors have a greater effect on this metric.
- **Bias:** average signed error. In this implementation, error is calculated as forecast minus actual, so positive bias indicates over-forecasting on average and negative bias indicates under-forecasting.

Actual FUELHH readings are half-hourly and are aggregated to hourly averages before matching them with hourly forecast values. Metrics are calculated over matched delivery intervals.

The current implementation uses a **previous-day 10:00 UTC forecast cutoff** for the day-ahead analysis. This is an implementation assumption and should be validated against the target team's operational procurement rules before production use.

The values shown by the deployed application are produced by the current implementation and source data. They should be interpreted in the context of the matching rules and assumptions above.

## API Endpoints

The backend provides the following endpoints:

| Endpoint | Purpose |
|---|---|
| `/` | Basic backend response |
| `/api/health` | Health check |
| `/api/overview?date=2026-01-01` | Daily overview |
| `/api/accuracy?start_date=2026-01-01&end_date=2026-01-31` | Accuracy metrics for a date range |
| `/api/forecasts?date=2026-01-01` | Forecast data for a selected date |

The date examples above are within the January 2026 assignment period.

## Repository Structure

```text
wind-scope/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── data_service.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   └── services/
│   │       └── api.js
│   ├── nginx.conf
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .gitignore
└── README.md
```

> This is a high-level overview of the main files. Other frontend source files and configuration files may also be present in the repository.

## Run Locally

### Prerequisites

- Git
- Docker Desktop with Docker Compose

### Option 1: Run with Docker Compose

1. Clone the repository:

   ```bash
   git clone YOUR_PUBLIC_GITHUB_REPOSITORY_URL
   cd YOUR_REPOSITORY_DIRECTORY
   ```

2. Build and start the services from the project root:

   ```bash
   docker compose up --build
   ```

3. Open the application:

   - Frontend: http://localhost:8080
   - Backend health check: http://localhost:8000/api/health

4. Stop the services with `Ctrl+C`. If you started them in detached mode, use:

   ```bash
   docker compose down
   ```

### Option 2: Run the services separately

**Backend**

From the repository root, create and activate a Python virtual environment, then install dependencies:

Windows Command Prompt:

```cmd
cd backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend**

Open a second terminal:

```cmd
cd frontend
npm install
npm run dev
```

The Vite development server typically runs at http://localhost:5173. The Vite configuration proxies `/api` requests to the local backend.

## Deployment Configuration

### Frontend — Vercel

Set this environment variable in the Vercel project settings for the relevant deployment environment:

```text
VITE_API_BASE_URL=https://windscope-backend-ajat.onrender.com
```

Redeploy the frontend after changing the variable. Vite environment variables are embedded into the frontend at build time.

### Backend — Render

The backend is deployed at:

```text
https://windscope-backend-ajat.onrender.com
```

Ensure the FastAPI CORS configuration allows the deployed frontend origin:

```text
https://wind-scope-phi.vercel.app
```

Retain the local development origins if you still use the local Vite server.

## Limitations and Assumptions

- The analysis is limited to January 2026 for this assignment.
- Actual readings are aggregated from half-hourly to hourly averages; this may affect comparisons depending on the source data and chosen aggregation method.
- The previous-day 10:00 UTC forecast cutoff is an implementation assumption, not a confirmed operational requirement.
- Metrics depend on the source records available and the rules used to select and match forecasts with actuals.
- This is an analysis and decision-support dashboard. It does not place trades or automatically execute electricity purchases.
- Before operational use, the forecast selection cutoff, data quality handling, and procurement team's requirements should be validated.

## AI-Use Disclosure

AI assistance was used during development to support implementation, debugging, documentation, and preparation of the project demonstration. The code and resulting application should be reviewed and tested by the project author. Any AI-generated or AI-assisted material has been used as a development aid, and the author remains responsible for the final implementation and its claims.

## Demo Video

Add the URL of the unlisted YouTube demonstration here after uploading:

`ADD_YOUR_UNLISTED_YOUTUBE_VIDEO_URL_HERE`

The video should demonstrate the customer problem and dashboard first, followed by the technical architecture, data sources, processing methodology, deployment, and limitations.
