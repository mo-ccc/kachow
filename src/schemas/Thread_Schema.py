from main import ma
from models.Thread import Thread

class ThreadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Thread

thread_schema = ThreadSchema(dump_only=("author_id", "time_created"))
threads_schema = ThreadSchema(many=True)