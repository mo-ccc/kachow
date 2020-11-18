import flask
from main import db
from models.Attachment import Attachment
from schemas.Attachment_Schema import attachment_schema
from pathlib import Path
import json
import uuid

attachments = flask.Blueprint('attachments', __name__)

@attachments.route('/attachments', methods=['POST'])
def create_attachment():
    response = flask.request.form["json"]
    jresponse = json.loads(response)
    
    data = attachment_schema.load(jresponse)
    if 'file' not in flask.request.files:
        return flask.abort(400, description="missing file")
    file = flask.request.files['file']
    extension = Path(file.filename).suffix
    
    unique_id = uuid.uuid4()
    file_location = f'att_files/{unique_id}{extension}'
    file.save(file_location)
    
    new_attachment = Attachment()
    new_attachment.post_id = data["post_id"]
    new_attachment.attachment_path = file_location
    new_attachment.post_position = data["post_position"]
    
    return flask.jsonify(attachment_schema.dump(new_attachment))
    