from flask import Flask, request, jsonify
import librosa
import io
from pydub import AudioSegment

# Function to analyze the audio file using librosa
def analyze_audio(file):
    try:
        print("Audio data:", y)
        print("Sample rate:", sr)

        # Analyze beats (just as an example)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        print(tempo, beat_times)

        # Return analysis result, needs to be in a list not numpy format
        return {"tempo": tempo.tolist(), "beats": beat_times.tolist()}
    except Exception as e:
        return {"error": f"File could not be processed. Error: {str(e)}"}
