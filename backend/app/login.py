import hashlib
from flask import request, jsonify
from database import db
from database import User

def md5_hash(password):
    """
    Hashes the password using MD5.
    """
    return hashlib.md5(password.encode()).hexdigest()

def handle_login():
    try:
        # Parse request data
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        # Query the user from the database
        user = User.query.filter_by(email=email).first()

        # Check if user exists and the password matches
        if user and user.password_hash == md5_hash(password):
            return jsonify({"success": True, "message": "Login successful"}), 200
        else:
            return jsonify({"success": False, "message": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
