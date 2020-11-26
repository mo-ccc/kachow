from main import ma
from models.Attachment import Attachment
from marshmallow import validate, fields

class AttachmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attachment
        include_fk = True
    
    post_position = fields.Integer(required=True, validate=validate.Range(min=0, max=2000))
    

attachment_schema = AttachmentSchema(dump_only=('attachment_path',))
attachments_schema = AttachmentSchema(many=True)