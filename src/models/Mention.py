from main import db

class Mention(db.Model):
    __tablename__ = "mentions"

    post_id = db.Column(db.Integer)
    mentioned_id = db.Column(db.Integer)
    
    from main import db