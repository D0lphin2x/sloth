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

    return render_template('results.html',
                         selected_sectors=selected_sectors,
                         sharpe_ratio=sharpe_ratio,
                         annual_returns=annual_returns)
if __name__ == '__main__':
    app.run(debug=True, port = 5001)
