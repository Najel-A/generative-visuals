from flask import Flask, jsonify
from flask_cors import CORS
from routes import upload_blueprint


'''
    Main file to run the development server
'''

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes; Allows for running on different ports
app.register_blueprint(upload_blueprint) # Register blueprint


if __name__ == '__main__':
    app.run(debug=True)
