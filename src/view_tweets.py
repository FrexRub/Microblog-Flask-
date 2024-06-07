from flask import Blueprint, make_response, request, jsonify
from flasgger import swag_from
from typing import List

from exceptions import UnicornException
from utils import add_file_media, create_tweet

tweets_bp = Blueprint('tweets_bp', __name__)


@tweets_bp.route("/", methods=["POST"])
def post_api_tweets():
    """
    Добавление твита от имени текущего пользователя
    :return: Dict[bool, int]
        статус ответа и ID добавленного твита
    """
    api_key: str = request.headers.get("api-key")

    if api_key is None:
        raise UnicornException(
            result=False,
            error_type="Ключ не задан",
            error_message="Ключ пользователя не задан",
        )

    tweet = request.get_json()

    print(tweet)
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
