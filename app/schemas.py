from marshmallow import Schema, fields


class IngredientSchema(Schema):
    unit = fields.String(required=True)
    name = fields.String(required=True)


class InstructionSchema(Schema):
    step = fields.Integer(required=True)
    description = fields.String(required=True)


class RecipeSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    ingredients = fields.List(fields.Nested(IngredientSchema), required=True)
    instructions = fields.List(fields.String(), required=True)