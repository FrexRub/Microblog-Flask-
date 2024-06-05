from flask import json, jsonify
from flasgger import Swagger
from flasgger import swag_from
from werkzeug.exceptions import default_exceptions

from app import app
from config import BASE_DIR
from view_users import router as router_user
from exceptions import UnicornException

app.register_blueprint(router_user, url_prefix="/api/users")
swagger = Swagger(app)

default_exceptions[418] = UnicornException


@app.errorhandler(418)
def handle_exception_418(e):
    response = e.get_response()
    response.data = json.dumps({
        "result": False,
        "error_type": e.error_type,
        "error_message": e.error_message,
    })
    response.content_type = "application/json"
    return response


app.register_error_handler(418, handle_exception_418)


@app.route('/colors/<palette>/')
# @swag_from('swagger/users.yml', validation=False)
def colors(palette):
    all_colors = {
        'cmyk': ['cyan', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
