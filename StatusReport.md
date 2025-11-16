# Status Report – IS477 Course Project  
**Author:** Tongtong Gu, Tanya Liu
**Date:** November 2025  

---

## 1. Overview

This project investigates the comparability of anthropometric measurements across two distinct data sources:  
(1) the **Mendeley Body Measurements dataset**, which consists primarily of children and adolescents measured in a controlled setting, and  
(2) the **NHANES August 2021–August 2023** body measurement and demographic files, which provide adult measurements gathered through the U.S. national health examination program.

Our guiding research question is:

**How do body measurement distributions—specifically age, waist circumference, and total height—differ between the Mendeley sample and the U.S. adult population, and what data quality challenges emerge when integrating these sources?**

This Status Report provides an update on technical progress, links to all generated artifacts, and a revised timeline for completion of the final project.


---

## 2. Progress Relative to Project Plan

Substantial progress has been made across all stages outlined in the original project plan, including acquisition, cleaning, profiling, integration, clustering analysis, and cross-source comparison. All work is tracked in GitHub with a clear repository structure and reproducible scripts.

---

### **2.1 Repository Organization**

A standardized project directory structure has been created:
- Created a consistent project directory structure:
  - `scripts/` — cleaning, integration, and analysis scripts  
  - `report_outputs/figs/` — generated visualizations  
  - `report_outputs/tables/` — summary tables and cluster results  
  - `data/raw/` — raw NHANES XPT files  
  - `data/processed/` — cleaned datasets  
- All files tracked in Git with regular commits.


This organization supports reproducibility and clear provenance across all workflow stages.

---

### **2.2 Mendeley Data Cleaning & Clustering Analysis**

**Artifacts:**

- `scripts/process_mendeley.py`  
- `scripts/analysis_clustering.py`  
- `data/processed/mendeley_clean.csv`  
- `report_outputs/tables/mendeley_with_clusters.csv`  
- `report_outputs/tables/kmeans_cluster_counts.csv`  
- `report_outputs/tables/hac_cluster_counts.csv`  
- Figures under `report_outputs/figs/`, including:  
  - `boxplot_TotalHeight.png`  
  - `boxplot_Waist.png`  
  - `dendrogram_ward.png`  
  - `silhouette_kmeans_k8.png`  
  - `tsne_kmeans_hac.png`

**Progress:**
- Cleaned raw dataset: removed missing values and standardized column names.  
- Conducted **k-means clustering (k=8)** and **hierarchical clustering (Ward linkage)**.  
- Generated diagnostic plots (silhouette, dendrogram, t-SNE).  
- Exported cluster assignments and summary tables.  

This completes all planned tasks related to Module 6 (extraction), Module 8 (analysis), and clustering-based exploration.

---

### **2.3 NHANES Data Acquisition & Cleaning**

**Artifacts:**

- `data/raw/BMX_L.xpt`  
- `data/raw/DEMO_L.xpt`  
- `scripts/process_nhanes.py`  
- `data/processed/nhanes_clean.csv`  
- `report_outputs/tables/nhanes_summary.csv`

**Progress:**
- Downloaded and loaded NHANES 2021–23 XPT files using `pandas.read_sas()`.  
- Extracted key variables: `Age`, `Gender`, `Waist`, `TotalHeight`.  
- Filtered for adults (Age ≥ 18).  
- Standardized column names to match Mendeley dataset.  
- Produced summary statistics and validated schema consistency.

The resulting dataset contains **6011 adult participants**, providing a strong comparison set for the final analysis.

---

### **2.4 Data Integration Pipeline (Module 7–8)**

**Artifacts:**

- `scripts/integrate_datasets.py`  
- `data/processed/integrated_anthro.csv`  
- `report_outputs/tables/integrated_summary.csv`

**Progress:**
- Selected harmonized variables: `Gender`, `Age`, `Waist`, `TotalHeight`.  
- Added a `source` label (`Mendeley` or `NHANES`).  
- Concatenated both datasets into a unified schema.  
- Verified successful integration and generated summary statistics.  

This completes all required tasks for dataset integration and schema alignment.

---

### **2.5 Data Quality Assessment (Module 9)**

**Artifacts:**

- `scripts/quality_report.py`  
- Summary tables in `report_outputs/tables/`:
  - `mendeley_summary.csv`
  - `nhanes_summary.csv`
  - `integrated_summary.csv`

