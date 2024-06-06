from flask import json, jsonify, make_response
from flasgger import Swagger
from flasgger import swag_from
from werkzeug.exceptions import default_exceptions

from app import app
from config import BASE_DIR
from view_users import user_bp
from view_medias import medias_bp
from view_tweets import tweets_bp
from exceptions import UnicornException

app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(medias_bp, url_prefix="/api/medias")
app.register_blueprint(tweets_bp, url_prefix="/api/tweets")
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

#
# @app.route('/colors/<palette>/')
# @swag_from('swagger/users.yml', validation=False)
# def colors(palette):
#     all_colors = {
#         'cmyk': ['cyan', 'magenta', 'yellow', 'black'],
#         'rgb': ['red', 'green', 'blue']
#     }
#     if palette == 'all':
#         result = all_colors
#     else:
#         result = {palette: all_colors.get(palette)}
#
#     return make_response(jsonify(result), 200)


if __name__ == "__main__":
    app.run(debug=True)
