import flask
from main import db
from models.Post import Post
from models.User import User
from schemas.Post_Schema import post_schema, posts_schema
import sqlalchemy
import flask_jwt_extended
from services import auth_service
import json

posts = flask.Blueprint('post', __name__)

def post_put(data, post, author, mentioned, is_post, thread_id=None):
    # content meaning message
    post.content = data["content"]
    
    # checks to see if user_ids are present in mentioned field
    # if true append each actual user to a list 'mentions'
    if mentioned != None:
        mentions = [User.query.get(u) for u in mentioned]
    else:
        mentions = []
    post.mentions = mentions
    
    # if it's a post request set these fields in the database
    if is_post == True:
        post.thread_id = thread_id
        post.author_id = author.user_id
        post.time_created = sqlalchemy.func.now()
    
    db.session.add(post)
    db.session.commit()
    return post

@posts.route('/threads/<thread_id>', methods=['POST'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def create_post(thread_id, jwt_user=None):
    response = flask.request.json
    mentioned = response.pop("mentions", None)
    data = post_schema.load(response)
    
    new_post = Post()
    p = post_put(data, new_post, jwt_user, mentioned, True, thread_id)
    return flask.jsonify(post_schema.dump(p))
    
@posts.route('/posts/<post_id>', methods=['PUT', 'PATCH'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def edit_post(post_id, jwt_user=None):
    response = flask.request.json
    mentioned = response.pop("mentions", None)
    data = post_schema.load(response)
    
    post = Post.query.get(post_id)
    if jwt_user.user_id != post.author_id:
        flask.abort(400, description="you do not own this post")
    
    p = post_put(data, post, jwt_user, mentioned, False)
    return flask.jsonify(post_schema.dump(p))
    
@posts.route('/posts/<post_id>', methods=['DELETE'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def delete_post(post_id, jwt_user=None):
    post = Post.query.get(post_id)
    if jwt_user.user_id != post.author_id:
        flask.abort(400, description="you do not own this post")
    
    for attachment in post.attachments:
        db.session.delete(attachment)
    db.session.delete(post)
    db.session.commit()
    return flask.jsonify(post_schema.dump(post))
