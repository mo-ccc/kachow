import flask
from main import db

tags = db.Table('tags',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.post_id'))
)