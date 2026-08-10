# Source Code

- **data_processing/** — Scripts to clean, merge, and validate raw data into `data/processed/`.
- **analysis/** — Statistical analysis, correlation, and trend computation functions, reused by both notebooks and the dashboard.
- **utils/** — Shared helper functions (e.g. mission duration bucketing, plotting themes).

Code here is imported by both `notebooks/` (exploration) and `dashboard/` (production use) — logic should live here once, not be duplicated.
