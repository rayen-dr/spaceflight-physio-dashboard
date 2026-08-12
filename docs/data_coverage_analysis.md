# Dataset-to-Parameter Coverage Analysis

This document is the authoritative record of what our 3 datasets actually contain versus the originally-desired parameter list, verified against real column names and values (not assumed). Any dashboard page or report claim should be checked against this file.

## Datasets in use
1. **`data/processed/astronauts_clean.csv`** — 570 astronauts (Kaggle). Columns: `name, country, gender, num_flights, parsed_flight_count, total_flight_days, duration_category, flights_raw`
2. **`data/raw/physiological_effects.csv`** — 38 literature-compiled findings. Columns: `record_id, system, measure, body_site_or_context, mission_duration_category, duration_days_approx, metric_type, value, value_low, value_high, unit, measurement_method, source_citation, source_url`
3. **`data/raw/i4_cbc_bloodwork.csv`** — 553 rows, Inspiration4 mission, real longitudinal blood panel. Columns: `ANALYTE, VALUE, RANGE_MIN, RANGE_MAX, UNITS, TEST_TYPE, SUBJECT_ID, SEX, TEST_DATE`. 4 subjects, 7 timepoints (L-92, L-44, L-3, R+1, R+45, R+82, R+194), 23 analytes.

## Full coverage table
*(See conversation / project chat log for the full parameter-by-parameter table — summarized findings below.)*

### Fully covered
- BMD by skeletal site (aggregate, literature)
- Orthostatic intolerance incidence (literature)
- Total sleep duration (aggregate, literature)
- Astronaut ID, sex, career flight count (Kaggle)
- Post-flight recovery trajectory, 23 blood analytes (I4 CBC) — our strongest, most real longitudinal asset

### Partially covered (proxy or incomplete)
- Muscle mass / strength (aggregate %, one strength data point)
- Bone density evolution (aggregate, no R+0/7/30/50 checkpoints)
- Sleep disturbance (proxy: % nights <6h, not a validated insomnia measure)
- Mission ID / type / vehicle (parseable from free text, not clean columns)

### Missing — not pursued further (see reasoning below)
- Type I muscle fiber atrophy, bone turnover markers, resting HR, blood pressure, HRV,
  sleep quality/efficiency score, in-flight/during-mission measurements (none of our 3
  datasets have any in-flight timepoint at all), exact per-mission duration/dates, age,
  countermeasure adherence.

**Why these are out of scope**: they require either IRB-gated individual astronaut clinical
data (LSDA — months-long request process, confirmed in Phase 1 research) or aren't published
in open form at individual level at all. Given the 1-month project timeline, we're scoping
around what's genuinely available rather than blocking on inaccessible data.

## Final project scope (data-driven, not aspirational)

| System | What we WILL show | What we explicitly will NOT claim |
|---|---|---|
| Bone | % density change by skeletal site & duration bucket (Short/Long); 1-year recovery % | No BMD-vs-lean-mass, no turnover markers, no exact R+ day tracking |
| Muscle | % mass change by muscle group & duration bucket; 1 strength proxy (calf) | No fiber-type data, no full-body strength testing |
| Cardiovascular | Orthostatic intolerance incidence by duration; stroke volume/cardiac output/plasma volume % change (fluid-shift phase) | No resting HR, BP, or HRV — clearly labeled as unavailable, not silently omitted |
| Sleep | Duration by mission phase; % nights <6h as a disturbance proxy | No sleep quality/efficiency score |
| Adaptation/Recovery | **I4 CBC real recovery trajectory (R+1→R+194) as the flagship longitudinal visual** | No in-flight/during-mission trend for ANY system — none of our data has that timepoint |
| Mission comparison | Mission names/years (parsed from text), career-level duration bucket | No exact per-mission duration or dates |
| Astronaut comparison | Sex, career flight count, career duration bucket, nationality | No age, no countermeasure adherence |

This scope is what gets built starting Phase 4 — every dashboard page should trace back to a ✅ or clearly-labeled ⚠️ row in this table.
