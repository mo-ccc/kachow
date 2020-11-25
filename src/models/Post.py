from main import db
from models.Attachment import Attachment
from models.UserPostJoint import tags

class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.thread_id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.String(), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), nullable=False)
    
    attachments = db.relationship('Attachment', backref='attachments')
    mentions = db.relationship('User', secondary=tags, back_populates='mentioned')