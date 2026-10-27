
from datetime import date, datetime, timezone

from app.data_service import fetch_actual_wind, fetch_forecast_snapshot

day = date(2026, 1, 1)

actuals = fetch_actual_wind(day, day)
cutoff = datetime(2025, 12, 31, 10, 0, tzinfo=timezone.utc)
forecasts = fetch_forecast_snapshot(cutoff)

print("ACTUALS")
print("Rows:", len(actuals))
print("First 6 timestamps:")
print(actuals.head(6).to_string(index=False))

print("\nFORECASTS")
print("Rows:", len(forecasts))
print("First 6 timestamps:")
print(forecasts[forecasts["startTime"].dt.date == day]
      .head(6).to_string(index=False))

print("\nForecast timestamp minutes:")
print(forecasts["startTime"].dt.minute.value_counts().sort_index())
