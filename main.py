from flask import Flask, request, render_template
import pandas as pd

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

    # Calculate the daily average closing price for each sector
    average_prices = filtered_data.groupby(['Date', 'sector'])['Close'].mean().reset_index()

    return render_template('results.html', average_prices=average_prices, selected_sectors=selected_sectors)

if __name__ == '__main__':
    app.run(debug=True)
