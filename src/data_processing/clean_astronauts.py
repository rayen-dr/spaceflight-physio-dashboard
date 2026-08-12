"""
clean_astronauts.py

Cleans the raw Kaggle "International Astronaut Database" and produces an
analysis-ready table for the dashboard's Astronaut Comparison and
Mission Comparison pages.

Input:  data/raw/astronaut_metadata.csv
Output: data/processed/astronauts_clean.csv

Key transformations:
- Parse "Total Flight Time (ddd:hh:mm)" into a numeric total_flight_days column
- Split the "Flights" text column into a clean list of individual mission names
- Bucket each astronaut into a career duration_category (Short / Medium / Long)
  based on cumulative flight time — NOT per-mission duration (see docs/data_sources.md
  for why per-mission duration isn't available in this dataset).
"""

import re
import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/astronaut_metadata.csv")
PROCESSED_PATH = Path("data/processed/astronauts_clean.csv")

# Career cumulative time-in-space brackets (days).
# These are intentionally different from the per-mission Short/Long brackets
# used in physiological_effects.csv — see docs/data_sources.md for the distinction.
DURATION_BINS = [-1, 14, 90, float("inf")]
DURATION_LABELS = ["Short (<14 days total)", "Medium (14-90 days total)", "Long (90+ days total)"]


def parse_flight_time_to_days(value: str) -> float:
    """Convert 'ddd:hh:mm' string to total days as a float."""
    if pd.isna(value):
        return None
    match = re.match(r"(\d+):(\d+):(\d+)", str(value).strip())
    if not match:
        return None
    days, hours, minutes = (int(x) for x in match.groups())
    return round(days + hours / 24 + minutes / 1440, 2)


def split_flights(value: str) -> list:
    """Split the 'Flights' text field into a list of individual mission entries."""
    if pd.isna(value):
        return []
    # Entries are comma-separated, but mission names can't contain commas themselves
    # in this dataset, so a simple split is safe here.
    return [f.strip() for f in str(value).split(",") if f.strip()]


def clean_astronauts(raw_path: Path = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(raw_path)

    df = df.rename(columns={
        "Name": "name",
        "Country": "country",
        "Gender": "gender",
        "Flights": "flights_raw",
        "Total Flights": "num_flights",
        "Total Flight Time (ddd:hh:mm)": "total_flight_time_raw",
    })

    # Drop exact duplicate rows and rows with no name
    df = df.drop_duplicates()
    df = df[df["name"].notna()].copy()

    # Parse total flight time into numeric days
    df["total_flight_days"] = df["total_flight_time_raw"].apply(parse_flight_time_to_days)

    # Parse flights into a list + a count check against num_flights
    df["flights_list"] = df["flights_raw"].apply(split_flights)
    df["parsed_flight_count"] = df["flights_list"].apply(len)

    # Career-length duration category (cumulative, not per-mission — see module docstring)
    df["duration_category"] = pd.cut(
        df["total_flight_days"], bins=DURATION_BINS, labels=DURATION_LABELS
    )

    # Standardize gender casing
    df["gender"] = df["gender"].str.strip().str.title()

    # Final column selection, ordered for readability
    output_cols = [
        "name", "country", "gender", "num_flights", "parsed_flight_count",
        "total_flight_days", "duration_category", "flights_raw",
    ]
    return df[output_cols].sort_values("total_flight_days", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    cleaned = clean_astronauts()
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_PATH, index=False)

    print(f"Cleaned {len(cleaned)} astronaut records -> {PROCESSED_PATH}")
    print(cleaned["duration_category"].value_counts())
    mismatches = (cleaned["num_flights"] != cleaned["parsed_flight_count"]).sum()
    print(f"Rows where num_flights != parsed mission count: {mismatches}")
