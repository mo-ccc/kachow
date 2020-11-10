import flask
from main import db
from models.Thread import Thread
from models.Post import Post
from schemas.Thread_Schema import thread_schema, threads_schema
from schemas.Post_Schema import post_schema, posts_schema
from sqlalchemy import func

threads = flask.Blueprint('thread', __name__, url_prefix='/threads')

@threads.route('/', methods=['GET'])
def get_threads():
    all_threads = Thread.query.all()
    output = threads_schema.dump(all_threads)
    return flask.jsonify(output)
    
@threads.route('/', methods=['POST'])
def create_thread():
    response = flask.request.json
    data = thread_schema.load(response)
    new_thread = Thread()
    new_thread.author_id = data["author_id"]
    new_thread.category_id = data["category_id"]
    new_thread.title = data["title"]
    new_thread.status = data["status"]
    new_thread.time_created = func.now()
    db.session.add(new_thread)
    db.session.commit()
    return flask.jsonify(threads_schema.dump(Thread.query.all()))
    
@threads.route('/<thread_id>', methods=['GET'])
def get_thread(thread_id):
    thread_info = Thread.query.filter_by(thread_id=thread_id).first_or_404()
    thread_out = thread_schema.dump(thread_info)
    
    posts = Post.query.filter_by(thread_id=thread_id).all()
    posts_out = posts_schema.dump(posts)
    
    compound_json = flask.jsonify({"thread_info":thread_out, "posts":posts_out})
    return compound_json
    
@threads.route('/<thread_id>', methods=['PUT', 'PATCH'])
def modify_thread(thread_id):
    response = flask.request.json
    data = thread_schema.load(response)
    thread = Thread.query.filter_by(thread_id=thread_id).first_or_404()
 
    thread.title = data["title"]
    thread.status = data["status"]
    thread.category_id = data["category_id"]
    db.session.commit()
    return 'ok'
    
@threads.route('/<thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    thread = Thread.query.filter_by(thread_id=thread_id).first_or_404()
    posts = Post.query.filter_by(thread_id=thread_id).all()
    for p in posts:
        db.session.delete(p)
    db.session.delete(thread)
    db.session.commit()
    return 'ok'