# 🏡 Real Estate Price Prediction

A machine learning-based web app that predicts real estate prices using features like location, area, and bedrooms. Built with Flask and Random Forest, it includes a compare-locations feature to help users analyze property trends. Ideal for buyers, sellers, and analysts.

---

## 🔍 Features

- 🔢 Predict property prices based on user inputs
- 📍 Compare average prices between two locations
- 🌐 User-friendly web interface (HTML/CSS + Flask)
- 📦 Trained model stored as `model.pkl`

---

## 🧠 Machine Learning

- **Models Tried**: Linear Regression, Random Forest, XGBoost
- **Best Model**: Random Forest Regressor (R² ≈ 0.67)
- **Preprocessing**: Null handling, encoding, feature scaling
- **Files Used**:
  - `model.pkl`: Trained model
  - `columns.pkl`: Feature names
  - `location.json`: Location coordinates

---

## 🛠 Tech Stack

- **Language**: Python
- **Libraries**: Pandas, Scikit-learn, XGBoost
- **Web**: Flask, HTML, CSS, Bootstrap
- **Tools**: Jupyter Notebook, GitHub

---

## 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/real-estate-price-prediction
cd real-estate-price-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
