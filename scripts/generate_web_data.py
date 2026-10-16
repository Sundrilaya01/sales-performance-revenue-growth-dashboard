"""
Generate Web Dashboard Data Payload
Extracts processed datasets into web/data.js for instant client-side execution.
"""

import os
import json
import pandas as pd

def generate_web_data():
    project_root = r"D:\Power BI\Sales Performance & Revenue Growth Dashboard"
    processed_dir = os.path.join(project_root, "data", "processed")
    web_dir = os.path.join(project_root, "web")
    os.makedirs(web_dir, exist_ok=True)

    fact = pd.read_csv(os.path.join(processed_dir, "fact_sales.csv"))
    prod = pd.read_csv(os.path.join(processed_dir, "dim_products.csv"))
    cust = pd.read_csv(os.path.join(processed_dir, "dim_customers.csv"))
    dim_date = pd.read_csv(os.path.join(processed_dir, "dim_date.csv"))
    reg = pd.read_csv(os.path.join(processed_dir, "dim_regions.csv"))
    fcst = pd.read_csv(os.path.join(processed_dir, "revenue_forecast_h1_2026.csv"))

    # Join fact with dimensions
    df = fact.merge(dim_date, on='date_key', how='left')
    df = df.merge(prod, on='product_id', how='left')
    df = df.merge(cust, on='customer_id', how='left')
    df = df.merge(reg, on='region_id', how='left')

    # Select necessary fields for web app
    selected_fields = [
        'order_id', 'date_key', 'date_x', 'year', 'quarter', 'month_number', 'month_name', 'month_year',
        'product_id', 'product_name', 'category', 'unit_price_x', 'unit_cost',
        'units_sold', 'sales_amount', 'cost', 'profit', 'profit_margin_pct', 'target_sales',
        'customer_id', 'customer_segment', 'sales_channel', 'state_city',
        'region_id', 'region_name'
    ]

    cleaned_df = df[selected_fields].rename(columns={
        'date_x': 'date',
        'unit_price_x': 'unit_price'
    })

    records = cleaned_df.to_dict(orient='records')
    fcst_records = fcst.to_dict(orient='records')

    js_content = f"""// Auto-generated data payload for Sales Performance Dashboard
const SALES_DATA = {json.dumps(records, indent=2)};

const FORECAST_DATA = {json.dumps(fcst_records, indent=2)};
"""

    out_file = os.path.join(web_dir, "data.js")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"Generated {out_file} with {len(records)} sales rows and {len(fcst_records)} forecast rows.")

if __name__ == "__main__":
    generate_web_data()
