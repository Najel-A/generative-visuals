from keras.models import Sequential
from keras.layers import LSTM, Dense, RepeatVector, TimeDistributed, Flatten, Reshape

def create_model(input_shape=(30,)):
    model = Sequential()
    model.add(Flatten(input_shape=input_shape))  # Flatten to 2D
    model.add(Dense(64, activation='relu')) # Learns pattern from input shape
    model.add(RepeatVector(10))  # Repeat flattened output to create a sequence for control values
    model.add(LSTM(128, activation='relu', return_sequences=True)) # Long short term memory
    model.add(TimeDistributed(Dense(32, activation='relu'))) # # Learn features for each frame
    model.add(TimeDistributed(Dense(5, activation='linear')))  # Output 5 controls for each time step

    model.compile(optimizer='adam', loss='mse')
    return model