from . import db


class Facility(db.Model):
    __tablename__ = 'facility'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(65536), nullable=False)
    date_posted = db.Column(db.String(128))


class Images(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    is_preview = db.Column(db.Boolean, default=True, nullable=False)
    image_url = db.Column(db.String(512), nullable=False)


class Models(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    model_url = db.Column(db.String(512), nullable=False)


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(256), nullable=False)
    image_url = db.Column(db.String(512), nullable=False)
