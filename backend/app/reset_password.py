from flask import request, jsonify
from database import PasswordReset, User, db
import secrets
from datetime import datetime, timedelta

from mail_script import generate_link

def validate_request_data():
    """
    Validates the incoming JSON request data for the reset password route.
    Returns JSON response and HTTP status code.
    """
    # Extract the Host header
    host = request.headers.get('Host')

    data = request.get_json()
    if not data:
        return {"success": False, "message": "Invalid JSON payload"}, 400
    
    email = data.get("email")

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"success": False, "message": "Email not found"}, 404

    # Generate a unique reset token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour

    # Save the token in the database
    reset_entry = PasswordReset(email=email, token=token, expires_at=expires_at)
    db.session.add(reset_entry)
    db.session.commit()
    
    return {"email": email, "token": token, "host": host}, 200

def handle_reset_password():
    """
    Handles the reset password logic.
    """
    # Validate request data
    output, status_code = validate_request_data()
    if status_code != 200:
        return jsonify(output), status_code

    # Execute external script and return result
    response, status_code = generate_link(output["email"], output["token"], output["host"])
    
    return jsonify(response), status_code
