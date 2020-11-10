from main import db

class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    content = db.Column(db.String())
    time_created = db.Column(db.DateTime(timezone=True))
    reply_post_id = db.Column(db.Integer)