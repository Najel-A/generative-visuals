from flask import Blueprint, request, jsonify

upload_blueprint = Blueprint('upload', __name__) # Creates a blueprint for the app.py

# Default Load
@upload_blueprint.route('/', methods=['GET'])
def get_data():
    data = {"message": "Hello routes.py!"}
    return jsonify(data)