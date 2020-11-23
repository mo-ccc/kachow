import flask
from main import db, bcrypt
from models.User import User
from models.Thread import Thread
from models.Post import Post
from schemas.User_Schema import user_schema, users_schema, UserSchema
import flask_jwt_extended
from services import auth_service

users = flask.Blueprint('users', __name__, url_prefix="/users")

def post_put(user, data, is_permitted=False):
    user.username = data["username"]
    user.email = data["email"]
    user.fname = data["fname"]
    user.lname = data["lname"]
    if is_permitted:
        user.role = data["role"]
    user.password = bcrypt.\
    generate_password_hash(data["password"]).decode('utf-8')
    db.session.add(new_user)
    db.session.commit()
    return flask.jsonify(user_schema.dump(user))
    

@users.route('/', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_users():
    all_users = User.query.all()
    output = users_schema.dump(all_users)
    return flask.jsonify(output)
    
@users.route('/', methods=['POST'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def create_user(jwt_user=None):
    response = flask.request.json
    data = user_schema.load(response)
    if jwt_user.role > 1:
        return flask.abort(400, description='You do not have permission to do that')
    new_user = User()
    post_put(new_user, data, is_permitted=True)
    
@users.route('/<int:id>', methods=['DELETE'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def delete_user(id, jwt_user=None):
    if jwt_user.role > 1:
        return flask.abort(400, description='You do not have permission to do that')
    if jwt_user.user_id == id:
        return flask.abort(400, description='You cannot delete your own account')
        
    user = User.query.filter_by(user_id=id).first_or_404()
    
    if jwt_user.role >= user.role:
        return flask.abort(400, description='You must be higher role than user')
    
    owned_threads = Thread.query.filter_by(author_id=user.user_id)
    owned_threads.update({'author_id':1})
    owned_posts = Post.query.filter_by(author_id=user.user_id)
    owned_posts.update({'author_id':1})
    db.session.delete(user)
    db.session.commit()
    return flask.jsonify(user_schema.dump(user))
    
@users.route('/<int:id>', methods=['PUT', 'PATCH'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def edit_user(id, jwt_user=None):
    if jwt_user.role > 0 and jwt_user.user_id != id:
        return flask.abort(400, description='You do not have permission to do that')
    user = User.query.filter_by(user_id=id).first_or_404()
    
    response = flask.request.json
    exclude_schema = UserSchema(exclude=("role",))
    
    if jwt_user.user_id != id:
        # if jwt_user is an admin allow edit of role
        return post_put(user, user_schema.load(response), is_permitted=True)
    else:
        # else exclude role from schema
        return post_put(user, exclude_schema.load(response), is_permitted=False)
    
    return flask.jsonify(user_schema.dump(user))
    