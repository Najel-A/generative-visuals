'''
    Input Upload takes in the file and verifies its content before establishing web socket
'''

import os
from flask import request, jsonify, current_app
import uuid
from flask_socketio import SocketIO, emit
from .analyze import analyze_file
import time

def upload_file(socketio):
    global is_client_ready
    print("SocketIO:", socketio)
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

    # Manage file limit in the uploads folder, doing this for temp before scaling to a DB
    max_files = 10
    existing_files = [
        os.path.join(upload_folder, f)
        for f in os.listdir(upload_folder)
        if os.path.isfile(os.path.join(upload_folder, f))
    ]

    # Sort by modification time (oldest first)
    existing_files.sort(key=lambda x: os.path.getmtime(x))

    # Delete oldest files if the limit is exceeded
    while len(existing_files) >= max_files:
        oldest_file = existing_files.pop(0)
        os.remove(oldest_file)
        print(f"Deleted old file: {oldest_file}")
    
    # Save latest file
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)


    '''
        This block is used for testing the websocket to the front end
    '''
    # After file upload, emit the 'progress' event via WebSocket
    # Call three functions here to analyze, process, and generate visuals with live updates using emit
    socketio.emit('progress', {'progress': 10})  # Initial progress is 0
    socketio.emit('progress', {'progress': 20})

    # Wait for WebSocket readiness
    # while not is_client_ready:
    #     time.sleep(0.1)  # Poll for readiness

    socketio.emit('progress', {'progress': 30})
    socketio.emit('progress', {'progress': 40})
    '''
        This block is used for testing the websocket to the front end
    '''


    analyze_file(socketio, file_path) # First step in the process


    print("Visuals Completed") # Temporary holder for debugging
    # Return file path, after processing
    return jsonify({"message": "File succesfully generated visuals.", "file_path": file_path})
