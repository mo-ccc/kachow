import flask
from main import db
from models.Post import Post
from models.User import User
from schemas.Post_Schema import post_schema, posts_schema
from sqlalchemy import func
import flask_jwt_extended
from services import auth_service
import json

posts = flask.Blueprint('post', __name__)

@posts.route('/threads/<thread_id>', methods=['POST'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def create_post(thread_id, jwt_user=None):
    response = flask.request.json
    data = post_schema.load(response)
    
    new_post = Post()
    new_post.thread_id = thread_id
    new_post.author_id = jwt_user.user_id
    new_post.content = data["content"]
    new_post.time_created = func.now()
    if "reply_post_id" in data:
        new_post.reply_post_id = data["reply_post_id"]
    
    db.session.add(new_post)
    db.session.commit()
    return flask.jsonify(post_schema.dump(new_post))
    