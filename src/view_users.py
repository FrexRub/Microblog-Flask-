from flask import Blueprint, jsonify

from app import db
from models import User


router = Blueprint('router', __name__)


@router.route("/me")
def get_user_me():
    return "User/me"


@router.route("/all")
def get_user_all():
    users = db.session.query(User).all()
    for user in users:
        print(user.name)
    return jsonify({"users": "full"})
