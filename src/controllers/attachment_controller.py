import flask
from main import db
from models.Attachment import Attachment
from models.Post import Post
from models.User import User
from schemas.Attachment_Schema import attachment_schema
import flask_jwt_extended
from services import auth_service
from pathlib import Path
import json
import os
import uuid
import boto3

attachments = flask.Blueprint('attachments', __name__, url_prefix='/attachments')

@attachments.route('/', methods=['POST'])
@flask_jwt_extended.jwt_required
@auth_service.verify_user
def create_attachment(jwt_user):
    response = flask.request.form["json"]
    jresponse = json.loads(response)
    
    data = attachment_schema.load(jresponse)
    if 'file' not in flask.request.files:
        return flask.abort(400, description="no file in body")
    file = flask.request.files['file']
    extension = Path(file.filename).suffix
    post = Post.query.get(data["post_id"])
    if post.author_id != jwt_user.user_id:
        return flask.abort(400, description="you do not own this post")
    
    unique_id = uuid.uuid4()
    file_location = f'attachments/{unique_id}{extension}'
    s3 = boto3.client('s3')
    
    s3.upload_fileobj(file, flask.current_app.config["AWS_S3_BUCKET"], file_location)
    
    new_attachment = Attachment()
    new_attachment.post_id = data["post_id"]
    new_attachment.attachment_path = f"{unique_id}{extension}"
    new_attachment.post_position = data["post_position"]
    
    db.session.add(new_attachment)
    db.session.commit()
    
    return flask.jsonify(attachment_schema.dump(new_attachment))
    
@attachments.route('/<int:id>', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_attachment_details(id):
    file = Attachment.query.get(id)
    if not file:
        return flask.abort(404)
    data = attachment_schema.dump(file)
    return flask.jsonify(data)
    
@attachments.route('/media/<string:unique_id>', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_attachment(unique_id):
    s3 = boto3.client('s3').Bucket(flask.current_app.config["AWS_S3_BUCKET"])
    file = f"attachments/{unique_id}"
    file_obj = s3.Object(file).get()
    
    return Response(
        file_obj['Body'].read(),
        mimetype='image/png',
        headers={"Content-Disposition": f"attachment;filename={unique_id}"}
    )
    