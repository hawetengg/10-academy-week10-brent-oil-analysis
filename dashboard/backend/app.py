from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load data
prices_df = pd.read_csv('../../data/brentOilPrices.csv')
events_df = pd.read_csv('../../data/events.csv')
prices_df['Date'] = pd.to_datetime(prices_df['Date'], format='%d-%b-%y')
events_df['Date'] = pd.to_datetime(events_df['Date'])

@app.route('/api/prices', methods=['GET'])
def get_prices():
    return jsonify({
        'dates': prices_df['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'prices': prices_df['Price'].tolist()
    })

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(events_df.to_dict(orient='records'))

@app.route('/api/change_points', methods=['GET'])
def get_change_points():
    return jsonify([
        {'date': '1990-08-01', 'description': 'Change Point (Gulf War)'}
    ])

if __name__ == '__main__':
    app.run(debug=True, port=5000)