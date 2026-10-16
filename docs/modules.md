# System Modules and Component Breakdown

This document provides a technical breakdown of all operational modules, Python scripts, configuration files, and data pipelines implemented in the project.

---

## 1. Module Inventory and Mapping

```
scripts/
|-- clean_and_prepare_data.py          [Module 1: ETL Pipeline and Schema Generator]
|-- validate_cleaning.py               [Module 2: ETL and Data Quality Validator]
|-- validate_data_model.py             [Module 3: Relational Star Schema Validator]
|-- dax_measures.dax                   [Module 4: DAX Measure Repository]
|-- validate_dax_measures.py           [Module 5: Mathematical Parity Validator]
|-- forecast_engine.py                 [Module 6: Statistical Time-Series Engine]
|-- validate_forecasting.py            [Module 7: Out-of-Sample Backtesting Suite]
|-- validate_dashboard_interactions.py [Module 8: Slicer and Interaction Validator]
|-- generate_web_data.py               [Module 9: Web Data Serializer]
|-- serve_dashboard.py                 [Module 10: Local Web Server Daemon]
|-- power_query_importer.m             [Module 11: Power Query M Expression Ingestor]
`-- powerbi_theme.json                 [Module 12: Visual Palette and Theme Token Engine]
```

---

## 2. Detailed Module Specifications

### Module 1: ETL Pipeline and Schema Generator
* **File:** `scripts/clean_and_prepare_data.py`
* **Purpose:** Ingests raw unnormalized transaction records, applies type enforcement, synthesizes deterministic keys, extracts dimensions, and generates a continuous calendar.
* **Inputs:** `data/raw/sales_performance_dataset.csv`
* **Outputs:**
  * `data/processed/fact_sales.csv` (600 rows)
  * `data/processed/dim_products.csv` (12 rows)
  * `data/processed/dim_customers.csv` (48 rows)
  * `data/processed/dim_date.csv` (731 rows)
  * `data/processed/dim_sales_reps.csv` (8 rows)
  * `data/processed/dim_regions.csv` (4 rows)
* **Key Functions:**
  * `clean_and_prepare_data()`: Main orchestrator.
  * Deterministic order ID generation: Formats `ORD-{year}-{idx:04d}`.
  * Standardized date key extraction: Computes integer `YYYYMMDD`.
  * Unit cost extraction: Standardizes costs per product catalog item.

### Module 2: ETL and Data Quality Validator
* **File:** `scripts/validate_cleaning.py`
* **Purpose:** Automated gatekeeper verifying that zero records were lost and zero financial discrepancies exist.
* **Checks Executed:**
  * Fact table row count equals source row count (exactly 600 rows).
  * Macro financial reconciliation: Asserts `Delta = $0.00` across Revenue ($1,577,535.00), Cost ($935,710.00), and Profit ($641,825.00).
  * Null check across all mandatory foreign keys and measures.
  * Foreign key referential integrity against parent dimension tables.

### Module 3: Relational Star Schema Validator
* **File:** `scripts/validate_data_model.py`
* **Purpose:** Asserts structural integrity of the dimensional data model before Power BI consumption.
* **Checks Executed:**
  * Primary key uniqueness in every dimension table.
  * Single-direction filtering validation (`Dimension -> Fact`).
  * Grain verification (fact table grain: 1 row per order line-item).
  * Zero orphan keys across all 5 relationships.

### Module 4: DAX Measure Repository
* **File:** `scripts/dax_measures.dax`
* **Purpose:** Contains verified DAX syntax for all 11 business measures.
* **Categories:**
  * Core aggregations: `Total Sales`, `Total Quantity`, `Total Orders`, `Average Order Value`.
  * Dynamic time-intelligence: `Sales Previous Year`, `Revenue Growth %`.
  * Cost and profit: `Total Cost`, `Total Profit`, `Profit Margin %`.
  * Quota benchmarks: `Target Sales`, `Sales Achievement %`.

### Module 5: Mathematical Parity Validator
* **File:** `scripts/validate_dax_measures.py`
* **Purpose:** Cross-validates DAX formula behavior against Python mathematical calculations to guarantee parity.
* **Checks Executed:**
  * Validates calculations globally across the entire 2-year period.
  * Validates calculations across individual filtered subsets (by Year, Region, Category).
  * Validates edge-case behavior (e.g., dividing by zero returns blank without error).

### Module 6: Statistical Time-Series Engine
* **File:** `scripts/forecast_engine.py`
* **Purpose:** Aggregates monthly transaction volumes, fits Holt-Winters Exponential Smoothing with Damped Trend, and projects future revenue.
* **Inputs:** `data/processed/fact_sales.csv`
* **Outputs:**
  * `data/processed/revenue_forecast_h1_2026.csv` (Forecast values and 95% confidence intervals).
  * `data/processed/monthly_revenue_actuals.csv` (Aggregated historical series).
* **Algorithms:** Holt-Winters Damped ETS, Linear Trend OLS, Naive Benchmark.

### Module 7: Out-of-Sample Backtesting Suite
* **File:** `scripts/validate_forecasting.py`
* **Purpose:** Executes an 18-month train / 6-month holdout test split to score forecasting accuracy on unseen data.
* **Metrics Computed:** MAE, RMSE, and MAPE across candidate models.
* **Acceptance Rule:** Asserts that the algorithmic model achieves an out-of-sample MAPE improvement of at least 5 percentage points over the naive baseline.

### Module 8: Slicer and Interaction Validator
* **File:** `scripts/validate_dashboard_interactions.py`
* **Purpose:** Tests dashboard cross-filtering, multi-select slicing, and chronological sorting rules.
* **Checks Executed:**
  * Asserts non-empty filtered tables for all valid slicer combinations.
  * Verifies chronological sort order of `month_year` using `year_month_sort`.

### Module 9: Web Data Serializer
* **File:** `scripts/generate_web_data.py`
* **Purpose:** Aggregates Star Schema data and forecast series into an optimized JavaScript data structure (`web/data.js`).
* **Output:** `web/data.js` containing KPI summaries, monthly actuals, projections, categorical distributions, and SKU metrics.

### Module 10: Local Web Server Daemon
* **File:** `scripts/serve_dashboard.py`
* **Purpose:** Serves the interactive dashboard locally on `http://localhost:8050` using Python's built-in `http.server`.
* **Execution:** Background daemon with non-blocking request handling.

### Module 11: Power Query M Expression Ingestor
* **File:** `scripts/power_query_importer.m`
* **Purpose:** Production M scripts to load and type-cast Star Schema CSVs in Power BI Desktop with zero manual column formatting.

### Module 12: Visual Palette and Theme Token Engine
* **File:** `scripts/powerbi_theme.json`
* **Purpose:** Corporate styling definitions defining visual tokens, font families, accessible contrast colors, and card background styling.
