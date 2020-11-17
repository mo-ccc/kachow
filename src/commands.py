import flask
from main import db
import random
import sqlalchemy

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
    from models.User import User
    from main import bcrypt
    
    users = []
    
    for x in range(1, 5):
        new_user = User()
        new_user.username = f"test_user{x}"
        new_user.email = f"test{x}@test.com"
        new_user.fname = "first"
        new_user.lname = "last"
        new_user.role = 2
        new_user.password = bcrypt.generate_password_hash("123456").decode('utf-8')
        db.session.add(new_user)
        users.append(new_user)
    db.session.commit()
    
    for x in range(1, 11):
        new_thread = Thread()
        new_thread.title = f"thread {x}"
        new_thread.author_id = random.choice(users).user_id
        new_thread.category_id = 1
        new_thread.status = random.randint(0, 2)
        new_thread.time_created = sqlalchemy.func.now()
        db.session.add(new_thread)
    db.session.commit()
    print("tables seeded")