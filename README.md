# 🚴‍♂️ TU Dortmund M.Sc. Data Science Application Report: Cycling Performance Analysis

This repository contains the complete **Python code** used to generate the statistical analysis and visualizations for the TU Dortmund Master's application report.

The analysis addresses the research questions concerning the relationship between **Rider Class**, **Stage Class**, and competitive **Points** performance in the dataset.

---

## 📂 Repository Contents

| File/Folder | Description |
| :--- | :--- |
| `analysis.py` | **The main analysis script.** Executes all steps: data loading, cleaning, descriptive statistics, assumption checks (Levene's), inferential testing (Kruskal-Wallis), and post-hoc analysis (Dunn's). |
| `data/` | Placeholder directory for the original raw data file (`cycling_data.csv`). **Note:** Due to security policies, the original data file is **not included** in this repository but **must be placed here** to run the script. |
| `output/` | Contains the generated statistical visualizations and the comprehensive descriptive tables referenced in the report. |
| `README.md` | This documentation file. |

---

## 🛠️ 1. Environment Setup

This project requires a standard Python data science environment.

### 1.1. Clone the Repository (Private Access Only)

    git clone https://github.com/parsafaramarzi/Dortmund-Summer-2026-Application-Statistical-Report

### 1.2. Install Dependencies

All necessary packages can be installed using `pip`. It's recommended to do this within a virtual environment.

    pip install pandas numpy scipy scikit-posthocs matplotlib seaborn

* **Key Packages:** `scipy.stats` (for Kruskal-Wallis, Levene), `scikit_posthocs` (for Dunn's post-hoc test).

### 1.3. Data Placement

Place the original raw data file, which should be named **`cycling_data.csv`**, into the **`./data/`** directory.

> **Note:** The script `analysis.py` is configured to look for the file in `./data/cycling_data.csv`.

---

## 🚀 2. Running the Analysis

Execute the main script from the root directory:

    python analysis.py

The script will print the statistical test results (Levene's, Kruskal-Wallis, and Dunn's post-hoc matrices) to the console and save all generated figures and summary tables to the **`./output/`** folder.

---

*This repository is maintained as a private resource for the purpose of academic review for the M.Sc. Data Science application to TU Dortmund, Sommersemester 2026. Access is restricted to authorized personnel.*
