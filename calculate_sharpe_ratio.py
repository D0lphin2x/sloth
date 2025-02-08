import numpy as np
import pandas as pd

def calculate_sharpe_ratio(df, risk_free_rate=4.495):
    # Ensure we are using previous close for returns calculation
    df["Returns"] = df["Close"].pct_change()

    # Drop first row (NaN due to pct_change)
    df = df.dropna()

    # Compute portfolio return (mean daily return across all index funds)
    R_p = df["Returns"].mean()

    # Compute portfolio standard deviation (daily)
    sigma_p = df["Returns"].std()

    # Convert risk-free rate (annual to daily)
    R_f_daily = risk_free_rate / 100 / 252  # Convert 4.495% annual to daily

    # Compute Sharpe Ratio (Annualized)
    sharpe_ratio = ((R_p - R_f_daily) / sigma_p) * np.sqrt(252)

    return sharpe_ratio
