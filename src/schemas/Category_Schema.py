from main import ma
from models.Category import Category

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category

category_schema = CategorySchema()
category_schema = CategorySchema(many=True)