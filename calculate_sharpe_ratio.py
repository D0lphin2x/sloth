import numpy as np

def calculate_sharpe_ratio(average_prices, risk_free_rate=0.04495):
    daily_returns = average_prices['Close'].pct_change().dropna()
    mean_return = daily_returns.mean()
    std_dev = daily_returns.std()

    # Calculate the Sharpe ratio
    sharpe_ratio = (mean_return - risk_free_rate/252) / std_dev
    return sharpe_ratio
