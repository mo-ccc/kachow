# initialize database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# initialize marshmallow
from flask_marshmallow import Marshmallow
ma = Marshmallow()

def create_app():
    # setup flask
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object('config_file.configuration')

    # initialize app using globals
    db.init_app(app)
    ma.init_app(app)

    # register blueprints
    from controllers import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)
        
    import commands
    app.register_blueprint(commands.command_db)
    
    return app

# test method
def hello_world():
    return "hello_world"