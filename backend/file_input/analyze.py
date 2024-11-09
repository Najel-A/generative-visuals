from flask import Flask, request, jsonify
import librosa
import io
from pydub import AudioSegment
import numpy as np

# Function to analyze the audio file using librosa
def analyze_audio(file, y, sr):
    try:
        # print("Audio data:", y)
        # print("Sample rate:", sr)

        # # Analyze beats (just as an example)
        # tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        # beat_times = librosa.frames_to_time(beats, sr=sr)
        # print(tempo, beat_times)

        # # Pitches and magnitudes
        # pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
        
        # # Root Mean Square Energy (loudness)
        # rms = librosa.feature.rms(y=y)

        # # Spectrogram (STFT)
        # D = librosa.stft(y)
        # spectrogram = np.abs(D)

        # # MFCC
        # mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        

        # # Return analysis result, needs to be in a list not numpy format
        # return {"tempo": tempo.tolist(), "beats": beat_times.tolist(),
        #         "pitches": pitches.tolist(), "magnitudes": magnitudes.tolist(),
        #         "rms": rms.tolist(), "mfcc": mfcc.tolist(), "spectrogram": spectrogram.tolist()}
    

        #y, sr = librosa.load(audio_file, sr=None)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        rms = librosa.feature.rms(y=y)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)

        # Aggregating or resampling to maintain consistency
        features = {
            "tempo": np.array([tempo]),
            "beats": np.mean(beat_frames),
            "mfcc": np.mean(mfcc, axis=1),  # Summarize MFCCs
            "rms": np.mean(rms),
            "pitches": np.mean(pitches),
            "magnitudes": np.mean(magnitudes),
            "chroma": np.mean(chroma, axis=1)
        }

        # Flatten to create a 1D array for input
        return np.concatenate([features[key].flatten() for key in features])

    except Exception as e:
        return {"error": f"File could not be processed. Error: {str(e)}"}