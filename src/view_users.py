from flask import Blueprint, jsonify, request
from flasgger import ValidationError

from app import db
from models import User
import schemas


router = Blueprint('router', __name__)


@router.route("/me", methods=["GET"])
def get_user_me():
    api_key: str = request.headers.get("api-key")
    if api_key is None:
        raise ValidationError('Please use api-key in Header.')
    return "User/me"


@router.route("/all")
def get_user_all():
    users = db.session.query(User).all()
    for user in users:
        print(user.name)
    # return jsonify(schemas.User.dump(users))
    return jsonify({"user": "User"})
