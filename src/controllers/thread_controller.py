import flask
from main import db
from models.Thread import Thread
from models.Post import Post
from models.User import User
from models.Category import Category
from schemas.Thread_Schema import thread_schema, threads_schema
from schemas.Post_Schema import post_schema, posts_schema
from services import auth_service
from sqlalchemy import func
import flask_jwt_extended
import json

threads = flask.Blueprint('thread', __name__, url_prefix='/threads')

@threads.route('/', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_threads():
    all_threads = Thread.query.all()
    output = threads_schema.dump(all_threads)
    return flask.jsonify(output)
    
@threads.route('/', methods=['POST'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def create_thread(jwt_user=None):
    response = flask.request.json
    response_categories = response.pop('categories', None)
    data = thread_schema.load(response)

    # create a new thread with parameters
    new_thread = Thread()
    new_thread.author_id = jwt_user.user_id
    new_thread.title = data["title"]
    new_thread.status = data["status"]
    new_thread.time_created = func.now()
    
    # add categories to thread
    categories = []
    for x in response_categories:
        categories.append(Category.query.get(x))
    new_thread.categories = categories
    
    # commit changes
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
@auth_service.verify_user
# jwt_user is passed from the verify_user decorator
def modify_thread(thread_id, jwt_user=None):
    response = flask.request.json
    response_categories = response.pop("categories", None)
    data = thread_schema.load(response)
    thread = Thread.query.filter_by(thread_id=thread_id).first_or_404()
    
    # permissions check
    if jwt_user.user_id != thread.author_id and jwt_user.role > 1:
        return flask.abort(400, description='You do not have permissions to do this')
 
    thread.title = data["title"]
    thread.status = data["status"]
    
    categories = []
    for x in response_categories:
        categories.append(Category.query.get(x))
    thread.categories = categories
    
    db.session.commit()
    return flask.jsonify(thread_schema.dump(thread))
    
@threads.route('/<thread_id>', methods=['DELETE'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def delete_thread(thread_id, jwt_user):
    thread = Thread.query.filter_by(thread_id=thread_id).first_or_404()
    posts_in_thread = Post.query.filter_by(thread_id=thread_id).all()
    if jwt_user.role > 1 or len(posts_in_thread) > 0:
        return flask.abort(400, description='You do not have valid permissions to do this')
    db.session.delete(thread)
    db.session.commit()
    return 'ok'