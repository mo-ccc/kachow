# setup flask
from flask import Flask
app = Flask(__name__)

# initialize database
from database import init_db
db = db_init(app)


# test method
def hello_world():
    return "hello_world"