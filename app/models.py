from . import db
from datetime import datetime

# Связующая таблица для отношения многие-ко-многим между Detail и Image
detail_image_association = db.Table('detail_image_association',
    db.Column('detail_id', db.Integer, db.ForeignKey('detail.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True)
)


class Facility(db.Model):
    __tablename__ = 'facility'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    preview_image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    preview_image = db.relationship('Image', uselist=False, post_update=True)
    details = db.relationship('Detail', backref='facility', lazy=True)


class Detail(db.Model):
    __tablename__ = 'detail'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    long_description = db.Column(db.Text, nullable=False)
    images = db.relationship('Image', secondary=detail_image_association, back_populates='details')


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    image_type = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    facility = db.relationship('Facility', back_populates='preview_image', uselist=False)
    details = db.relationship('Detail', secondary=detail_image_association, back_populates='images')


# Пример добавления изображения в качестве превью для Facility
def set_facility_preview_image(facility_id, image_url):
    facility = Facility.query.get(facility_id)
    if facility:
        # Создаем новое изображение с типом 'preview'
        preview_image = Image(image_type='preview', image_url=image_url)
        db.session.add(preview_image)
        db.session.commit()

        # Устанавливаем это изображение в качестве превью для Facility
        facility.preview_image = preview_image
        db.session.commit()