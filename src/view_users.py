from flask import Blueprint, jsonify, request

from app import db
from exceptions import UnicornException
from models import User

from schemas import UserSchema


router = Blueprint('router', __name__)


@router.route("/me", methods=["GET"])
def get_user_me():
    api_key: str = request.headers.get("api-key")
    if api_key is None:
        raise UnicornException(
            result=False,
            error_type="Ошибка заголовка",
            error_message="В запросе отсутствует заголовок",
        )
    return api_key


@router.route("/all")
def get_user_all():
    users_schema = UserSchema(many=True)
    users = db.session.query(User).all()
    print("valiate", users_schema.validate(users))
    result = users_schema.dump(users)
    print(result)
    for user in users:
        print(user.name)
    return jsonify(result)
