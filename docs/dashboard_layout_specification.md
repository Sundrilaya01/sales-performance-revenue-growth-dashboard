# Power BI Dashboard Layout & Visual Specification

**Project:** Sales Performance & Revenue Growth Dashboard  
**Phase:** Phase 5  -  Dashboard Development  
**Role:** Senior Power BI Report Developer and Dashboard Designer  
**Page Title:** Executive Sales & Revenue Overview  
**Canvas Resolution:** 16:9 Widescreen (1280 x 720 px / 1920 x 1080 px scaled)  
**Theme:** `scripts/powerbi_theme.json` (Corporate Executive Slate & Navy)  

---

## 1. Visual Canvas Grid Layout Architecture

```
+-----------------------------------------------------------------------------------------------------------------------+
|  PAGE HEADER: Executive Sales & Revenue Growth Dashboard                     [Slicer: Year] [Region] [Category] [Seg] |
+-----------------------------------------------------------------------------------------------------------------------+
|  [ KPI CARD 1 ]          |  [ KPI CARD 2 ]          |  [ KPI CARD 3 ]          |  [ KPI CARD 4 ]                      |
|  Total Sales             |  Revenue Growth %        |  Average Order Value     |  Total Orders                        |
|  $1,577,535.00           |  +31.8% (YoY)            |  $2,629.23               |  600                                 |
+--------------------------+--------------------------+--------------------------+--------------------------------------+
|  [ VISUAL 5: MIDDLE LEFT ]                          |  [ VISUAL 6: MIDDLE CENTER ] |  [ VISUAL 7: MIDDLE RIGHT ]      |
|  Monthly Revenue Velocity & Prior-Year Benchmark    |  Revenue by Category         |  Revenue by Region               |
|  (Line & Column Chart: 24 Month Chronological Axis) |  (Horizontal Bar Chart)      |  (Clustered Column Chart)        |
|  Current Sales vs. Sales Previous Year              |  Electronics, Furniture, etc.|  East, South, North, West        |
+-----------------------------------------------------+------------------------------+----------------------------------+
|  [ VISUAL 8: BOTTOM LEFT / CENTER ]                                                |  [ VISUAL 9: BOTTOM RIGHT ]      |
|  Product Performance Breakdown Matrix                                              |  Customer Segment & Channel Mix  |
|  (12 SKUs: Units, Total Sales, COGS, Profit, Margin %, AOV)                        |  (Existing vs. New / Channels)   |
+------------------------------------------------------------------------------------+----------------------------------+
```

---

## 2. Visual Inventory & Field Well Configuration

### Section A: Top Row  -  Executive KPI Cards

| Card ID | Visual Title | Primary Measure | Callout Font & Format | Secondary Subtitle / Indicator | Target Value (Unfiltered) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KPI-01** | **Total Sales** | `[Total Sales]` | 26pt Bold, Currency (`$#,##0.00`) | Quota: `$1,653,311.10` (`95.4%`) | `$1,577,535.00` |
| **KPI-02** | **Revenue Growth %** | `[Revenue Growth %]` | 26pt Bold, Percentage (`+0.0%`) | Conditional Color: Green/Red | `+31.8%` (2025) / `BLANK` (2024) |
| **KPI-03** | **Average Order Value** | `[Average Order Value]` | 26pt Bold, Currency (`$#,##0.00`) | Benchmark: `$2,500.00` Target | `$2,629.23` |
| **KPI-04** | **Total Orders** | `[Total Orders]` | 26pt Bold, Whole Number (`#,##0`) | Units Sold: `5,708` | `600` Orders |

---

### Section B: Middle Row  -  Trends & Dimensional Performance

#### Visual 5: Monthly Revenue Trend & Prior-Year Benchmark
* **Visual Type:** Line and Clustered Column Chart (or Line Chart with 2 series)
* **X-Axis (Shared):** `dim_date[month_year]`
  * **Critical Sort Rule:** Column `dim_date[month_year]` must be set to **Sort by Column -> `dim_date[year_month_sort]`** (or `date_key`). This guarantees 24 chronological intervals from `Jan 2024` through `Dec 2025` without alphabetical distortion.
