# ProjectPlan.md

**Comparative Profiling and Integration of Anthropometric Data: Mendeley Body Measurements vs. NHANES 2021–2022**

## Contributors
- **Tongtong Gu** 
- **Tanya Liu** 

## Overview
This project implements an end-to-end, reproducible data lifecycle to integrate and analyze two complementary anthropometric datasets:

1) **Body Measurements Datasets** (Mendeley Data; DOI: 10.17632/bjv6c9pmp4.1) with height, weight, waist, chest, and BMI;  
2) **NHANES Anthropometry 2021–2022** (CDC/NCHS; files **BMX_L.XPT** + **DEMO_L.XPT**) with nationally representative measurements, demographics, and survey-design metadata.

Our goals are to (a) characterize similarities and differences in distributions and correlations across sources and survey protocols, (b) assess data quality and reproducibility via a transparent, automated workflow, and (c) evaluate cross-dataset generalizability of simple predictive models (e.g., BMI or obesity status as outcomes). We will standardize units, reconcile schemas, and **apply NHANES survey design (weights/strata/PSU)** to produce population-level estimates. We focus on **adults (≥18y)** for comparability and to avoid pediatric BMI percentile complexities.

## Research Questions
1. **Distributional Consistency:** How do univariate and joint distributions of height, weight, BMI, and waist circumference compare between Mendeley and NHANES?  
2. **Derivation Robustness:** How consistent is **derived BMI** (from height/weight) with **reported BMI** across sources? What are typical deviations and correlates?  
3. **Measurement Relationships:** Are correlations among key measures (e.g., waist–BMI) stable across datasets after aligning age/sex?  
4. **Population Comparability:** Using NHANES survey weights, how do population-level estimates (means/percentiles, adult obesity prevalence) contrast with those from the unweighted Mendeley dataset?  
5. **Modeling & Transfer:** Do models trained on one dataset generalize to the other after harmonization (train-on-Mendeley/test-on-NHANES and vice versa)?  
6. **Data Quality & Provenance:** What issues (missingness, outliers, unit/rounding inconsistencies, duplicates) arise, and can they be mitigated within an auditable pipeline?

## Datasets

### 1) Body Measurements Datasets (Mendeley Data)
- **Citation:** Kiru, Muhammad (2021), “Body Measurements Datasets”, Mendeley Data, V1. DOI: 10.17632/bjv6c9pmp4.1  
- **Format:** CSV (metric units anticipated; verify during profiling)  
- **Core variables:** `height`, `weight`, `BMI`, `waist`, `chest`; demographics if available (confirm).  
- **Access:** Direct HTTP download from Mendeley Data; respect license/terms and required citation.  
- **Use:** Exploratory baseline with straightforward schema; reproducibility checks by re-deriving BMI and comparing to provided BMI.  
- **Note:** Contains **chest circumference**, which is **not** available in NHANES; chest-related analyses will be limited to this dataset and explicitly labeled as single-source.

### 2) NHANES Anthropometry 2021–2022 (CDC/NCHS)
- **Files:** **BMX_L.XPT** (anthropometry) and **DEMO_L.XPT** (demographics + survey design)  
- **Format:** SAS Transport `.XPT` with codebooks  
- **Key variables (BMX):** `BMXBMI` (BMI, kg/m²), `BMXWT` (weight, kg), `BMXHT` (standing height, cm), `BMXWAIST` (waist, cm)  
- **Key variables (DEMO):** `RIDAGEYR` (age), `RIAGENDR` (sex), `RIDRETH3` (race/ethnicity), **survey design** `WTMEC2YR` (exam weight), `SDMVSTRA` (strata), `SDMVPSU` (PSU)  
- **Join key:** **`SEQN`**  
- **Access:** Public NHANES website (2021–2022 cycle) with programmatic download of `.XPT` and documentation  
- **Use:** Authoritative benchmark enabling **survey-weighted** estimates and demographic stratification  
- **Note:** **Chest circumference not collected** in BMX; cross-dataset comparisons will therefore focus on height, weight, BMI, and waist.

> **Harmonization Note:** We will create a variable crosswalk to unify names/units (cm, kg, kg/m²) and document conversions, rounding, and plausibility bounds. Chest will be analyzed only within Mendeley. Adults (≥18y) will be selected for primary analyses.

### Variable Crosswalk (initial)
| Unified name | NHANES (BMX/DEMO) | Mendeley CSV | Units | Notes |
|---|---|---|---|---|
| `height_cm` | `BMXHT` | `height` | cm | verify units |
| `weight_kg` | `BMXWT` | `weight` | kg | verify units |
| `BMI` | `BMXBMI` | `BMI` / derived | kg/m² | store both reported & derived |
| `waist_cm` | `BMXWAIST` | `waist` | cm |  |
| `sex` | `RIAGENDR` | (if present) | F/M | map 1→M, 2→F → `F/M` |
| `age_years` | `RIDAGEYR` | (if present) | years | adults (≥18y) |
| `race_ethnicity` | `RIDRETH3` | (n/a/if present) | code→labels | NHANES only |
| `source` | — | — | — | `NHANES` or `Mendeley` |

