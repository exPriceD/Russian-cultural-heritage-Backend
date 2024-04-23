from marshmallow import Schema, fields, validate


class FacilitySchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=True, validate=validate.Length(min=1))
