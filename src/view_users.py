from flask import Blueprint

# from src.app import db
# from src.models import User


router = Blueprint('router', __name__)


@router.route("/me")
def get_user_me():
    return "User/me"


# @router.route("/all")
# def get_user_all():
#     users = db.session.query(User).all()
#     return {"user": users}
