from main import db

class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, nullable=False)
    thread_id = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True))
    reply_post_id = db.Column(db.Integer)