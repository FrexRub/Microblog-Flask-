from typing import List

from app import ma
from models import User


# from typing import List
#
# from pydantic import BaseModel, Field
#
#
# class ResultClass(BaseModel):
#     rusult: bool = Field(..., title="Response status")
#
#
# class TweetIn(BaseModel):
#     tweet_data: str = Field(title="Text Tweet")
#     tweet_media_ids: List[int] = Field(title="ID medias of Tweet")
#
#
# class TweetOut(ResultClass):
#     tweet_id: int = Field(..., title="Tweet ID")
#
#
# class MediaOut(ResultClass):
#     media_id: int = Field(..., title="Media ID")
#
#
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
# class Like(BaseModel):
#     user_id: int = Field(title="ID User")
#     name: str = Field(title="Name User")
#
#
# class Tweet(BaseModel):
#     id: int = Field(title="ID Tweet")
#     content: str = Field(title="Text Tweet")
#     attachments: List[str] = Field(title="Links of media files")
#     author: User = Field(title="Info about author")
#     likes: List[Like] = Field(title="Info about authors of the likes")
#
#
# class Tweets(ResultClass):
#     tweets: List[Tweet] = Field(title="List of Tweets")
