### Objective

Develop an AI-powered forecasting module capable of predicting future financial performance for NIFTY 100 companies using historical financial statements.

### Modules Developed
src/
└── forecasting/
    ├── __init__.py
    ├── preprocess.py
    ├── forecast_engine.py
    ├── model_selector.py
    ├── evaluation.py
    ├── export.py
    └── forecast_runner.py

### Features Implemented
Historical financial data preprocessing
Multi-metric forecasting
Linear Regression forecasting
Exponential Smoothing forecasting
Automatic model comparison
MAE and RMSE evaluation
Forecast export to CSV
Forecast pipeline integration into main.py
Forecasted Metrics
Sales
Operating Profit
Net Profit
Earnings Per Share (EPS)
Net Cash Flow

### Outputs Generated
output/
└── forecasting/
    ├── sales_forecast.csv
    ├── operating_profit_forecast.csv
    ├── net_profit_forecast.csv
    ├── eps_forecast.csv
    └── net_cash_flow_forecast.csv

### Technologies Used
Python
Pandas
NumPy
Scikit-learn
Statsmodels