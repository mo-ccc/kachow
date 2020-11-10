from main import db
import flask_sqlalchemy

class Thread(db.Model):
    __tablename__ = "threads"

    thread_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    title = db.Column(db.String(150))
    status = db.Column(db.Integer)
    time_created = db.Column(db.DateTime(timezone=True))
    category_id = db.Column(db.Integer)