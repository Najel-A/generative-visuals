from flask import Flask
from flask_cors import CORS
from routes import *
from flask_socketio import SocketIO, emit
from socket_handler import init_socketio
from routes import upload_blueprint

'''
    Main file to run the development server
'''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' # creates folder if non-existent for music file
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Register blueprints, url_prefixes caused an error
app.register_blueprint(upload_blueprint)

is_client_ready = False
socketio = SocketIO(app, cors_allowed_origins="*") #Initializing SocketIO
init_socketio(socketio)

# Change for 0.0.0.0 for EC2
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    #app.run(host='0.0.0.0', port=5000, debug=True) # not used for WebSocket
