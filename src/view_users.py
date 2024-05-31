from flask import Blueprint

router = Blueprint('router', __name__)


@router.route("/me")
def get_user_me():
    return "User/me"
