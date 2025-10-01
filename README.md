
# 🧠 Bitcoin Price Prediction using ML  
A beginner-friendly academic project that predicts Bitcoin price movement using machine learning, built with Python and Flask. It features a clean web interface, modular backend, and real-time prediction capability.

---

## 🎨 Design Theme  
Minimalist UI with Form-Based Prediction

- Clean Input Form – Simple and intuitive layout  
- Organized Templates – Login, Register, Dashboard, Admin views  
- Responsive Pages – Accessible on desktop and mobile  
- Modular Code – Separation of logic, models, and templates  
- SQLite Integration – Lightweight and fast  
- Flask Routing – Smooth navigation between pages

---

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
- Web App: [http://localhost:5000](http://localhost:5000)  
- Prediction Form: Available on homepage  
- Admin Dashboard: Accessible after login  

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
- 📊 Feature Engineering: `open-close`, `low-high`, `quarter-end`  
- 🧠 ML Models: Logistic Regression, SVM, XGBoost  
- 🖥️ Web Interface: Flask-based form and dashboard  
- 🔐 User Auth: Login, Register, Admin access  
- 📉 EDA Notebook: Visual insights into Bitcoin trends  
- 📱 Responsive Design: Mobile-friendly layout

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
- SQLite  

---

Backend Setup
cd backend
pip install -r requirements.txt
python init_db.py
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
Frontend Setup
cd frontend
npm install
npm start

## 📁 Project Structure  

```
FINAL/
├── data/data/btc-usd-max.csv
├── instance/btc_prices.db
├── mvenv/
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── users.html
│   └── ... (other HTML files)
├── add_admin.py
├── app.py
├── crud_operations.py
├── is_admin.py
├── models.py
├── requirements.txt
└── run.py
```

---

## 🎯 Key Components  
- Home Page: Input form for OHLC values  
- Prediction Logic: ML models trained on historical data  
- Admin Panel: View users and manage access  
- Templates: HTML pages rendered via Flask  
- Database: SQLite for storing price and user data  

---

## 🔧 API Routes  
```http
GET    /             # Home page  
POST   /predict      # Submit form and get prediction  
GET    /login        # User login  
POST   /register     # User registration  
GET    /admin        # Admin dashboard  
```

---

## 📦 Sample Data  
- `btc-usd-max.csv` – Historical Bitcoin OHLC data  
- `btc_prices.db` – SQLite database for predictions and users  

---

🔧 Code Quality
- Simplified Structure – Clean, modular code
- Reduced Complexity – Focused on core logic
- Responsive Design – Mobile-first layout
- Built with ❤️ for learning and experimentatio


## 🛠️ Troubleshooting  

- **App not running:** Activate virtual environment and run `app.py`  
- **Missing modules:** `pip install -r requirements.txt`  
- **DB errors:** Ensure `btc_prices.db` exists in `instance/`  
- **Template issues:** Confirm HTML files are inside `templates/`  
- **Form not working:** Check `POST` method and route in `app.py`

---

## 📄 About  
Bitcoin price prediction project using ML and Flask, designed for academic learning and practical deployment.
