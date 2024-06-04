from flask import Blueprint, jsonify, make_response, request
from flasgger import swag_from
from typing import List, Optional

from app import db
from exceptions import UnicornException
from models import User
from schemas import UserSchema
from utils import get_users_all, get_users_my

router = Blueprint('router', __name__)


#
@router.route("/me", methods=["GET"])
@swag_from('swagger/get_user_me.yml', validation=False)
def get_user_me():
    """
    Пользователь может получить информацию о своём профиле
    :param api_key: str
        ключ пользователя
    :return: schemas.UserOut
        данные пользователя и статус ответа
    """
    api_key: str = request.headers.get("api-key", "test")
    get_users_my(api_key)
    # if api_key is None:
    #     raise UnicornException(
    #         result=False,
    #         error_type="Ошибка заголовка",
    #         error_message="В запросе отсутствует заголовок",
    #     )

    # res = get_user_me_from_db(api_key)

    #
    # me_data, following, followers = res
    # user_followers= [
    #     UserSchema(id=i_user.id, name=i_user.name) for i_user in followers
    # ]
    # user_following = [
    #     UserSchema(id=i_user.id, name=i_user.name) for i_user in following
    # ]
    # user_me = schemas.UserAll(
    #     id=me_data.id,
    #     name=me_data.name,
    #     followers=user_followers,
    #     following=user_following,
    # )

    user_me = {
        "api_key": api_key,
        "id": "me_data.id",
        "name": "me_data.name",
        "followers": "user_followers",
        "following": "user_following",
    }

    return make_response(user_me, 200)


@router.route("/all")
def get_user_all():
    result = get_users_all()
    print(result)
    return jsonify(result)

