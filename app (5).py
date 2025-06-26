from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import pickle
import json
from datetime import datetime

# ------------------ Load Trained Items -------------------
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# Location data
with open("location.json", "r") as f:
    location_data = json.load(f)

# Dataset for trends
location_df = pd.read_csv("Bengaluru_House_Data.csv")

# ------------------ Flask App Init -----------------------
app = Flask(__name__, static_folder='static')

# ------------------ Helper Function ----------------------
def get_price_trend(location, predicted_price):
    trend_df = location_df[location_df['location'] == location].copy()
    
    if trend_df.empty:
        return {
            2020: 50,
            2021: 52,
            2022: 55,
            2023: 58,
            2024: 60,
            2025: round(predicted_price, 2)
        }

    # Simulate year if not available
    if 'year' not in trend_df.columns:
        trend_df['year'] = np.random.choice(range(2020, 2024), size=len(trend_df))

    yearly_avg = trend_df.groupby('year')['price'].mean().sort_index().to_dict()
    current_year = datetime.now().year
    yearly_avg[current_year] = round(predicted_price, 2)
    return yearly_avg

# ------------------ Home Page ----------------------------
@app.route('/')
def index():
    area_types = ['Super built-up  Area', 'Built-up  Area', 'Plot  Area', 'Carpet  Area']
    locations = sorted([loc['name'] for loc in location_data])
    bhks = [1, 2, 3, 4, 5]
    return render_template('index (4).html', area_types=area_types, locations=locations, bhks=bhks)

# ------------------ Prediction Page ----------------------
@app.route('/predict', methods=['POST'])
def predict():
    area_type = request.form['area_type']
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    balcony = int(request.form['balcony'])
    total_sqft = float(request.form['total_sqft'])

    selected_features = request.form.getlist('features')
    nearby_places = request.form.get('nearby_places', '')
    auto_nearby = 'auto_nearby' in request.form

    input_data = pd.DataFrame([{
        'area_type': area_type,
        'location': location,
        'size': bhk,
        'bath': bath,
        'balcony': balcony,
        'total_sqft': total_sqft
    }])
    input_data = pd.get_dummies(input_data)
    input_data = input_data.reindex(columns=columns, fill_value=0)
    if 'total_sqft' in input_data.columns:
        input_data['total_sqft'] = np.log1p(input_data['total_sqft'])

    log_pred = model.predict(input_data)[0]
    predicted_price = np.expm1(log_pred)

    loc_info = next((item for item in location_data if item["name"] == location), None)

    # 🔄 Updated Trend Data (dict of year -> price)
    trend_data = get_price_trend(location, predicted_price)

    return render_template('result1 (3).html',
                           price=round(predicted_price, 2),
                           location=location,
                           lat=loc_info['lat'] if loc_info else None,
                           lng=loc_info['lng'] if loc_info else None,
                           bhk=bhk,
                           bath=bath,
                           sqft=int(total_sqft),
                           features=selected_features,
                           nearby_places=nearby_places or "Not specified",
                           show_auto_nearby=auto_nearby,
                           trend_data=trend_data)

# ------------------ Compare Form Page --------------------
@app.route('/compare_page')
def compare_page():
    locations = sorted([loc['name'] for loc in location_data])
    bhks = [1, 2, 3, 4, 5]
    return render_template('compare_from (2).html', locations=locations, bhks=bhks)

# ------------------ Compare Result Page ------------------
@app.route('/compare', methods=['POST'])
def compare():
    try:
        data = request.form

        def prepare_input(area_type, location, bhk, bath, balcony, sqft):
            df = pd.DataFrame([{
                'area_type': area_type,
                'location': location,
                'size': bhk,
                'bath': bath,
                'balcony': balcony,
                'total_sqft': sqft
            }])
            df = pd.get_dummies(df)
            df = df.reindex(columns=columns, fill_value=0)
            df['total_sqft'] = np.log1p(df['total_sqft'])
            return df

        # Property 1
        p1 = {
            'area_type': data.get('area_type1'),
            'location': data.get('location1'),
            'bhk': int(data.get('bhk1')),
            'bath': int(data.get('bath1')),
            'balcony': int(data.get('balcony1')),
            'sqft': float(data.get('sqft1')),
            'features': request.form.getlist('features1')
        }
        input1 = prepare_input(p1['area_type'], p1['location'], p1['bhk'], p1['bath'], p1['balcony'], p1['sqft'])
        p1['price'] = round(np.expm1(model.predict(input1)[0]), 2)

        # Property 2
        p2 = {
            'area_type': data.get('area_type2'),
            'location': data.get('location2'),
            'bhk': int(data.get('bhk2')),
            'bath': int(data.get('bath2')),
            'balcony': int(data.get('balcony2')),
            'sqft': float(data.get('sqft2')),
            'features': request.form.getlist('features2')
        }
        input2 = prepare_input(p2['area_type'], p2['location'], p2['bhk'], p2['bath'], p2['balcony'], p2['sqft'])
        p2['price'] = round(np.expm1(model.predict(input2)[0]), 2)

        return render_template('compare_result (2).html', p1=p1, p2=p2)

    except Exception as e:
        return f"Error: {e}", 500

# ------------------ AI Chatbot API -----------------------
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.get_json().get('message', '').lower()

    if "under 60" in user_input or "below 60" in user_input:
        reply = "You can explore areas like Whitefield, Electronic City, and Sarjapur Road under ₹60L."
    elif "average rent" in user_input and "marathahalli" in user_input:
        reply = "The average rent in Marathahalli is around ₹18,000/month for a 2BHK."
    elif "best location" in user_input or "good area" in user_input:
        reply = "Top recommended areas are HSR Layout, Indiranagar, Whitefield, and Electronic City."
    elif "investment" in user_input:
        reply = "Electronic City and Sarjapur are great for long-term investment due to IT growth."
    elif "hello" in user_input or "hi" in user_input:
        reply = "Hi there! 👋 I’m your RealEstateBot. Ask me anything about flats, areas, or prices!"
    elif "rent" in user_input:
        reply = "Most 2BHKs in major localities range from ₹15,000 to ₹30,000 depending on amenities."
    elif "3bhk" in user_input or "4bhk" in user_input:
        reply = "3BHK and 4BHK flats are more common in areas like Bellandur, Whitefield, and JP Nagar."
    else:
        reply = "I'm still learning 🤖. Try asking about budget homes, rent in areas, or good locations."

    return jsonify({'reply': reply})

# ------------------ Run App ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
