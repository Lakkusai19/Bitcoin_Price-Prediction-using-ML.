
from flask import Flask, request, render_template, redirect, url_for, flash,session
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import plotly.express as px
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from functools import wraps
from forms import RegistrationForm, LoginForm, AddUserForm, EditUserForm
from models import db, Price, User
from functools import wraps
from forms import LoginForm

# Initialize Flask app and configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///btc_prices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mock database
users = [
    {"id": 1, "name": "Admin User", "email": "admin@example.com", "is_admin": True},
]

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# Helper functions to load and process data
def load_data():
    df = pd.read_csv("data/data/btc-usd-max.csv", parse_dates=["date"], index_col="date")
    df['percent_change'] = df['price'].pct_change() * 100
    return df

def train_and_predict(df, days_ahead=30, specific_date=None):
    scaler = StandardScaler()
    df['timestamp'] = df.index.astype(np.int64) // 10**9
    X = scaler.fit_transform(df[['timestamp']])
    y = df['price']

    model = LinearRegression()
    model.fit(X, y)

    latest_price = df['price'].iloc[-1]

    if specific_date:
        timestamp = specific_date.timestamp()
        timestamp_scaled = scaler.transform([[timestamp]])
        predicted_price = model.predict(timestamp_scaled)[0]
        predicted_price_adjusted = latest_price + (predicted_price - model.predict(scaler.transform([[df['timestamp'].iloc[-1]]]))[0])
        return predicted_price_adjusted

    future_dates = [df.index[-1] + timedelta(days=i) for i in range(1, days_ahead + 1)]
    future_timestamps = np.array([date.timestamp() for date in future_dates])
    future_timestamps_scaled = scaler.transform(future_timestamps.reshape(-1, 1))
    future_trend_predictions = model.predict(future_timestamps_scaled)

    future_prices = [latest_price]
    today_pred = model.predict(scaler.transform([[df['timestamp'].iloc[-1]]]))[0]
    adjustment = latest_price - today_pred

    for trend in future_trend_predictions:
        adjusted_price = trend + adjustment
        future_prices.append(adjusted_price)
        adjustment = adjusted_price - latest_price

    future_df = pd.DataFrame({'Date': future_dates, 'Predicted_Price': future_prices[1:]})
    return model, future_df, scaler

def resample_data(df, range_type):
    if range_type == 'weekly':
        return df.resample('W').last()
    elif range_type == 'monthly':
        return df.resample('M').last()
    elif range_type == 'yearly':
        return df.resample('Y').last()
    else:
        return df

# Admin check decorator with @wraps to avoid endpoint conflicts
def admin_required(f):
    @wraps(f)  # Preserve the function name and signature
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return wrapper

