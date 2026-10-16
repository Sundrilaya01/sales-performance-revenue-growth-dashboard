# System Architecture

## 1. Overview
The Sales Performance and Revenue Growth solution is engineered as a decoupled, 4-tier analytics architecture delivering data engineering, dimensional modeling, mathematical business metrics, predictive time-series forecasting, and interactive reporting.

---

## 2. Architectural Blueprint

```
+------------------------------------------------------------------------+
|                          1. INGESTION TIER                             |
|              Raw Source: data/raw/sales_performance_dataset.csv        |
+------------------------------------------------------------------------+
                                   |
                                   v
+------------------------------------------------------------------------+
|                      2. DATA ENGINEERING TIER                          |
|  * Python ETL Engine: scripts/clean_and_prepare_data.py                |
|  * Quality Gates: scripts/validate_cleaning.py ($0.00 delta check)     |
|  * Star Schema Generator: Creates 1 Fact and 5 Normalized Dimensions   |
+------------------------------------------------------------------------+
                                   |
                                   v
+------------------------------------------------------------------------+
|                   3. STORAGE & DIMENSIONAL MODEL TIER                  |
|  * Fact_Sales (600 rows): order_id, date_key, product_id, customer_id |
|  * Dim_Products (12 rows): product_name, category, unit_cost, price    |
|  * Dim_Customers (48 rows): region, state_city, segment, channel       |
|  * Dim_Date (731 continuous days): 2024-01-01 to 2025-12-31 calendar   |
|  * Dim_Sales_Reps (8 rows): regional commercial account managers       |
|  * Dim_Regions (4 rows): East, West, North, South territories          |
+------------------------------------------------------------------------+
                   /                                   \
                  v                                     v
+----------------------------------+   +---------------------------------+
|      4A. ANALYTICS ENGINE        |   |     4B. FORECASTING ENGINE      |
|  * 11 Explicit DAX Measures      |   |  * Holt-Winters Damped ETS      |
|  * Mathematical Parity Validator |   |  * Backtested MAPE (30.16%)     |
|  * Power Query M Importers       |   |  * H1 2026 Projections Export   |
+----------------------------------+   +---------------------------------+
                  \                                     /
                   v                                   v
+------------------------------------------------------------------------+
|                      5. PRESENTATION & DELIVERY TIER                   |
|  * Enterprise Power BI: Theme tokens, 16:9 grid layout specification   |
|  * Interactive Web Dashboard: Native HTML5/CSS/JS served on port 8050  |
+------------------------------------------------------------------------+
```

---

## 3. Layer Specifications

### 3.1 Data Ingestion and Storage Layer
* **Responsibility:** Isolates raw transactional records in immutable storage.
* **Storage Location:** `data/raw/sales_performance_dataset.csv`.
* **Characteristics:** Read-only reference dataset guaranteeing complete reproducibility.

### 3.2 Processing and ETL Layer
* **Responsibility:** Sanitizes raw inputs, generates deterministic keys, normalizes categorical attributes, constructs the continuous calendar, and asserts financial parity.
* **Implementation:** `scripts/clean_and_prepare_data.py`.
* **Quality Gate:** `scripts/validate_cleaning.py` confirms 100% row preservation and exact parity ($0.00 delta across Revenue, Cost, and Profit).

### 3.3 Relational Dimensional Model Layer
* **Responsibility:** Enforces a normalized Star Schema with single-direction One-to-Many (`1:*`) relationships.
* **Tables:** `Fact_Sales` (600 rows), `Dim_Products` (12 rows), `Dim_Customers` (48 rows), `Dim_Date` (731 rows), `Dim_Sales_Reps` (8 rows), `Dim_Regions` (4 rows).
* **Referential Integrity:** Verified 0 orphan keys.

### 3.4 Analytical and Modeling Layer
* **Business Logic:** 11 explicit DAX measures authored in `scripts/dax_measures.dax` and validated in `scripts/validate_dax_measures.py`.
* **Predictive Modeling:** Holt-Winters Exponential Smoothing with Damped Trend (`scripts/forecast_engine.py`) validated via an 18-month train / 6-month holdout test split.

### 3.5 Presentation Layer
* **Power BI Implementation:** Desktop model with corporate theme (`scripts/powerbi_theme.json`) and M ingestion code (`scripts/power_query_importer.m`).
* **Web Dashboard:** Browser-based application served locally on port 8050 (`scripts/serve_dashboard.py`).

---

## 4. Technology Stack
* **Business Intelligence:** Microsoft Power BI, DAX, Power Query (M).
* **Data Engineering and Statistical Modeling:** Python 3.13, Pandas, NumPy, Statsmodels, Scikit-Learn.
* **Presentation and Web:** Vanilla HTML5, CSS3, JavaScript, Python HTTP daemon.
* **Quality Assurance:** 5 automated test scripts with 100% pass verification.
