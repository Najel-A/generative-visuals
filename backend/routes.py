'''
     To reduce space in the routes, going to create functions in separate directories and just import it here
'''

from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO
from file_input.input_upload import upload_file  # Import your file upload function



# Creates a blueprint for the app.py
upload_blueprint = Blueprint('upload', __name__)

# Default Load Route
@upload_blueprint.route('/', methods=['GET'])
def get_data():
    return jsonify({"message": "Connection Established"})

# File Upload Route
@upload_blueprint.route('/upload', methods=['POST'])
def upload_file_route():
    """Route to handle file upload."""
    from app import socketio  # Import socketio from app.py
    return upload_file(socketio)  # Pass socketio to the upload_file function
