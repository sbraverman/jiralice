from chalice import BadRequestError, ChaliceViewError
from marshmallow import Schema, fields

class Schemas:
    class CreateTicket(Schema):
        messages = fields.Str(required=True)

    """
    class LoginSchema(Schema):
        email = fields.Email(required=True)
        password = fields.Str(required=True)

    class RegisterSchema(LoginSchema):
        first_name = fields.Str(required=True)
        last_name = fields.Str(required=True)
        birthday = fields.Date(required=True)

    class RegisteredSchema(Schema):
        user_token = fields.Str(required=True)

    class PinNumberSchema(RegisteredSchema):
        pn = fields.Integer(required=True)

    class StartEventSchema(PinNumberSchema):
        drink_level = fields.Integer(required=True)

    class LevelEventSchema(RegisteredSchema):
        confirm_level = fields.Str(required=True)

    class TestAwkSchema(Schema):
        pass

    class EndEventSchema(RegisteredSchema):
        pass

    class AlertSchema(RegisteredSchema):
        pass

    class ViewEventsSchema(Schema):
        pass

    class ValidateUserSchema(RegisteredSchema):
        verification_token = fields.Str(required=True)
    """

class Validator(object):

    def __init__(self, class_name, parameters):
        self.class_name = class_name
        self.parameters = parameters

    def sanitize_params(self):
        title_class = self.class_name.title().replace('/', '').replace('-', '')
        full_class = '{0}Schema'.format(title_class)
        try:
            schema_class = getattr(Schemas, full_class)()
        except Exception as e:
            raise ChaliceViewError(e)
        sanitized_params = schema_class.load(self.parameters)
        if sanitized_params.errors:
            raise BadRequestError(sanitized_params.errors)
        return sanitized_params.data
