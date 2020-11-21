from main import db
import flask_sqlalchemy
from models.CategoryThreadJoint import association_table
from models.Category import Category

class Thread(db.Model):
    __tablename__ = "threads"

    thread_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), nullable=False)
    
    posts = db.relationship('Post', backref='posts')
    categories = db.relationship('Category', secondary=association_table, back_populates='threads')
    
    def __repr__(self):
        return f"<Thread {self.thread_id}, {self.title}"