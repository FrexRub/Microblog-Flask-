from schemas import UserSchema
from models import User
from app import db


def get_user_by_apy_key(apy_key_user: str):
    """
    Возвращает данные пользователя по ключу apy_key_user
    :param apy_key_user: str
        ключ пользователя
    :return: Optional[models.User]
        данные пользователя или None, если пользователь не найден
    """
    query = db.session.execute(
        db.select(User).filter(User.apy_key_user == apy_key_user)
    )
    return query.scalars().first()


def get_users_all():
    users_schema = UserSchema(many=True)
    users = db.session.query(User).all()
    print("valiate", users_schema.validate(users))
    result = users_schema.dump(users)
    return result


def get_users_my(apy_key_user: str):
    users_schema = UserSchema()
    user = get_user_by_apy_key(apy_key_user)
    print("valiate", users_schema.validate(user))
    result = users_schema.dump(user)
    print(result)
    # return result
