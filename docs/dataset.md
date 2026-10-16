# Dataset Specifications & Data Dictionary

This document details the source data, schemas, field definitions, relationships, and data quality constraints for the Sales Performance & Revenue Growth Dashboard.

---

## 1. Dataset Overview & Provenance

- **Domain:** Retail & Enterprise B2B/B2C Sales Transactions
- **Provenance:** **Curated Synthetic Benchmark Dataset** (`data/raw/sales_performance_dataset.csv`, 101,909 bytes).
- **Time Horizon:** 2024-01-01 to 2025-12-31 (731 continuous calendar days).
- **Cleaned Storage Location:** `data/processed/`
- **Model Architecture:** Star Schema (1 Fact Table, 5 Dimension Tables).

---

## 2. Processed Table Schemas & Data Dictionary

### Table: `Fact_Sales` (`data/processed/fact_sales.csv`)
Captures line-item sales orders and transaction performance.

| Column Name | Data Type | Key Type | Description | Constraints / Rules |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | Varchar(20) | Primary Key | Unique transaction order code (`ORD-YYYY-XXXX`) | Non-null, Unique |
| `date_key` | Integer | Foreign Key | Integer date key (`YYYYMMDD`) | Ref `Dim_Date.date_key` |
| `date` | Date | Attribute | ISO transaction date (`YYYY-MM-DD`) | 2024-01-01 to 2025-12-31 |
| `product_id` | Varchar(20) | Foreign Key | Product SKU identifier | Ref `Dim_Product.product_id` |
| `customer_id` | Varchar(20) | Foreign Key | Customer account/cohort identifier | Ref `Dim_Customer.customer_id` |
| `rep_id` | Varchar(20) | Foreign Key | Sales representative identifier | Ref `Dim_Sales_Reps.rep_id` |
| `region_id` | Varchar(20) | Foreign Key | Sales region identifier | Ref `Dim_Regions.region_id` |
| `units_sold` | Integer | Metric | Units ordered | `units_sold > 0` |
| `unit_price` | Decimal(10,2) | Metric | Selling price per unit | `unit_price > 0` |
| `sales_amount` | Decimal(12,2) | Metric | Total transaction revenue (`units_sold * unit_price`) | Matches source `Revenue` |
| `cost` | Decimal(12,2) | Metric | Cost of Goods Sold (`units_sold * unit_cost`) | Matches source `Cost` |
| `profit` | Decimal(12,2) | Metric | Gross margin profit (`sales_amount - cost`) | Matches source `Profit` |
| `profit_margin_pct` | Decimal(5,2) | Metric | Profit margin percentage (`(profit / sales_amount) * 100`) | 32.00% to 53.33% |
| `target_sales` | Decimal(12,2) | Benchmark | Quota / target revenue assigned | Positive float |
| `actual_sales` | Decimal(12,2) | Metric | Actual realized revenue | Identical to `sales_amount` |
| `achievement_pct` | Decimal(6,2) | Metric | Target quota achievement rate | 80.06% to 117.58% |
| `growth_pct` | Decimal(6,2) | Metric | Historical transaction velocity indicator | -82.40% to +193.37% |

---

### Table: `Dim_Products` (`data/processed/dim_products.csv`)
Master catalog of 12 distinct products across 4 categories.

| Column Name | Data Type | Key Type | Description | Values / Examples |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | Varchar(20) | Primary Key | Deterministic SKU code | `PRD-ELE-001`, `PRD-FUR-001` |
| `product_name` | Varchar(100) | Attribute | Full product name | UltraBook Pro 15, 4K IPS Monitor 27" |
| `category` | Varchar(50) | Attribute | Product vertical | Electronics, Furniture, Office Supplies, Accessories |
| `unit_price` | Decimal(10,2) | Attribute | Standard catalog selling price | $75.00 to $1,250.00 |
| `unit_cost` | Decimal(10,2) | Attribute | Standard manufacturing / inventory cost | $35.00 to $850.00 |
| `unit_margin` | Decimal(10,2) | Attribute | Unit margin (`unit_price - unit_cost`) | $40.00 to $400.00 |
| `target_margin_pct` | Decimal(5,2) | Attribute | Target unit margin percentage | 32.00% to 53.33% |

---

### Table: `Dim_Customers` (`data/processed/dim_customers.csv`)
48 distinct customer cohort profiles categorized by region, city, segment, and channel.

| Column Name | Data Type | Key Type | Description | Values / Examples |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | Varchar(20) | Primary Key | Unique account code | `CUST-0001` to `CUST-0048` |
| `country` | Varchar(50) | Attribute | Country location | United States |
| `region` | Varchar(50) | Attribute | Geographic territory | East, West, North, South |
| `state_city` | Varchar(100) | Attribute | Metropolitan area / city | New York, Seattle, Dallas, etc. |
| `customer_segment` | Varchar(50) | Attribute | Customer status tier | Existing, New |
| `sales_channel` | Varchar(50) | Attribute | Inbound purchasing channel | Online, Offline |

---

### Table: `Dim_Sales_Reps` (`data/processed/dim_sales_reps.csv`)
8 sales executives managing regional accounts.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `rep_id` | Varchar(20) | Primary Key | Representative ID (`REP-001` to `REP-008`) |
| `sales_rep_name` | Varchar(100) | Attribute | Sales Executive Full Name (e.g., Emily Watson, Alex Rivera) |
| `assigned_region` | Varchar(50) | Attribute | Territory assigned (East, West, North, South) |

---

### Table: `Dim_Regions` (`data/processed/dim_regions.csv`)
4 primary geographical sales territories.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `region_id` | Varchar(20) | Primary Key | Region code (`REG-01` to `REG-04`) |
| `region_name` | Varchar(50) | Attribute | East, West, North, South |
| `country` | Varchar(50) | Attribute | United States |

---

### Table: `Dim_Date` (`data/processed/dim_date.csv`)
731 continuous calendar days from 2024-01-01 to 2025-12-31 without gaps.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `date_key` | Integer | Primary Key | Date key (`YYYYMMDD`) |
| `date` | Date | Attribute | ISO calendar date (`YYYY-MM-DD`) |
| `year` | Integer | Hierarchy L1 | Calendar year (2024, 2025) |
| `quarter` | Varchar(5) | Hierarchy L2 | `Q1`, `Q2`, `Q3`, `Q4` |
| `quarter_name` | Varchar(10) | Attribute | e.g., `2024 Q1` |
| `month_number` | Integer | Hierarchy L3 | 1 to 12 |
| `month_name` | Varchar(20) | Hierarchy L3 | January - December |
| `month_year` | Varchar(15) | Attribute | e.g., `Jan 2024` |
| `day_of_month` | Integer | Attribute | 1 to 31 |
| `day_of_week` | Integer | Attribute | 1 (Monday) to 7 (Sunday) |
| `day_name` | Varchar(15) | Attribute | Monday - Sunday |
| `is_weekend` | Integer | Flag | `1` if Saturday/Sunday, else `0` |

---

## 3. Data Integrity & Validation Rules
- **No Orphan Records:** 100% of foreign keys in `Fact_Sales` reference valid primary keys in dimensions. Verified with `scripts/validate_cleaning.py`.
- **Financial Parity:** Macro totals reconcile exactly with source totals:
  - $\sum \text{sales\_amount} = \$1,577,535.00$
  - $\sum \text{cost} = \$935,710.00$
  - $\sum \text{profit} = \$641,825.00$
