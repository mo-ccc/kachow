import flask

thread = flask.Blueprint('thread', __name__, url_prefix='/threads')

@thread.route('/', methods=['GET'])
def get_threads():
    return 'got'