from app.models import db, Recipe, Ingredient, Instruction


def create_recipe_service(validated_data):
    recipe = Recipe(
        title=validated_data["title"],
        description=validated_data["description"],
    )

    db.session.add(recipe)
    db.session.flush()

    for ingredient_data in validated_data["ingredients"]:
        ingredient = Ingredient(
            unit=ingredient_data["unit"],
            name=ingredient_data["name"],
            recipe_id=recipe.id,
        )
        
        db.session.add(ingredient)

    for step_number, instruction_data in enumerate(validated_data["instructions"], start=1):
        instruction = Instruction(
            step=step_number,
            description=instruction_data,
            recipe_id=recipe.id,
        )
        
        db.session.add(instruction)

    db.session.commit()

    return recipe
