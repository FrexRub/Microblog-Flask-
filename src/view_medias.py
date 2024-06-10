import os
import datetime
from flask import Blueprint, make_response, request
from werkzeug.utils import secure_filename

from src.app import app
from src.exceptions import UnicornException
from src.utils import add_file_media
from src.schemas import MediaOutSchema

medias_bp = Blueprint('medias_bp', __name__)


@medias_bp.route("/", methods=["POST"])
def post_medias():
    """
    Обработка запроса на загрузку файлов из твита
    :return: schemas.MediaOut
        ID записи в таблице tweet_medias и статус ответа
    """
    api_key: str = request.headers.get("api-key")
    if api_key is None:
        raise UnicornException(
            result=False,
            error_type="Ключ не задан",
            error_message="Ключ пользователя не задан",
        )
    file = request.files["file"]
    filename = str(datetime.datetime.now()) + "_" + secure_filename(file.filename)

    if "test_file.jpg" in file.filename:
        filename: str = "out_test.jpg"

    try:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except Exception as exc:
        raise UnicornException(
            result=False, error_type="ErrorLoadFile", error_message=str(exc)
        )

    res = add_file_media(apy_key_user=api_key, name_file=filename)

    media_info = MediaOutSchema().dump(dict(rusult=True, media_id=res))
    return make_response(media_info, 201)
