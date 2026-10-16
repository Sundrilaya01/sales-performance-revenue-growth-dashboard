"""
Data Cleaning and Preparation Pipeline
Project: Sales Performance & Revenue Growth Dashboard
Role: Senior Data Engineer
Phase: Phase 2 - Data Collection & Preparation

This script reads the raw sales dataset from data/raw/, performs validation,
standardization, key generation, and dimensional modeling (Star Schema),
and exports the cleaned tables to data/processed/.
"""

import os
import sys
import pandas as pd
import numpy as np

def run_pipeline():
    project_root = r"D:\Power BI\Sales Performance & Revenue Growth Dashboard"
    raw_path = os.path.join(project_root, "data", "raw", "sales_performance_dataset.csv")
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    print("=================================================================")
    print("STEP 1: LOADING RAW DATASET")
    print(f"Source file: {raw_path}")
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw dataset not found at {raw_path}")

    raw_df = pd.read_csv(raw_path)
    initial_rows, initial_cols = raw_df.shape
    print(f"Loaded {initial_rows} rows and {initial_cols} columns successfully.")

    print("\nSTEP 2: AUDITING QUALITY & PROVENANCE")
    # Missing values check
    missing_counts = raw_df.isnull().sum()
    total_missing = missing_counts.sum()
    print(f"Total missing values: {total_missing}")

    # Duplicates check
    exact_duplicates = raw_df.duplicated().sum()
    print(f"Exact duplicate rows: {exact_duplicates}")

    # Date parsing
    raw_df['Date_Parsed'] = pd.to_datetime(raw_df['Date'], format='%Y-%m-%d', errors='coerce')
    invalid_dates = raw_df['Date_Parsed'].isnull().sum()
    print(f"Invalid dates detected: {invalid_dates}")
    if invalid_dates > 0:
        raise ValueError("Invalid dates present in raw data!")

    # Sort strictly by date for reproducible sequencing
    df = raw_df.sort_values(by=['Date_Parsed', 'Region', 'State/City', 'Product Name']).reset_index(drop=True)

    print("\nSTEP 3: GENERATING DETERMINISTIC KEYS & MASTER ENTITIES")
    # 1. Product Dimension
    product_records = []
    prod_grouped = df.groupby(['Product Category', 'Product Name']).agg({
        'Selling Price': 'first',
        'Cost': lambda s: (s / df.loc[s.index, 'Units Sold']).iloc[0]
    }).reset_index()

    # Deterministic product ID generator
    cat_prefix = {
        'Electronics': 'ELE',
        'Furniture': 'FUR',
        'Office Supplies': 'OFF',
        'Accessories': 'ACC'
    }

    prod_id_map = {}
    prod_rows = []
    cat_counters = {k: 1 for k in cat_prefix.values()}

    for _, row in prod_grouped.sort_values(by=['Product Category', 'Product Name']).iterrows():
        p_cat = row['Product Category']
        p_name = row['Product Name']
        p_price = float(row['Selling Price'])
        p_cost = float(row['Cost'])
        p_margin = p_price - p_cost
        p_margin_pct = round((p_margin / p_price) * 100, 2)
        
        pref = cat_prefix.get(p_cat, 'GEN')
        pid = f"PRD-{pref}-{cat_counters[pref]:03d}"
        cat_counters[pref] += 1
        
        prod_id_map[p_name] = pid
        prod_rows.append({
            'product_id': pid,
            'product_name': p_name,
            'category': p_cat,
            'unit_price': p_price,
            'unit_cost': p_cost,
            'unit_margin': p_margin,
            'target_margin_pct': p_margin_pct
        })

    dim_product_df = pd.DataFrame(prod_rows)
    print(f"Created Dim_Product: {len(dim_product_df)} distinct products.")

    # 2. Sales Rep Dimension
    reps_grouped = df[['Sales Executive Name', 'Region']].drop_duplicates().sort_values(by=['Region', 'Sales Executive Name']).reset_index(drop=True)
    rep_id_map = {}
    rep_rows = []
    for idx, row in reps_grouped.iterrows():
        rid = f"REP-{idx + 1:03d}"
        rep_id_map[row['Sales Executive Name']] = rid
        rep_rows.append({
            'rep_id': rid,
            'sales_rep_name': row['Sales Executive Name'],
            'assigned_region': row['Region']
        })
    dim_rep_df = pd.DataFrame(rep_rows)
    print(f"Created Dim_Sales_Rep: {len(dim_rep_df)} sales representatives.")

    # 3. Customer Cohort / Account Dimension
    # Map each distinct (Region, State/City, Customer Type, Sales Channel)
    cust_grouped = df[['Region', 'State/City', 'Customer Type', 'Sales Channel']].drop_duplicates().sort_values(
        by=['Region', 'State/City', 'Customer Type', 'Sales Channel']
    ).reset_index(drop=True)
    cust_id_map = {}
    cust_rows = []
    for idx, row in cust_grouped.iterrows():
        cid = f"CUST-{idx + 1:04d}"
        key_tuple = (row['Region'], row['State/City'], row['Customer Type'], row['Sales Channel'])
        cust_id_map[key_tuple] = cid
        cust_rows.append({
            'customer_id': cid,
            'country': 'United States',
            'region': row['Region'],
            'state_city': row['State/City'],
            'customer_segment': row['Customer Type'],
            'sales_channel': row['Sales Channel']
        })
    dim_customer_df = pd.DataFrame(cust_rows)
    print(f"Created Dim_Customer: {len(dim_customer_df)} customer accounts/cohorts.")

    # 4. Region Dimension
    reg_id_map = {
        'East': 'REG-01',
        'West': 'REG-02',
        'North': 'REG-03',
        'South': 'REG-04'
    }
    reg_rows = [
        {'region_id': 'REG-01', 'region_name': 'East', 'country': 'United States'},
        {'region_id': 'REG-02', 'region_name': 'West', 'country': 'United States'},
        {'region_id': 'REG-03', 'region_name': 'North', 'country': 'United States'},
        {'region_id': 'REG-04', 'region_name': 'South', 'country': 'United States'}
    ]
    dim_region_df = pd.DataFrame(reg_rows)

    # 5. Calendar / Date Dimension
    min_date = df['Date_Parsed'].min()
    max_date = df['Date_Parsed'].max()
    full_date_range = pd.date_range(start='2024-01-01', end='2025-12-31', freq='D')
    date_rows = []
    for d in full_date_range:
        date_rows.append({
            'date_key': int(d.strftime('%Y%m%d')),
            'date': d.strftime('%Y-%m-%d'),
            'year': int(d.year),
            'quarter': f"Q{d.quarter}",
            'quarter_name': f"{d.year} Q{d.quarter}",
            'month_number': int(d.month),
            'month_name': d.strftime('%B'),
            'month_year': d.strftime('%b %Y'),
            'day_of_month': int(d.day),
            'day_of_week': int(d.dayofweek + 1),
            'day_name': d.strftime('%A'),
            'is_weekend': 1 if d.dayofweek >= 5 else 0
        })
    dim_date_df = pd.DataFrame(date_rows)
    print(f"Created Dim_Date: {len(dim_date_df)} continuous calendar days (2024-2025).")

    print("\nSTEP 4: CONSTRUCTING AND VALIDATING FACT TABLE")
    fact_rows = []
    for idx, row in df.iterrows():
        oid = f"ORD-{row['Year']}-{idx + 1:04d}"
        pid = prod_id_map[row['Product Name']]
        rid = rep_id_map[row['Sales Executive Name']]
        cust_key = (row['Region'], row['State/City'], row['Customer Type'], row['Sales Channel'])
        cid = cust_id_map[cust_key]
        reg_id = reg_id_map[row['Region']]

        u_sold = int(row['Units Sold'])
        u_price = float(row['Selling Price'])
        s_amount = float(row['Revenue'])
        cost = float(row['Cost'])
        profit = float(row['Profit'])
        margin_pct = float(row['Profit Margin %'])
        t_sales = float(row['Target Sales'])
        act_sales = float(row['Actual Sales'])
        achieve_pct = float(row['Achievement %'])
        growth_pct = float(row['Growth %'])
        d_key = int(row['Date_Parsed'].strftime('%Y%m%d'))

        fact_rows.append({
            'order_id': oid,
            'date_key': d_key,
            'date': row['Date'],
            'product_id': pid,
            'customer_id': cid,
            'rep_id': rid,
            'region_id': reg_id,
            'units_sold': u_sold,
            'unit_price': u_price,
            'sales_amount': s_amount,
            'cost': cost,
            'profit': profit,
            'profit_margin_pct': margin_pct,
            'target_sales': t_sales,
            'actual_sales': act_sales,
            'achievement_pct': achieve_pct,
            'growth_pct': growth_pct
        })

    fact_sales_df = pd.DataFrame(fact_rows)

    print("\nSTEP 5: FINANCIAL RECONCILIATION & INTEGRITY CHECKS")
    # 1. Sales amount check
    calc_sales = fact_sales_df['units_sold'] * fact_sales_df['unit_price']
    sales_diff = np.abs(fact_sales_df['sales_amount'] - calc_sales).max()
    print(f"Max difference in Sales Amount = Units * Unit Price: {sales_diff:.4f}")
    assert sales_diff < 0.001, "Sales Amount check failed!"

    # 2. Profit check
    calc_profit = fact_sales_df['sales_amount'] - fact_sales_df['cost']
    profit_diff = np.abs(fact_sales_df['profit'] - calc_profit).max()
    print(f"Max difference in Profit = Sales Amount - Cost: {profit_diff:.4f}")
    assert profit_diff < 0.001, "Profit check failed!"

    # 3. Source total reconciliation
    raw_total_rev = raw_df['Revenue'].sum()
    fact_total_rev = fact_sales_df['sales_amount'].sum()
    print(f"Raw Revenue Total:  ${raw_total_rev:,.2f}")
    print(f"Fact Revenue Total: ${fact_total_rev:,.2f}")
    rev_reconciled = abs(raw_total_rev - fact_total_rev)
    print(f"Revenue Reconciliation Delta: ${rev_reconciled:.4f}")
    assert rev_reconciled < 0.01, "Revenue reconciliation failed!"

    raw_total_profit = raw_df['Profit'].sum()
    fact_total_profit = fact_sales_df['profit'].sum()
    profit_reconciled = abs(raw_total_profit - fact_total_profit)
    print(f"Profit Reconciliation Delta:  ${profit_reconciled:.4f}")
    assert profit_reconciled < 0.01, "Profit reconciliation failed!"

    raw_total_cost = raw_df['Cost'].sum()
    fact_total_cost = fact_sales_df['cost'].sum()
    cost_reconciled = abs(raw_total_cost - fact_total_cost)
    print(f"Cost Reconciliation Delta:    ${cost_reconciled:.4f}")
    assert cost_reconciled < 0.01, "Cost reconciliation failed!"

    print("\nSTEP 6: EXPORTING CLEANED DATASETS")
    out_files = {
        "fact_sales.csv": fact_sales_df,
        "dim_products.csv": dim_product_df,
        "dim_customers.csv": dim_customer_df,
        "dim_sales_reps.csv": dim_rep_df,
        "dim_regions.csv": dim_region_df,
        "dim_date.csv": dim_date_df
    }

    for fname, odf in out_files.items():
        out_path = os.path.join(processed_dir, fname)
        odf.to_csv(out_path, index=False)
        print(f"Exported {fname} ({len(odf)} rows, {len(odf.columns)} cols) -> {out_path}")

    # Also export consolidated cleaned master dataset
    consolidated_df = fact_sales_df.merge(dim_product_df[['product_id', 'product_name', 'category', 'unit_cost']], on='product_id', how='left')
    consolidated_df = consolidated_df.merge(dim_customer_df[['customer_id', 'country', 'region', 'state_city', 'customer_segment', 'sales_channel']], on='customer_id', how='left')
    consolidated_df = consolidated_df.merge(dim_rep_df[['rep_id', 'sales_rep_name']], on='rep_id', how='left')
    consolidated_path = os.path.join(processed_dir, "cleaned_sales_consolidated.csv")
    consolidated_df.to_csv(consolidated_path, index=False)
    print(f"Exported cleaned_sales_consolidated.csv ({len(consolidated_df)} rows, {len(consolidated_df.columns)} cols)")

    print("\nPIPELINE COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_pipeline()
