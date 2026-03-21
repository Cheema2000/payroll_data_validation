# 💼 LA City Payroll — Data Pipeline & Dashboard

An end-to-end **ETL data pipeline** built with Python that cleans, validates, and loads LA City payroll data into a SQLite database, then visualizes it through an interactive Streamlit dashboard.

---

## Project Structure

```
payroll_data_validation/
├── data/
│   ├── data.csv                # Raw LA City payroll data
│   └── clean_payroll.csv       # Cleaned & transformed data
├── src/
│   ├── clean_data.py           # Step 1 — Clean & transform raw data
│   └── validate_data.py        # Step 2 — Validate data quality
├── dashboard/
│   └── app.py                  # Streamlit interactive dashboard
├── load_to_sql.py              # Step 3 — Load cleaned data into SQLite
├── payroll.db                  # SQLite database (auto-generated)
├── requirements.txt
└── README.md
```

---

## Pipeline Overview

```
data/data.csv
     │
     ▼
src/clean_data.py        ← Strip $, commas | calculate gross/tax/net pay
     │
     ▼
data/clean_payroll.csv
     │
     ▼
src/validate_data.py     ← Null checks | negative pay | outliers | type validation
     │
     ▼
load_to_sql.py           ← Load into SQLite (payroll.db)
     │
     ▼
dashboard/app.py         ← Interactive Streamlit dashboard
```

---

## Features

### Data Cleaning (`src/clean_data.py`)
- Removes unnamed/empty columns
- Strips `$` signs and commas from currency fields
- Calculates **gross pay** from Q1 + Q2 + Q3 payments
- Applies **20% tax deduction** to compute net pay
- Renames columns to clean snake_case format

### Data Validation (`src/validate_data.py`)
- Null/missing value detection
- Negative pay checks
- Zero-pay employee flagging
- Outlier detection (>3 standard deviations from mean)
- Net pay vs gross pay integrity check
- Employment type validation

### Dashboard (`dashboard/app.py`)
- **KPI Cards** — Total employees, total payroll, avg net pay, avg tax
- **Top 10 Departments** by average gross pay (horizontal bar chart)
- **Employment Type Breakdown** (donut chart)
- **Gross Pay Distribution** (histogram)
- **Gross vs Net Pay by Department** (grouped bar chart)
- **Top 20 Earners** table with formatted currency
- **Sidebar Filters** — filter by department, employment type, and pay range
- **Download** filtered data as CSV

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Cheema2000/payroll_data_validation.git
cd payroll_data_validation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the pipeline
```bash
# Step 1 — Clean the data
python src/clean_data.py

# Step 2 — Validate the data
python src/validate_data.py

# Step 3 — Load into SQLite
python load_to_sql.py
```

### 4. Launch the dashboard
```bash
streamlit run dashboard/app.py
```

Then open **http://localhost:8501** in your browser.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core language |
| **Pandas** | Data cleaning & transformation |
| **SQLite** | Lightweight SQL database |
| **Streamlit** | Interactive dashboard |
| **Plotly** | Charts & visualizations |

---

## Dataset

Los Angeles City employee payroll data including department, job title, employment type, and quarterly payments (Q1–Q3).

- **1,030 employee records**
- Fields: `employee_id`, `department`, `job_title`, `employment_type`, `gross_pay`, `tax_deduction`, `net_pay`

---

## Author

**Hamza Cheema**
[GitHub](https://github.com/Cheema2000)
