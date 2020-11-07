from main import db

class Thread(db.Model):
    __tablename__ = "attachments"

    attachment_path = db.Column(db.String(), unique=True)
    post_id = db.Column(db.Integer)
    post_position = db.Column(db.Integer)