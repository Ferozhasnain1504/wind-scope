
import httpx
from collections import Counter

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"


def inspect_endpoint(path: str, params: dict) -> None:
    print(f"\n{'=' * 60}")
    print(f"Endpoint: {path}")

    try:
        response = httpx.get(
            f"{BASE_URL}{path}",
            params=params,
            timeout=60,
        )

        print("Request URL:", response.url)
        print("HTTP status:", response.status_code)
        response.raise_for_status()

        payload = response.json()

        if isinstance(payload, dict):
            records = payload.get("data", [])
        elif isinstance(payload, list):
            records = payload
        else:
            records = []

        print("Records returned:", len(records))

        if not records:
            print("No records returned. Check the date parameters.")
            return

        print("First record:", records[0])

        if path.endswith("FUELHH/stream"):
            fuel_counts = Counter(
                row.get("fuelType") for row in records
            )
            print("Fuel types in this response:", fuel_counts)

            wind_records = [
                row for row in records
                if row.get("fuelType") == "WIND"
            ]

            print("Wind records in response:", len(wind_records))

            if wind_records:
                print("First wind record:", wind_records[0])

        times = [
            row.get("startTime")
            for row in records
            if row.get("startTime")
        ]

        if times:
            print("Earliest startTime:", min(times))
            print("Latest startTime:", max(times))

        print("Available fields:", list(records[0].keys()))

    except httpx.HTTPError as exc:
        print("HTTP request failed:", exc)
    except (ValueError, TypeError) as exc:
        print("Could not parse response:", exc)



def inspect_forecast_history(publish_time: str) -> None:
    path = "/forecast/generation/wind/history"

    try:
        response = httpx.get(
            f"{BASE_URL}{path}",
            params={"publishTime": publish_time},
            timeout=60,
        )

        print("\nHistorical forecast endpoint")
        print("Request URL:", response.url)
        print("HTTP status:", response.status_code)
        response.raise_for_status()

        payload = response.json()

        if isinstance(payload, dict):
            records = payload.get("data", [])
        elif isinstance(payload, list):
            records = payload
        else:
            records = []

        print("Records returned:", len(records))

        if records:
            print("First record:", records[0])
            print(
                "Publication timestamps:",
                sorted({
                    row.get("publishTime")
                    for row in records
                    if row.get("publishTime")
                })[:10],
            )
        else:
            print("No forecast records returned.")

    except httpx.HTTPError as exc:
        print("Historical forecast request failed:", exc)


if __name__ == "__main__":
    inspect_endpoint(
        "/datasets/FUELHH/stream",
        {
            "settlementDateFrom": "2026-01-01",
            "settlementDateTo": "2026-01-02",
        },
    )

    inspect_endpoint(
        "/datasets/WINDFOR/stream",
        {
            "from": "2026-01-01T00:00:00Z",
            "to": "2026-01-02T00:00:00Z",
        },
    )

    inspect_forecast_history("2026-01-14T10:00:00Z")
