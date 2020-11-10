from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
import dotenv

dotenv.load_dotenv()
def init_db(app):
    connection = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
    app.config["SQLALCHEMY_DATABASE_URI"] = connection
        

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    return db