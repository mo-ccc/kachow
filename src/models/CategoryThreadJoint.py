from main import db
import flask_sqlalchemy

association_table = db.Table('association',
    db.Column('thread_id', db.Integer, db.ForeignKey('threads.thread_id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id'))
)