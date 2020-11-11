from main import ma
from models.Mention import Mention

class MentionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mention

Mention_schema = MentionSchema()
Mentions_schema = MentionSchema(many=True)