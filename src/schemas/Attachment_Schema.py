from main import ma
from models.Attachment import Attachment

class AttachmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attachment

Attachment_schema = AttachmentSchema()
Attachments_schema = AttachmentSchema(many=True)