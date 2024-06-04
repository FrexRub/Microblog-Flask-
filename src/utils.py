from schemas import UserSchema
from models import User
from app import db


def get_users_all():
    users_schema = UserSchema(many=True)
    users = db.session.query(User).all()
    print("valiate", users_schema.validate(users))
    result = users_schema.dump(users)
    return result


