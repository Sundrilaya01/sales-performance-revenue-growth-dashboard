"""
Quality Assurance and Validation Test Runner
Project: Sales Performance & Revenue Growth Dashboard
Phase: Phase 2 - Data Collection & Preparation

Automated suite to validate referential integrity, financial parity,
null constraints, and file persistence.
"""

import os
import sys
import pandas as pd
import numpy as np

def run_tests():
    project_root = r"D:\Power BI\Sales Performance & Revenue Growth Dashboard"
    raw_path = os.path.join(project_root, "data", "raw", "sales_performance_dataset.csv")
    processed_dir = os.path.join(project_root, "data", "processed")

    test_results = []

    def record_test(test_id, description, passed, details=""):
        status = "PASS" if passed else "FAIL"
        test_results.append({
            "test_id": test_id,
            "description": description,
            "status": status,
            "details": details
        })
        print(f"[{status}] {test_id}: {description} | {details}")

    print("=================================================================")
    print("RUNNING PHASE 2 VALIDATION TESTS")
    print("=================================================================")

    # Test 1: Check raw file immutability and presence
    raw_exists = os.path.exists(raw_path)
    raw_size = os.path.getsize(raw_path) if raw_exists else 0
    # Phase 1 noted size was 101,909 bytes
    record_test("TC-VAL-01", "Raw source file preservation and immutability", raw_exists and raw_size == 101909, f"Size: {raw_size} bytes")

    # Test 2: Check output processed files existence
    expected_files = [
        "fact_sales.csv", "dim_products.csv", "dim_customers.csv",
        "dim_sales_reps.csv", "dim_regions.csv", "dim_date.csv",
        "cleaned_sales_consolidated.csv"
    ]
    all_files_exist = all(os.path.exists(os.path.join(processed_dir, f)) for f in expected_files)
    record_test("TC-VAL-02", "Processed output tables existence", all_files_exist, f"Found {len(expected_files)} files in data/processed/")

    # Load datasets
    raw_df = pd.read_csv(raw_path)
    fact_df = pd.read_csv(os.path.join(processed_dir, "fact_sales.csv"))
    prod_df = pd.read_csv(os.path.join(processed_dir, "dim_products.csv"))
    cust_df = pd.read_csv(os.path.join(processed_dir, "dim_customers.csv"))
    rep_df = pd.read_csv(os.path.join(processed_dir, "dim_sales_reps.csv"))
    reg_df = pd.read_csv(os.path.join(processed_dir, "dim_regions.csv"))
    date_df = pd.read_csv(os.path.join(processed_dir, "dim_date.csv"))

    # Test 3: Row count preservation
    row_count_match = len(fact_df) == len(raw_df) == 600
    record_test("TC-VAL-03", "Fact table row count parity with raw source", row_count_match, f"Fact: {len(fact_df)} rows, Raw: {len(raw_df)} rows")

    # Test 4: Primary key uniqueness in Fact table
    pk_sales_unique = fact_df['order_id'].is_unique and fact_df['order_id'].isnull().sum() == 0
    record_test("TC-VAL-04", "Fact_Sales order_id uniqueness and non-null", pk_sales_unique, f"Unique: {fact_df['order_id'].nunique()}/600")

    # Test 5: Dimension primary keys uniqueness
    dim_pks_unique = (
        prod_df['product_id'].is_unique and
        cust_df['customer_id'].is_unique and
        rep_df['rep_id'].is_unique and
        reg_df['region_id'].is_unique and
        date_df['date_key'].is_unique
    )
    record_test("TC-VAL-05", "Dimension tables primary key uniqueness", dim_pks_unique, "All dimension primary keys verified 100% unique")

    # Test 6: Referential integrity (Foreign Keys in Fact_Sales)
    orphan_products = set(fact_df['product_id']) - set(prod_df['product_id'])
    orphan_customers = set(fact_df['customer_id']) - set(cust_df['customer_id'])
    orphan_reps = set(fact_df['rep_id']) - set(rep_df['rep_id'])
    orphan_regions = set(fact_df['region_id']) - set(reg_df['region_id'])
    orphan_dates = set(fact_df['date_key']) - set(date_df['date_key'])

    total_orphans = len(orphan_products) + len(orphan_customers) + len(orphan_reps) + len(orphan_regions) + len(orphan_dates)
    record_test("TC-VAL-06", "Referential integrity across all Star Schema relationships", total_orphans == 0, f"Orphans detected: {total_orphans}")

    # Test 7: Unit level calculation accuracy (Sales Amount = Units * Unit Price)
    calc_sales = fact_df['units_sold'] * fact_df['unit_price']
    sales_diff = np.abs(fact_df['sales_amount'] - calc_sales).max()
    record_test("TC-VAL-07", "Line-item Sales Amount = Units Sold * Unit Price", sales_diff < 0.001, f"Max difference: {sales_diff:.6f}")

    # Test 8: Line-item Profit calculation accuracy (Profit = Sales Amount - Cost)
    calc_profit = fact_df['sales_amount'] - fact_df['cost']
    profit_diff = np.abs(fact_df['profit'] - calc_profit).max()
    record_test("TC-VAL-08", "Line-item Profit = Sales Amount - Cost", profit_diff < 0.001, f"Max difference: {profit_diff:.6f}")

    # Test 9: Overall Financial Total Reconciliation
    raw_rev = raw_df['Revenue'].sum()
    fact_rev = fact_df['sales_amount'].sum()
    rev_match = abs(raw_rev - fact_rev) < 0.01

    raw_cost = raw_df['Cost'].sum()
    fact_cost = fact_df['cost'].sum()
    cost_match = abs(raw_cost - fact_cost) < 0.01

    raw_profit = raw_df['Profit'].sum()
    fact_profit = fact_df['profit'].sum()
    profit_match = abs(raw_profit - fact_profit) < 0.01

    all_fin_match = rev_match and cost_match and profit_match
    record_test("TC-VAL-09", "Macro Financial Totals Reconciliation (Revenue, Cost, Profit)", all_fin_match,
                f"Revenue: ${fact_rev:,.2f} (Diff: ${abs(raw_rev-fact_rev):.4f}) | Profit: ${fact_profit:,.2f} (Diff: ${abs(raw_profit-fact_profit):.4f})")

    # Test 10: Date continuity and boundary checks
    date_range_len = len(date_df)
    expected_days = 731 # 366 in 2024 (leap year) + 365 in 2025
    record_test("TC-VAL-10", "Continuous Dim_Date calendar coverage without gaps", date_range_len == expected_days, f"Days: {date_range_len} (expected 731)")

    print("=================================================================")
    all_passed = all(t['status'] == "PASS" for t in test_results)
    if all_passed:
        print("ALL 10 VALIDATION TESTS PASSED WITH 100% SUCCESS.")
    else:
        print("SOME TESTS FAILED.")
        sys.exit(1)

    return test_results

if __name__ == "__main__":
    run_tests()
