from flask import Flask, request, jsonify
import librosa
import soundfile as sf
import io
import numpy as np
from .generate import *

'''
TODO: Handle file input here
'''

def upload_file():
    # Check if a file is part of the request; frontend check?
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If no file is selected, can probably handle this in frontend?
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Checks the file extension; fix later
    allowed_extensions = {'.mp3', '.wav'}
    file_extension = file.filename.rsplit('.', 1)[-1].lower()

    #Reject invalid types
    if file_extension not in allowed_extensions:
        return jsonify({"error": "Invalid file type."})

    # Attempt to load audio using librosa
    try:

        file.seek(0)
        audio_data = file.read()  # Read the file content
        # Load the audio from the BytesIO stream
        y, sr = librosa.load(io.BytesIO(audio_data), sr=None)

        # Check getting bypassed on an all zero array
        if np.all(y == 0):
            print("The array contains only zeros.")
            return jsonify({"error": "Audio file could not be processed or it is silent."}), 400

        result = analyze_audio(audio_data)

    except Exception as e:
        return jsonify({"error": f"File could not be processed. Error: {str(e)}"}), 400

    # return the analysis result
    return jsonify(result), 200


def test():
    data = {"message": "Hello routes.py!"}
    return jsonify(data)
