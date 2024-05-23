import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)
Migrate(app, db)

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    instructions = db.Column(db.Text)

    def __repr__(self):
        return f"<Recipe {self.id}: {self.title}>"

@app.route('/')
def test_endpoint():
    return f"Hello, welcome to my app"

@app.route("/create-recipe", methods=["POST"])
def create_recipe():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    instructions = data.get("instructions")

    new_recipe = Recipes(
        title=title,
        description=description,
        instructions=instructions
    )

    db.session.add(new_recipe)
    db.session.commit()
    
    return jsonify({"message": "Recipe successfully created", "recipe": {"id": new_recipe.id, "title": new_recipe.title, "description": new_recipe.description, "instructions": new_recipe.instructions}}), 201

