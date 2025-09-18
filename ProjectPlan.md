# ProjectPlan.md

## Title
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
