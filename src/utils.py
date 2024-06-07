import os
from psycopg2 import errors
from typing import Tuple, List, Optional, Literal

import sqlalchemy.exc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import StaleDataError

from schemas import UserSchema
from models import User, TweetMedia, Tweet
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


def user_following(id_follower: int, apy_key_user: str, metod: Literal["following", "unfollowing"]) -> bool:
    """
    Добавление подписчика пользователю
    :param id_follower: int
        ID подписчика
    :param apy_key_user: str
        ключ пользователя
    :return: Union[str, bool]
        статус выполнения операции
    """
    data_user: Optional[User] = get_user_by_apy_key(apy_key_user)
    if data_user is None:
        raise UnicornException(
            result=False,
            error_type="Пользователь не найден",
            error_message=f"Пользователь с ключом {apy_key_user} не найден",
        )

    # Поиск данных подписчика
    user_folower: Optional[User] = db.session.get(User, id_follower)

    if user_folower is None:
        raise UnicornException(
            result=False,
            error_type="Пользователь не найден",
            error_message=f"Пользователь с ключом {id_follower} не найден",
        )

    if metod == "following":
        try:
            data_user.following.append(user_folower)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return False
        else:
            return True

    if metod == "unfollowing":
        try:
            data_user.following.remove(user_folower)
        except StaleDataError:
            db.session.rollback()
            return False
        else:
            db.session.commit()
            return True


def add_file_media(apy_key_user: str, name_file: str):
    """
    Добавляет в БД имя прикрепленного к твиттеру файла
    :param apy_key_user: str
        ключ пользователя
    :param name_file: str
        имя файла
    :return: Option[int]
        ID новой записи (при успешном добавлении в БД)
    """

    data_user: Optional[User] = get_user_by_apy_key(apy_key_user)

    if data_user is None:
        raise UnicornException(
            result=False,
            error_type="Пользователь не найден",
            error_message=f"Пользователь с ключом {apy_key_user} не найден",
        )

    new_media: TweetMedia = TweetMedia(name_file=name_file)

    try:
        db.session.add(new_media)
    except SQLAlchemyError:
        db.session.rollback()
        raise UnicornException(
            result=False,
            error_type="File not append",
            error_message="ошибка записи в БД",
        )
    else:
        db.session.commit()
    return new_media.media_id


def create_tweet(apy_key_user: str, tweet_data: str, tweet_media_ids: Optional[List[int]]) -> int:
    """
    Добавляет новый твиттер в БД
    :param apy_key_user: str
        ключ пользователя
    :param tweet_data: str
        текстовое содержание твиттера
    :param tweet_media_ids: Optional[List[int]]
        список ID прикрепленных к твиттеру изображений (при наличии)
    :return: Union[str, int]
        ID созданного твиттера (при успешном добавлении в БД)
    """
    data_user: Optional[User] = get_user_by_apy_key(apy_key_user)

    if data_user is None:
        raise UnicornException(
            result=False,
            error_type="Пользователь не найден",
            error_message=f"Пользователь с ключом {apy_key_user} не найден",
        )

    new_tweet: Tweet = Tweet(
        tweet_data=tweet_data,
        tweet_media_ids=tweet_media_ids,
        user_id=data_user.id,
    )

    try:
        db.session.add(new_tweet)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise UnicornException(
            result=False,
            error_type="Ошибка БД",
            error_message=f"{exc}",
        )
    return new_tweet.id


def name_file_from_tweet_medias(list_id_name_file: List[int]) -> List[str]:
    """
    Возвращает список имен файлов по их ID из таблицы TweetMedia
    :param session: AsyncSession
        текущая сессия
    :param list_id_name_file: List[int]
        список ID имен файлов
    :return: List[str]
        список имен файлов, или пустой
    """
    list_name_file: List[str] = list()
    for i_id in list_id_name_file:
        res: Optional[TweetMedia] = db.session.get(TweetMedia, i_id)
        if res:
            list_name_file.append(res.name_file)
    return list_name_file


def delete_files_from_tweet(id_files_tweet: List[int]) -> None:
    name_files: List[str] = name_file_from_tweet_medias(id_files_tweet)
    for i_file in name_files:
        name_file: str = os.path.join("media", i_file)
        os.remove(name_file)


def delete_tweets(apy_key_user: str, id_tweet: int) -> bool:
    """
    Удаление твиттера пользователя по ID
    :param apy_key_user: str
        ключ пользователя
    :param id_tweet: int
        ID твиттера
    :return: bool
        статус выполнения операции
    """
    data_user: Optional[User] = get_user_by_apy_key(apy_key_user)

    if data_user is None:
        raise UnicornException(
            result=False,
            error_type="Пользователь не найден",
            error_message=f"Пользователь с ключом {apy_key_user} не найден",
        )

    # Проверяем принадлежность твитера пользователю
    query = db.session.execute(
        db.select(Tweet).filter(
            db.and_(
                Tweet.user_id == data_user.id,
                Tweet.id == id_tweet,
            )
        )
    )
    tweet: Optional[Tweet] = query.scalars().one_or_none()
    if tweet:
        tweet_media_ids: List[int] = tweet.tweet_media_ids
        try:
            db.session.delete(tweet)
        except SQLAlchemyError:
            db.session.rollback()
            return False
        else:
            db.session.commit()
            if len(tweet_media_ids) != 0:
                delete_files_from_tweet(tweet_media_ids)
                stmt = db.delete(TweetMedia).filter(
                    TweetMedia.media_id.in_(tweet_media_ids)
                )
                db.session.execute(stmt)
                db.session.commit()
            return True
    else:
        return False


def add_like_tweet(apy_key_user: str, id_tweet: int) -> bool:
    """
    Добавляет лайк твиттеру с указанным ID
    :param apy_key_user: str
        ключ пользователя
    :param id_tweet: int
        ID твиттера
    :return: bool
        статус выполнения операции
    """
    # query = db.session.execute(
    #     db.select(User)
    #     .where(User.apy_key_user == apy_key_user)
    #     .options(db.selectinload(User.like_tweet))
    # )
    # data_user: Optional[User] = query.scalars().first()

    data_user: Optional[User] = get_user_by_apy_key(apy_key_user)

    if data_user is None:
        raise UnicornException(
            result=False,
            error_type="Пользователь не найден",
            error_message=f"Пользователь с ключом {apy_key_user} не найден",
        )

    tweet: Tweet = db.session.get(Tweet, id_tweet)

    # Проверка автора твита
    if tweet.user_id == data_user.id:
        return False

    try:
        data_user.like_tweet.append(tweet)
    except errors.UniqueViolation:
    # except IntegrityError:
        db.session.rollback()
        return False
    else:
        db.session.commit()
        return True
