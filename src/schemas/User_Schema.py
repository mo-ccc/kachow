from main import ma
from models.User import User
from marshmallow import validate, fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ("password",)
    username = fields.Str(validate=validate.Length(min=3, max=15))
    email = fields.Str(validate=validate.Email())
    fname = fields.Str(validate=validate.Length(max=15))
    lname = fields.Str(validate=validate.Length(max=15))
    role = fields.Integer(validate=validate.Range(min=0, max=3))
    password = fields.Str(validate=validate.Length(min=3, max=50))

user_schema = UserSchema()
users_schema = UserSchema(many=True)