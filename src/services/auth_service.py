import inspect
import flask_jwt_extended
from models.User import User

def verify_user(func):
    def wrapper(*args, **kwargs):
        jwt_id = flask_jwt_extended.get_jwt_identity()
        user = User.query.filter_by(user_id=jwt_id).first()
        if not user:
            return flask.abort(400, description='Not a valid user')
        kwargs['jwt_user'] = user
        return func(*args, **kwargs)
    wrapper.__name__=func.__name__
    return wrapper