from flask import Flask, request, jsonify
'''
TODO: Handle file input here
'''

def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Checks the file extension
    allowed_extensions = {'.mp3', '.wav'}
    file_extension = file.filename.rsplit('.', 1)[-1].lower()

    if f".{file_extension}" not in allowed_extensions:
        return jsonify({"error": "Unsupported file type. Only .mp3 and .wav are allowed."}), 400

    # Temporary Return
    '''
    @TODO:
        Return frames and sequence?
    '''
    result = "OK"
    return jsonify({"message": "File uploaded successfully", "result": result}), 200


def test():
    data = {"message": "Hello routes.py!"}
    return jsonify(data)