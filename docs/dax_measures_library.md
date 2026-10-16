# DAX Measures & KPI Library

**Project:** Sales Performance & Revenue Growth Dashboard  
**Phase:** Phase 4 — DAX Measures and KPI Validation  
**Role:** Senior Power BI Developer and DAX Specialist  
**Status:** Validated Technical Specification & DAX Definitions  

---

## 1. Overview & Best Practices

All measures in this library follow strict Power BI performance and formatting standards:
1. **Explicit Measures Only:** All visual calculations must consume explicit DAX measures, never implicit column aggregations.
2. **Safe Division (`DIVIDE`):** Protects against divide-by-zero runtime exceptions, returning `BLANK()` when the denominator is zero or missing.
3. **Time-Intelligence Integrity:** Relies on the verified, contiguous `Dim_Date` table marked as the model Date Table.
4. **No Arbitrary Multipliers:** Percentages return fractional values ($0.00$ to $1.00$) formatted as Percentage (`0.0%`), never multiplied by 100 in the DAX definition.

---

## 2. Core Measures Library

### Measure 1: `Total Sales`
* **Business Definition:** Total monetary value of transactions completed.
* **DAX Formula:**
  ```dax
  Total Sales = 
  SUM(fact_sales[sales_amount])
  ```
* **Format:** Currency (`$#,##0.00`)
* **Required Columns:** `fact_sales[sales_amount]`
* **Expected Dataset Total:** `$1,577,535.00`
* **Validation Method:** Reconciled against raw source revenue ($Variance = $0.00$).

---

### Measure 2: `Total Quantity`
* **Business Definition:** Total physical units of product ordered across all transactions.
* **DAX Formula:**
  ```dax
  Total Quantity = 
  SUM(fact_sales[units_sold])
  ```
* **Format:** Whole Number (`#,##0`)
* **Required Columns:** `fact_sales[units_sold]`
* **Expected Dataset Total:** `5,708` units
* **Validation Method:** Reconciled against raw source units ($Variance = 0$).

---

### Measure 3: `Total Orders`
* **Business Definition:** Total number of distinct transaction orders processed.
* **DAX Formula:**
  ```dax
  Total Orders = 
  DISTINCTCOUNT(fact_sales[order_id])
  ```
* **Format:** Whole Number (`#,##0`)
* **Required Columns:** `fact_sales[order_id]`
* **Expected Dataset Total:** `600` orders
* **Validation Method:** Reconciled against distinct order row count.

---

### Measure 4: `Average Order Value` (AOV)
* **Business Definition:** Average revenue generated per unique transaction order.
* **DAX Formula:**
  ```dax
  Average Order Value = 
  DIVIDE([Total Sales], [Total Orders], BLANK())
  ```
* **Format:** Currency (`$#,##0.00`)
* **Required Measures:** `[Total Sales]`, `[Total Orders]`
* **Expected Dataset Value:** `$2,629.23` ($\frac{\$1,577,535.00}{600}$)
* **Validation Method:** Direct arithmetic parity check.
* **Known Limitations:** Evaluates to `BLANK()` if no orders exist in current filter context.

---

### Measure 5: `Sales Previous Year` (PY Sales)
* **Business Definition:** Total sales realized in the equivalent calendar period of the previous year.
* **DAX Formula:**
  ```dax
  Sales Previous Year = 
  CALCULATE(
      [Total Sales],
      SAMEPERIODLASTYEAR(dim_date[date])
  )
  ```
* **Format:** Currency (`$#,##0.00`)
* **Required Columns & Relationships:** `dim_date[date]` active relationship to `fact_sales[date]` (or `date_key`).
* **Expected Benchmark Values:**
  - Full Year 2025 Prior Year: `$680,675.00` (Equal to Full Year 2024 Sales)
  - Full Year 2024 Prior Year: `BLANK()` (No 2023 transactions exist)
  - January 2025 Prior Year: `$37,230.00`
  - February 2025 Prior Year: `$61,165.00`
* **Validation Method:** Multi-period time slice comparison.

---

### Measure 6: `Revenue Growth %` (YoY)
* **Business Definition:** Percentage change in revenue compared to the prior-year period.
* **DAX Formula:**
  ```dax
  Revenue Growth % = 
  VAR CurrentSales = [Total Sales]
  VAR PriorSales = [Sales Previous Year]
  RETURN
      IF(
          ISBLANK(PriorSales) || PriorSales == 0,
          BLANK(),
          DIVIDE(CurrentSales - PriorSales, PriorSales)
      )
  ```
