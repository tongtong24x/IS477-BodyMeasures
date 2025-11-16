# Data Dictionary

This document describes the main variables used in the project across the Mendeley, NHANES, and integrated datasets.

---

## 1. Common Variables (Used for Integration)

These variables appear in both cleaned datasets and in the integrated dataset.

| Column       | Datasets                    | Type    | Description                                                   | Notes / Coding                                             |
|--------------|-----------------------------|---------|---------------------------------------------------------------|-----------------------------------------------------------|
| `Gender`     | Mendeley, NHANES, Integrated | numeric | Participant sex / gender                                      | Coded as 1 = Male, 2 = Female (NHANES convention).       |
| `Age`        | Mendeley, NHANES, Integrated | numeric | Age in years                                                  | In Mendeley: mostly children/teens; in NHANES: adults (≥18). |
| `Waist`      | Mendeley, NHANES, Integrated | numeric | Waist circumference                                           | In NHANES: measured in cm using standardized protocol; in Mendeley: child measurements, exact protocol/units may differ. |
| `TotalHeight`| Mendeley, NHANES, Integrated | numeric | Standing height                                               | In NHANES: standing height in cm; in Mendeley: total body height for children/adolescents. |
| `source`     | Integrated                  | string  | Data source indicator                                         | `"Mendeley"` or `"NHANES"`; added during integration.     |

---

## 2. Mendeley-Specific Variables (in `mendeley_clean.csv`)

These variables are only available in the Mendeley dataset and are used primarily for clustering and descriptive analysis.

| Column               | Type    | Description                                        | Notes |
|----------------------|---------|----------------------------------------------------|-------|
| `HeadCircumference`  | numeric | Head circumference                                | Unit as in original Mendeley dataset (not harmonized). |
| `ShoulderWidth`      | numeric | Shoulder width / biacromial breadth               | Used in clustering analysis. |
| `ChestWidth`         | numeric | Chest width                                       | Used in clustering analysis. |
| `Belly`              | numeric | Abdominal / belly circumference or width          | Used in clustering analysis. |
| `Hips`               | numeric | Hip width or circumference                        | Used in clustering analysis. |
| `ArmLength`          | numeric | Arm length                                        | Used in clustering analysis. |
| `ShoulderToWaist`    | numeric | Vertical distance from shoulder to waist          | Postural / proportional measure. |
| `WaistToKnee`        | numeric | Vertical distance from waist to knee              | Leg proportion measure. |
| `LegLength`          | numeric | Leg length                                        | Used in clustering analysis. |
| `index`              | integer | Row index from original file                      | Not used in modeling; mainly an identifier. |

> Note: Names above reflect the cleaned version used in `mendeley_clean.csv` after removing trailing spaces and normalizing capitalization.

---

## 3. NHANES-Specific Variables (in Raw XPT and `nhanes_clean.csv`)

These variables are present in NHANES but not necessarily in Mendeley. Some are used internally in processing; others are retained for reference.

### 3.1 Variables Used in Cleaning / Integration

| Column       | Type    | Description                                                         | Notes |
|--------------|---------|---------------------------------------------------------------------|-------|
| `SEQN`       | integer | NHANES respondent sequence number                                  | Unique per participant; used to merge DEMO_L and BMX_L. |
| `RIDAGEYR`   | numeric | Age in years at the time of screening                              | Renamed to `Age` in cleaned dataset. |
| `RIAGENDR`   | numeric | Gender                                                              | Coded 1 = Male, 2 = Female; renamed to `Gender`. |
| `BMXWAIST`   | numeric | Waist circumference in cm                                           | Renamed to `Waist`. |
| `BMXHT`      | numeric | Standing height in cm                                               | Renamed to `TotalHeight`. |

### 3.2 Other NHANES Variables (Not Used in This Project)

NHANES includes many additional variables (e.g., sampling weights, survey design variables, health indicators, examination status). These are not used directly in this project but are documented in the official NHANES documentation for the 2021–2023 cycle.

Examples include:

- `WTMEC2YR` — examination sample weight (not used)  
- `SDMVPSU`, `SDMVSTRA` — design variables (not used)  

We intentionally omit these variables from the cleaned dataset to keep the focus on body measurements and basic demographics.

---

## 4. Derived and Output Variables

### 4.1 Cluster Labels (Mendeley Clustering Outputs)

In clustering outputs (e.g., `mendeley_with_clusters.csv`), we add derived label columns:

| Column             | Type    | Description                                           |
|--------------------|---------|-------------------------------------------------------|
| `cluster_kmeans`   | integer | Cluster assignment from k-means clustering (k = 8).   |
| `cluster_hac`      | integer | Cluster assignment from hierarchical clustering (Ward). |

These labels are used for visualization and to interpret differences in body-shape profiles across clusters.

---

This data dictionary should be read together with the main README and the official documentation for the Mendeley dataset and NHANES 2021–2023.
