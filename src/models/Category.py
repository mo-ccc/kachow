from main import db
from models.CategoryThreadJoint import association_table

class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    
    threads = db.relationship("Thread", secondary=association_table, back_populates='categories')