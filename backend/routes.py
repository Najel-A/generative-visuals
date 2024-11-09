from flask import Blueprint, request, jsonify
from file_input.input_upload import *

'''
    To reduce space in the routes, going to create functions in separate directories and just import it here
'''

upload_blueprint = Blueprint('upload', __name__) # Creates a blueprint for the app.py

# Default Load
@upload_blueprint.route('/', methods=['GET'])
def get_data():
    return test()

# File Upload Input
@upload_blueprint.route('/upload', methods=['POST'])
def upload_file_route():  # Defines a route function that calls the upload_file function
    return upload_file()  # Calls the uploaded file function that was imported