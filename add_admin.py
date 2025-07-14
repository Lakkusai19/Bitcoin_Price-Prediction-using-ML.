from app import db  # Import the db object from your Flask app
from models import User  # Import the User model from your app
from flask_bcrypt import Bcrypt  # Import Bcrypt for hashing passwords

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Hash the password for secure storage
hashed_password = bcrypt.generate_password_hash('1144').decode('utf-8')

# Create the admin user
admin_user = User(
    username='admin',
    email='lakkuanagasa1122@gmail.com',
    password=hashed_password,
    is_admin=True
)

# Add the new admin user to the database
db.session.add(admin_user)
db.session.commit()

print("Admin user added successfully.")
