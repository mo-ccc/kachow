import flask
from main import db
from models.Thread import Thread
from models.Post import Post
from models.User import User
from schemas.Thread_Schema import thread_schema, threads_schema
from schemas.Post_Schema import post_schema, posts_schema
from sqlalchemy import func
import flask_jwt_extended

threads = flask.Blueprint('thread', __name__, url_prefix='/threads')

@threads.route('/', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_threads():
    all_threads = Thread.query.all()
    output = threads_schema.dump(all_threads)
    return flask.jsonify(output)
    
@threads.route('/', methods=['POST'])
@flask_jwt_extended.jwt_required
def create_thread():
    response = flask.request.json
    data = thread_schema.load(response)
    
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.filter_by(user_id=jwt_id).first()
    if not user:
        return flask.abort(400, description='Not a valid user')
    # create a new thread with parameters
    new_thread = Thread()
    new_thread.author_id = user.user_id
    new_thread.category_id = data["category_id"]
    new_thread.title = data["title"]
    new_thread.status = data["status"]
    new_thread.time_created = func.now()
    db.session.add(new_thread)
    db.session.commit()
    return flask.jsonify(thread_schema.dump(new_thread))
    
@threads.route('/<thread_id>', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_thread(thread_id):
    thread_info = Thread.query.filter_by(thread_id=thread_id).first_or_404()
    thread_out = thread_schema.dump(thread_info)
    
    posts = Post.query.filter_by(thread_id=thread_id).all()
    posts_out = posts_schema.dump(posts)
    
    # combine thread info and posts into one json
    compound_json = flask.jsonify({"thread_info":thread_out, "posts":posts_out})
    return compound_json
    
@threads.route('/<thread_id>', methods=['PUT', 'PATCH'])
@flask_jwt_extended.jwt_required
def modify_thread(thread_id):
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.filter_by(user_id=jwt_id)
    if not user:
        return flask.abort(400, description='Not a valid user')
        
    response = flask.request.json
    data = thread_schema.load(response)
    thread = Thread.query.filter_by(thread_id=thread_id).first_or_404()
    
    # permissions check
    if user.id != thread.author_id or user.role > 1:
        return flask.abort(400, description='You do not have permissions to do this')
 
    thread.title = data["title"]
    thread.status = data["status"]
    thread.category_id = data["category_id"]
    db.session.commit()
    return 'ok'
    
@threads.route('/<thread_id>', methods=['DELETE'])
@flask_jwt_extended.jwt_required
def delete_thread(thread_id):
    thread = Thread.query.filter_by(thread_id=thread_id).first_or_404()
    posts = Post.query.filter_by(thread_id=thread_id).all()
    for p in posts:
        db.session.delete(p)
    db.session.delete(thread)
    db.session.commit()
    return 'ok'