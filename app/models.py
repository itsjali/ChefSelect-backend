from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    ingredients = db.relationship("Ingredient", backref="recipe", lazy=True)
    instructions = db.relationship("Instruction", backref="recipe", lazy=True)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)


class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
