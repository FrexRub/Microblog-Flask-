# for docker
from src.database import db

# for alembic
# from ..src.database import Base


followers = db.Table(
    "followers",
    db.metadata,
    db.Column("user_id", db.ForeignKey("users.id"), primary_key=True),
    db.Column("following_id", db.ForeignKey("users.id"), primary_key=True),
    db.UniqueConstraint(
        "user_id", "following_id", name="idx_unique_user_following"
    ),
)


class LikesTweet(db.Model):
    __tablename__ = "likes_tweet"
    __table_args__ = (
        db.UniqueConstraint("user_id", "tweet_id", name="idx_unique_user_tweet"),
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweets.id"), primary_key=True)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    apy_key_user = db.Column(db.String, nullable=False)

    tweet = db.relationship("Tweet", back_populates="user")
    like_tweet = db.relationship(
        "Tweet",
        secondary="likes_tweet",
        back_populates="like_user",
        lazy="selectin",
    )

    following = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.user_id == id),
        secondaryjoin=(followers.c.following_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )


class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True, index=True)
    tweet_data = db.Column(db.String, nullable=False)
    tweet_media_ids = db.Column(db.ARRAY(db.Integer), default=[], nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="tweet")
    like_user = db.relationship(
        "User",
        secondary="likes_tweet",
        back_populates="like_tweet",
        lazy="selectin",
    )

    @db.hybrid_property
    def like_count(self):
        query = db.select(db.func.count(LikesTweet.tweet_id)).where(
            LikesTweet.tweet_id == self.id
        )
        result = db.object_session(self).execute(query)
        return result.scalars().one()

    @like_count.expression
    def like_count(cls):
        return (
            db.select(db.func.count(LikesTweet.tweet_id))
            .where(LikesTweet.tweet_id == cls.id)
            .label("like_count")
        )


class TweetMedia(db.Model):
    __tablename__ = "tweet_medias"
    media_id = db.Column(db.Integer, primary_key=True, index=True)
    name_file = db.Column(db.String, nullable=False)
