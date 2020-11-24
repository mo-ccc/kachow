import flask
from flask_jwt_extended import create_access_token
from models.User import User
from schemas.User_Schema import UserSchema
from main import db, bcrypt, jwt
import datetime

auth = flask.Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('login', methods=['POST'])
def login():
    # from the UserSchema make an auth schema
    # with only the email and password fields
    auth_schema = UserSchema(only=("email", "password"))
    fields = auth_schema.load(flask.request.json)
    # get the user with the matching email
    user = User.query.filter_by(email=fields["email"]).first()
    # if the user doesn't exist and password doesn't match abort
    if not user or not bcrypt.check_password_hash(user.password, fields["password"]):
        return flask.abort(400, description='invalid credentials')
    
    # return an access token with expiry time of 1 day
    expiry = datetime.timedelta(days=1)
    access_token = create_access_token(identity=user.user_id, 
                                       expires_delta=expiry
                                       )
    return flask.jsonify(access_token)