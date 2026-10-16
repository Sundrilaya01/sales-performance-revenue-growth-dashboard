# Machine Learning and Time-Series Model Evaluation

This document outlines the statistical time-series forecasting methodology, mathematical equations, backtesting validation framework, and empirical performance metrics implemented in `scripts/forecast_engine.py`.

---

## 1. Objective and Problem Formulation
* **Primary Objective:** Generate statistically defensible 6-month forward monthly revenue projections ($y_{t+h}$ for $h \in [1, 6]$) to support commercial quota allocation and inventory buffering.
* **Granularity:** Monthly aggregated commercial revenue across all product categories and territories.
* **Historical Horizon:** 24 continuous calendar months (January 2024 to December 2025).
* **Forecast Horizon:** January 2026 to June 2026 (H1 2026).

---

## 2. Algorithm Selection and Mathematical Framework

### Candidate Models Evaluated:
1. **Holt-Winters Exponential Smoothing with Damped Trend (`ETS_HoltWinters_Damped`):**
   * Selected as the primary forecasting algorithm.
   * Commercial revenue typically displays growth momentum that faces natural friction over time. Standard linear trend models tend to overproject revenue into infinity. The damping factor ($\phi < 1$) dampens the trend into a realistic asymptotic trajectory.

### Mathematical Formulation:
The Holt-Winters additive damped trend formulation is expressed as:

* **Level Update ($l_t$):**
  $$l_t = \alpha y_t + (1 - \alpha)(l_{t-1} + \phi b_{t-1})$$

* **Damped Trend Update ($b_t$):**
  $$b_t = \beta (l_t - l_{t-1}) + (1 - \beta) \phi b_{t-1}$$

* **Forecast for $h$ Steps Ahead ($\hat{y}_{t+h|t}$):**
  $$\hat{y}_{t+h|t} = l_t + \left( \sum_{i=1}^{h} \phi^i \right) b_t$$

Where:
* $\alpha \in [0, 1]$ is the level smoothing parameter.
* $\beta \in [0, 1]$ is the trend smoothing parameter.
* $\phi \in (0, 1)$ is the damping parameter.
* $\sum_{i=1}^{h} \phi^i = \phi \frac{1 - \phi^h}{1 - \phi}$ converges as $h \to \infty$.

2. **Linear Trend OLS Regression (Secondary Baseline):**
   * Modeled as $\hat{y}_t = \beta_0 + \beta_1 t$.
   * Serves as an unconstrained parametric trend benchmark.

3. **Naive Prior-Year Benchmark (Conventional Baseline):**
   * Modeled as $\hat{y}_t = y_{t-12}$.
   * Represents conventional corporate budgeting where each month's forecast equals the corresponding month of the prior year.

---

## 3. Backtesting Protocol and Train-Test Split

To prevent look-ahead bias and measure true out-of-sample generalization:
* **Training Window:** Months 1 to 18 (January 2024 to June 2025).
* **Holdout Testing Window:** Months 19 to 24 (July 2025 to December 2025).
* Temporal sequence was strictly preserved (no random shuffling).

---

## 4. Empirical Evaluation Scores

The models were evaluated against the unseen 6-month holdout test set using the following performance metrics:

### Performance Comparison Table:

| Model | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | Mean Absolute Percentage Error (MAPE) | Performance vs. Baseline |
| :--- | :--- | :--- | :--- | :--- |
| **Holt-Winters Damped ETS** | **$31,530.53** | **$41,456.15** | **30.16%** | **Outperformed Baseline by 10.97 percentage points** |
| Linear Trend (OLS) | $30,948.27 | $40,844.82 | 29.60% | Outperformed Baseline by 11.53 percentage points |
| Naive Prior-Year Benchmark | $38,675.00 | $43,488.47 | 41.13% | Conventional Corporate Baseline |

### Metric Definitions:
* **Mean Absolute Error (MAE):**
  $$\text{MAE} = \frac{1}{n} \sum_{t=1}^{n} |y_t - \hat{y}_t|$$
* **Root Mean Squared Error (RMSE):**
  $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{t=1}^{n} (y_t - \hat{y}_t)^2}$$
* **Mean Absolute Percentage Error (MAPE):**
  $$\text{MAPE} = \frac{100\%}{n} \sum_{t=1}^{n} \left| \frac{y_t - \hat{y}_t}{y_t} \right|$$

---

## 5. Production Forecast for H1 2026

The final model was refit on the full 24-month historical series to generate the official H1 2026 projection:

| Month | Projected Revenue ($) | Lower 95% Bound ($) | Upper 95% Bound ($) |
| :--- | :--- | :--- | :--- |
| January 2026 | $77,935.21 | $30,001.02 | $125,869.40 |
| February 2026 | $78,542.18 | $30,598.15 | $126,486.21 |
| March 2026 | $79,144.33 | $31,190.20 | $127,098.46 |
| April 2026 | $79,741.70 | $31,777.22 | $127,706.18 |
| May 2026 | $80,334.32 | $32,359.28 | $128,309.36 |
| June 2026 | $80,922.22 | $32,936.42 | $128,908.02 |
| **Total H1 2026** | **$476,131.06** | **$188,465.06** | **$763,797.05** |

*Output stored in:* `data/processed/revenue_forecast_h1_2026.csv`.

---

## 6. Model Limitations and Ongoing Monitoring
1. **Short Historical Series (24 Months):** While adequate for Holt-Winters ETS, 24 months represents 2 full annual cycles. More granular daily or weekly series would enable capturing sub-monthly promotional dynamics.
2. **Exogenous Variables:** The current model is univariate (driven by historical revenue velocity). Future iterations could incorporate marketing spend, seasonal promotions, or macroeconomic indicators as exogenous regressors.
3. **Retraining Trigger:** Scheduled quarterly, or automatically if rolling out-of-sample MAPE on subsequent monthly actuals exceeds 35%.
