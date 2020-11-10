import flask
from main import db
from models.Thread import Thread
from schemas.Thread_Schema import thread_schema, threads_schema
from sqlalchemy import func

thread = flask.Blueprint('thread', __name__, url_prefix='/threads')

@thread.route('/', methods=['GET'])
def get_threads():
    all_threads = Thread.query.all()
    output = threads_schema.dump(all_threads)
    return flask.jsonify(output)
    
@thread.route('/', methods=['POST'])
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
    