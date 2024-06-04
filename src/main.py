from flask import json
from flasgger import Swagger
from werkzeug.exceptions import default_exceptions

from app import app
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


if __name__ == "__main__":
    app.run(debug=True)
