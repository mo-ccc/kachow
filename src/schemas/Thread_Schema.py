from main import ma
from models.Thread import Thread

class ThreadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Thread

thread_schema = ThreadSchema()
threads_schema = ThreadSchema(many=True)