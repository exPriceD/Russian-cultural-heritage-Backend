from marshmallow import Schema, fields, validate


class FacilitySchema(Schema):
    editor_key = fields.String(required=True, validate=validate.Length(min=1))
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=True, validate=validate.Length(min=1))
