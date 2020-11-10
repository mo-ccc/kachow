import flask
from main import db
from models.Post import Post
from schemas.Post_Schema import post_schema, posts_schema
from sqlalchemy import func
import json

posts = flask.Blueprint('post', __name__)

@posts.route('/threads/<thread_id>', methods=['POST'])
def create_post(thread_id):
    response = flask.request.json
    print(response)
    data = post_schema.load(response)
    
    new_post = Post()
    new_post.thread_id = thread_id
    new_post.author_id = data["author_id"]
    new_post.content = data["content"]
    new_post.time_created = func.now()
    new_post.reply_post_id = data["reply_post_id"]
    
    db.session.add(new_post)
    db.session.commit()
    return 'ok'
    