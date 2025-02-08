from flask import Flask, request, render_template
import requests
from calculate_sharpe_ratio import calculate_sharpe_ratios

app = Flask(__name__)

# Replace with the actual API endpoint and your API key
API_ENDPOINT = "https://api.example.com/index-funds"
API_KEY = "your_api_key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    sharpe_ratio_min = float(request.form.get('sharpe_ratio_min'))
    sharpe_ratio_max = float(request.form.get('sharpe_ratio_max'))

    # Fetch data from the API
    response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
    data = response.json()

    # Calculate Sharpe ratios
    data_with_sharpe_ratios = calculate_sharpe_ratios(data)

    # Filter data based on Sharpe ratio criteria
    filtered_data = [
        fund for fund in data_with_sharpe_ratios
        if sharpe_ratio_min <= fund['sharpe_ratio'] <= sharpe_ratio_max
    ]

    return render_template('results.html', funds=filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
