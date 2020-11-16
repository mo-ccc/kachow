from main import ma
from models.User import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ("password",)

user_schema = UserSchema()
users_schema = UserSchema(many=True)