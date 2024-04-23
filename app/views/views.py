from flask import Response, Blueprint, request
from app.models import Facility, Images, Models
from app.utils import get_current_time, allowed_file
from app.schemas import FacilitySchema
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from app import db
import json

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/facility', methods=['GET'])
def get_facility():
    facility = Facility.query.all()
    facility_list = [
        {
            "id": facility.id,
            "title": facility.title,
            "description": facility.description,
            "date_posted": facility.date_posted
        }
        for facility in facility
    ]

    response = {
        "status": 200,
        "facility": facility_list
    }
    return Response(response=json.dumps(response, ensure_ascii=False), status=200, mimetype='application/json')


@api.route('/facility/<int:id>', methods=['GET'])
def get_facility_by_id(facility_id: int):
    facility = Facility.query.filter_by(id=facility_id).first()

    if facility is None:
        response = {"status": 404, "message": "No such facility"}
        return Response(response=json.dumps(response, ensure_ascii=False), status=404, mimetype='application/json')

    images = Images.query.filter_by(facility_id=facility_id).all()
    model = Models.query.filter_by(facility_id=facility_id).first()

    facility_images = [image.image_url for image in images]

    response = {
        "status": 200,
        "facility": {
            "id": facility.id,
            "title": facility.title,
            "description": facility.description,
            "date_posted": facility.date_posted,
            "model": model.model_url,
            "images": facility_images
        }
    }
    return Response(response=json.dumps(response, ensure_ascii=False), status=200, mimetype='application/json')


@api.route('/facility', methods=['POST'])
def upload_files():
    schema = FacilitySchema()
    try:
        data = schema.load(request.form)
    except ValidationError as err:
        response = {"status": 400, "text": err.messages}
        return Response(response=json.dumps(response, ensure_ascii=False), status=400, mimetype='application/json')

    facility_name = data.get('title')
    description = data.get('description')

    uploaded_images = request.files.getlist('images')
    uploaded_model = request.files.get('model')

    if not uploaded_images or not all(allowed_file(image.filename) for image in uploaded_images):
        response = {
            "status": 400,
            "text": "At least one image is required. All files must be images with extensions: png, jpg, jpeg, gif, bmp"
        }
        return Response(response=json.dumps(response, ensure_ascii=False), status=400, mimetype='application/json')

    if not uploaded_model or not uploaded_model.filename.lower().endswith('.glb'):
        response = {"status": 400, "text": "A valid .glb model file is required"}
        return Response(response=json.dumps(response, ensure_ascii=False), status=400, mimetype='application/json')

    date_now = get_current_time()

    new_facility = Facility(name=facility_name, description=description, date_posted=date_now)

    db.session.add(new_facility)
    db.session.commit()

    new_facility_id = new_facility.id

    for image in uploaded_images:
        image_filename = secure_filename(image.filename)
        image_url = f'static/facility/images/{image_filename}'
        image.save(image_url)
        new_image = Images(facility_id=new_facility_id, image_url=image_url, is_preview=False)
        db.session.add(new_image)
        db.session.commit()

    model_filename = secure_filename(uploaded_model.filename)
    model_url = f'static/facility/models/{model_filename}'
    uploaded_model.save(model_url)

    new_model = Models(facility_id=new_facility_id, model_url=model_url)

    db.session.add(new_model)
    db.session.commit()

    response = {"status": 200, "text": "Facility created successfully"}
    return Response(response=json.dumps(response, ensure_ascii=False), status=200, mimetype='application/json')
