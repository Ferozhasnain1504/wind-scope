
from datetime import date

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.data_service import (
    build_day_ahead_dataset,
    calculate_accuracy,
)

app = FastAPI(
    title="WindScope API",
    description="UK wind generation forecast analytics",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://wind-scope-phi.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def load_dataset(start_date: date, end_date: date) -> pd.DataFrame:
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be before or equal to end_date",
        )

    if start_date < date(2026, 1, 1) or end_date > date(2026, 1, 31):
        raise HTTPException(
            status_code=400,
            detail="This pilot supports January 2026 only",
        )

    try:
        return build_day_ahead_dataset(
            start_date,
            end_date,
            cutoff_hour_utc=10,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not retrieve Elexon data: {exc}",
        ) from exc


def serialize_records(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []

    output = df.copy()

    for column in output.columns:
        if pd.api.types.is_datetime64_any_dtype(output[column]):
            output[column] = output[column].map(
                lambda value: (
                    value.isoformat()
                    if pd.notna(value)
                    else None
                )
            )

    output = output.astype(object).where(pd.notna(output), None)

    return output.to_dict(orient="records")


@app.get("/")
def root():
    return {
        "app": "WindScope API",
        "status": "running",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "windscope-backend",
    }


@app.get("/api/overview")
def overview(
    delivery_date: date = Query(
        alias="date",
        description="Delivery date in January 2026",
    ),
):
    df = load_dataset(delivery_date, delivery_date)
    metrics = calculate_accuracy(df)

    matched = df.dropna(subset=["actual", "forecast"])

    return {
        "delivery_date": delivery_date.isoformat(),
        "resolution": "hourly forecast timestamps",
        "forecast_cutoff": "10:00 UTC on the previous day",
        "metrics": metrics,
        "data": serialize_records(df),
        "matched_intervals": len(matched),
    }


@app.get("/api/accuracy")
def accuracy(
    start_date: date = Query(
        default=date(2026, 1, 1)
    ),
    end_date: date = Query(
        default=date(2026, 1, 31)
    ),
):
    df = load_dataset(start_date, end_date)

    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "resolution": "hourly forecast timestamps",
        "metrics": calculate_accuracy(df),
    }


@app.get("/api/forecasts")
def forecasts(
    delivery_date: date = Query(
        alias="date",
        description="Delivery date in January 2026",
    ),
):
    df = load_dataset(delivery_date, delivery_date)

    return {
        "delivery_date": delivery_date.isoformat(),
        "records": serialize_records(df),
    }
