# Methodology

## 1. Data Collection Strategy

Three datasets were combined, chosen deliberately after verifying real access constraints (see `docs/data_sources.md` and `docs/data_coverage_analysis.md`):

1. **Astronaut/mission metadata** (Kaggle) — chosen over raw NASA LSDA individual records because LSDA requires a formal IRB-approved request process taking months, incompatible with a 1-month internship timeline.
2. **Literature-compiled physiological effects** — since NASA OSDR/GeneLab is dominated by 'omics data from model organisms (mice, plants) rather than clean human tabular data, we built our own dataset from peer-reviewed published findings (means, percentage changes, incidence rates) across Bone, Muscle, Cardiovascular, and Sleep systems. This is a standard secondary-analysis approach in space medicine communication.
3. **Inspiration4 CBC bloodwork** (NASA OSDR, OSD-569/LSDS-7) — the one dataset in this project offering genuine individual-level, longitudinal, repeated-measures data (4 subjects, 7 timepoints, 23 blood analytes), used as a case study rather than a population-level source given its small n.

## 2. Data Cleaning

- **Astronauts**: parsed `Total Flight Time (ddd:hh:mm)` into a numeric `total_flight_days` field; split the free-text `Flights` column into individual mission entries; validated the parsed mission count against the source's own `Total Flights` column (0 mismatches across 570 records).
- **Missions**: exploded each astronaut's mission list into one row per (astronaut, mission) pair; classified vehicle type via best-effort string matching on mission name prefixes (Soyuz, STS, SpaceX, etc.) — explicitly documented as non-authoritative.
- **I4 CBC**: converted timepoint labels (`L-92`, `R+45`, etc.) into a sortable order and a `phase` (pre-flight/post-flight) label; computed each subject's own pre-flight baseline (mean of the 3 pre-launch draws) per analyte, then percent change from that baseline at every timepoint — this is what powers the recovery-trajectory charts.

## 3. Data Quality Handling

During statistical analysis (`notebooks/02_statistical_analysis.ipynb`), we flagged every CBC reading falling outside the lab's own reference range (16 of 553 rows). Investigating the cluster, 7 of those 16 belonged to a single subject/timepoint (C003, L-92) with simultaneous extreme abnormalities across nearly every white-cell parameter — implausible as a real finding, and far more consistent with a data entry or unit-scaling error. This timepoint was flagged and excluded from headline trend charts, documented transparently rather than silently deleted or silently kept.

## 4. Statistical Approach — Deliberately Conservative

Given the literature dataset contains only 8-10 rows per physiological system (often just 2-5 rows per Short/Long duration bucket), we made a deliberate decision **not** to run formal hypothesis tests (t-tests, ANOVA) on these aggregate study-level numbers — a p-value computed on n=3 vs n=4 group means would imply false precision. Instead, we report descriptive comparisons (means by duration bucket), clearly labeled as directional/hypothesis-generating rather than statistically confirmed.

For the I4 CBC data, we verified textbook assumptions (e.g. "spaceflight-induced anemia") directly against the actual pivoted values rather than accepting the expected pattern at face value — and found the expected dip was **not** clearly present for this short (~3-day) mission, most likely because the mission was too brief to trigger effects documented in much longer ISS missions. This is reported as a genuine, duration-dependent finding rather than forced to match the literature's usual (longer-duration-based) narrative.

## 5. Dashboard Design Principles

- Every page's data limitation is stated explicitly as a warning box, sourced directly from `docs/data_coverage_analysis.md`, so the dashboard and the documentation never contradict each other.
- Duration-category color coding (orange = short, blue = long, grey = mixed) is kept consistent across all pages.
- The Recovery Case Study page is positioned as the dashboard's centerpiece precisely because it's the only dataset offering true individual-level longitudinal measurement — the honest "strongest evidence" in the project, rather than overselling the aggregate literature data as more than it is.

## 6. Known Limitations (Full List)

See `docs/data_coverage_analysis.md` for the complete parameter-by-parameter breakdown. In summary: no in-flight/during-mission measurements exist in any of our 3 datasets for any physiological system; no resting heart rate, blood pressure, or HRV; no bone turnover markers or muscle fiber-type data; no astronaut age; no per-mission exact duration or dates; no countermeasure adherence data. These are named and explained, not silently omitted.