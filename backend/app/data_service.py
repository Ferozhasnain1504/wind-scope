
from datetime import date, datetime, timedelta, timezone

import httpx
import pandas as pd

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"


def fetch_records(path: str, params: dict) -> list[dict]:
    """Fetch records from an Elexon API endpoint."""
    response = httpx.get(
        f"{BASE_URL}{path}",
        params=params,
        timeout=60,
    )
    response.raise_for_status()

    payload = response.json()

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        return payload.get("data", [])

    return []



def fetch_actual_wind(
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Fetch half-hourly wind actuals and aggregate them into hourly means."""
    records = fetch_records(
        "/datasets/FUELHH/stream",
        {
            "settlementDateFrom": start_date.isoformat(),
            "settlementDateTo": end_date.isoformat(),
        },
    )

    df = pd.DataFrame(records)

    if df.empty:
        return pd.DataFrame(columns=["startTime", "actual"])

    df = df[df["fuelType"] == "WIND"].copy()

    if df.empty:
        return pd.DataFrame(columns=["startTime", "actual"])

    df["startTime"] = pd.to_datetime(df["startTime"], utc=True)
    df["actual"] = pd.to_numeric(df["generation"], errors="coerce")

    df = (
        df[["startTime", "actual"]]
        .dropna()
        .drop_duplicates("startTime", keep="last")
        .sort_values("startTime")
        .copy()
    )

    # Combine 00:00 and 00:30 into the hourly mean for 00:00.
    df["startTime"] = df["startTime"].dt.floor("h")

    df = (
        df.groupby("startTime", as_index=False)
        .agg(actual=("actual", "mean"))
        .sort_values("startTime")
        .reset_index(drop=True)
    )

    return df


def fetch_forecast_snapshot(
    requested_publish_time: datetime,
) -> pd.DataFrame:
    """Fetch the historical forecast snapshot applicable to a cutoff."""
    if requested_publish_time.tzinfo is None:
        requested_publish_time = requested_publish_time.replace(
            tzinfo=timezone.utc
        )

    records = fetch_records(
        "/forecast/generation/wind/history",
        {
            "publishTime": requested_publish_time.astimezone(
                timezone.utc
            ).isoformat(timespec="seconds").replace("+00:00", "Z"),
        },
    )

    df = pd.DataFrame(records)

    if df.empty:
        return pd.DataFrame(
            columns=["startTime", "publishTime", "forecast"]
        )

    df["startTime"] = pd.to_datetime(
        df["startTime"], utc=True
    )
    df["publishTime"] = pd.to_datetime(
        df["publishTime"], utc=True
    )
    df["forecast"] = pd.to_numeric(
        df["generation"], errors="coerce"
    )

    # Never accept a publication later than the requested cutoff.
    df = df[df["publishTime"] <= pd.Timestamp(
        requested_publish_time
    ).tz_convert("UTC")]

    return (
        df[["startTime", "publishTime", "forecast"]]
        .dropna(subset=["startTime", "publishTime", "forecast"])
        .sort_values(["startTime", "publishTime"])
        .drop_duplicates("startTime", keep="last")
        .reset_index(drop=True)
    )


def build_day_ahead_dataset(
    start_date: date,
    end_date: date,
    cutoff_hour_utc: int = 10,
) -> pd.DataFrame:
    """
    Match actual wind generation with the forecast available
    at the configured UTC cutoff on the previous day.

    This is an explicit pilot assumption, not a claim about
    the official UK trading deadline.
    """
    actuals = fetch_actual_wind(start_date, end_date)

    if actuals.empty:
        return pd.DataFrame()

    snapshots = []

    delivery_day = start_date

    while delivery_day <= end_date:
        previous_day = delivery_day - timedelta(days=1)

        cutoff = datetime(
            previous_day.year,
            previous_day.month,
            previous_day.day,
            cutoff_hour_utc,
            tzinfo=timezone.utc,
        )

        snapshot = fetch_forecast_snapshot(cutoff)

        if not snapshot.empty:
            # Keep only the requested delivery date.
            snapshot = snapshot[
                snapshot["startTime"].dt.date == delivery_day
            ].copy()

            snapshots.append(snapshot)

        delivery_day += timedelta(days=1)

    if not snapshots:
        return actuals.assign(
            forecast=pd.NA,
            publishTime=pd.NaT,
            error=pd.NA,
        )

    forecasts = pd.concat(snapshots, ignore_index=True)

    forecasts = forecasts.drop_duplicates(
        "startTime", keep="last"
    )

    matched = actuals.merge(
        forecasts,
        on="startTime",
        how="left",
        validate="one_to_one",
    )

    matched["error"] = matched["forecast"] - matched["actual"]

    return matched.sort_values("startTime").reset_index(drop=True)


def calculate_accuracy(df: pd.DataFrame) -> dict:
    """Calculate metrics only for intervals with both values."""
    if df.empty or not {"actual", "forecast"}.issubset(df.columns):
        return {
            "mae": None,
            "rmse": None,
            "bias": None,
            "matched_intervals": 0,
            "missing_forecasts": 0,
        }

    valid = df.dropna(subset=["actual", "forecast"]).copy()

    if valid.empty:
        return {
            "mae": None,
            "rmse": None,
            "bias": None,
            "matched_intervals": 0,
            "missing_forecasts": len(df),
        }

    errors = valid["forecast"] - valid["actual"]

    return {
        "mae": round(float(errors.abs().mean()), 2),
        "rmse": round(float((errors.pow(2).mean()) ** 0.5), 2),
        "bias": round(float(errors.mean()), 2),
        "matched_intervals": int(len(valid)),
        "missing_forecasts": int(len(df) - len(valid)),
    }
