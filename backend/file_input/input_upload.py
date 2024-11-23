'''
    Input Upload takes in the file and verifies its content before establishing web socket
'''

import os
from flask import request, jsonify, current_app
import uuid
from flask_socketio import SocketIO, emit

def upload_file(socketio):
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Validate file type (e.g., check extension)
    allowed_extensions = {"mp3", "wav"}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return jsonify({"error": "Unsupported file type"}), 400

    # Save the file with UUID and file name
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)

    # After file upload, emit the 'progress' event via WebSocket
    socketio.emit('progress', {'progress': 50})  # Initial progress is 0

    # Return file path
    return jsonify({"message": "File uploaded successfully", "file_path": file_path})
