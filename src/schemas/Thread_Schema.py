from main import ma
from models.Thread import Thread
from schemas.User_Schema import user_schema

class ThreadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Thread
    user = ma.Nested(user_schema, only=("user_id", "email", "fname", "lname"))

thread_schema = ThreadSchema(dump_only=("time_created",))
threads_schema = ThreadSchema(many=True)