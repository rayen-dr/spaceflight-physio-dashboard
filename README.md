# Analysis of the Physiological Effects of Spaceflight

**An interactive dashboard for exploring how the human body adapts to microgravity, built on open astronaut data and published spaceflight physiology research.**

> Internship project — TUNSA (Tunisian Space Association) · 2nd-Year Preparatory Engineering Student

---

## Table of Contents
- [Abstract](#abstract)
- [Objectives](#objectives)
- [Dataset Description](#dataset-description)
- [Methodology](#methodology)
- [Architecture](#architecture)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard Preview](#dashboard-preview)
- [Results](#results)
- [Technologies Used](#technologies-used)
- [Future Work](#future-work)
- [Internship Context](#internship-context)
- [Author](#author)
- [License](#license)

---

## Abstract

*(2-4 sentences — to be finalized once analysis is complete. Draft: This project analyzes the physiological effects of spaceflight on astronauts — including bone density, muscle mass, cardiovascular function, and sleep — using data compiled from published space medicine research and open astronaut/mission records. An interactive Streamlit dashboard allows exploration of these effects across mission durations, astronauts, and physiological systems, supporting comparison and trend analysis for space medicine education and decision support.)*

## Objectives

- Quantify how key physiological systems (bone, muscle, cardiovascular, sleep) change during spaceflight
- Compare physiological impact across mission durations (short vs. long-duration flights)
- Enable exploration and comparison across astronauts and missions
- Deliver an interactive, filterable dashboard for non-technical exploration of the findings
- Practice a full, professional data science workflow: collection → cleaning → EDA → statistical analysis → dashboard → reporting

## Dataset Description

This project combines two complementary data sources:

1. **Astronaut & Mission Metadata** — astronaut demographics, agency, mission names, and mission durations, sourced from public astronaut records (Kaggle).
2. **Physiological Effects Dataset** — a literature-compiled table where each row represents a published, peer-reviewed measurement (e.g. "% change in femoral neck BMD after 6-month ISS mission"), covering:
   - **Bone health** — bone mineral density changes by skeletal site and mission duration
   - **Muscle health** — muscle volume/mass changes by muscle group and mission duration
   - **Cardiovascular** — orthostatic intolerance incidence, stroke volume, cardiac output changes
   - **Sleep** — in-flight vs. pre/post-flight sleep duration

Full source-by-source provenance (study citations, access dates, and direct links) is documented in [`docs/data_sources.md`](docs/data_sources.md).

> **Note on data access:** NASA's raw individual-level astronaut biomedical data (LSDA) requires a formal request process with IRB approval, taking months — not feasible within this internship's timeline. This project instead uses **published aggregate findings** from peer-reviewed space medicine literature, a standard and transparent approach for secondary analysis.

## Methodology

*(To be expanded per phase — see `docs/methodology.md`)*
1. Data collection from Kaggle + literature review
2. Data cleaning & preprocessing
3. Exploratory Data Analysis (EDA)
4. Statistical analysis (trends, correlations by mission duration)
5. Dashboard integration
6. Reporting

## Architecture

*(Diagram to be added to `assets/diagrams/` — data sources → processing pipeline → dashboard)*

## Folder Structure

```
spaceflight-physio-dashboard/
├── docs/              # Data provenance, architecture, methodology docs
├── notebooks/         # Exploratory analysis notebooks
├── src/               # Reusable data processing & analysis code
│   ├── data_processing/
│   ├── analysis/
│   └── utils/
├── data/              # raw / processed / external datasets
├── reports/           # Figures + final written report
├── dashboard/         # Streamlit multipage app
├── tests/             # Unit tests
├── assets/            # Images, diagrams
├── requirements.txt
├── LICENSE
└── README.md
```

Each folder contains its own `README.md` explaining its contents in detail.

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/spaceflight-physio-dashboard.git
cd spaceflight-physio-dashboard

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the dashboard locally
streamlit run dashboard/app.py
```

## Dashboard Preview

*(Screenshots to be added here once dashboard pages are built)*

| Page | Screenshot |
|---|---|
| Home | `assets/images/home_screenshot.png` |
| Bone Health | `assets/images/bone_screenshot.png` |
| Mission Comparison | `assets/images/mission_comparison_screenshot.png` |

## Results

*(To be filled in after analysis — key findings, trends, and correlations discovered)*

## Technologies Used

- **Python** — pandas, numpy, scipy, statsmodels
- **Visualization** — matplotlib, seaborn, plotly
- **Dashboard** — Streamlit
- **Version Control** — Git & GitHub

## Future Work

- Expand physiological coverage (e.g. immune system, radiation exposure, psychological/behavioral health)
- Incorporate NASA OSDR 'omics data for deeper molecular-level analysis
- Request access to individual-level LSDA data for higher-resolution longitudinal analysis
- Add predictive modeling (e.g. estimating physiological impact for planned mission durations)

## Internship Context

This project was completed as part of an internship at **TUNSA (Tunisian Space Association)**, developed by a 2nd-year Preparatory Engineering student in Tunisia, under mentorship guidance covering data science, space medicine, and software engineering best practices.

## Author

**RAYEN KAROUS**
2nd-Year Preparatory Engineering Student · Tunisia
[LinkedIn](https://www.linkedin.com/in/rayen-karous) · [GitHub](https://github.com/rayen-dr) · [Email](mailto:karousfarouk@gmail.com)

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
