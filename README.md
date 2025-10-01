
# 🧠 Bitcoin Price Prediction using Machine Learning

A beginner-friendly academic project that predicts Bitcoin price movement using machine learning. This web-based application uses historical OHLC (Open, High, Low, Close) data to classify future price trends.

## 🎨 Design Theme

- **Clean UI** – Simple and intuitive layout for easy interaction  
- **Minimalist Styling** – Focused on functionality and clarity  
- **Responsive Pages** – Works well on desktop and mobile  
- **Form-Based Input** – Users can enter custom data for predictions  
- **Prediction Output** – Clear display of model results  
- **Organized Codebase** – Logical separation of backend and templates

---
## project Structure

FINAL/
├── __pycache__/
├── data/
│   └── data/
│       └── btc-usd-max.csv
├── instance/
│   └── btc_prices.db
├── mvenv/
├── templates/
│   ├── add_user.html
│   ├── admin_dashboard.html
│   ├── admin_login.html
│   ├── base.html
│   ├── create_user.html
│   ├── edit_user.html
│   ├── forgot_password.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── users.html
├── add_admin.py
├── app.py
├── btc_prices.db
├── crud_operations.py
├── is_admin.py
├── models.py
├── requirements.txt
└── run.py




## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Backend Setup
```bash
git clone https://github.com/Lakkusai19/Bitcoin_Price-Prediction-using-ML.git
cd Bitcoin_Price-Prediction-using-ML
pip install -r requirements.txt
python app.py
```

---

## 🌐 Access the Application

- **Frontend:** [http://localhost:5000](http://localhost:5000)  
- **Backend API:** Integrated within Flask routes  
- **Prediction Form:** Available on homepage

---

## 👤 Demo Input

Use sample OHLC values to test predictions:
- Open: 20000  
- High: 21000  
- Low: 19500  
- Close: 20500  
- Volume: 3500  
- Date: 2022-10-01

---

## ✨ Features

- 📊 Feature Engineering: `open-close`, `low-high`, `quarter-end` indicators  
- 🧠 ML Models: Logistic Regression, SVM, XGBoost  
- 🖥️ Web Interface: Flask-based form for input and output  
- 📉 EDA: Visual insights into Bitcoin price trends  
- 🔍 Trend Classification: Predicts upward/downward movement  
- 📱 Responsive Design: Accessible on desktop and mobile

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS (inline and template-based)

### Backend
- Python
- Flask
- scikit-learn
- XGBoost
- Pandas
- NumPy

---

## 📊 Data Source

- Historical Bitcoin OHLC data (CSV format)
- Feature columns include:
  - `Open`, `High`, `Low`, `Close`, `Volume`, `Date`
  - Engineered features: `open-close`, `low-high`, `quarter-end`

---

## 🎯 Key Components

- **Home Page:** Input form for OHLC values  
- **Prediction Logic:** ML models trained on historical data  
- **EDA Notebook:** Visualizations and insights  
- **Model Training:** `models.py` handles training and evaluation  
- **Templates:** HTML pages rendered via Flask

---

## 🔧 API Endpoints

```http
GET    /                         # Home page with input form  
POST   /predict                  # Submit form and get prediction  
```

---

## 📦 Sample Data

- Includes sample CSV files for training and testing
- Demo input values available in README and form

---

## 🔧 Code Quality

- **Simplified Structure** – Clean separation of logic and templates  
- **Reduced Complexity** – Focused on core ML and Flask integration  
- **Responsive Design** – Mobile-friendly layout  
- **Modular Code** – Easy to extend or replace models

---

## 📄 License

This project is open-source under the MIT License.

---

```

Let me know if you’d like to add badges (build status, license, Python version), a logo, or even host it with GitHub Pages or Render. I can help you set that up too.
