from chalice import Chalice
import os

from chalicelib.controllers.jiralice import JiraliceController

app = Chalice(app_name='jiralice')
app.debug = False 

@app.route('/create-ticket', methods=['POST'])
def create_ticket():
    return JiraliceController(app, os.environ).create_ticket()

