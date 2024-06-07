from flask import Blueprint, make_response, request, jsonify
from flasgger import swag_from
from typing import List

from exceptions import UnicornException
from utils import (
    create_tweet,
    delete_tweets,
    add_like_tweet,
    delete_like_tweet
)

tweets_bp = Blueprint('tweets_bp', __name__)


@tweets_bp.route("/", methods=["POST", "GET"])
def api_tweets():
    """
    Добавление твита/получение ленты твитов от имени текущего пользователя
    :return: Dict[str, Union[bool, int]]
        статус ответа и ID добавленного твита
    """
    api_key: str = request.headers.get("api-key")

    if api_key is None:
        raise UnicornException(
            result=False,
            error_type="Ключ не задан",
            error_message="Ключ пользователя не задан",
        )

    if request.method == "POST":
        tweet = request.get_json()
        res: int = create_tweet(
            apy_key_user=api_key,
            tweet_data=tweet["tweet_data"],
            tweet_media_ids=tweet["tweet_media_ids"],
        )
        tweet_info = {
            "result": True,
            "tweet_id": res
        }
        return make_response(jsonify(tweet_info), 201)

    if request.method == "GET":
        pass
        # res: Union[str, List[schemas.Tweet]] = await out_tweets_user(
        #     session=session, apy_key_user=api_key
        # )
        # if isinstance(res, str):
        #     err: List[str] = res.split("&")
        #     raise UnicornException(
        #         result=False,
        #         error_type=err[0].strip(),
        #         error_message=err[1].strip(),
        #     )
        # return schemas.Tweets(rusult=True, tweets=res)


@tweets_bp.route("/<int:id>", methods=["DELETE"])
def delete_tweets_id(id: int):
    """
    Обработка запроса на удаление твита
    :param id: int
        ID твита
    :return: Dict[str, bool]
        статус ответа
    """
    api_key: str = request.headers.get("api-key")

    if api_key is None:
        raise UnicornException(
            result=False,
            error_type="Ключ не задан",
            error_message="Ключ пользователя не задан",
        )

    res: bool = delete_tweets(apy_key_user=api_key, id_tweet=id)

    if res:
        status_code = 200
    else:
        status_code = 400

    result_info = {
        "result": res,
    }

    return make_response(jsonify(result_info), status_code)


@tweets_bp.route("/<int:id>/likes", methods=["POST", "DELETE"])
def tweet_likes(id: int):
    """
    Обработка запроса на постановку/удаление отметки 'нравится' на твит
    :param id: int
        ID твита
    :return: Dict[str, bool]
        статус ответа
    """
    res: bool = False
    api_key: str = request.headers.get("api-key")
    if api_key is None:
        raise UnicornException(
            result=False,
            error_type="Ключ не задан",
            error_message="Ключ пользователя не задан",
        )

    if request.method == "POST":
        res: bool = add_like_tweet(apy_key_user=api_key, id_tweet=id)
        if res:
            status_code = 200
        else:
            status_code = 400

    if request.method == "DELETE":
        res: bool = delete_like_tweet(apy_key_user=api_key, id_tweet=id)
        if res:
            status_code = 200
        else:
            status_code = 400

    result_info = {
        "result": res,
    }

    return make_response(jsonify(result_info), status_code)
