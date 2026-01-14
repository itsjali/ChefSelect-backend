from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.auth.decorators import token_required
from app.models import Recipe
from app.schemas import RecipeDetailsSchema, ExtendedRecipeDetailsSchema
from app.services import create_recipe_service

main_bp = Blueprint("main", __name__)


@main_bp.route("/create-recipe", methods=["POST"], endpoint="create_recipe")
@token_required
def create_recipe():
    """
    Endpoint that creates the Recipe object using the data from the the frontend.

    Marshmallow is used to validate the data, if its valid the data is passed
    to the create recipe function. If valid, a 200 is returned.

    If the data validation fails a 400 is returned with error messages.     
    """
    data = request.get_json()
    try:
        schema = RecipeDetailsSchema()
        validated_data = schema.load(data)

        create_recipe_service(validated_data)

        return jsonify({"message": "Recipe created successfully"}), 200
    
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400


@main_bp.route("/get-recipes", methods=["GET"], endpoint="get_recipes")
@token_required
def get_recipes():
    """
    Endpoint that queries all recipes from the db and returned to the frontend. 
    """
    recipes = Recipe.query.all()
    schema = ExtendedRecipeDetailsSchema(many=True)
    return jsonify({"message": "Success", "data": schema.dump(recipes)}), 200
