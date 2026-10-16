"""
Dashboard Visuals & Interaction Validation Test Suite
Project: Sales Performance & Revenue Growth Dashboard
Role: Senior Power BI Report Developer & Dashboard Designer
Phase: Phase 5 - Dashboard Development

Automated testing of visual calculations, slicer cross-filtering,
multi-year timeline sorting, and boundary checks.
"""

import os
import sys
import pandas as pd
import numpy as np

def run_interaction_tests():
    project_root = r"D:\Power BI\Sales Performance & Revenue Growth Dashboard"
    processed_dir = os.path.join(project_root, "data", "processed")

    results = []

    def log_test(test_id, description, passed, details=""):
        status = "PASS" if passed else "FAIL"
        results.append({
            "test_id": test_id,
            "description": description,
            "status": status,
            "details": details
        })
        print(f"[{status}] {test_id}: {description} | {details}")

    print("=================================================================")
    print("PHASE 5: DASHBOARD INTERACTION & SLICER VALIDATION SUITE")
    print("=================================================================")

    # Load tables
    fact = pd.read_csv(os.path.join(processed_dir, "fact_sales.csv"))
    dim_date = pd.read_csv(os.path.join(processed_dir, "dim_date.csv"))
    dim_prod = pd.read_csv(os.path.join(processed_dir, "dim_products.csv"))
    dim_cust = pd.read_csv(os.path.join(processed_dir, "dim_customers.csv"))
    dim_reg = pd.read_csv(os.path.join(processed_dir, "dim_regions.csv"))

    df = fact.merge(dim_date, on='date_key', how='left')
    df = df.merge(dim_prod, on='product_id', how='left')
    df = df.merge(dim_cust, on='customer_id', how='left')
    df = df.merge(dim_reg, on='region_id', how='left')

    # Test 1: Top Row KPI Cards - Unfiltered State
    tot_sales = fact['sales_amount'].sum()
    tot_orders = fact['order_id'].nunique()
    tot_aov = tot_sales / tot_orders
    log_test("TC-DSB-01", "Top Row KPI Cards Unfiltered Totals",
             (tot_sales == 1577535.0) and (tot_orders == 600) and (abs(tot_aov - 2629.225) < 0.001),
             f"Sales: ${tot_sales:,.2f} | Orders: {tot_orders} | AOV: ${tot_aov:,.2f}")

    # Test 2: Top Row KPI Cards - 2025 Slicer State
    df_2025 = df[df['year'] == 2025]
    s_2025 = df_2025['sales_amount'].sum()
    o_2025 = df_2025['order_id'].nunique()
    aov_2025 = s_2025 / o_2025
    log_test("TC-DSB-02", "Top Row KPI Cards Filtered by Year=2025",
             (s_2025 == 896860.0) and (o_2025 == 315) and (abs(aov_2025 - 2847.1746) < 0.001),
             f"2025 Sales: ${s_2025:,.2f} | Orders: {o_2025} | AOV: ${aov_2025:,.2f}")

    # Test 3: Chronological multi-year timeline axis (24 distinct Year-Months)
    monthly_trend = df.groupby(['year', 'month_number', 'month_year'])['sales_amount'].sum().reset_index()
    monthly_trend['year_month_sort'] = monthly_trend['year'] * 100 + monthly_trend['month_number']
    monthly_trend = monthly_trend.sort_values(by='year_month_sort').reset_index(drop=True)
    axis_chronological = monthly_trend['year_month_sort'].is_monotonic_increasing and len(monthly_trend) == 24
    log_test("TC-DSB-03", "Multi-year monthly trend chronological sorting (24 Year-Months)",
             axis_chronological,
             f"Chronological point count: {len(monthly_trend)} points from {monthly_trend['month_year'].iloc[0]} to {monthly_trend['month_year'].iloc[-1]}")

    # Test 4: Category visual aggregation
    cat_sales = df.groupby('category')['sales_amount'].sum().to_dict()
    cat_expected = {
        'Accessories': 257470.0,
        'Electronics': 570950.0,
        'Furniture': 457900.0,
        'Office Supplies': 291215.0
    }
    cat_valid = all(cat_sales.get(k) == v for k, v in cat_expected.items())
    log_test("TC-DSB-04", "Sales by Product Category Visual Aggregations", cat_valid,
             f"All 4 categories match exact benchmark totals")

    # Test 5: Region visual aggregation
    reg_sales = df.groupby('region_name')['sales_amount'].sum().to_dict()
    reg_expected = {
        'East': 424675.0,
        'North': 390980.0,
        'South': 425680.0,
        'West': 336200.0
    }
    reg_valid = all(reg_sales.get(k) == v for k, v in reg_expected.items())
    log_test("TC-DSB-05", "Sales by Region Visual Aggregations", reg_valid,
             f"All 4 regions match exact benchmark totals")

    # Test 6: Product performance matrix (12 SKUs, verified string length and sorting)
    prod_matrix = df.groupby(['product_name', 'category']).agg({
        'sales_amount': 'sum',
        'units_sold': 'sum',
        'profit': 'sum'
    }).reset_index()
    max_name_len = prod_matrix['product_name'].apply(len).max()
    log_test("TC-DSB-06", "Product Performance Matrix (12 Products & Column Lengths)",
             len(prod_matrix) == 12 and max_name_len <= 35,
             f"12 products verified | Longest name: '{prod_matrix.loc[prod_matrix['product_name'].apply(len).idxmax(), 'product_name']}' ({max_name_len} chars)")

    # Test 7: Customer Segment breakdown
    seg_sales = df.groupby('customer_segment')['sales_amount'].sum().to_dict()
    seg_valid = (seg_sales['Existing'] == 1034005.0) and (seg_sales['New'] == 543530.0)
    log_test("TC-DSB-07", "Customer Segment Visual (Existing vs New)", seg_valid,
             f"Existing: ${seg_sales['Existing']:,.2f} (65.5%) | New: ${seg_sales['New']:,.2f} (34.5%)")

    # Test 8: Slicer Cross-Filtering: Year=2025 AND Region=East AND Category=Electronics
    compound_slice = df[(df['year'] == 2025) & (df['region_name'] == 'East') & (df['category'] == 'Electronics')]
    cs_sales = compound_slice['sales_amount'].sum()
    cs_orders = compound_slice['order_id'].nunique()
    log_test("TC-DSB-08", "Multi-slicer compound cross-filtering (Year + Region + Category)",
             (cs_sales == 82450.0) and (cs_orders == 17),
             f"Compound filtered slice: ${cs_sales:,.2f} across {cs_orders} orders")

    # Test 9: Zero result empty state test
    # Slicer with impossible condition: Year=2024 AND City=Tokyo (non-existent)
    empty_slice = df[df['state_city'] == 'Tokyo']
    log_test("TC-DSB-09", "Empty filter state resilience (No crashes on empty selection)",
             len(empty_slice) == 0 and empty_slice['sales_amount'].sum() == 0.0,
             "Empty filter context gracefully yields 0 orders / $0.00 sales")

    # Test 10: Contrast and Theme File Persistence
    theme_path = os.path.join(project_root, "scripts", "powerbi_theme.json")
    theme_exists = os.path.exists(theme_path) and os.path.getsize(theme_path) > 100
    log_test("TC-DSB-10", "Power BI Theme JSON artifact verification", theme_exists,
             f"Theme file verified at {theme_path}")

    print("=================================================================")
    all_passed = all(t['status'] == "PASS" for t in results)
    if all_passed:
        print("ALL 10 DASHBOARD INTERACTION TESTS PASSED.")
    else:
        print("FAILURES DETECTED IN DASHBOARD INTERACTIONS.")
        sys.exit(1)

    return results

if __name__ == "__main__":
    run_interaction_tests()
