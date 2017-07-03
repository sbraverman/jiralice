from chalice import Chalice

from controllers.jiralice import JiraliceController

app = Chalice(app_name='jiralice')
app.debug = True


@app.route('/')
def index():
    return app.current_request.stage_vars 
    return {"hello": "Word"}

@app.route('/create-ticket', methods=['POST'], api_key_required=True)
def create_ticket():
    return JiraliceController(app).create_ticket()

