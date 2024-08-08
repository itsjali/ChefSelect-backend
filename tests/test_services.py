from app.services import create_recipe_service


def test_create_recipe_service_success(test_client, init_database,):
    valid_recipe_data = {
        "title": "Chicken Curry",
        "description": "Delicious chicken curry with rice",
        "ingredients": [
            {"unit": "100g", "name": "Chicken"},
            {"unit": "200g", "name": "Rice"}
        ],
        "instructions": [
            "Cook the rice",
            "Cook the chicken and add curry"
        ]
    }
    with test_client.application.app_context():
        recipe = create_recipe_service(valid_recipe_data)
        
        # Check that recipe object
        assert recipe.title == valid_recipe_data["title"]
        assert recipe.description == valid_recipe_data["description"]

        # Check that ingredients object
        assert len(recipe.ingredients) == 2
        for i, ingredient in enumerate(recipe.ingredients):
            assert ingredient.unit == valid_recipe_data["ingredients"][i]["unit"]
            assert ingredient.name == valid_recipe_data["ingredients"][i]["name"]

        # Check that instructions object
        assert len(recipe.instructions) == 2
        for i, instruction in enumerate(recipe.instructions):
            assert instruction.step == i + 1
            assert instruction.description == valid_recipe_data["instructions"][i]
