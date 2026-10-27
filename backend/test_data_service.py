
from datetime import date

from app.data_service import (
    build_day_ahead_dataset,
    calculate_accuracy,
)

if __name__ == "__main__":
    df = build_day_ahead_dataset(
        date(2026, 1, 1),
        date(2026, 1, 3),
        cutoff_hour_utc=10,
    )

    print("\nDataset preview:")
    print(df.head(10).to_string(index=False))

    print("\nData quality:")
    print("Rows:", len(df))
    print("Matched forecasts:", df["forecast"].notna().sum())
    print("Missing forecasts:", df["forecast"].isna().sum())

    valid = df.dropna(subset=["actual", "forecast"])
    errors = valid["forecast"] - valid["actual"]

    print("\nError validation:")
    print("Positive errors:", (errors > 0).sum())
    print("Negative errors:", (errors < 0).sum())
    print("Zero errors:", (errors == 0).sum())
    print("Minimum error:", errors.min())
    print("Maximum error:", errors.max())

    print("\nAccuracy metrics:")
    print(calculate_accuracy(df))
