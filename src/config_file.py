from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.getenv("DB_URI")
        if not value:
            raise ValueError("no DB_URI environnment variable")
        return value
    
    @property
    def JWT_SECRET_KEY(self):
        value = os.getenv("SECRET_KEY")
        if not value:
            raise ValueError("no SECRET_KEY environnment variable")
        return value
    
    @property
    def AWS_S3_BUCKET(self):
        value = os.getenv("AWS_S3_BUCKET")
        if not value:
            raise ValueError("no AWS_S3_BUCKET environnment variable")
        return value
    
    # 10 megabytes
    MAX_CONTENT_LENGTH = 10*1024*1024

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