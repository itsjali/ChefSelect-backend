from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def test_endpoint():
    return "Hello, welcome to my app"


@app.route('/create-recipe', methods=['POST'])
def create_recipe():
    return jsonify({'message': 'Recipe successfully created'}), 201

