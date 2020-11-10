# setup flask
from flask import Flask
app = Flask(__name__)

# initialize database
from database import init_db
db = init_db(app)

# initialize marshmallow
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

# register blueprints
from controllers import blueprints
for bp in blueprints:
    app.register_blueprint(bp)

# test method
def hello_world():
    return "hello_world"