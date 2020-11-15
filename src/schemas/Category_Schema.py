from main import ma
from models.Category import Category
from marshmallow import validate, fields

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
    name = fields.Str(validate=validate.Length(min=1, max=10))

category_schema = CategorySchema()
category_schema = CategorySchema(many=True)