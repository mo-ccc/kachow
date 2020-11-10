from main import ma
from models.Post import Post

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post

post_schema = PostSchema()
posts_schema = PostSchema(many=True)