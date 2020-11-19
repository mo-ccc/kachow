from main import ma
from models.Thread import Thread
from schemas.User_Schema import user_schema
from schemas.Post_Schema import posts_schema

class ThreadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Thread
    thread_author = ma.Nested(user_schema, only=("user_id", "email", "fname", "lname", "role"))

thread_schema = ThreadSchema(dump_only=("time_created",))
threads_schema = ThreadSchema(many=True)