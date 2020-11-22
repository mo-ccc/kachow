from main import db

class Mention(db.Model):
    __tablename__ = "mentions"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), nullable=False)
    mentioned_id = db.Column(db.Integer)