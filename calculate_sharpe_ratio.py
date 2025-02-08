import numpy as np
import pandas as pd

def calculate_sharpe_ratio(df, risk_free_rate=4.495):
    # Ensure 'Date' is a datetime column and sort
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['Ticker', 'Date'])

    # Compute returns per stock
    df['Returns'] = df.groupby('Ticker')['Close'].pct_change()

    # Drop rows with NaN returns (first day for each stock)
    df = df.dropna(subset=['Returns'])

    # Pivot to get daily returns matrix (dates x tickers)
    returns_pivot = df.pivot(index='Date', columns='Ticker', values='Returns')

    # Get market caps for each Ticker
    market_caps = df.groupby('Ticker')['Market Cap'].first()

    # Compute weights (normalized by total market cap)
    total_market_cap = market_caps.sum()
    weights = market_caps / total_market_cap

    # Align weights with the columns in returns_pivot
    weights = weights[returns_pivot.columns].values  # Ensure order matches

    # Calculate daily portfolio returns (weighted average)
    portfolio_returns = returns_pivot.dot(weights)

    # Compute portfolio metrics
    R_p = portfolio_returns.mean()
    sigma_p = portfolio_returns.std()

    # Convert risk-free rate to daily
    R_f_daily = risk_free_rate / 100 / 252

    # Annualize Sharpe Ratio
    sharpe_ratio = ((R_p - R_f_daily) / sigma_p) * np.sqrt(252)

    return sharpe_ratio