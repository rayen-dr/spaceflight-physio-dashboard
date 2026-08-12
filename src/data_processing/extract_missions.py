"""
extract_missions.py

The Kaggle astronaut dataset stores missions as free text per astronaut
(e.g. "Soyuz TM-6 (1988), STS-124 (2008)"). This script explodes that into
a mission-level table: one row per (astronaut, mission) pair, so we can
count crew size per mission and give the dashboard something to filter by.

Input:  data/processed/astronauts_clean.csv
Output: data/processed/missions_exploded.csv

Limitation (see docs/data_coverage_analysis.md): only mission NAME and YEAR
are recoverable this way. No mission duration, launch/return date, or vehicle
type is available as a clean field — mission "type" here is a best-effort
string-parse of the name prefix (Soyuz / STS / SpaceX Crew / other), not an
authoritative classification.
"""

import re
import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/processed/astronauts_clean.csv")
OUTPUT_PATH = Path("data/processed/missions_exploded.csv")

VEHICLE_PATTERNS = {
    "Soyuz": r"^Soyuz",
    "Space Shuttle (STS)": r"^STS",
    "SpaceX Crew Dragon": r"^SpaceX",
    "Mir": r"^Mir",
    "Shenzhou": r"^Shenzhou",
    "Vostok/Voskhod": r"^(Vostok|Voskhod)",
}


def classify_vehicle(mission_name: str) -> str:
    for label, pattern in VEHICLE_PATTERNS.items():
        if re.match(pattern, mission_name.strip()):
            return label
    return "Other / Unclassified"


def extract_missions(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    astro = pd.read_csv(input_path)
    rows = []
    for _, astronaut in astro.iterrows():
        for entry in str(astronaut["flights_raw"]).split(","):
            entry = entry.strip()
            match = re.match(r"(.+?)\s*\((\d{4})\)", entry)
            if not match:
                continue
            mission_name, year = match.groups()
            rows.append({
                "astronaut_name": astronaut["name"],
                "country": astronaut["country"],
                "mission_name": mission_name.strip(),
                "year": int(year),
                "vehicle_type": classify_vehicle(mission_name.strip()),
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    missions = extract_missions()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    missions.to_csv(OUTPUT_PATH, index=False)

    print(f"Extracted {len(missions)} astronaut-mission pairs -> {OUTPUT_PATH}")
    print(f"Unique missions: {missions['mission_name'].nunique()}")
    print(missions['vehicle_type'].value_counts())
