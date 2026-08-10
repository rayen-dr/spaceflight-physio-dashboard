# Data Directory

- **raw/** — Original, untouched data as obtained from sources (Kaggle astronaut/mission metadata, literature-compiled physiological effects table). Never edited directly.
- **processed/** — Cleaned, merged, analysis-ready datasets produced by scripts in `src/data_processing/`.
- **external/** — Reference tables (e.g. study citation list, mission duration category definitions) that support the main datasets but aren't primary data themselves.

Raw data files are excluded from version control (see `.gitignore`) to keep the repo lightweight. See `docs/data_sources.md` for exact provenance of every dataset and how to regenerate `raw/` locally.
