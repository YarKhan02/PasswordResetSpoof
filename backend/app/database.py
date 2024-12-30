from flask_sqlalchemy import SQLAlchemy

import hashlib

# Initialize the database instance
db = SQLAlchemy()

def md5_hash(password):
    """
    Hashes the password using MD5.
    """
    return hashlib.md5(password.encode()).hexdigest()

class User(db.Model):
    """
    User model representing users in the database.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email address
    password_hash = db.Column(db.Text, nullable=False)  # Hashed password

class PasswordReset(db.Model):
    """
    PasswordReset model to store password reset tokens.
    """
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    email = db.Column(db.String(255), nullable=False)  # User's email associated with the token
    token = db.Column(db.String(255), nullable=False, unique=True)  # Unique reset token
    expires_at = db.Column(db.DateTime, nullable=False)  # Expiration time for the token
    used = db.Column(db.Boolean, default=False)  # Whether the token has been used

def add_test_users():
    """
    Adds test users to the database if they don't already exist.
    """
    test_users = [
        {"email": "iyark2002@gmail.com", "password": "password"},
        {"email": "user2@example.com", "password": "securepassword"},
        {"email": "user3@example.com", "password": "admin12345"},
    ]

    for user_data in test_users:
        # Check if the user already exists
        if not User.query.filter_by(email=user_data["email"]).first():
            hashed_password = md5_hash(user_data["password"])
            user = User(email=user_data["email"], password_hash=hashed_password)
            db.session.add(user)

    db.session.commit()
    print("Test users added successfully.")

def init_db(app):
    """
    Initializes the database with the given Flask app and adds test data.
    """
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Create tables and add test data
    with app.app_context():
        db.drop_all()  # Drop all tables
        db.create_all()  # Create tables if they don't exist
        add_test_users()  # Add test users
