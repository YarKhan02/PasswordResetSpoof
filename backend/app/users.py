from flask import jsonify
from database import db, User  # Import the database instance and User model

def get_all_users():
    """
    Fetch all user emails from the database.
    """
    try:
        # Query all users
        users = User.query.all()

        # Return the list of users with their emails and hashed passwords
        return jsonify({
            "success": True,
            "users": [
                {"email": user.email, "password_hash": user.password_hash} for user in users
            ]
        }), 200

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
