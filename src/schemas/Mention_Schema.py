from main import ma
from models.Mention import Mention

class MentionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mention

mention_schema = MentionSchema()
mentions_schema = MentionSchema(many=True)