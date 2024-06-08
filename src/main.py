from flask import json
from flasgger import Swagger
from werkzeug.exceptions import default_exceptions

from src.app import app
from src.view_users import user_bp
from src.view_medias import medias_bp
from src.view_tweets import tweets_bp
from src.exceptions import UnicornException

app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(medias_bp, url_prefix="/api/medias")
app.register_blueprint(tweets_bp, url_prefix="/api/tweets")
swagger = Swagger(app, template_file='openapi.json')

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
