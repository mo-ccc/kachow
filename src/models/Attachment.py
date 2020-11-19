from main import db

class Attachment(db.Model):
    __tablename__ = "attachments"
    
    attachment_id = db.Column(db.Integer, primary_key=True)
    attachment_path = db.Column(db.String(), unique=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), nullable=False)
    post_position = db.Column(db.Integer, nullable=False)