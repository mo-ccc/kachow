import flask
from main import db
from models.Thread import Thread
from schemas.Thread_Schema import thread_schema, threads_schema

thread = flask.Blueprint('thread', __name__, url_prefix='/threads')

@thread.route('/', methods=['GET'])
def get_threads():
    all_threads = Thread.query.all()
    output = threads_schema.dump(all_threads)
    return flask.jsonify(output)