## Ethical, Legal, and Policy Considerations
- **Human subjects & privacy:** Both sources are public and de-identified; no re-identification attempts. Only aggregates/visuals will be shared in-repo.  
- **Licenses & terms:** Cite NHANES and Mendeley per their guidance; include a code LICENSE (MIT).  
- **Attribution & reuse:** Cite datasets’ DOIs/URLs and software; include software/version metadata.  
- **Responsible reporting:** Avoid stigmatizing language; frame results as population-level or subgroup aggregates with clear sampling caveats.

## Team & Roles
- **Tongtong Gu (Lead: Data Engineering & Integration)** — acquisition scripts; SHA-256 integrity checks; SQLite schema; harmonization/crosswalk; Snakemake workflow; unit tests.  
- **Tanya Liu (Lead: Quality, Analysis & Visualization)** — profiling & data quality; outlier/missing-data strategy; survey-weighted estimation for NHANES; statistical tests; modeling; plots & narrative.

> Both contributors co-author documentation and review each other’s PRs. Contribution statements and commit history will reflect individual work.

## Methods & Workflow

### Directory Layout (proposed)


### Tooling
- **Python:** `requests`, `hashlib`, `pandas`, `pyreadstat` (XPT), `numpy`, `scipy`, `statsmodels`, `patsy`, `scikit-learn`  
- **Survey design:** `statsmodels` survey API (primary) or `rpy2` → R `survey` (fallback) using `WTMEC2YR`, `SDMVSTRA`, `SDMVPSU`  
- **Workflow:** **Snakemake** automating acquisition → parsing → integration → QC → analysis → visualization  
- **Provenance:** Logged parameters, versions, file hashes; frozen environments (`requirements.txt`, optional `environment.yml`)  
- **Reproducibility:** Single entry-point run (`snakemake -j 1`); outputs mirrored to **Box** as required; raw inputs retrieved programmatically

### Data Acquisition & Integrity
- Programmatically download **Mendeley CSV** and NHANES **`BMX_L.XPT` + `DEMO_L.XPT`**; persist **SHA-256** per raw file.  
- Maintain a **download manifest** (URL, timestamp, expected/observed hash, file size, record counts).  
- Sanity checks: **`SEQN`** uniqueness and joinability between BMX_L and DEMO_L.

### Storage & Organization
- **SQLite** for integrated analysis:  
  - `participants` (DEMO_L subset): `SEQN`, `RIDAGEYR`, `RIAGENDR`, `RIDRETH3`, `WTMEC2YR`, `SDMVSTRA`, `SDMVPSU`  
  - `measurements` (BMX_L subset): `SEQN`, `BMXBMI`, `BMXWT`, `BMXHT`, `BMXWAIST`  
  - `mendeley_measures`: unified variables from Mendeley CSV (+ provenance columns)  
  - `crosswalk`: variable mapping, units, transforms, and source provenance  
- Enforce units (metric) and plausibility via constraints (e.g., adult `height_cm BETWEEN 120 AND 230`, configurable by age).

### Extraction, Enrichment, Integration
- Normalize units; compute **derived BMI** = `weight_kg / (height_m^2)` and store residual vs reported BMI.  
- Create **age groups** (e.g., 18–29, 30–39, …) and harmonize **sex** (`F/M`).  
- Implement the **variable crosswalk** and tag rows with `source`.  
- Retain provenance columns (file name, acquisition date, hash).

### Data Quality Assessment
- **Missingness:** counts/proportions, visual summaries; MCAR/MAR plausibility notes.  
- **Outliers:** physiologic bounds, robust Z (MAD), distribution-aware rules (e.g., implausible height/weight combos).  
- **Internal consistency:** BMI recomputation residuals; rounding pattern checks; duplicates.  
- **Cross-dataset comparability:** KS tests, QQ plots, and distance metrics (e.g., EMD) on key variables.  
- **Documentation:** Auto-rendered **QC report** (HTML/MD) saved in `docs/`; include an **OpenRefine operation history (recipe)** for any manual cleaning steps.

### Analysis & Modeling
- **Descriptive (unweighted vs weighted):** means, medians, percentiles; hist/density/violin plots by source, sex, and age group.  
- **Correlation structure:** Pearson/Spearman heatmaps; source-stratified comparisons.  
- **Survey-weighted NHANES:** adult obesity prevalence (BMI ≥ 30), height/weight percentiles; standard errors using `SDMVSTRA`/`SDMVPSU`.  
- **Predictive models:**  
  - Regression: `BMI ~ age + sex + waist + height + interactions` (consider nonlinear terms/GAM).  
  - Classification: Obesity (yes/no) with calibrated probabilities; **cross-dataset transfer** tests.  
- **Model quality:** cross-validation, calibration, permutation importance (SHAP if time allows); fairness-aware reporting (descriptive, not prescriptive).

### Visualization
- Publication-quality plots (Matplotlib/Altair): distribution overlays, ridgelines/violins, correlation heatmaps, calibration curves.  
- Export PNG/SVG and embed in the final README.

