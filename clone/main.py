from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Replace with the actual API endpoint and your API key
API_ENDPOINT = "https://api.example.com/index-funds"
API_KEY = "your_api_key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    std_dev_min = request.form.get('std_dev_min')
    std_dev_max = request.form.get('std_dev_max')

    # Fetch data from the API
    response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})
    data = response.json()

    # Filter data based on standard deviation criteria
    filtered_data = [
        fund for fund in data
        if std_dev_min <= fund['standard_deviation'] <= std_dev_max
    ]

    return render_template('results.html', funds=filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