# Routes
@app.route('/')
@login_required
def index():
    df = load_data()

    latest_data = df.iloc[-1]
    price = latest_data['price']
    market_cap = latest_data['market cap']
    volume = latest_data['volume']

    today = datetime.today().strftime('%Y-%m-%d')
    time_range = request.args.get('time_range', 'daily')

    df_resampled = resample_data(df, time_range)

    price_fig = px.line(df_resampled, x=df_resampled.index, y="price", title=f"$Bitcoin Price Over Time ({time_range.capitalize()})")
    market_cap_fig = px.line(df_resampled, x=df_resampled.index, y="market cap", title=f"$Market Cap Over Time ({time_range.capitalize()})")
    volume_fig = px.line(df_resampled, x=df_resampled.index, y="volume", title=f"$Trading Volume Over Time ({time_range.capitalize()})")
    percent_change_fig = px.line(df_resampled, x=df_resampled.index, y="percent_change", title=f"$Daily Percentage Change in Bitcoin Price ({time_range.capitalize()})")

    price_graph_html = price_fig.to_html(full_html=False, include_plotlyjs='cdn')
    market_cap_graph_html = market_cap_fig.to_html(full_html=False, include_plotlyjs='cdn')
    volume_graph_html = volume_fig.to_html(full_html=False, include_plotlyjs='cdn')
    percent_change_graph_html = percent_change_fig.to_html(full_html=False, include_plotlyjs='cdn')

    _, future_df, _ = train_and_predict(df)
    future_graph_json = future_df.to_json(date_format='iso', orient='records')

    return render_template("index.html",
                           price=price,
                           market_cap=market_cap,
                           volume=volume,
                           price_graph=price_graph_html,
                           market_cap_graph=market_cap_graph_html,
                           volume_graph=volume_graph_html,
                           percent_change_graph=percent_change_graph_html,
                           future_prices=future_graph_json,
                           today=today,
                           time_range=time_range)

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    selected_date = request.form['prediction_date']
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')

    df = load_data()
    prediction = train_and_predict(df, specific_date=selected_date_obj)

    latest_data = df.iloc[-1]
    price = latest_data['price']
    market_cap = latest_data['market cap']
    volume = latest_data['volume']

    price_fig = px.line(df, x=df.index, y="price", title="$Bitcoin Price Over Time")
    market_cap_fig = px.line(df, x=df.index, y="market cap", title="$Market Cap Over Time")
    volume_fig = px.line(df, x=df.index, y="volume", title="$Trading Volume Over Time")
    percent_change_fig = px.line(df, x=df.index, y="percent_change", title="$Daily Percentage Change in Bitcoin Price")

    price_graph_html = price_fig.to_html(full_html=False, include_plotlyjs='cdn')
    market_cap_graph_html = market_cap_fig.to_html(full_html=False, include_plotlyjs='cdn')
    volume_graph_html = volume_fig.to_html(full_html=False, include_plotlyjs='cdn')
    percent_change_graph_html = percent_change_fig.to_html(full_html=False, include_plotlyjs='cdn')

    _, future_df, _ = train_and_predict(df)
    future_graph_json = future_df.to_json(date_format='iso', orient='records')

    percent_change = ((prediction - price) / price) * 100

    return render_template('index.html',
                           price=price,
                           market_cap=market_cap,
                           volume=volume,
                           price_graph=price_graph_html,
                           market_cap_graph=market_cap_graph_html,
                           volume_graph=volume_graph_html,
                           percent_change_graph=percent_change_graph_html,
                           future_prices=future_graph_json,
                           prediction=round(prediction, 2),
                           percent_change=round(percent_change, 2),
                           today=datetime.today().strftime('%Y-%m-%d'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to log in first", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to ensure user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id or not any(user for user in users if user['id'] == user_id and user['is_admin']):
            flash("You do not have permission to perform this action", "error")
            return redirect(url_for('admin_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Route to add user
@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        
        # Add new user to the "database"
        new_user = {
            "id": len(users) + 1,
            "name": name,
            "email": email,
            "is_admin": False  # Default to non-admin
        }
        users.append(new_user)
        
        # Flash success message
        flash(f"User {name} added successfully!", "success")
        
        # Redirect to the admin dashboard
        return redirect(url_for('admin_dashboard'))
    
    # Render the "Add User" form template
    return render_template('add_user.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')  # Your dashboard page template

@app.route('/admin/users')
@login_required
@admin_required
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)


@app.route('/admin_dashboard')
def admin_dashboard():
    # Fetch all users from the database
    users = User.query.all()  # Assuming you're using SQLAlchemy
    return render_template('admin_dashboard.html', users=users)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        # Add user to the database
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('create_user.html')


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))




@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Handle sending a reset password email here
        flash('If this email is registered, a password reset link will be sent shortly.', 'info')
        return redirect(url_for('login'))

    return render_template('forgot_password.html')  # Render a page where user can input their email.






@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()  # Assuming you're using Flask-WTF for forms
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Verify credentials logic here
        if email == "lakkunagasai1144@gmail.com" and password == "11441144":  # Example check
            flash("Login successful!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid email or password!", "error")
    return render_template('admin_login.html', form=form)



@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Get form data
    new_name = request.form.get('name')
    new_email = request.form.get('email')
    # new_password=request.form.get('password')

    # Ensure email and name are provided
    if not new_name or not new_email:
        flash('Name and Email are required', 'danger')
        return redirect(url_for('edit_user', user_id=user.id))

    # Update the user details
    user.name = new_name
    user.email = new_email
    # user.password=new_password
    # Commit to the database
    db.session.commit()
    
    flash('User updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))  # Or redirect back to the users page


@app.route('/edit_user/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    # Fetch the user record by ID
    user = User.query.get_or_404(user_id)
    
    # Render a template with the current user data
    return render_template('edit_user.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)







































