'''
Parameters: socket and music file

Color: If the song has an energetic and upbeat feel, bright and vibrant colors 
(e.g., yellows, oranges, neon blues) will work well ideally

For a mellow or dreamy vibe, consider pastel shades, cool tones (blues, purples), and gradients.

For a Bass heavy maybe like Red, Green, Blue as a solid color but flash on the drops

'''

import os
from flask import request, jsonify, current_app
import uuid
from flask_socketio import SocketIO, emit
import librosa
import random
import numpy as np
import colorsys

# Map features to a color palette
def map_to_color(rms_value, centroid_value):
    brightness = rms_value * 0.8 + 0.2  # Use RMS for brightness
    hue = centroid_value * 0.8  # Use spectral centroid for hue, adjust range if needed. (0.6-0.8 seems good)
    r, g, b = colorsys.hls_to_rgb(hue, brightness, 1.0) # Convert to RGB
    return (int(r * 255), int(g * 255), int(b * 255))

def analyze_file(socketio, file):
    socketio.emit('progress', {'progress': random.randint(5, 10)})  # Progress at 10%
    y, sr = librosa.load(file, sr=None)
    print(y, sr)
    socketio.emit('progress', {'progress': random.randint(10, 30)})  # Progress at 30%
    # Analyze the tempo and beat of the song file
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print(f"Tempo: {tempo}")
    
    # Extract spectral centroid and RMS energy
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    socketio.emit('progress', {'progress': random.randint(30, 60)})  # Progress at 60%
    # Normalize features
    spectral_centroid_norm = (spectral_centroid - spectral_centroid.min()) / (spectral_centroid.max() - spectral_centroid.min())
    rms_norm = (rms - rms.min()) / (rms.max() - rms.min())
    socketio.emit('progress', {'progress': random.randint(60, 80)})  # Progress at 80%
    '''
        Create a color array to pass to ML part to create smooth transitions. Take about 4-8 points of the array
        to train model to create an array to smooth to that next color?
    '''
    
    socketio.emit('progress', {'progress': random.randint(80, 95)})  # Progress at 95%
    colors = []
    for i in range(len(beat_frames)):
        time = librosa.frames_to_time(beat_frames[i], sr=sr)
        rms_value = rms_norm[0, i] if i < rms_norm.shape[1] else 0.5
        centroid_value = spectral_centroid_norm[0, i] if i < spectral_centroid_norm.shape[1] else 0.5
        color = map_to_color(rms_value, centroid_value)
        colors.append(color)
    
    print("# of RGB Color combos:", len(colors))
    print(colors)
    socketio.emit('progress', {'progress': 100})  # Progress at 100%