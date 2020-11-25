from main import ma
from models.Thread import Thread
from schemas.User_Schema import user_schema
from schemas.Post_Schema import posts_schema
from schemas.Category_Schema import categories_schema
from marshmallow import validate, fields

class ThreadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Thread
    
    title = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    status = fields.Integer(required=True, validate=validate.Range(min=0, max=2))
        
    thread_author = ma.Nested(user_schema, only=("user_id", "email", "fname", "lname", "role"))
    categories = ma.Nested(categories_schema, only=("category_id", "name"))

thread_schema = ThreadSchema(dump_only=("time_created",))
threads_schema = ThreadSchema(many=True)