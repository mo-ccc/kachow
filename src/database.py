from flask_sqlalchemy import SQLAlchemy
import os
import dotenv

dotenv.load_dotenv()
def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASS')}@"
        f"{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    return db