from main import ma
from models.Attachment import Attachment
import marshmallow

class AttachmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attachment
        include_relationships = True
        include_fk = True
    content = marshmallow.fields.String()
    

attachment_schema = AttachmentSchema(dump_only=('attachment_path',))
attachments_schema = AttachmentSchema(many=True)