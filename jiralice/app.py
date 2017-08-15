from chalice import Chalice
import os

from chalicelib.controllers.jiralice import JiraliceController

app = Chalice(app_name='jiralice')
app.debug = True


@app.route('/')
def index():
    return {'s': os.environ['JIRA_URL']} 
    return {"hello": "Word"}

@app.route('/create-ticket', methods=['POST'])
def create_ticket():
    try:
        return JiraliceController(app, os.environ).create_ticket()
    except Exception as e:
        return {"No": "yes"}

