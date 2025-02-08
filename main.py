from flask import Flask, request, render_template
import pandas as pd
from calculate_sharpe_ratio import calculate_performance

app = Flask(__name__)

# Load sector mapping from CSV file
sector_df = pd.read_csv('snp500.csv')
sector_mapping = dict(zip(sector_df['Symbol'], sector_df['GICS Sector']))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    selected_sectors = request.form.getlist('sectors')
    
    df = pd.read_csv('updated_stocks_data.csv')
    df['sector'] = df['Ticker'].map(sector_mapping)
    filtered_data = df[df['sector'].isin(selected_sectors)]

    # Add market cap
    sector_df = pd.read_csv('New_SNP500.csv')
    market_cap_mapping = dict(zip(sector_df['Symbol'], sector_df['Market Cap']))
    filtered_data['Market Cap'] = filtered_data['Ticker'].map(market_cap_mapping)
    filtered_data = filtered_data.dropna(subset=['Market Cap'])

    # Get both metrics
    sharpe_ratio, annual_returns = calculate_performance(filtered_data)

    # Ensure 'Date' column is in datetime format and strip time component
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date']).dt.date

    # Debugging step: Print the first few rows of the filtered data
    print(filtered_data.head())

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
                         daily_prices=daily_prices.to_dict())

if __name__ == '__main__':
    app.run(debug=True, port=5001)
