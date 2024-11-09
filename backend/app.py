from flask import Flask, jsonify
from flask_cors import CORS
from routes import upload_blueprint
from flask_socketio import SocketIO, emit
from file_input.input_upload import trim_audio
from pydub import AudioSegment
from file_input.analyze import analyze_audio
from file_input.model import create_model
import librosa
import numpy as np
import io


'''
    Main file to run the development server
'''

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes; Allows for running on different ports
app.register_blueprint(upload_blueprint) # Register blueprint

#Initializing SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

#WebSocket event handling
@socketio.on('audio_stream')
def handle_audio_stream(data):
    try:
        audio_chunk = data['audio_chunk']
        audio_chunk_io = io.BytesIO(audio_chunk)

        trimmed_audio = trim_audio(audio_chunk_io)
        y, sr = librosa.load(trimmed_audio, sr=None)

        features = analyze_audio(None, y, sr)
        features = np.expand_dims(features, axis=0)  # Reshape for prediction

        # Get control prediction from the model
        model = create_model()
        prediction = model.predict(features)
        control_sequence = prediction.squeeze().tolist()

        # Send controls back to the client
        controls = {
            #"color_scheme": control_sequence[:3],  # First 3 values as RGB
            #"camera_movement": control_sequence[3:6]
            #"visual_effects": "pulsating" if np.mean(control_sequence) > 0.5 else "static",
        }

        # Emit controls back to client
        emit('audio_controls', controls)
    except Exception as e:
        emit('error', {"error: Fault in processing audio chunk"})

# Change for 0.0.0.0 for EC2
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