* **Column Values (Bars):** `[Total Sales]` (Corporate Navy: `#1E3A8A`)
* **Line Values (Trend):** `[Sales Previous Year]` (Slate Teal: `#0D9488`, dashed stroke)
* **Tooltip Fields:** `[Total Sales]`, `[Sales Previous Year]`, `[Revenue Growth %]`, `[Total Quantity]`
* **Data Labels:** Enabled on line markers for key inflection months.

#### Visual 6: Sales by Product Category
* **Visual Type:** Horizontal Clustered Bar Chart
* **Y-Axis (Categories):** `dim_products[category]` (Sorted descending by `[Total Sales]`)
* **X-Axis (Values):** `[Total Sales]`
* **Data Bar Color:** Deep Cobalt (`#1E3A8A`)
* **Data Labels:** Inside base, formatted as Currency Millions/Thousands (`$571.0K`, `$457.9K`, `$291.2K`, `$257.5K`)
* **Tooltips:** `[Total Profit]`, `[Profit Margin %]`, `[Total Quantity]`

#### Visual 7: Sales by Region
* **Visual Type:** Clustered Column Chart
* **X-Axis:** `dim_regions[region_name]` (East, South, North, West)
* **Y-Axis:** `[Total Sales]`
* **Color:** Gradient Accent (`#3B82F6`)
* **Tooltips:** `[Total Sales]`, `[Total Orders]`, `[Profit Margin %]`

---

### Section C: Bottom Row  -  Granular Matrix & Segmentation

#### Visual 8: Product Performance Matrix
* **Visual Type:** Matrix / Table
* **Rows:** `dim_products[category]` $\rightarrow$ `dim_products[product_name]`
* **Values (Columns):**
  1. `[Total Quantity]` (Formatted `#,##0`)
  2. `[Total Sales]` (Formatted `$#,##0.00`, Sorted Descending)
  3. `[Total Cost]` (Formatted `$#,##0.00`)
  4. `[Total Profit]` (Formatted `$#,##0.00`)
  5. `[Profit Margin %]` (Formatted `0.0%`, with subtle green background heat-shading)
  6. `[Average Order Value]` (Formatted `$#,##0.00`)
* **Column Widths & Padding:** Auto-fit with minimum column width 90px; compact cell padding.
* **Totals:** Bottom row subtotal and grand total enabled.

#### Visual 9: Customer Segment & Channel Mix
* **Visual Type:** Clustered Column Chart
* **X-Axis:** `dim_customers[customer_segment]` (Existing vs. New)
* **Legend:** `dim_customers[sales_channel]` (Offline vs. Online)
* **Y-Axis:** `[Total Sales]`
* **Tooltips:** `[Sales Achievement %]`, `[Total Orders]`

---

### Section D: Global Filters (Slicers Panel)

| Slicer Name | Source Field | Slicer Style | Default Selection | Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Year** | `dim_date[year]` | Tile / Horizontal Pills | `All` (or `2025`) | Slices all visuals across entire page |
| **Region** | `dim_regions[region_name]` | Dropdown with Search | `All` | Filters East, North, South, West |
| **Category** | `dim_products[category]` | Dropdown with Search | `All` | Filters 4 product categories |
| **Customer Tier** | `dim_customers[customer_segment]` | Tile Pills (`Existing`, `New`) | `All` | Filters customer cohorts |

---

## 3. Design Tokens & Styling Standards

* **Page Background:** Neutral Off-White (`#F8FAFC`)
* **Card & Visual Backgrounds:** Pure White (`#FFFFFF`) with 8px corner radius and subtle drop-shadow (`rgba(0,0,0,0.05)`).
* **Typography Hierarchy:**
  - Page Title: Segoe UI Bold, 18pt, `#0F172A`
  - Visual Titles: Segoe UI Semibold, 12pt, `#1E293B`
  - KPI Callout Values: Segoe UI Bold, 26pt, `#0F172A`
  - Axis & Data Labels: Segoe UI, 9pt, `#64748B`
