
from datetime import date, datetime, time, timedelta, timezone

import pandas as pd

from app.data_service import fetch_records, fetch_forecast_snapshot

start_date = date(2026, 1, 1)
end_date = date(2026, 1, 7)
cutoff_hour = 10

raw = fetch_records(
    "/datasets/WINDFOR/stream",
    {
        "publishDateTimeFrom": "2025-12-30T00:00:00Z",
        "publishDateTimeTo": "2026-01-07T10:00:00Z",
    },
)

stream = pd.DataFrame(raw)
stream["publishTime"] = pd.to_datetime(stream["publishTime"], utc=True)
stream["startTime"] = pd.to_datetime(stream["startTime"], utc=True)
stream["generation"] = pd.to_numeric(stream["generation"], errors="coerce")

for offset in range((end_date - start_date).days + 1):
    delivery_day = start_date + timedelta(days=offset)
    previous_day = delivery_day - timedelta(days=1)

    cutoff = datetime.combine(
        previous_day, time(cutoff_hour), tzinfo=timezone.utc
    )

    day_stream = stream[
        (stream["startTime"].dt.date == delivery_day)
        & (stream["publishTime"] <= pd.Timestamp(cutoff))
    ].sort_values("publishTime").drop_duplicates("startTime", keep="last")

    history = fetch_forecast_snapshot(cutoff)
    history = history[history["startTime"].dt.date == delivery_day]

    comparison = day_stream[["startTime", "generation"]].merge(
        history[["startTime", "forecast"]],
        on="startTime",
        how="outer",
        indicator=True,
    )

    differences = (
        comparison["generation"] - comparison["forecast"]
    ).abs()

    equal = (
        comparison["_merge"].eq("both").all()
        and differences.notna().all()
        and differences.le(0.01).all()
    )

    print(
        delivery_day,
        "| stream:", len(day_stream),
        "| history:", len(history),
        "| agree:", equal,
    )
