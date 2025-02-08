from flask import Flask, request, render_template
import pandas as pd
from calculate_sharpe_ratio import calculate_sharpe_ratio

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

    # Read data from the CSV file
    df = pd.read_csv('updated_stocks_data.csv')

    # Map tickers to sectors
    df['sector'] = df['Ticker'].map(sector_mapping)

    # Filter data based on selected sectors
    filtered_data = df[df['sector'].isin(selected_sectors)]

    # Load market cap data from New_SNP500.csv
    sector_df = pd.read_csv('New_SNP500.csv')
    market_cap_mapping = dict(zip(sector_df['Symbol'], sector_df['Market Cap']))
    
    # Add market cap to filtered_data
    filtered_data['Market Cap'] = filtered_data['Ticker'].map(market_cap_mapping)

    # Drop rows where Market Cap is NaN (if any ticker isn't in New_SNP500.csv)
    filtered_data = filtered_data.dropna(subset=['Market Cap'])

    # Calculate the Sharpe ratio with market cap weighting
    sharpe_ratio = calculate_sharpe_ratio(filtered_data)

    return render_template('results.html', selected_sectors=selected_sectors, sharpe_ratio=sharpe_ratio)
if __name__ == '__main__':
    app.run(debug=True)
