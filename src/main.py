# setup flask
from flask import Flask
app = Flask(__name__)

# register blueprints
from controllers import blueprints
for bp in blueprints:
    app.register_blueprint(bp)

# initialize database
from database import init_db
db = init_db(app)


# test method
def hello_world():
    return "hello_world"