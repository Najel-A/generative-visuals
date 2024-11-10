from keras.models import load_model
from model import create_model
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from file_input.analyze import analyze_audio
from io import BytesIO
import numpy as np
import librosa
import os

def load_and_preprocess(file_object):
    try:
        file_object.seek(0)
        y, sr = librosa.load(file_object, sr=None) #Load audio
        features = analyze_audio(file_object, y, sr) #Extract features

        features = features.reshape((features.shape[0], -1, 1)) #Reshaping features
        return features
    except Exception as e:
        return {"error": f"File could not be processed. Error: {str(e)}"}

#Prepare dataset from the files and labels (light, dark mood)
def prepare_dataset(files,labels):
    X = []
    y = []

    for idx, file_object in enumerate(files):
        features = load_and_preprocess(file_object)

        if isinstance(features,dict) and 'error' in features:
            print(f"Skipping file {idx}: {features['error']}")
            continue  # Skip files that failed to process

        X.append(features)
        y.append(labels[idx])  # Assume labels are provided in the same order as files

    X = np.array(X)
    y = np.array(y)

    return X,y

def train_model():
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    #Instantiate the model
    model = create_model(input_shape=(X.shape[1],))
    # Train the model
    model.fit(X_train, y_train, epochs=10, batch_size=8, validation_data=(X_val, y_val))

    # Evaluate the model
    loss = model.evaluate(X_val, y_val)
    print(f"Validation Loss: {loss}")

    model.save("audio_model.h5")

if __name__ == "__main__":

    files = []
    labels = []

    X, y = prepare_dataset(files,labels)

    train_model(X, y)
