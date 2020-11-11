from main import ma
from models.User import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

User_schema = UserSchema()
Users_schema = UserSchema(many=True)