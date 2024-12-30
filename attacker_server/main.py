from flask import Flask, request, jsonify
from flask_cors import CORS

import logging

# Configure logging to write to the console
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
CORS(app)

@app.route('/capture-token', methods=['POST'])
def capture_token():
    """
    API endpoint to capture tokens sent via POST.
    """
    data = request.get_json()
    token = data.get('token')

    # Log an example message
    logging.info("This message will appear in Docker logs %s", token)

    if token:
        print(f"Captured Token: {token}")
        file_path = "captured_tokens.txt"
        with open(file_path, "w") as f:
            f.write(token)
        return jsonify({"success": True}), 200
    
    return jsonify({"success": False, "message": "No token provided"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)