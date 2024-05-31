from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database import db_url

db = SQLAlchemy()


class MyServer(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_config(self):
        self.config['JSON_AS_ASCII'] = False
        self.config['JSON_SORT_KEYS'] = False
        self.config['SECRET_KEY'] = 'secret'
        self.config['SQLALCHEMY_DATABASE_URI'] = db_url
        db.init_app(app=self)
