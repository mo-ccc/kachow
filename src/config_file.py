from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True
    
env = os.getenv("FLASK_DEV")

if env == "development":
    configuration = DevelopmentConfig()
elif env == "testing":
    configuration = TestingConfig()   
else:
    configuration = ProductionConfig()