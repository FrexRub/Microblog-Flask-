from flask import json, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from werkzeug.exceptions import default_exceptions

from src.app import app, db
from src.utils import add_data_to_db
from src.view_users import user_bp
from src.view_medias import medias_bp
from src.view_tweets import tweets_bp
from src.exceptions import UnicornException

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    # "specs_route": "/apidocs/",
    "specs_route": "/api/docs/",
}

app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(medias_bp, url_prefix="/api/medias")
app.register_blueprint(tweets_bp, url_prefix="/api/tweets")

app.json_encoder = LazyJSONEncoder
template = dict(swaggerUiPrefix=LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')))

swagger = Swagger(app, template=template, config=swagger_config, template_file='openapi.json')

# swagger = Swagger(app, template=template, template_file='openapi.json')

# swagger = Swagger(app, template_file='openapi.json')

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


@app.before_request
def create_bd():
    db.create_all()
    add_data_to_db()


app.register_error_handler(418, handle_exception_418)

if __name__ == "__main__":
    app.run(debug=True)
