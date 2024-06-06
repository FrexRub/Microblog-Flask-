from flask import Blueprint, make_response, request, jsonify
from flasgger import swag_from
from typing import List

from exceptions import UnicornException
from utils import add_file_media
from schemas import Tweet, TweetIn

tweets_bp = Blueprint('tweets_bp', __name__)


@tweets_bp.route("/", methods=["POST"])
# @router.post("/", status_code=201, response_model=schemas.TweetOut)
def post_api_tweets():
    """
    Добавление твита от имени текущего пользователя
    :return: schemas.UserOut
        данные пользователя и статус ответа
    """
    api_key: str = request.headers.get("api-key")

    if api_key is None:
        raise UnicornException(
            result=False,
            error_type="Ключ не задан",
            error_message="Ключ пользователя не задан",
        )

    res = request.get_json()
    tweet_schema = TweetIn()
    tweet =tweet_schema.dump(res)

    print(res, res['tweet_data'])
    print(tweet)
    # res = create_tweet(
    #     apy_key_user=api_key,
    #     tweet_data=tweet["tweet_data"],
    #     tweet_media_ids=tweet.tweet_media_ids,
    # )
    # if isinstance(res, str):
    #     err: List[str] = res.split("&")
    #     raise UnicornException(
    #         result=False,
    #         error_type=err[0].strip(),
    #         error_message=err[1].strip(),
    #     )
    # return schemas.TweetOut(rusult=True, tweet_id=res)
    return make_response(jsonify("new tweet"), 200)
