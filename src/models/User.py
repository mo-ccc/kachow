from main import db

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    fname = db.Column(db.String())
    lname = db.Column(db.String())
    role = db.Column(db.SmallInteger)
    pfp = db.Column(db.String())
    enc_pass = db.Column(db.String())
    