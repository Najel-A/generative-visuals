import os
import numpy as np
from file_input.analyze import analyze_audio
from file_input.model import create_model
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import librosa
import io

def load_audio_data(file_path):
    """
    Loads and processes the audio data using librosa and analyzes it.
    """
    try:
        # Load audio file using librosa
        y, sr = librosa.load(file_path, sr=None)

        # Process audio and extract features
        features = analyze_audio(None, y, sr)
        features = np.expand_dims(features, axis=0)  # Reshape to match input shape

        return features
    except Exception as e:
        print(f"Error loading or processing audio: {e}")
        return None


def generate_control_labels():
    # Example: Random control sequence (just for demonstration purposes)
    # In a real setup, replace this with actual control sequences based on your dataset
    control_sequence = np.random.rand(1, 10, 5)  # Generate random control sequence for 10 time steps
    return control_sequence


def train_model(audio_file_path, epochs=10, batch_size=32):
    """
    Main function to train the model on a single audio file.
    """
    features = load_audio_data(audio_file_path)
    if features is None:
        print("Error: Features could not be loaded.")
        return

    # Generate control sequence labels (for now, using a placeholder)
    control_labels = generate_control_labels()

    # Split data into training and testing sets (for this case, we only have one example, so train only)
    X_train, y_train = features, control_labels

    # Create the model
    model = create_model(input_shape=X_train.shape[1:])

    # Compile the model
    model.compile(optimizer=Adam(), loss='mse')

    # Train the model
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    # Save the model after training
    model.save('generative_visual_model.keras')
    print("Model trained and saved.")


if __name__ == "__main__":
    audio_file_path = "/Users/yipvi/generative-visuals/backend/sample_music/21.wav"
    train_model(audio_file_path)
