from . import db
from datetime import datetime


class Facility(db.Model):
    __tablename__ = 'facility'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(65536), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)


class Images(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    image_type = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)


class Models(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    model_url = db.Column(db.String(300), nullable=False)
