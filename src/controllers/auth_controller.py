import flask
from flask_jwt_extended import create_access_token
from models.User import User
from schemas.User_Schema import UserSchema
from main import db, bcrypt, jwt

auth = flask.Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('login', methods=['POST'])
def login():
    auth_schema = UserSchema(only=("email", "password"))
    fields = auth_schema.load(flask.request.json)
    user = User.query.filter_by(email=fields["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, fields["password"]):
        return flask.abort(400, description='invalid credentials')
    
    access_token = create_access_token(identity=user.user_id)
    return flask.jsonify(access_token), 200