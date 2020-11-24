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
    from models.User import User
    from main import bcrypt
    
    users = []
    
    # create account for deleted users
    db.session.add(User(username='deleteduser', email='deleteduser@kachow.com',
        fname='deleted', lname='user', role=3,
        password=bcrypt.generate_password_hash('l9@2u84$2#').decode('utf-8')))

    # create account for admin
    db.session.add(User(username='admin', email='admin@kachow.com', 
        fname='admin', lname='admin', role=0, 
        password=bcrypt.generate_password_hash("admin").decode('utf-8')))
    
    # generate random accounts
    for x in range(1, 5):
        new_user = User()
        new_user.username = f"test_user{x}"
        new_user.email = f"test{x}@test.com"
        new_user.fname = "first"
        new_user.lname = "last"
        new_user.role = random.randint(1, 2)
        new_user.password = bcrypt.generate_password_hash("123456").decode('utf-8')
        db.session.add(new_user)
        users.append(new_user)
    db.session.commit()
    
    from models.Category import Category
    categories = []
    # generate 2 categories
    for x in range(1, 3):
        new_category = Category(name=f"category: {x}")
        db.session.add(new_category)
        categories.append(new_category)
    db.session.commit()
    
    from models.Thread import Thread
    threads = []
    # generate threads
    for x in range(1, 11):
        new_thread = Thread()
        new_thread.title = f"thread {x}"
        new_thread.author_id = random.choice(users).user_id
        new_thread.status = random.randint(0, 2)
        new_thread.time_created = sqlalchemy.func.now()
        new_thread.categories = categories
        db.session.add(new_thread)
        if x > 1:
            threads.append(new_thread)
    db.session.commit()
    
    from models.Post import Post
    posts = []
    # posts required for unittest
    db.session.add(Post(thread_id=1, author_id=4, 
        content="change me", mentions=[], time_created=sqlalchemy.func.now())
    )
    db.session.add(Post(thread_id=1, author_id=4, 
        content="delete me", mentions=[], time_created=sqlalchemy.func.now())
    )
    # randomise posts
    for x in range(1, 30):
        new_post = Post()
        t_id = threads[x%9].thread_id
        new_post.thread_id = t_id
        new_post.author_id = random.choice(users).user_id
        new_post.content = f"post {x} in thread: {t_id}"
        new_post.mentions = users
        new_post.time_created = sqlalchemy.func.now()
        db.session.add(new_post)
        posts.append(new_post)
    db.session.commit()
    
    from models.Attachment import Attachment
    # create random attachments
    # does not add images
    for x in range(1, 30):
        new_attachment = Attachment()
        new_attachment.post_id = random.choice(posts).post_id
        new_attachment.attachment_path = f"{x}"
        new_attachment.post_position = 1
        db.session.add(new_attachment)
    db.session.commit()
    
    print("tables seeded")