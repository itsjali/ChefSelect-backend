import pytest
from marshmallow import ValidationError

from app.schemas import IngredientSchema, InstructionSchema, RecipeSchema


def test_ingredient_schema_with_valid_data():
    ingredient = {"unit": "100g", "name": "Chicken"}

    ingredient_schema = IngredientSchema()
    result = ingredient_schema.load(ingredient)
    
    assert result["unit"] == "100g"
    assert result["name"] == "Chicken"


def test_ingredient_schema_raises_validation_error_if_invalid_data():
    ingredient = {"unit": "100g"}

    ingredient_schema = IngredientSchema()

    with pytest.raises(ValidationError):
        ingredient_schema.load(ingredient)


def test_instruction_schema_with_valid_data():
    instruction = {"step": 1, "description": "Cook the chicken"}

    instruction_schema = InstructionSchema()
    result = instruction_schema.load(instruction)

    assert result["step"] == 1
    assert result["description"] == "Cook the chicken"


def test_instruction_schema_raises_validation_error_if_invalid_data():
    instruction = {"step": 1}

    instruction_schema = InstructionSchema()

    with pytest.raises(ValidationError):
        instruction_schema.load(instruction)


def test_recipe_schema_with_valid_data():
    recipe = {
        "title": "Chicken Curry",
        "description": "Delicious chicken curry with rice",
        "ingredients": [
            {"unit": "100g", "name": "Chicken"},
            {"unit": "200g", "name": "Rice"}
        ],
        "instructions": ["Step 1", "Step 2"]
    }

    recipe_schema = RecipeSchema()
    result = recipe_schema.load(recipe)
    
    assert result["title"] == "Chicken Curry"
    assert result["description"] == "Delicious chicken curry with rice"
    assert len(result["ingredients"]) == 2
    assert result["ingredients"][0]["unit"] == "100g"
    assert result["ingredients"][0]["name"] == "Chicken"
    assert len(result["instructions"]) == 2
    assert result["instructions"][0] == "Step 1"


def test_recipe_schema_raises_validation_error_if_invalid_data():
    recipe = {
        "title": "Chicken Curry",
        "description": "Delicious chicken curry with rice",
        "ingredients": [
            {"unit": "100g", "name": "Chicken"},
            {"unit": "200g", "name": "Rice"}
        ]
    }

    recipe_schema = RecipeSchema()

    with pytest.raises(ValidationError):
        recipe_schema.load(recipe)
