
from datetime import date

from app.data_service import build_day_ahead_dataset, calculate_accuracy

df = build_day_ahead_dataset(
    date(2026, 1, 1),
    date(2026, 1, 7),
    cutoff_hour_utc=10,
)

print("\n--- Data quality report: Jan 1–7, 2026 ---")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

if df.empty:
    print("No data returned.")
else:
    print("\nFirst five rows:")
    print(df.head().to_string(index=False))

    valid = df.dropna(subset=["actual", "forecast"]).copy()

    print("\n--- Generation summary (MW) ---")
    print("Average actual:", round(valid["actual"].mean(), 2))
    print("Average forecast:", round(valid["forecast"].mean(), 2))
    print("Minimum actual:", round(valid["actual"].min(), 2))
    print("Maximum actual:", round(valid["actual"].max(), 2))
    print("Minimum forecast:", round(valid["forecast"].min(), 2))
    print("Maximum forecast:", round(valid["forecast"].max(), 2))

    print("\n--- Error checks ---")
    errors = valid["forecast"] - valid["actual"]
    print("Positive errors:", int((errors > 0).sum()))
    print("Negative errors:", int((errors < 0).sum()))
    print("Zero errors:", int((errors == 0).sum()))
    print("Correlation:", round(valid["forecast"].corr(valid["actual"]), 3))

    print("\n--- Accuracy metrics ---")
    print(calculate_accuracy(df))

    print("\n--- Publication times ---")
    if "publishTime" in valid.columns:
        print(
            valid["publishTime"]
            .value_counts()
            .sort_index()
            .to_string()
        )
