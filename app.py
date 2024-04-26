from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def test_endpoint():
    return "Hello, welcome to my app"


@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    return jsonify({'message': 'Recipe successfully created'}), 201

