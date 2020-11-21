from main import ma
from models.Thread import Thread
from schemas.User_Schema import user_schema
from schemas.Post_Schema import posts_schema
from schemas.Category_Schema import categories_schema

class ThreadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Thread
    thread_author = ma.Nested(user_schema, only=("user_id", "email", "fname", "lname", "role"))
    categories = ma.Nested(categories_schema, only=("category_id", "name"))

thread_schema = ThreadSchema(dump_only=("time_created",))
threads_schema = ThreadSchema(many=True)