from chalice import BadRequestError, ChaliceViewError
from marshmallow import Schema, fields

class Schemas:
    class CreateTicketSchema(Schema):
        pass


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
