import os
import sys
from sys import exit

class BaseController(object):

    def __init__(self, app):
        self.app = app
        self.user = False
        self.request = app.current_request
        self.json_params = self.request.json_body
        #self.resource_path = self.request.context['resource-path']
        self.method = self.request.method
        self.current_path = self.request.to_dict()
        #self.region = os.environ['AWS_REGION']

