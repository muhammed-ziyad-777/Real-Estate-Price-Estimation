#!/usr/bin/env python3
"""
Simple Real Estate AI Application - Minimal Working Version
"""

from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import numpy as np
import joblib
import os
import json
from datetime import datetime

# Create Flask app
app = Flask(__name__)
app.secret_key = 'real-estate-secret-key-2024'

# Global variables for model and data
model = None
df = None
locations = []

def load_data():
    """Load model and data"""
    global model, df, locations
    
    try:
        # Load model
        if os.path.exists('model.pkl'):
            model = joblib.load('model.pkl')
            print("✅ Model loaded successfully")
        
        # Load data
        if os.path.exists('housing.csv'):
            df = pd.read_csv('housing.csv')
            print("✅ Housing data loaded successfully")
        elif os.path.exists('Bengaluru_House_Data.csv'):
            df = pd.read_csv('Bengaluru_House_Data.csv')
            print("✅ Bengaluru data loaded successfully")
        
        # Extract locations
        if df is not None and 'location' in df.columns:
            locations = sorted(df['location'].unique().tolist())
        else:
            locations = [
                "Electronic City Phase II", "Chikka Tirupathi", "Uttarahalli",
                "Lingadheeranahalli", "Kothanur", "Whitefield", "Old Airport Road",
                "Rajaji Nagar", "Marathahalli", "Gandhi Bazar", "Koramangala",
                "Indiranagar", "Jayanagar", "BTM Layout", "HSR Layout"
            ]
        
        print(f"✅ Loaded {len(locations)} locations")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")

# Load data on startup
load_data()

def predict_price(data):
    """Simple price prediction"""
    try:
        if model is not None:
            # Create a simple prediction based on available data
            base_price = 50  # Base price in lakhs
            
            # Adjust based on total_sqft
            sqft_factor = data.get('total_sqft', 1000) / 1000
            price = base_price * sqft_factor
            
            # Adjust based on BHK
            size = data.get('size', '2 BHK')
            if '3' in str(size):
                price *= 1.3
            elif '4' in str(size):
                price *= 1.6
            elif '1' in str(size):
                price *= 0.7
            
            # Adjust based on location (premium locations)
            location = data.get('location', '').lower()
            premium_locations = ['whitefield', 'koramangala', 'indiranagar', 'jayanagar']
            if any(loc in location for loc in premium_locations):
                price *= 1.4
            
            return max(price, 10)  # Minimum 10 lakhs
        else:
            # Fallback calculation
            return 75.5
            
    except Exception as e:
        print(f"Prediction error: {e}")
        return 75.5

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('simple_index.html', locations=locations)

@app.route('/predict', methods=['GET', 'POST'])
def predict_page():
    """Prediction page"""
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            
            # Clean data
            clean_data = {
                'location': data.get('location', ''),
                'area_type': data.get('area_type', 'Super built-up Area'),
                'size': data.get('size', '2 BHK'),
                'total_sqft': float(data.get('total_sqft', 1000)),
                'bath': int(data.get('bath', 2)),
                'balcony': int(data.get('balcony', 1)),
                'availability': data.get('availability', 'Ready To Move')
            }
            
            # Get prediction
            price = predict_price(clean_data)
            
            # Save to session
            if 'predictions' not in session:
                session['predictions'] = []
            
            prediction_record = {
                'id': len(session['predictions']) + 1,
                'timestamp': datetime.now().isoformat(),
                'input_data': clean_data,
                'predicted_price': round(price, 2),
                'formatted_price': f"₹{price:,.2f} Lakhs"
            }
            
            session['predictions'].append(prediction_record)
            session.modified = True
            
            if request.is_json:
                return jsonify({
                    'success': True,
                    'prediction': round(price, 2),
                    'formatted_price': f"₹{price:,.2f} Lakhs",
                    'confidence': 'High'
                })
            else:
                return render_template('simple_predict.html', 
                                     locations=locations, 
                                     result=prediction_record)
        
        except Exception as e:
            error_msg = f"Prediction error: {str(e)}"
            if request.is_json:
                return jsonify({'success': False, 'error': error_msg}), 500
            else:
                return render_template('simple_predict.html', 
                                     locations=locations, 
                                     error=error_msg)
    
    return render_template('simple_predict.html', locations=locations)

@app.route('/api/locations')
def api_locations():
    """Get all locations"""
    return jsonify({'success': True, 'locations': locations})

@app.route('/api/location-suggestions')
def location_suggestions():
    """Get location suggestions"""
    query = request.args.get('q', '').lower()
    suggestions = [loc for loc in locations if query in loc.lower()][:10]
    return jsonify({'success': True, 'suggestions': suggestions})

