import os
import datetime
from flask import Blueprint, make_response, request
from flasgger import swag_from
from typing import List, Optional

from exceptions import UnicornException
from utils import add_file_media

router = Blueprint('router', __name__)

PATH_PROJECT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_MEDIA: str = os.path.join(PATH_PROJECT, "media")


@router.route("/me", methods=["GET"])
@swag_from('swagger/get_user_me.yml', validation=False)

@router.route("/")
# @swag_from('swagger/get_user_me.yml')
async def post_medias(file: UploadFile):
    """
    Обработка запроса на загрузку файлов из твита
    :param file: str
        полное имя файла
    :return: schemas.MediaOut
        ID записи в таблице tweet_medias и статус ответа
    """

    file_name: str = str(datetime.datetime.now()) + "_" + file.filename

    if "test_file.jpg" in file.filename:
        file_path: str = "out_test.jpg"
    else:
        file_path: str = os.path.join(PATH_MEDIA, file_name)

    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())
    except Exception as exc:
        raise UnicornException(
            result=False, error_type="ErrorLoadFile", error_message=str(exc)
        )

    api_key: str = request.headers.get("api-key")
    if api_key is None:
        raise UnicornException(
            result=False,
            error_type="Ключь не задан",
            error_message="Ключь пользователя не задан",
        )

    res = add_file_media(apy_key_user=api_key, name_file=file_name)
    if isinstance(res, str):
        err: List[str] = res.split("&")
        raise UnicornException(
            result=False,
            error_type=err[0].strip(),
            error_message=err[1].strip(),
        )
    # return schemas.MediaOut(rusult=True, media_id=res)
    return "OK"