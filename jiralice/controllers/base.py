import os

from models.schema_filter import Validator


class BaseController(object):

    def __init__(self, app, env_vars):
        self.app = app
        self.user = False
        self.request = app.current_request
        self.json_params = self.request.json_body
        self.resource_path = self.request.context['resourcePath']
        self.method = self.request.method
        self.current_path = self.request.to_dict()
        self.sanitized_params = self.get_sanitized_params()
        self.env_vars = env_vars
        #self.region = os.environ['AWS_REGION']


    def get_sanitized_params(self):
        if self.method == 'POST':
            validator = Validator(self.resource_path, self.json_params)
            return validator.sanitize_params()
        return {}
