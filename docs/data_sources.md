# Data Sources & Provenance

This document records exactly where every number in `data/raw/physiological_effects.csv` comes from, and how to obtain the astronaut/mission metadata dataset. Required for academic transparency and reproducibility.

---

## 1. Astronaut & Mission Metadata

**Source**: Kaggle — public astronaut/mission datasets (e.g. "International Astronaut Dataset 1961–2021", "Astronaut health dataset")
**Access**: Requires a free Kaggle account. Not auto-downloadable from this environment (Kaggle requires browser/API-key auth) — download manually:

1. Go to Kaggle and search "astronaut dataset" or use a direct dataset URL
2. Click Download (or use Kaggle API: `kaggle datasets download -d <dataset-slug>`)
3. Save the CSV into `data/raw/astronaut_metadata.csv`

**Expected fields**: astronaut name, agency/nationality, mission name(s), launch date, mission duration (days), age, sex (where available)

**License**: Check the specific Kaggle dataset's license tab before use (most astronaut datasets are CC0 / public domain, but verify per-dataset).

> We'll finalize which exact Kaggle dataset once you've downloaded 1-2 candidates and we check field completeness together (Phase 2, next step).

---

## 2. Physiological Effects Dataset (Literature-Compiled)

Each row in `data/raw/physiological_effects.csv` is a finding drawn from a specific peer-reviewed publication or systematic review. Full citations below.

### Bone

| Study | Finding used | Link |
|---|---|---|
| Sibonga et al. / NASA bone loss reviews | Femoral neck ~1%/month, hip 1-1.5%/month, lumbar spine 1-1.6%/month (DXA) | nasa.gov/directorates/esdmd/hhp/bone-and-mineral-evaluation-and-analysis |
| Systematic review & meta-analysis of bone loss in space travelers (npj Microgravity) | Region-specific changes: skull +2.2%, thorax/upper limbs −1.4%, lumbar spine/pelvis −6.2%, lower limbs −4.9% | ncbi.nlm.nih.gov/pmc/articles/PMC7200725 |
| Pre-flight exercise and bone metabolism study (PMC) | Distal tibia: −2.9% to −4.3% bone strength/vBMD | pmc.ncbi.nlm.nih.gov/articles/PMC8862023 |
| Bone Health in Space Flight (PMC, LSAH cohort, n=94) | 0.5–1.5% BMD reduction per month; incomplete recovery at 1 year (hip 34.0%, spine 46.8% of astronauts back to baseline) | pmc.ncbi.nlm.nih.gov/articles/PMC12626757 |

### Muscle

| Study | Finding used | Link |
|---|---|---|
| LeBlanc et al. 1995 (STS-47, 8-day mission) | Soleus-gastrocnemius −6.3%, anterior calf −3.9%, hamstrings −8.3%, quadriceps −6.0%, intrinsic back −10.3% | pubmed.ncbi.nlm.nih.gov/8747608 |
| Update on effects of microgravity on musculoskeletal system (npj Microgravity, 2021 review) | Short flight (6-9d): quadriceps/gastrocnemius −6%, back −10%. Long flight (~6mo): quadriceps −12%, soleus-gastrocnemius −13%, back up to −20%, calf twitch force −25 to −30% | nature.com/articles/s41526-021-00158-4 |
| Canadian Space Agency | Short flights (5-11 days): up to 20% muscle mass loss | asc-csa.gc.ca/eng/astronauts/space-medicine/muscles.asp |

### Cardiovascular

| Study | Finding used | Link |
|---|---|---|
| Orthostatic intolerance in spaceflight: systematic review & meta-analysis (2026) | Pooled OI incidence 30% (n=221 astronauts); stroke volume mean diff −5.37 mL; baroreflex sensitivity SMD −0.87 | sciencedirect.com/science/article/pii/S0094576526003346 |
| Long-term spaceflight and the cardiovascular system (Precision Clinical Medicine) | OI incidence 20-30% short-duration vs. 83% long-duration (129-190 days); plasma volume reduced 7-20% | academic.oup.com/pcm/article/3/4/284/5858004 |
| The Cardiovascular System in Space (PMC review) | Early in-flight: stroke volume +35-46%, cardiac output +18-41% (fluid shift); hypovolemia −10-15% blood volume | ncbi.nlm.nih.gov/pmc/articles/PMC8773383 |

### Sleep

| Study | Finding used | Link |
|---|---|---|
| Barger et al. 2014 (64 Shuttle + 21 ISS astronauts, actigraphy) | In-flight sleep: Shuttle 5.96h, ISS 6.09h (scheduled: 8.5h). Post-flight: Shuttle 6.74h, ISS 6.95h | medicalnewstoday.com/articles/280818 ; pmc.ncbi.nlm.nih.gov/articles/PMC10391686 |
| Santy et al. 1988 (58 Shuttle astronauts) | In-flight 6.0h vs. ground baseline 7.9h | pmc.ncbi.nlm.nih.gov/articles/PMC5975626 |
| Flynn-Evans et al. (circadian misalignment, 21 ISS astronauts, 3248 nights) | Circadian-aligned sleep 6.4h vs. misaligned 5.4h | nature.com/articles/npjmgrav201519 |

---

## Notes on Methodology

- All physiological values are **published aggregate/group-level statistics** (means, percentage changes, or incidence rates), not raw individual astronaut records — appropriate given data-access constraints (see main README).
- Where multiple studies report overlapping measures (e.g. bone loss %/month), multiple rows are kept in the dataset with their source noted, rather than collapsed into one "true" number — this preserves scientific transparency about the range of reported findings.
- "Short-duration" = missions roughly ≤ 16 days (Shuttle-era). "Long-duration" = missions roughly ≥ 4-6 months (ISS-era). Exact boundaries are noted per-row since studies define this cutoff slightly differently.