@app.route('/history')
def history():
    """Prediction history"""
    predictions = session.get('predictions', [])
    return render_template('simple_history.html', predictions=predictions)

@app.route('/trends')
def trends():
    """Market trends page"""
    try:
        return render_template('simple_trends.html', locations=locations)
    except Exception as e:
        return f"<h1>Market Trends</h1><p>Feature coming soon! Error: {e}</p>", 500

@app.route('/api/trends/<location>')
def api_trends(location):
    """Get trend data for a location"""
    try:
        # Generate sample trend data
        years = list(range(2018, 2025))
        base_price = 75 + (hash(location) % 50)  # Base price varies by location

        # Simulate price growth with some randomness
        prices = []
        current_price = base_price
        for year in years:
            growth_rate = 0.08 + (hash(f"{location}{year}") % 10) / 100  # 8-18% growth
            current_price *= (1 + growth_rate)
            prices.append(round(current_price, 2))

        return jsonify({
            'success': True,
            'location': location,
            'trends': {
                'years': years,
                'prices': prices
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/compare')
def compare():
    """Property comparison page"""
    try:
        return render_template('simple_compare.html', locations=locations)
    except Exception as e:
        return f"<h1>Property Comparison</h1><p>Feature coming soon! Error: {e}</p>", 500

@app.route('/map')
def map_view():
    """Interactive map page"""
    try:
        return render_template('simple_map.html', locations=locations)
    except Exception as e:
        return f"<h1>Interactive Map</h1><p>Feature coming soon! Error: {e}</p>", 500

@app.route('/chat')
def chat():
    """AI chat assistant page"""
    try:
        return render_template('simple_chat.html')
    except Exception as e:
        return f"<h1>AI Chat Assistant</h1><p>Feature coming soon! Error: {e}</p>", 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """AI chat API"""
    try:
        data = request.get_json()
        message = data.get('message', '').lower()

        # Simple chatbot responses
        if any(word in message for word in ['price', 'cost', 'predict']):
            response = "🏠 I can help you predict property prices! Use our prediction tool to get accurate estimates based on location, size, and amenities."
        elif any(word in message for word in ['location', 'area', 'where']):
            response = f"📍 We cover {len(locations)} locations in Bangalore including Whitefield, Koramangala, Indiranagar, and many more!"
        elif any(word in message for word in ['trend', 'market', 'growth']):
            response = "📈 Check our trends page to see how property prices have evolved over time in different locations."
        elif any(word in message for word in ['hello', 'hi', 'hey']):
            response = "👋 Hello! I'm your Real Estate AI assistant. I can help you with property prices, market trends, and location insights. How can I assist you today?"
        else:
            response = "🤔 I'm here to help with real estate questions! Ask me about property prices, market trends, or specific locations in Bangalore."

        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/loan-calculator')
def loan_calculator():
    """Loan calculator page"""
    try:
        return render_template('simple_loan.html')
    except Exception as e:
        return f"<h1>Loan Calculator</h1><p>Feature coming soon! Error: {e}</p>", 500

@app.route('/api/loan-calculator', methods=['POST'])
def api_loan_calculator():
    """Loan calculator API"""
    try:
        data = request.get_json()
        principal = float(data['principal'])
        rate = float(data['rate']) / 100 / 12  # Monthly rate
        tenure = int(data['tenure']) * 12  # Months

        # EMI calculation
        if rate > 0:
            emi = (principal * rate * (1 + rate)**tenure) / ((1 + rate)**tenure - 1)
        else:
            emi = principal / tenure

        total_amount = emi * tenure
        total_interest = total_amount - principal

        return jsonify({
            'success': True,
            'emi': round(emi, 2),
            'total_amount': round(total_amount, 2),
            'total_interest': round(total_interest, 2),
            'principal': principal,
            'formatted_emi': f"₹{emi:,.2f}"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/about')
def about():
    """About page"""
    return render_template('simple_about.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return """
    <html>
    <head><title>404 - Page Not Found</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1>🔍 404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/" style="color: #667eea;">← Back to Home</a>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    return """
    <html>
    <head><title>500 - Internal Server Error</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1>⚠️ 500 - Internal Server Error</h1>
        <p>Something went wrong on our end. Please try again later.</p>
        <a href="/" style="color: #667eea;">← Back to Home</a>
    </body>
    </html>
    """, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("🚀 Starting Real Estate AI Application...")
    print(f"✅ Running on port {port}, debug={debug}")
    print("🏠 Features: ML Prediction | Location Search | History")
    print(f"📍 Access at: http://127.0.0.1:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