## Timeline & Ownership (high-level)

**Legend:** TG = Tongtong Gu, TL = Tanya Liu, both = joint

### Phase 1 — Setup & Acquisition (Owner: TG; Support: TL)
- Create GitHub repo, base structure, LICENSE, .gitignore.
- Implement programmatic download + SHA-256 checks for:
  - Mendeley CSV
  - NHANES 2021–2022 **BMX_L.XPT** (anthropometry) and **DEMO_L.XPT** (demographics/survey design)

---

### Phase 2 — Harmonization & Storage (Owner: TG; Review: TL)
- Build **variable crosswalk** (unified names/units), document conversions (cm/kg/kg·m⁻²).
- Load to **SQLite**:
  - `participants` (DEMO_L subset with `SEQN`, `RIDAGEYR`, `RIAGENDR`, `RIDRETH3`, `WTMEC2YR`, `SDMVSTRA`, `SDMVPSU`)
  - `measurements` (BMX_L subset with `SEQN`, `BMXBMI`, `BMXWT`, `BMXHT`, `BMXWAIST`)
  - `mendeley_measures` (unified variables + provenance)
- Enforce adult filter (≥18y) and plausibility constraints.

---

### Phase 3 — Data Quality & Documentation (Owner: TL; Support: TG)
- Profile missingness/outliers; recompute BMI and compare to reported values.
- Flag duplicates/rounding patterns; generate **QC report**.
- If manual edits applied, include **OpenRefine operation history (recipe)**.


---

### Phase 4 — Analysis & Modeling (Owner: TL; Support: TG)
- Descriptive stats and visuals: NHANES (weighted) vs Mendeley (unweighted).
- Correlation comparisons (by age/sex); KS/QQ/EMD on key measures.
- Models:
  - Regression: `BMI ~ age + sex + waist + height (+nonlinear terms as needed)`
  - Classification: Obesity (BMI ≥ 30) with calibration
  - **Cross-dataset transfer** (train on one, test on the other)

---

### Phase 5 — Workflow & Reproducibility (Owner: TG; Review: TL)
- Orchestrate end-to-end with **Snakemake** (acquire→parse→integrate→QC→EDA→models→viz).
- Freeze environment (`requirements.txt` / optional `environment.yml`), `pip freeze`.
- Upload outputs to **Box**; document paths and run instructions.

---

### Phase 6 — Final Report & Release (Owner: both)
- Write **README.md** (Summary, Data profile, Data quality, Findings, Reproducing, References).
- Add contribution statement; clean repository; tag **final-project** release.

## Requirement Coverage (summary)
- **Data lifecycle** — both → README methods/diagram
- **Ethical/legal/policy** — TL → README “Data profile” + citations/licenses + no re-ID statement
- **Acquisition (≥2 datasets)** — TG → `scripts/acquire/` + checksums + manifest
- **Storage & organization** — TG → SQLite schema/DDL + folder conventions
- **Extraction & enrichment** — TG (TL review) → unit conversions; BMI derivation; age groups; sex harmonization
- **Data integration** — TG → SEQN join; crosswalk; harmonized tables
- **Data quality** — TL → `scripts/quality/`; QC report; OpenRefine operation history
- **Data cleaning** — TL → cleaning scripts/notes; OpenRefine recipe archived
- **Workflow & provenance** — TG → Snakemake; logs; environment freeze
- **Reproducibility & transparency** — both → README “Reproducing”; Box link; run-all instructions
- **Metadata & documentation** — TL (TG review) → data dictionary/codebook; schema diagram; references


## Constraints
- **Coverage mismatch:** NHANES BMX does not include chest circumference; chest analyses are single-source (Mendeley) only and labeled as such.
- **Demographics in Mendeley:** If age/sex are absent or incomplete, cross-dataset comparisons will be limited to height/weight/BMI/waist and stratified only where data permit.
- **Survey design complexity:** We will use 2-year examination weights (`WTMEC2YR`) with `SDMVSTRA`/`SDMVPSU`. Variance estimation beyond linearization or multi-cycle combining is out of scope if time is limited.
- **Population scope:** Primary analyses focus on adults (≥18y); pediatric BMI percentiles are out of scope unless time permits.
- **Licensing & redistribution:** Raw data are retrieved programmatically and kept out of Git; only derived outputs and metadata are shared with proper citations.
- **Timeline risk:** If time is tight, we prioritize: acquisition → harmonization → QC → descriptive comparisons → minimal models → documentation.


## Gaps & Open Questions
- Confirm Mendeley demographics availability; constrain cross-dataset comparisons if absent.  
- Decide on race/ethnicity stratifications given Mendeley limitations.  
- Scope SHAP/fairness diagnostics based on time budget.  
- Optional: extend to NHANES 2023–2024 (BMX_M) and document weight-combination strategy.


## References 
- Kiru, M. (2021). *Body Measurements Datasets*. Mendeley Data. DOI: 10.17632/bjv6c9pmp4.1  
- CDC/NCHS. *NHANES 2021–2022 Anthropometry (BMX_L) and Demographics (DEMO_L) Documentation and Data Files*.  

---
