from flask import Flask, request, jsonify
import librosa
import soundfile as sf
import io
from .generate import *

'''
TODO: Handle file input here
'''

def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    # If no file is selected, can probably handle this in frontend
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Checks the file extension
    allowed_extensions = {'.mp3', '.wav'}
    file_extension = file.filename.rsplit('.', 1)[-1].lower()
    
    # Inspect File for librosa
    # Reset file pointer to the beginning of the file
    file.seek(0)
    
    # Attempt to load audio using librosa
    try:
        audio_data = file.read()  # Read the file content
        # Load the audio from the BytesIO stream
        y, sr = librosa.load(io.BytesIO(audio_data), sr=None)
        print(f"Normalized audio data: {y}")
        print(f"Shape of y: {y.shape}, Sample Rate: {sr}")
        print(y, sr)
        
        if len(y) == 0:
            return jsonify({"error": "File could not be processed. Audio is empty."}), 400

        #return jsonify({"message": "File uploaded successfully", "sample_rate": sr, "duration": len(y) / sr}), 200

    except Exception as e:
        return jsonify({"error": f"File could not be processed. Error: {str(e)}"}), 400


    file.seek(0)
    filetmp = file.read()
    result = analyze_audio(filetmp)

    # return the analysis result
    return jsonify(result), 200


def test():
    data = {"message": "Hello routes.py!"}
    return jsonify(data)