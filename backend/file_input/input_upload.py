from flask import Flask, request, jsonify
import librosa
import soundfile as sf
import io
import numpy as np
from .analyze import *
from .model import *
from pydub import AudioSegment

'''
TODO: Handle file input here
'''

#Trim audio file to 10 seconds
def trim_audio(file,duration_ms=10000):
    #Loads audio and trims it to duration_ms which is 10 seconds
    audio = AudioSegment.from_file(io.BytesIO(file))
    audio_trim = audio[:duration_ms]

    #Converts trimmed audio to wav
    audio_trim_io = io.BytesIO()
    audio_trim.export(audio_trim_io, format="wav")

    audio_trim_io.seek(0)

    return audio_trim_io



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
    # if file_extension not in allowed_extensions:
    #     return jsonify({"error": "Invalid file type."})

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

        # result = analyze_audio(audio_data, y, sr) # pass in the time series and sample rate. OMIT audio data
        features = analyze_audio(audio_data, y, sr)
        features = np.expand_dims(features, axis=0)  # Reshape for prediction

        # Get model prediction; outputs only 5 controls for each time step
        model = create_model()
        prediction = model.predict(features)
        predicted_class = np.argmax(prediction)
        print(prediction)
        print(predicted_class)
        control_sequence = prediction.squeeze().tolist()

    except Exception as e:
        return jsonify({"error": f"File could not be processed. Error: {str(e)}"}), 400

    # return the analysis result
    # return jsonify(result), 200

    # Sends controls to frontend
    controls = {
        "color_scheme": control_sequence[:3],  # First 3 values as RGB
        "camera_movement": control_sequence[3:6],
        "visual_effects": "pulsating" if np.mean(control_sequence) > 0.5 else "static",
    }

    return jsonify(controls)


def test():
    data = {"message": "Hello routes.py!"}
    return jsonify(data)
