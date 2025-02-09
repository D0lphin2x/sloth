from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from calculate_sharpe_ratio import calculate_performance

app = Flask(__name__)

# Load sector mapping from CSV file
sector_df = pd.read_csv('snp500.csv')
sector_mapping = dict(zip(sector_df['Symbol'], sector_df['GICS Sector']))

# Define the sectors to be displayed
display_sectors = [
    "Technology", "Health Care", "Financials", "Real Estate", "Energy",
    "Materials", "Consumer Discretionary", "Industrials", "Utilities",
    "Consumer Staples", "Communications"
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    sectors = display_sectors
    return render_template('index.html', sectors=sectors)

@app.route('/search', methods=['POST'])
def search():
    selected_sectors = request.form.get('sectors').split(',')
    
    df = pd.read_csv('updated_stocks_data.csv')
    df['sector'] = df['Ticker'].map(sector_mapping)
    filtered_data = df[df['sector'].isin(selected_sectors)]

    # Add market cap
    sector_df = pd.read_csv('New_SNP500.csv')
    market_cap_mapping = dict(zip(sector_df['Symbol'], sector_df['Market Cap']))
    filtered_data['Market Cap'] = filtered_data['Ticker'].map(market_cap_mapping)
    filtered_data = filtered_data.dropna(subset=['Market Cap'])

    # Calculate portfolio-level Sharpe ratio and annual returns
    sharpe_ratio, annual_returns = calculate_performance(filtered_data)

    # Calculate Sharpe ratios for individual companies
    company_sharpe_ratios = filtered_data.groupby('Ticker').apply(lambda x: calculate_performance(x)[0])

    # Ensure 'Date' column is in datetime format and strip time component
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date']).dt.date

    # Calculate daily average prices
    filtered_data = filtered_data.sort_values(['Date'])
    daily_prices = filtered_data.groupby('Date')['Close'].mean()

    # Convert dates to strings for rendering
    daily_prices.index = daily_prices.index.astype(str)

    # Debugging step: Print the daily prices
    print(daily_prices.head())

    # Ensure all variables are defined
    if selected_sectors is None:
        selected_sectors = []
    if sharpe_ratio is None:
        sharpe_ratio = 0.0
    if annual_returns is None:
        annual_returns = {}
    if daily_prices is None:
        daily_prices = {}

    return render_template('results.html',
                         selected_sectors=selected_sectors,
                         sharpe_ratio=sharpe_ratio,
                         annual_returns=annual_returns,
                         daily_prices=daily_prices.to_dict(),
                         company_sharpe_ratios=company_sharpe_ratios.to_dict())

if __name__ == '__main__':
    app.run(debug=True, port=5001)