**Findings:**
- Mendeley dataset is heavily concentrated in **children and adolescents**, while NHANES consists of adults.  
- Distribution differences (especially waist and height) are driven by population differences.  
- Units and measurement protocols differ slightly between sources.  
- No significant missingness, but strong heterogeneity across sources.

These findings will be fully documented in the final report’s Data Quality section.

---

### **2.6 Integrated Analysis and Visualization**

**Artifacts:**

- `scripts/integrated_analysis.py`  
- Figures:
  - `integrated_age_by_source.png`
  - `integrated_waist_by_source.png`
  - `integrated_height_by_source.png`

**Progress:**
- Created cross-source comparisons for Age, Waist, and TotalHeight.  
- Visualizations show dramatic differences due to underlying population characteristics.  
- Results will be expanded into the Findings section in the final README.

---

### **2.7 Reproducibility & Workflow Automation (Module 11–12)**

A central `run_all.py` script is being drafted to orchestrate:

1. Clean Mendeley  
2. Clean NHANES  
3. Integrate datasets  
4. Generate quality tables  
5. Run clustering analysis  
6. Produce integrated comparisons  

This will satisfy the workflow automation and reproducibility requirements for Milestone 4.

---

## 3. Updated Timeline

| Task | Status | Expected Completion |
|------|--------|----------------------|
| Mendeley cleaning & clustering | ✔ Completed | — |
| NHANES acquisition & cleaning | ✔ Completed | — |
| Data integration | ✔ Completed | — |
| Quality assessment | ✔ Completed | — |
| Integrated analysis | ✔ Completed | — |
| Workflow automation (run_all.py) | In progress | Nov 20 |
| Data dictionary / metadata | Not started | Nov 23 |
| Final README report | In progress | Nov 30 |
| requirements.txt + citations | Not started | Dec 3 |
| Final GitHub release | Pending | Dec 10 |

---

## 4. Changes to Project Plan

- Adjusted project scope to emphasize **data comparability analysis** rather than predictive modeling due to the heterogeneous populations.  
- Chose to prioritize **descriptive statistics + clustering + distributional comparison**, which better aligns with Modules 6–10 and the datasets available.  
- Integrated analysis expanded to include age-related stratification and visual distribution comparisons.  
- Added workflow automation as a deliverable to enhance reproducibility.

---

## 5. Constraints and Gaps

- **Population mismatch:** Mendeley contains mostly children, NHANES contains only adults. Direct statistical comparison must be interpreted cautiously.  
- **Measurement units/protocols differ** across datasets, limiting alignment.  
- **Survey weights not used** for NHANES because the goal is curation, not population inference.  
- **Mendeley dataset licensing** needs to be confirmed and documented in the final report.  
- Some variables (e.g., BMI, chest width) were not present in NHANES and thus excluded from integration.

---

## 6. Individual Contributions

### **Tongtong Gu**  
*(Lead: Data Engineering & Integration)*  

- Implemented data acquisition workflows for NHANES `.xpt` files and developed dataset loading utilities.
- Wrote preprocessing and cleaning scripts for both the Mendeley and NHANES datasets, including variable standardization and missing value handling.
- Designed and executed the data integration pipeline, harmonizing schemas across sources and producing the unified dataset.
- Generated summary statistics and supported the creation of integrated analysis outputs.
- Organized and documented the repository structure, maintained reproducibility scripts, and ensured pipeline consistency across modules.

### **Tanya Liu**  
*(Lead: Data Quality & Analysis)*  

- Conducted exploratory data profiling and contributed to early-stage cleaning decisions.
- Reviewed the integrated dataset and verified the correctness of variable alignment and naming conventions.
- Assisted in generating clustering outputs and contributed to visualization diagnostics for the Mendeley dataset.
- Worked on preliminary distributional comparisons between Mendeley and NHANES body measurements.
- Contributed to documentation and team discussions regarding data quality findings and next steps.

---

## 7. Next Steps Before Final Submission

- Finalize `run_all.py` automation script.  
- Write detailed **README.md** with Summary, Data Profile, Data Quality, Findings, Future Work.  
- Prepare `data_dictionary.md` describing variables and metadata.  
- Add `requirements.txt` with software dependencies.  
- Document licenses and ethical considerations.  
- Create final GitHub tag and release by December 10.

---


