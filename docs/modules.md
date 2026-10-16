# System Modules & Component Breakdown

This document describes all operational modules within the project, their responsibilities, inputs, outputs, and dependencies.

---

## 1. Module Inventory

```
Project Root
├── Module 1: Ingestion & Pipeline Ingestor
├── Module 2: Data Cleaning & Preprocessing
├── Module 3: Dimensional Modeling & Semantic Relations
├── Module 4: DAX & Business Calculation Engine
├── Module 5: Predictive Analytics & Forecasting Engine
├── Module 6: Power BI Reporting & UI Visualization
└── Module 7: Quality Assurance & Data Reconciliation
```

---

## 2. Detailed Module Descriptions

### Module 1: Ingestion & Pipeline Ingestor
- **Purpose:** Reliable ingestion of disparate raw data sources.
- **Inputs:** Raw files (CSV, XLSX, SQL dumps, REST APIs).
- **Outputs:** Staging data structures with raw metadata (ingestion timestamp, batch ID).
- **Core Logic:** Handles file encoding, batch chunking, and schema drift detection.

### Module 2: Data Cleaning & Preprocessing
- **Purpose:** Prepares raw data into clean, compliant tabular sets.
- **Inputs:** Staged raw tables.
- **Outputs:** Curated tables ready for star schema relationships.
- **Core Logic:**
  - Date parsing and timezone standardization.
  - Value imputation and handling of missing fields.
  - Outlier detection in revenue and discount rates.

### Module 3: Dimensional Modeling & Semantic Relations
- **Purpose:** Constructs the Star Schema data model.
- **Inputs:** Curated tables.
- **Outputs:** Relational model with 1-to-many single-direction filtering relationships.
- **Core Logic:** Ensures no bidirectional ambiguities, creates surrogate keys, optimizes memory usage (cardinality reduction).

### Module 4: DAX & Business Calculation Engine
- **Purpose:** Computes business KPIs dynamically based on user slicers and filter contexts.
- **Inputs:** Fact and Dimension tables in Power BI.
- **Outputs:** Standardized Measures (Total Revenue, YoY Growth %, Profit Margin %, Churn Rate, Run Rate).
- **Core Logic:** Evaluates measures using `CALCULATE`, `DATESYTD`, `SAMEPERIODLASTYEAR`, `DIVIDE`, and context transition.

### Module 5: Predictive Analytics & Forecasting Engine
- **Purpose:** Analyzes historical sales velocity and generates forward-looking revenue forecasts.
- **Inputs:** Aggregated time-series sales records, promotional markers, seasonal indicators.
- **Outputs:** Forecasted revenue, confidence intervals (lower/upper bound 95%), trend indicators.
- **Core Logic:** Time-series decomposition, baseline statistical models, and trend regression.

### Module 6: Power BI Reporting & UI Visualization
- **Purpose:** Provides interactive dashboards for executives and operational teams.
- **Inputs:** Semantic model, DAX measures, and forecast outputs.
- **Outputs:** Executive views, drill-down tables, Pareto charts, cohort heatmaps, and geospatial maps.
- **Core Logic:** High-contrast, clean visual hierarchy, synchronized slicers, and cross-highlighting.

### Module 7: Quality Assurance & Data Reconciliation
- **Purpose:** Guarantees data veracity between source systems and the dashboard.
- **Inputs:** Source totals vs. final dashboard measures.
- **Outputs:** Verification reports, parity audit logs, tolerance breach alerts.
- **Core Logic:** Checksum matching, row count validation, negative margin detection, orphan key identification.
