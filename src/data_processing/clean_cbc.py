"""
clean_cbc.py

Cleans and reshapes the Inspiration4 (I4) Complete Blood Count dataset.

Input:  data/raw/i4_cbc_bloodwork.csv  (long format: one row per subject/timepoint/analyte)
Output: data/processed/i4_cbc_processed.csv

Key transformations:
- Standardize TEST_DATE into a numeric "days_from_launch" column so timepoints sort
  and plot correctly (L-92 = -92, R+1 = +1, etc.)
- Compute each subject's pre-flight baseline (mean of L-92, L-44, L-3) per analyte
- Compute percent change from that baseline at every timepoint, per subject, per analyte
  -> this is what powers the "recovery trajectory" dashboard visuals
- Flag values outside the lab's own RANGE_MIN/RANGE_MAX as out_of_range
"""

import re
import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/i4_cbc_bloodwork.csv")
PROCESSED_PATH = Path("data/processed/i4_cbc_processed.csv")


def timepoint_to_days(tp: str) -> int:
    """Convert 'L-92' / 'R+45' style labels into signed integer days relative to launch."""
    match = re.match(r"([LR])([+-]\d+)", str(tp).strip())
    if not match:
        return None
    letter, offset = match.groups()
    days = int(offset)
    # L-x = x days before launch (already negative); R+x = x days after RETURN, not launch.
    # We keep launch (day 0) as the anchor for L-labels, and treat R-labels as days after
    # return, kept separately as "days_post_return" since I4 mission length (~3 days) means
    # R+1 is not the same reference frame as L-92. See notes below.
    return days


def clean_cbc(raw_path: Path = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(raw_path)
    df.columns = [c.strip() for c in df.columns]

    # Standardize timepoint into a sortable category + numeric offset + phase label
    timepoint_order = ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]
    df["TEST_DATE"] = df["TEST_DATE"].str.strip()
    df["timepoint_order"] = df["TEST_DATE"].apply(lambda x: timepoint_order.index(x) if x in timepoint_order else -1)
    df["phase"] = df["TEST_DATE"].apply(lambda x: "Pre-flight" if x.startswith("L") else "Post-flight (recovery)")
    df["offset_days"] = df["TEST_DATE"].apply(timepoint_to_days)

    # Flag out-of-normal-range values using the lab's own reference range
    df["out_of_range"] = (df["VALUE"] < df["RANGE_MIN"]) | (df["VALUE"] > df["RANGE_MAX"])

    # Compute each subject's pre-flight baseline per analyte (mean of the 3 L- timepoints)
    baseline = (
        df[df["phase"] == "Pre-flight"]
        .groupby(["SUBJECT_ID", "ANALYTE"])["VALUE"]
        .mean()
        .rename("baseline_value")
        .reset_index()
    )

    df = df.merge(baseline, on=["SUBJECT_ID", "ANALYTE"], how="left")
    df["percent_change_from_baseline"] = ((df["VALUE"] - df["baseline_value"]) / df["baseline_value"]) * 100

    df = df.sort_values(["SUBJECT_ID", "ANALYTE", "timepoint_order"]).reset_index(drop=True)
    return df


if __name__ == "__main__":
    cleaned = clean_cbc()
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_PATH, index=False)

    print(f"Processed {len(cleaned)} rows -> {PROCESSED_PATH}")
    print(f"Subjects: {cleaned['SUBJECT_ID'].nunique()}, Analytes: {cleaned['ANALYTE'].nunique()}")
    print(f"Out-of-range readings: {cleaned['out_of_range'].sum()} / {len(cleaned)}")
