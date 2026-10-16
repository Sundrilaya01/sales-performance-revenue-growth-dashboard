# Data Quality & Cleansing Report

**Project:** Sales Performance & Revenue Growth Dashboard  
**Phase:** Phase 2  -  Data Collection & Preparation  
**Author:** Senior Data Engineer  
**Date:** 2026-10-16  

---

## 1. Executive Summary
This report documents the quality audit, cleansing rules, normalization, and reconciliation results for the sales transaction dataset. The raw dataset (`sales_performance_dataset.csv`) was processed into a relational Star Schema comprising 1 Fact table and 5 Dimension tables, plus a consolidated master view. All 600 raw records were preserved with 0 loss, 100% referential integrity, and exact $0.00 financial reconciliation.

---

## 2. Dataset Provenance & Nature
* **Source Path:** `data/raw/sales_performance_dataset.csv`
* **File Size:** 101,909 bytes (preserved without modification)
* **Provenance Classification:** **Synthetic Demonstration & Benchmark Dataset**
* **Evidence of Provenance:**
  - Highly structured, symmetric distribution of transactions across 4 regions, 12 cities, and 12 products.
  - Zero null values, perfectly rounded unit selling prices ($75.00 to $1,250.00), and invariant product unit costs.
  - Absence of native transaction/order keys in the raw format.
  - Target Sales and Achievement percentages mathematically aligned with typical corporate forecasting demos.
* **Ethics & Transparency Note:** All downstream documentation and analytics explicitly acknowledge this dataset as synthetic benchmark data; no claim is made that this represents proprietary company operational data.

---

## 3. Data Cleansing & Normalization Rules

| Source Column | Target Table(s) & Column(s) | Transformation & Standardization Rule |
| :--- | :--- | :--- |
| *(None / Implicit)* | `fact_sales.order_id` | Deterministically generated business key: `ORD-YYYY-XXXX` (e.g., `ORD-2024-0001` to `ORD-2025-0600`) preserving temporal sequence. |
| `Date` | `fact_sales.date`, `fact_sales.date_key`, `dim_date` | Parsed safely to ISO `YYYY-MM-DD` and integer date key `YYYYMMDD`. |
| `Product Category`, `Product Name` | `dim_products.product_id`, `product_name`, `category` | Extracted 12 distinct products; assigned deterministic primary keys (`PRD-ELE-001`, `PRD-FUR-001`, etc.). |
| `Selling Price` | `dim_products.unit_price`, `fact_sales.unit_price` | Standardized unit selling price. Cast to `float64`. |
| `Cost` / `Units Sold` | `dim_products.unit_cost`, `fact_sales.cost` | Verified unit cost is invariant per SKU ($Unit Cost = Cost / Units Sold$). Maintained standard COGS in product dimension. |
| `Region`, `State/City`, `Customer Type`, `Sales Channel` | `dim_customers.customer_id`, `state_city`, `customer_segment`, `sales_channel` | Grouped into 48 distinct customer cohort accounts (`CUST-0001` to `CUST-0048`) under country `United States`. |
| `Sales Executive Name`, `Region` | `dim_sales_reps.rep_id`, `sales_rep_name`, `assigned_region` | Mapped to 8 sales executive entities (`REP-001` to `REP-008`). |
| `Region` | `dim_regions.region_id`, `region_name` | Mapped 4 geographic regions (`REG-01` to `REG-04`). |
| `Units Sold` | `fact_sales.units_sold` | Validated $Units > 0$. Cast to `int64`. |
| `Revenue` | `fact_sales.sales_amount` | Standardized column name; reconciled against $Units Sold \times Unit Price$. |
| `Profit` | `fact_sales.profit` | Reconciled against $Sales Amount - Cost$. |
| `Profit Margin %` | `fact_sales.profit_margin_pct` | Reconciled against $(Profit / Sales Amount) \times 100$. |
| `Target Sales` | `fact_sales.target_sales` | Preserved float benchmark values. |
| `Actual Sales` | `fact_sales.actual_sales` | Verified identical to `sales_amount` ($Delta = 0.00$). |
| `Achievement %` | `fact_sales.achievement_pct` | Reconciled against $(Actual Sales / Target Sales) \times 100$. |
| `Growth %` | `fact_sales.growth_pct` | Preserved historical velocity indicator. |

