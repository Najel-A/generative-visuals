'''
Training the ML algorithm will take time, for now creating a LinearRegression Model to handle
color gradient scaling for now, as changes to the frontend will be made. From LinearRegression
create a neural network as we introduce new variables that will help determine the color scheme, for
example mood or brightness.
'''

from sklearn.linear_model import LinearRegression
import numpy as np
from flask_socketio import SocketIO, emit
import random

# Training data
def train_model(socketio, colors):
    socketio.emit('progress_train', {'progress': random.randint(5, 10)})  # Progress at 10%
    num_colors = len(colors)
    t_values = np.linspace(0, num_colors - 1, num_colors)  # [0, 1, 2, ..., num_colors-1]
    rgb_values = np.array(colors)
    socketio.emit('progress_train', {'progress': random.randint(10, 40)})  # Progress at 40%

    # Train the model for each RGB channel separately
    models = [LinearRegression().fit(t_values.reshape(-1, 1), rgb_values[:, i]) for i in range(3)]

    # Generate smooth transition from each distinct RGB color value
    t_steps = np.linspace(0, num_colors - 1, 100 * (num_colors - 1))  # Intermediate t values
    gradient = np.column_stack([model.predict(t_steps.reshape(-1, 1)) for model in models])
    socketio.emit('progress_train', {'progress': random.randint(40, 70)})  # Progress at 70%

    # Ensure RGB values are integers and clamped to [0, 255]
    gradient = np.clip(np.round(gradient), 0, 255).astype(int)
    print(gradient) # For testing
    socketio.emit('progress_train', {'progress': 100})  # Progress at 100%
    return gradient