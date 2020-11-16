import flask
from main import db
import random

command_db = flask.Blueprint('db', __name__)

@command_db.cli.command('create')
def create_db():
    db.create_all()
    print("tables created")
    
@command_db.cli.command('drop')
def drop_db():
    db.drop_all()
    print("tables dropped")
    
@command_db.cli.command('seed')
def seed_db():
    from models.Thread import Thread
    from models.Post import Post
    
    for x in range(1, 11):
        new_thread = Thread()
        new_thread.title = f"thread {x}"
        new_thread.status = random.randint(0, 2)
        db.session.add(new_thread)
    db.session.commit()