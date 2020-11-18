import flask
from main import db
from models.Attachment import Attachment
from schemas.Attachment_Schema import attachment_schema
from pathlib import Path
import json
import uuid

attachments = flask.Blueprint('attachments', __name__, url_prefix='/attachments')

@attachments.route('/', methods=['POST'])
def create_attachment():
    response = flask.request.form["json"]
    jresponse = json.loads(response)
    
    data = attachment_schema.load(jresponse)
    if 'file' not in flask.request.files:
        return flask.abort(400, description="no file in body")
    file = flask.request.files['file']
    extension = Path(file.filename).suffix
    
    unique_id = uuid.uuid4()
    file_location = f'att_files/{unique_id}{extension}'
    file.save(file_location)
    
    new_attachment = Attachment()
    new_attachment.post_id = data["post_id"]
    new_attachment.attachment_path = f"{unique_id}{extension}"
    new_attachment.post_position = data["post_position"]
    
    db.session.add(new_attachment)
    db.session.commit()
    
    return flask.jsonify(attachment_schema.dump(new_attachment))
    
@attachments.route('/<int:id>', methods=['GET'])
def get_attachment_details(id):
    file = Attachment.query.get(id)
    if not file:
        return flask.abort(400, description="missing file")
    data = attachment_schema.dump(file)
    return flask.jsonify(data)
    
@attachments.route('/media/<string:unique_id>', methods=['GET'])
def get_attachment(unique_id):
    pass