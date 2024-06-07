from typing import List

from app import ma
from models import User
from marshmallow import Schema, fields


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


class TweetSchema(Schema):
    # class Meta:
    #     fields = ("id", "content", "attachments", "author", "likes")

    id = fields.Integer()
    content = fields.String()
    attachments = fields.List()  : List[str]
    author: UserSchema
    likes: List[LikeSchema] = list()
#

