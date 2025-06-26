# 🏡 Real Estate Price Prediction

A machine learning-based web app that predicts real estate prices using features like location, area, and bedrooms. Built with Flask and Random Forest, it includes a compare-locations feature to help users analyze property trends. Ideal for buyers, sellers, and analysts.

---

## 🔍 Features

- 🔢 Predict property prices based on inputs like location, square feet, BHK, and bathrooms.
- 📍 Compare prices between two locations using trend analysis.
- 🧠 Machine learning-powered predictions using Random Forest.
- 🌐 Web-based interface with Flask, Bootstrap, and HTML.
- 📦 Trained model, ready to use in production.

---

## 🧠 Machine Learning

- **Algorithms Tested**:  
  - Linear Regression – R²: 0.30  
  - XGBoost Regressor – R²: 0.68  
  - ✅ Random Forest Regressor – **R²: 0.67**

- **Evaluation Metrics**: R² Score, MAE, RMSE  
- **Preprocessing**:
  - Label Encoding
  - Standard Scaling
  - Null value handling
  - Feature Engineering (e.g., price per sq.ft.)

---

## 🛠 Tech Stack

| Area        | Tech Used                       |
|-------------|---------------------------------|
| Language    | Python                          |
| ML Libraries| Pandas, Scikit-learn, XGBoost   |
| Web         | Flask, HTML, CSS, Bootstrap     |
| IDE         | Jupyter Notebook, VS Code       |
| Deployment  | GitHub (local testing)          |

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/your-username/real-estate-price-prediction
cd real-estate-price-prediction

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python app.py
Open your browser and go to: http://localhost:5000

📁 Project Structure
php
Copy
Edit
├── app.py                  # Flask backend
├── model.pkl               # Trained model
├── columns.pkl             # Features used
├── location.json           # Coordinates for map comparison
├── Templates/
│   ├── index.html
│   ├── predict.html
│   ├── result.html
│   └── compare.html
├── static/                 # CSS / JS files
├── model3.ipynb            # Jupyter notebook (EDA + training)
└── README.md               # Project documentation
💡 Sample Inputs & Outputs
🎯 Prediction Input
Location: Whitefield

Total Sqft: 1200

BHK: 2

Bathrooms: 2

Balcony: 1

Status: Ready to Move

➡️ Predicted Price: ₹72.5 Lakhs (Example output)

📊 Compare Two Locations
Compare price trends between:

Whitefield vs Electronic City

Rajaji Nagar vs Marathahalli

➡️ Displays graph with average price/sqft over time or overall comparison.

🧪 Testing Tips
Make sure model files (model.pkl, columns.pkl) exist in root directory

Flask runs locally at port 5000 by default

Test /predict and /compare manually from the UI

🔐 Security Note
This app is for educational/demo use only. For production deployment:

Add input validation

Handle exceptions gracefully

Secure model and routes

🚧 Future Improvements
🗺️ Add interactive map with property pins (Folium/Leaflet)

📈 Trend charts with more filters (year, builder, etc.)

🔄 API endpoints for integration with external tools

☁️ Cloud deployment (Heroku, Render, etc.)

🙏 Credits
Created by Mohammed Ziyad
This project is part of a machine learning + web development learning exercise.

🌐 GitHub Repo
🔗 View on GitHub

yaml
Copy
Edit

---

### ✅ Summary of What’s Added:
- Sample input/output
- Testing tips
- Security & future features
- Clean markdown tables and structure

Would you like me to:
- Generate this as a downloadable `README.md` file?
- Include screenshots or help you add them in markdown format?
- Create a `requirements.txt` file to go along with it?

Let me know and I’ll prepare everything for your GitHub upload!











Tools



