import flask
from main import db, bcrypt
from models.User import User
from schemas.User_Schema import user_schema, users_schema

users = flask.Blueprint('users', __name__, url_prefix="/users")

@users.route('/', methods=['GET'])
def get_users():
    all_users = User.query.all()
    output = users_schema.dump(all_users)
    return flask.jsonify(output)
    
@users.route('/', methods=['POST'])
def create_user():
    response = flask.request.json
    data = user_schema.load(response)
    new_user = User()
    new_user.username = data["username"]
    new_user.email = data["email"]
    new_user.fname = data["fname"]
    new_user.lname = data["lname"]
    new_user.role = data["role"]
    new_user.password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    db.session.add(new_user)
    db.session.commit()
    return flask.jsonify(user_schema.dump(new_user))
    
@users.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(user_id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return flask.jsonify(user_schema.dump(user))
    