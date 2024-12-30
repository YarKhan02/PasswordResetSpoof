from flask import Flask
from flask_cors import CORS
from database import init_db
from reset_password import handle_reset_password
from login import handle_login
from users import get_all_users
from confirm_new_password import reset_new_password

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Initialize the database
init_db(app)

@app.route("/reset-password", methods=["POST"])
def reset_password():
    return handle_reset_password()

@app.route("/login", methods=["POST"])
def verify_login():
    return handle_login()

@app.route("/confirm-password", methods=["POST"])
def confirm_password():
    return reset_new_password()

@app.route("/users", methods=["GET"])
def users():
    return get_all_users()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
