from marshmallow import Schema, fields

from src.app import ma


class MediaOutSchema(Schema):
    rusult = fields.Boolean()
    media_id = fields.Integer()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("id", "name")


class LikeSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("user_id", "name")


class TweetSchema(Schema):
    id = fields.Integer(required=True)
    content = fields.String(required=True)
    attachments = fields.List(fields.String())
    author = fields.Nested(UserSchema())
    likes = fields.List(fields.Nested(LikeSchema()))
#
