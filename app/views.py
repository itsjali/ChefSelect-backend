from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.auth.decorators import token_required
from app.schemas import RecipeSchema
from app.services import create_recipe_service

main_bp = Blueprint("main", __name__)


@main_bp.route("/create-recipe", methods=["POST"])
@token_required
def create_recipe():
    """
    Endpoint that receives data from the frontend 
    """
    data = request.get_json()
    try:
        schema = RecipeSchema()
        validated_data = schema.load(data)

        recipe = create_recipe_service(validated_data)

        return jsonify({"message": "Success", "data": recipe.title}), 200
    
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
