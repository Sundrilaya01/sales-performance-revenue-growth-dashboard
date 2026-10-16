"""
Predictive Revenue Forecasting Engine
Project: Sales Performance & Revenue Growth Dashboard
Role: Senior Business Intelligence Analyst & Forecasting Engineer
Phase: Phase 6 - Forecasting and Growth Analysis

Performs:
1. Monthly aggregation & time-series continuity validation (24 months).
2. Out-of-sample holdout backtesting (18 train / 6 test).
3. Holt-Winters Exponential Smoothing model estimation.
4. 6-Month forward forecasting (H1 2026) with 95% confidence intervals.
5. Export of actual and forecast tables to data/processed/.
"""

import os
import sys
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error, mean_squared_error

def run_forecast_pipeline():
    project_root = r"D:\Power BI\Sales Performance & Revenue Growth Dashboard"
    processed_dir = os.path.join(project_root, "data", "processed")

    print("=================================================================")
    print("STEP 1: AGGREGATING MONTHLY REVENUE SERIES")
    print("=================================================================")

    fact = pd.read_csv(os.path.join(processed_dir, "fact_sales.csv"))
    dim_date = pd.read_csv(os.path.join(processed_dir, "dim_date.csv"))
    df = fact.merge(dim_date, on='date_key', how='left')

    monthly = df.groupby(['year', 'month_number', 'month_name']).agg(
        total_revenue=('sales_amount', 'sum'),
        total_units=('units_sold', 'sum'),
        total_orders=('order_id', 'nunique'),
        total_cost=('cost', 'sum'),
        total_profit=('profit', 'sum')
    ).reset_index()

    monthly['year_month'] = monthly['year'].astype(str) + '-' + monthly['month_number'].apply(lambda x: f"{x:02d}")
    monthly['date'] = pd.to_datetime(monthly['year_month'] + '-01')
    monthly = monthly.sort_values(by='date').reset_index(drop=True)

    print(f"Aggregated {len(monthly)} continuous months ({monthly['date'].min().strftime('%Y-%m')} to {monthly['date'].max().strftime('%Y-%m')}).")
    assert len(monthly) == 24, "Expected exactly 24 contiguous months!"

    # Export monthly actuals
    actuals_path = os.path.join(processed_dir, "monthly_revenue_actuals.csv")
    monthly.to_csv(actuals_path, index=False)
    print(f"Exported monthly actuals -> {actuals_path}")

    print("\n=================================================================")
    print("STEP 2: OUT-OF-SAMPLE HOLDOUT BACKTESTING (18 TRAIN / 6 TEST)")
    print("=================================================================")

    y = monthly['total_revenue'].values
    train = y[:18] # 2024-01 to 2025-06
    test = y[18:]  # 2025-07 to 2025-12

    # Model A: Baseline (Prior Year corresponding period: 2024-07 to 2024-12)
    py_baseline = y[6:12]
    mae_base = mean_absolute_error(test, py_baseline)
    rmse_base = np.sqrt(mean_squared_error(test, py_baseline))
    mape_base = np.mean(np.abs((test - py_baseline) / test)) * 100

    # Model B: Linear Trend OLS
    t_train = sm.add_constant(np.arange(len(train)))
    ols_fit = OLS(train, t_train).fit()
    t_test = sm.add_constant(np.arange(len(train), len(y)))
    ols_pred = ols_fit.predict(t_test)
    mae_ols = mean_absolute_error(test, ols_pred)
    rmse_ols = np.sqrt(mean_squared_error(test, ols_pred))
    mape_ols = np.mean(np.abs((test - ols_pred) / test)) * 100

    # Model C: Holt-Winters Exponential Smoothing (Damped Trend)
    hw_fit = ExponentialSmoothing(train, trend='add', seasonal=None, damped_trend=True).fit()
    hw_pred = hw_fit.forecast(6)
    mae_hw = mean_absolute_error(test, hw_pred)
    rmse_hw = np.sqrt(mean_squared_error(test, hw_pred))
    mape_hw = np.mean(np.abs((test - hw_pred) / test)) * 100

    print(f"Baseline (Prior Year)   | MAE: ${mae_base:,.2f} | RMSE: ${rmse_base:,.2f} | MAPE: {mape_base:.2f}%")
    print(f"Linear Trend OLS        | MAE: ${mae_ols:,.2f} | RMSE: ${rmse_ols:,.2f} | MAPE: {mape_ols:.2f}%")
    print(f"Holt-Winters Damped ETS | MAE: ${mae_hw:,.2f} | RMSE: ${rmse_hw:,.2f} | MAPE: {mape_hw:.2f}%")

    print("\n=================================================================")
    print("STEP 3: FULL ESTIMATION & 6-MONTH FORWARD FORECASTING (H1 2026)")
    print("=================================================================")

    # Full fit on 24 months
    hw_full = ExponentialSmoothing(y, trend='add', seasonal=None, damped_trend=True).fit()
    forecast_6m = hw_full.forecast(6)

    residuals = y - hw_full.fittedvalues
    residual_std = np.std(residuals)

    future_dates = pd.date_range(start='2026-01-01', periods=6, freq='MS')
    forecast_records = []

    # Historical actuals formatted
    for idx, r in monthly.iterrows():
        forecast_records.append({
            'date': r['date'].strftime('%Y-%m-%d'),
            'year': int(r['year']),
            'month': int(r['month_number']),
            'month_name': r['month_name'],
            'year_month': r['year_month'],
            'data_type': 'Actual',
            'actual_revenue': round(float(r['total_revenue']), 2),
            'predicted_revenue': round(float(r['total_revenue']), 2),
            'lower_bound_95': round(float(r['total_revenue']), 2),
            'upper_bound_95': round(float(r['total_revenue']), 2),
            'model_id': 'Observed_Historical'
        })

    # Future 6 months forecast
    for step, (f_date, f_val) in enumerate(zip(future_dates, forecast_6m), start=1):
        # Prediction interval grows with forecast horizon
        margin = 1.96 * residual_std * np.sqrt(1 + (step - 1) * 0.15)
        lower_bound = max(0.0, float(f_val - margin))
        upper_bound = float(f_val + margin)

        forecast_records.append({
            'date': f_date.strftime('%Y-%m-%d'),
            'year': int(f_date.year),
            'month': int(f_date.month),
            'month_name': f_date.strftime('%B'),
            'year_month': f_date.strftime('%Y-%m'),
            'data_type': 'Forecast',
            'actual_revenue': np.nan,
            'predicted_revenue': round(float(f_val), 2),
            'lower_bound_95': round(lower_bound, 2),
            'upper_bound_95': round(upper_bound, 2),
            'model_id': 'ETS_HoltWinters_Damped'
        })
        print(f"H1 2026 -> {f_date.strftime('%Y-%m')}: Predicted=${f_val:,.2f} [95% CI: ${lower_bound:,.2f} - ${upper_bound:,.2f}]")

    forecast_df = pd.DataFrame(forecast_records)
    forecast_path = os.path.join(processed_dir, "revenue_forecast_h1_2026.csv")
    forecast_df.to_csv(forecast_path, index=False)
    print(f"\nExported complete forecast series ({len(forecast_df)} rows) -> {forecast_path}")

    print("\nFORECASTING PIPELINE COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_forecast_pipeline()
