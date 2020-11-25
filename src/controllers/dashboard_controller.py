from main import db
from models.Thread import Thread
from models.Post import Post
from schemas.Post_Schema import PostSchema
import flask
import flask_jwt_extended
from services import auth_service

dash = flask.Blueprint('dash', __name__)

@dash.route('/dashboard', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_chart():
    open_threads = Thread.query.filter_by(status=0).count()
    closed_threads = Thread.query.filter_by(status=1).count()
    other_threads = Thread.query.filter_by(status=2).count()
    
    return flask.jsonify({
        "open": open_threads,
        "closed": closed_threads,
        "other": other_threads
    })
    
@dash.route('/notifications', methods=['GET'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def get_notifications(jwt_user=None):
    notifications = Post.query.filter(Post.mentions.any(user_id=jwt_user.user_id)).all()
    posts_schema = PostSchema(exclude=("mentions", "attachments", "content", "reply_post_id"), many=True)
    return flask.jsonify(posts_schema.dump(notifications))