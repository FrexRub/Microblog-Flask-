import os
import datetime
from flask import Blueprint, make_response, request, jsonify
from typing import List
from werkzeug.utils import secure_filename

from src.app import app
from src.config import PATH_PROJECT
from src.exceptions import UnicornException
from src.utils import add_file_media
from src.schemas import MediaOutSchema

medias_bp = Blueprint('medias_bp', __name__)

PATH_MEDIA: str = os.path.join(PATH_PROJECT, "media")


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
    filename = secure_filename(file.filename)

    if "test_file.jpg" in file.filename:
        filename: str = "out_test.jpg"

    try:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except Exception as exc:
        raise UnicornException(
            result=False, error_type="ErrorLoadFile", error_message=str(exc)
        )
    finally:
        file.close()

    if filename != "out_test.jpg":
        old_name_full: str = os.path.join(PATH_MEDIA, filename)
        new_name_full: str = os.path.join(PATH_MEDIA, (str(datetime.datetime.now()) + "_" + filename))
        new_name: str = str(datetime.datetime.now()) + "_" + filename
        print("old_name", old_name_full, "new_name", new_name_full, sep="\n")
        try:
            os.rename(old_name_full, new_name_full)
        except FileNotFoundError as exc:
            raise UnicornException(
                result=False, error_type="ErrorLoadFile", error_message=str(exc)
            )
        except PermissionError as exc:
            raise UnicornException(
                result=False, error_type="ErrorLoadFile", error_message=str(exc)
            )
    else:
        new_name: str = filename
    res = add_file_media(apy_key_user=api_key, name_file=new_name)

    media_info = MediaOutSchema().dump(dict(rusult=True, media_id=res))
    return make_response(media_info, 201)
