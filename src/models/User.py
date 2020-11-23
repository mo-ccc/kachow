from main import db
from models.UserPostJoint import tags

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    fname = db.Column(db.String(), nullable=False)
    lname = db.Column(db.String(), nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)
    password = db.Column(db.String(), nullable=False)
    
    threads = db.relationship('Thread', backref='thread_author')
    posts = db.relationship('Post', backref='post_author')
    mentioned = db.relationship('Post', secondary=tags, back_populates='mentions')