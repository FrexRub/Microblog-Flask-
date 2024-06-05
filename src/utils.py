from typing import Tuple, List, Optional

from schemas import UserSchema
from models import User
from app import db
from exceptions import UnicornException


def get_user_by_apy_key(apy_key_user: str) -> Optional[User]:
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


def get_users_my(apy_key_user: str) -> Tuple[User, List[User], List[User]]:
    user: Optional[User] = get_user_by_apy_key(apy_key_user)
    if user is None:
        raise UnicornException(
            result=False,
            error_type="Пользователь не найден",
            error_message=f"Пользователь с ключом {apy_key_user} не найден",
        )

    # Выгрузка данных по подпискам и подписчикам
    query = db.session.execute(user.following)
    following = query.scalars().all()
    query = db.session.execute(user.followers)
    followers = query.scalars().all()

    return user, following, followers


def get_user_id(id_user: int) -> Tuple[User, List[User], List[User]]:
    user: Optional[User] = db.session.get(User, id_user)

    if user is None:
        raise UnicornException(
            result=False,
            error_type="Пользователь не найден",
            error_message=f"Пользователь с ключом {id_user} не найден",
        )

    # Выгрузка данных по подпискам и подписчикам
    query = db.session.execute(user.following)
    following = query.scalars().all()
    query = db.session.execute(user.followers)
    followers = query.scalars().all()

    return user, following, followers
