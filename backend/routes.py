from flask import Blueprint, request, jsonify
from file_input.input_upload import *
import time

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
    time.sleep(20)
    return upload_file()  # Calls the uploaded file function that was imported

#Functionality GET Request
#@upload_blueprint.route('/process_audio', methods=['GET'])
    #Pseudocode
    # Use query parameter?? to pass audio file

    # Retrieve file .. download_audio

    #Trim audio using function trim_audio function I implemented in input_upload.py
    #Then analyze the audio

    #Return analysis result
