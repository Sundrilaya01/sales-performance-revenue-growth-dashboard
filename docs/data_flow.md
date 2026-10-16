# Data Flow and Pipeline Architecture

## 1. End-to-End Pipeline Sequence

```
[Raw CSV Source]
       |
       v (scripts/clean_and_prepare_data.py)
[Transformation & Schema Synthesis]
       |
       +---> [scripts/validate_cleaning.py: Parity Check $0.00 delta]
       |
       v (Exports to data/processed/)
[Star Schema: Fact_Sales + 5 Dimensions]
       |
       +---> [Power BI Semantic Model (scripts/power_query_importer.m)]
       |            |
       |            v
       |     [11 DAX Measures (scripts/dax_measures.dax)]
       |            |
       |            v
       |     [Power BI Visuals & Canvas Grid]
       |
       +---> [Statistical Forecasting Engine (scripts/forecast_engine.py)]
       |            |
       |            v
       |     [revenue_forecast_h1_2026.csv (MAPE 30.16%)]
       |
       `---> [scripts/generate_web_data.py]
                    |
                    v
             [web/data.js -> Interactive Web Dashboard (localhost:8050)]
```

---

## 2. Pipeline Stages

### Stage 1: Ingestion
* Ingests `data/raw/sales_performance_dataset.csv` into Pandas memory.
* Audits raw column schemas and total line-item count (600 transactions).

### Stage 2: Cleansing, Normalization, and Surrogate Key Synthesis
* Standardizes dates into ISO `YYYY-MM-DD` and generates integer foreign keys (`date_key`).
* Synthesizes deterministic transaction keys (`order_id`: `ORD-YYYY-XXXX`).
* Normalizes product SKU properties into standard costs and selling prices.
* Aggregates customer profiles into 48 distinct account profiles.
* Generates a continuous calendar table across all 731 calendar days in 2024 to 2025.

### Stage 3: Dimensional Model Formulation (Star Schema)
* Exports 6 partitioned CSV tables to `data/processed/`:
  * `fact_sales.csv` (Fact table, 600 rows)
  * `dim_products.csv` (12 rows)
  * `dim_customers.csv` (48 rows)
  * `dim_date.csv` (731 rows)
  * `dim_sales_reps.csv` (8 rows)
  * `dim_regions.csv` (4 rows)
* Automated gatekeeper (`scripts/validate_cleaning.py`) confirms row count parity and exact $0.00 delta across Revenue, Cost, and Profit.

### Stage 4: Analytical Calculations and Forecasting
* **DAX Layer:** Evaluates dynamic aggregation and time intelligence across user-selected slicer contexts.
* **Forecasting Layer:** Runs Holt-Winters Damped ETS modeling, executes holdout backtesting, and exports 6-month projections with 95% confidence intervals to `data/processed/revenue_forecast_h1_2026.csv`.

### Stage 5: Presentation and Delivery
* **Power BI Desktop:** Connects via Power Query M expressions, applies theme styling, and displays executive visuals.
* **Web Dashboard:** Reads aggregated JSON/JS data structures and renders interactive charts on `http://localhost:8050`.
