from typing import List

from app import ma
from models import User


# class ResultClass(ma.Schema):
#     rusult: bool


# class TweetIn(ma.Schema):
#     tweet_data: str
#     tweet_media_ids: List[int]


#
#
# class TweetOut(ResultClass):
#     tweet_id: int = Field(..., title="Tweet ID")
#
#
class MediaOutSchema(ma.Schema):
    rusult: bool
    media_id: int


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("id", "name")


class UserAllSchema(UserSchema):
    followers: List[User]
    following: List[User]
    result: bool


#
#
# class UserOut(ResultClass):
#     user: UserAll = Field(..., title="User info")
#
#
class Like(ma.SQLAlchemySchema):
    class Meta:
        fields = ("user_id", "name")


class Tweet(ma.SQLAlchemySchema):
    class Meta:
        fields = ("id", "content", "attachments", "author", "likes")

    # id: int = Field(title="ID Tweet")
    # content: str = Field(title="Text Tweet")
    # attachments: List[str] = Field(title="Links of media files")
    # author: User = Field(title="Info about author")
    # likes: List[Like] = Field(title="Info about authors of the likes")
#
#
# class Tweets(ResultClass):
#     tweets: List[Tweet] = Field(title="List of Tweets")
