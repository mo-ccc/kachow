from main import ma
from models.Post import Post
from schemas.User_Schema import user_schema, users_schema
from schemas.Attachment_Schema import attachments_schema

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True
    post_author = ma.Nested(user_schema, only=("user_id", "email", "fname", "lname", "role"))
    attachments = ma.Nested(attachments_schema)
    mentions = ma.Nested(users_schema)

post_schema = PostSchema(dump_only=("time_created", "thread_id", "author_id"))
posts_schema = PostSchema(many=True)