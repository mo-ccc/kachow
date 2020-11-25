from main import ma
from models.Category import Category
from marshmallow import validate, fields

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
    name = fields.Str(validate=validate.Length(min=1, max=30))

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)