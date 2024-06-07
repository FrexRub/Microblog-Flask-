import os
import datetime
from flask import Blueprint, make_response, request, jsonify
from typing import List
from werkzeug.utils import secure_filename

from exceptions import UnicornException
from utils import add_file_media
from schemas import MediaOutSchema

medias_bp = Blueprint('medias_bp', __name__)

PATH_PROJECT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    print("api_key", api_key)

    file = request.files["file"]
    file_name: str = str(datetime.datetime.now()) + "_" + secure_filename(file.filename)

    print("file_name", file_name)

    if "test_file.jpg" in file.filename:
        file_path: str = "out_test.jpg"
    else:
        file_path: str = os.path.join(PATH_MEDIA, file_name)

    try:
        # with open(file_path, "wb") as f:
        #     f.write(file.file.read())
        print("file_path", file_path)
        file.save(file_path)
    except Exception as exc:
        raise UnicornException(
            result=False, error_type="ErrorLoadFile", error_message=str(exc)
        )

    res = add_file_media(apy_key_user=api_key, name_file=file_name)
    if isinstance(res, str):
        err: List[str] = res.split("&")
        raise UnicornException(
            result=False,
            error_type=err[0].strip(),
            error_message=err[1].strip(),
        )

    # media_info = {
    #     "result": True,
    #     "media_id": res
    # }

    # media_schema = MediaOutSchema()
    # media_info = media_schema(rusult=True, media_id=res)

    media_info = MediaOutSchema().dump(dict(rusult=True, media_id=res))

    # return make_response(jsonify(media_info), 200)
    return make_response(jsonify("media_info"), 200)