---

## 4. Before-and-After Row Counts & Schema Summary

| Table Name | Output Path | Rows (Before) | Rows (After) | Columns | Primary Key |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Raw Source** | `data/raw/sales_performance_dataset.csv` | 600 | 600 (Unchanged) | 21 | None |
| **Fact_Sales** | `data/processed/fact_sales.csv` |  -  | 600 | 17 | `order_id` |
| **Dim_Products** | `data/processed/dim_products.csv` |  -  | 12 | 7 | `product_id` |
| **Dim_Customers**| `data/processed/dim_customers.csv` |  -  | 48 | 6 | `customer_id` |
| **Dim_Sales_Reps**| `data/processed/dim_sales_reps.csv` |  -  | 8 | 3 | `rep_id` |
| **Dim_Regions** | `data/processed/dim_regions.csv` |  -  | 4 | 3 | `region_id` |
| **Dim_Date** | `data/processed/dim_date.csv` |  -  | 731 | 12 | `date_key` |
| **Consolidated** | `data/processed/cleaned_sales_consolidated.csv`|  -  | 600 | 26 | `order_id` |

---

## 5. Missing-Value and Duplicate Audit Findings
* **Missing Values Found:** 0 missing values across all source rows and fields.
* **Duplicate Rows Found:** 0 duplicate rows in source data.
* **Duplicate Treatment:** Because no duplicates were present, zero records were dropped.
* **Referential Integrity Audit:**
  - Orphan `product_id` in Fact: **0**
  - Orphan `customer_id` in Fact: **0**
  - Orphan `rep_id` in Fact: **0**
  - Orphan `region_id` in Fact: **0**
  - Orphan `date_key` in Fact: **0**

---

## 6. Financial Reconciliation Results

| Metric | Raw Dataset Total | Processed Fact Total | Difference | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **Total Revenue / Sales Amount** | $1,577,535.00 | $1,577,535.00 | **$0.0000** | **PERFECT MATCH** |
| **Total Cost (COGS)** | $935,710.00 | $935,710.00 | **$0.0000** | **PERFECT MATCH** |
| **Total Profit** | $641,825.00 | $641,825.00 | **$0.0000** | **PERFECT MATCH** |
| **Total Units Sold** | 5,708 units | 5,708 units | **0 units** | **PERFECT MATCH** |
| **Total Target Sales** | $1,653,311.10 | $1,653,311.10 | **$0.0000** | **PERFECT MATCH** |
| **Line-Item $Sales = Units \times Price$** | Max Discrepancy: $0.000000 | Max Discrepancy: $0.000000 | **0.00** | **PERFECT MATCH** |
| **Line-Item $Profit = Sales - Cost$** | Max Discrepancy: $0.000000 | Max Discrepancy: $0.000000 | **0.00** | **PERFECT MATCH** |

---

## 7. Automated Test Suite Execution Summary
Automated verification executed via `scripts/validate_cleaning.py`:
- `TC-VAL-01`: Raw source file preservation and immutability  -  **PASS**
- `TC-VAL-02`: Processed output tables existence (7 files)  -  **PASS**
- `TC-VAL-03`: Fact table row count parity with raw source (600 rows)  -  **PASS**
- `TC-VAL-04`: Fact_Sales `order_id` uniqueness and non-null (600/600)  -  **PASS**
- `TC-VAL-05`: Dimension tables primary key uniqueness (100% unique)  -  **PASS**
- `TC-VAL-06`: Referential integrity across all Star Schema relationships (0 orphans)  -  **PASS**
- `TC-VAL-07`: Line-item Sales Amount = Units Sold * Unit Price ($Delta = 0.00$)  -  **PASS**
- `TC-VAL-08`: Line-item Profit = Sales Amount - Cost ($Delta = 0.00$)  -  **PASS**
- `TC-VAL-09`: Macro Financial Totals Reconciliation ($Delta = $0.00)  -  **PASS**
- `TC-VAL-10`: Continuous Dim_Date calendar coverage without gaps (731 days)  -  **PASS**
