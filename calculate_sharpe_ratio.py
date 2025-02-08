import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def calculate_performance(df, risk_free_rate=4.495):
    # Convert to datetime and sort
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['Ticker', 'Date'])
    
    # Get latest date in dataset
    latest_date = df['Date'].max()
    
    # Calculate time windows
    periods = {
        '1_year': latest_date - timedelta(days=365),
        '3_year': latest_date - timedelta(days=3*365),
        '5_year': latest_date - timedelta(days=5*365),
        '10_year': latest_date - timedelta(days=10*365)
    }

    # Get market caps and weights
    market_caps = df.groupby('Ticker')['Market Cap'].first()
    total_market_cap = market_caps.sum()
    weights = market_caps / total_market_cap

    # Calculate returns for each period
    annual_returns = {}
    
    for period_name, start_date in periods.items():
        period_returns = []
        
        for ticker, group in df.groupby('Ticker'):
            # Get start and end prices for period
            try:
                start_price = group[group['Date'] <= start_date].iloc[-1]['Close']
                end_price = group.iloc[-1]['Close']
                returns = (end_price - start_price) / start_price
                period_returns.append(returns * weights[ticker])
            except:
                continue  # Skip if insufficient data
        
        # Sum weighted returns and annualize
        total_return = sum(period_returns)
        years = int(period_name.split('_')[0])
        annualized_return = ((1 + total_return) ** (1/years) - 1) * 100
        
        annual_returns[period_name] = annualized_return

    # Calculate Sharpe Ratio (existing code)
    df['Returns'] = df.groupby('Ticker')['Close'].pct_change()
    df = df.dropna(subset=['Returns'])
    returns_pivot = df.pivot(index='Date', columns='Ticker', values='Returns')
    portfolio_returns = returns_pivot.dot(weights)
    
    R_p = portfolio_returns.mean()
    sigma_p = portfolio_returns.std()
    R_f_daily = risk_free_rate / 100 / 252
    sharpe_ratio = ((R_p - R_f_daily) / sigma_p) * np.sqrt(252)

    return sharpe_ratio, annual_returns