from flask import request, jsonify
from hashlib import md5
from datetime import datetime
from database import db, User, PasswordReset

def reset_new_password():
    """
    Handles password reset using a token.
    """
    try:
        # Get data from the request
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')

        # Validate input
        if not token or not new_password:
            return jsonify({"success": False, "message": "Token and new password are required"}), 400

        # Find the token in the PasswordReset table
        reset_entry = PasswordReset.query.filter_by(token=token).first()

        if not reset_entry:
            return jsonify({"success": False, "message": "Invalid token"}), 404

        # Check if the token has expired
        if reset_entry.expires_at < datetime.utcnow():
            return jsonify({"success": False, "message": "Token has expired"}), 403

        # Find the user associated with the email
        user = User.query.filter_by(email=reset_entry.email).first()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        # Hash the new password using MD5
        hashed_password = md5(new_password.encode()).hexdigest()

        # Update the user's password
        user.password_hash = hashed_password
        db.session.commit()

        # Optionally, delete the reset token after use
        db.session.delete(reset_entry)
        db.session.commit()

        return jsonify({"success": True, "message": "Password reset successfully"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
