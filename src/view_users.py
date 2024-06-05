from flask import Blueprint, make_response, request
from flasgger import swag_from
from typing import List, Optional

from models import User
from schemas import UserSchema
from utils import get_users_my, get_user_id

router = Blueprint('router', __name__)


@router.route("/me", methods=["GET"])
@swag_from('swagger/get_user_me.yml', validation=False)
def get_user_me():
    """
    Пользователь может получить информацию о своём профиле
    :param api_key: str
        ключ пользователя
    :return: UserAllSchema
        данные пользователя и статус ответа
    """
    api_key: str = request.headers.get("api-key", "test")
    me_data, following, followers = get_users_my(api_key)

    schema_user_following = UserSchema(many=True)
    user_following: List[User] = schema_user_following.dump(following)

    schema_user_followers = UserSchema(many=True)
    user_followers: List[User] = schema_user_followers.dump(followers)

    user_info = {
        "result": True,
        "user": {
            "id": me_data.id,
            "name": me_data.name,
            "followers": user_followers,
            "following": user_following,
        },
    }

    return make_response(user_info, 200)


@router.get("/<int:id>")
@swag_from('swagger/get_user_id.yml')
def get_user_id_(id: int):
    """
    Обработка запроса на получение информацию о профиле пользователя по ID
    :param id: int
        ID пользователя
    :return: UserAllSchema
        данные пользователя и статус ответа
    """
    me_data, following, followers = get_user_id(id)

    schema_user_following = UserSchema(many=True)
    user_following: List[User] = schema_user_following.dump(following)

    schema_user_followers = UserSchema(many=True)
    user_followers: List[User] = schema_user_followers.dump(followers)

    user_info = {
        "result": True,
        "user": {
            "id": me_data.id,
            "name": me_data.name,
            "followers": user_followers,
            "following": user_following,
        },
    }

    return make_response(user_info, 200)