* **Format:** Percentage (`+0.0%;-0.0%;0.0%`)
* **Required Measures:** `[Total Sales]`, `[Sales Previous Year]`
* **Expected Benchmark Values:**
  - Full Year 2025 YoY: `+31.8%` (`+31.7604%`)
  - Full Year 2024 YoY: `BLANK()` (Returns `BLANK()` safely because 2023 data does not exist)
  - January 2025 YoY: `+122.9%` (`+122.8579%`)
  - February 2025 YoY: `-27.6%` (`-27.5730%`)
  - October 2025 YoY: `+108.9%` (`+108.9212%`)
* **Validation Method:** Tested against independent baseline calculations.
* **Known Limitations:** Will return `BLANK()` for all 2024 periods due to the lack of 2023 history.

---

## 3. Supported Optional Measures

Cost and target information is present and validated in `fact_sales`.

### Measure 7: `Total Cost`
* **Business Definition:** Total Cost of Goods Sold (COGS).
* **DAX Formula:**
  ```dax
  Total Cost = 
  SUM(fact_sales[cost])
  ```
* **Format:** Currency (`$#,##0.00`)
* **Required Columns:** `fact_sales[cost]`
* **Expected Dataset Total:** `$935,710.00`

---

### Measure 8: `Total Profit`
* **Business Definition:** Gross profit earned after deducting standard inventory COGS.
* **DAX Formula:**
  ```dax
  Total Profit = 
  [Total Sales] - [Total Cost]
  ```
* **Format:** Currency (`$#,##0.00`)
* **Required Measures:** `[Total Sales]`, `[Total Cost]`
* **Expected Dataset Total:** `$641,825.00`

---

### Measure 9: `Profit Margin %`
* **Business Definition:** Proportion of total revenue remaining as gross profit.
* **DAX Formula:**
  ```dax
  Profit Margin % = 
  DIVIDE([Total Profit], [Total Sales], BLANK())
  ```
* **Format:** Percentage (`0.0%` or `0.00%`)
* **Required Measures:** `[Total Profit]`, `[Total Sales]`
* **Expected Dataset Total:** `40.69%` (`0.406853`)

---

### Measure 10: `Target Sales`
* **Business Definition:** Aggregate sales quota allocated for the selected period/dimension.
* **DAX Formula:**
  ```dax
  Target Sales = 
  SUM(fact_sales[target_sales])
  ```
* **Format:** Currency (`$#,##0.00`)
* **Required Columns:** `fact_sales[target_sales]`
* **Expected Dataset Total:** `$1,653,311.10`

---

### Measure 11: `Sales Achievement %`
* **Business Definition:** Percentage of sales quota attained ($Actual / Target$).
* **DAX Formula:**
  ```dax
  Sales Achievement % = 
  DIVIDE([Total Sales], [Target Sales], BLANK())
  ```
* **Format:** Percentage (`0.0%`)
* **Required Measures:** `[Total Sales]`, `[Target Sales]`
* **Expected Dataset Total:** `95.42%` (`0.954167`)

---

## 4. Dimensional Slice Benchmarks (Context Transition Validation)

| Slicing Dimension | Filter Value | Total Sales | Total Profit | Profit Margin % | Total Quantity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Category** | Accessories | $257,470.00 | $131,310.00 | 51.00% | 2,126 |
| **Category** | Electronics | $570,950.00 | $206,080.00 | 36.09% | 761 |
| **Category** | Furniture | $457,900.00 | $180,460.00 | 39.41% | 610 |
| **Category** | Office Supplies | $291,215.00 | $123,975.00 | 42.57% | 2,211 |
| **Region** | East | $424,675.00 | $173,760.00 | 40.92% | 1,514 |
| **Region** | North | $390,980.00 | $159,265.00 | 40.73% | 1,414 |
| **Region** | South | $425,680.00 | $172,400.00 | 40.50% | 1,566 |
| **Region** | West | $336,200.00 | $136,400.00 | 40.57% | 1,214 |
| **Annual Year** | 2024 | $680,675.00 | $276,460.00 | 40.62% | 2,467 |
| **Annual Year** | 2025 | $896,860.00 | $365,365.00 | 40.74% | 3,241 |
| **Total Model** | *(All)* | **$1,577,535.00** | **$641,825.00** | **40.69%** | **5,708** |
