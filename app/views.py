from flask import jsonify, Response, Blueprint
from .models import Facility, Images, Models
from . import db
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