* **Color Usage Rule:** Color is never used as the sole indicator of performance. Positive and negative badges always include numerical signs (`+` / `-`) alongside Green (`#10B981`) or Red (`#EF4444`).

---

## 4. Manual Power BI Desktop Implementation Procedure

To construct this dashboard inside Power BI Desktop:

1. **Apply Corporate Theme:**
   - In Power BI Desktop, navigate to **View** ribbon -> click **Themes** dropdown -> select **Browse for themes**.
   - Select and load [`scripts/powerbi_theme.json`](file:///d:/Power%20BI/Sales%20Performance%20&%20Revenue%20Growth%20Dashboard/scripts/powerbi_theme.json).
2. **Add Global Slicers:**
   - Insert 4 Slicer visuals across the top toolbar area: `dim_date[year]`, `dim_regions[region_name]`, `dim_products[category]`, `dim_customers[customer_segment]`.
3. **Insert Top KPI Cards:**
   - Insert 4 **Card (New)** or standard **Card** visuals across coordinates $Y=80\text{px}$, assigning the measures specified in Section A.
4. **Insert Middle Row Charts:**
   - Insert **Line and Clustered Column Chart** on the left ($W=580\text{px}, H=260\text{px}$). Set Shared Axis to `dim_date[month_year]`, Column Values to `[Total Sales]`, Line Values to `[Sales Previous Year]`.
   - Insert **Clustered Bar Chart** in the center ($W=320\text{px}, H=260\text{px}$) for Category sales.
   - Insert **Clustered Column Chart** on the right ($W=320\text{px}, H=260\text{px}$) for Regional sales.
5. **Insert Bottom Row Tables:**
   - Insert **Matrix** on the bottom left ($W=850\text{px}, H=280\text{px}$) with rows `dim_products[category]` and `dim_products[product_name]`.
   - Insert **Clustered Column Chart** on the bottom right ($W=370\text{px}, H=280\text{px}$) for Customer Segment by Channel.
6. **Save Project:**
   - Save the report as `Sales Performance & Revenue Growth Dashboard.pbix`.

---

## 5. Interaction Test Matrix (Automated Verification)

Executed via automated test suite [`scripts/validate_dashboard_interactions.py`](file:///d:/Power%20BI/Sales%20Performance%20&%20Revenue%20Growth%20Dashboard/scripts/validate_dashboard_interactions.py):

| Test ID | Interaction / Filter Scenario | Expected Behavior & Calculation | Verified Test Result |
| :--- | :--- | :--- | :--- |
| `TC-DSB-01` | Baseline / Unfiltered Slicer State | KPI Cards display: Sales $1,577,535.00, Orders: 600, AOV: $2,629.23 | **PASS** |
| `TC-DSB-02` | Slicer Selection: `Year = 2025` | Sales: $896,860.00, Orders: 315, AOV: $2,847.17, Growth: +31.8% | **PASS** |
| `TC-DSB-03` | Timeline Axis Sorting | 24 continuous chronological points sorted by `year_month_sort` | **PASS** |
| `TC-DSB-04` | Category Breakdown Parity | Electronics: $570,950.00, Furniture: $457,900.00, Office: $291,215.00, Acc: $257,470.00 | **PASS** |
| `TC-DSB-05` | Regional Breakdown Parity | East: $424,675.00, South: $425,680.00, North: $390,980.00, West: $336,200.00 | **PASS** |
| `TC-DSB-06` | Matrix Long Product Names | 12 SKUs, max title length 29 chars (no text truncation errors) | **PASS** |
| `TC-DSB-07` | Customer Segment Breakdown | Existing: $1,034,005.00 (65.5%), New: $543,530.00 (34.5%) | **PASS** |
| `TC-DSB-08` | Compound Cross-Filter: Year=2025 + East + Electronics | Reconciles to $82,450.00 across exactly 17 orders | **PASS** |
| `TC-DSB-09` | Empty Filter State Resilience | Empty selection gracefully handles zero data without engine crash | **PASS** |
| `TC-DSB-10` | Theme JSON Artifact Verification | Theme file verified intact at `scripts/powerbi_theme.json` | **PASS** |
