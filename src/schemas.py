from typing import List

from app import ma
from models import User


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


class LikeSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("user_id", "name")


class TweetSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("id", "content", "attachments", "author", "likes")

    # id: int = Field(title="ID Tweet")
    # content: str = Field(title="Text Tweet")
    # attachments: List[str] = Field(title="Links of media files")
    # author: User = Field(title="Info about author")
    # likes: List[Like] = Field(title="Info about authors of the likes")
#

