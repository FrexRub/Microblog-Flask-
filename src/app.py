from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from database import db_url


class MyServer(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_config(self):
        self.config['JSON_AS_ASCII'] = False
        self.config['JSON_SORT_KEYS'] = False
        self.config['SECRET_KEY'] = 'secret'
        self.config['SQLALCHEMY_DATABASE_URI'] = db_url
        self.config['SWAGGER'] = {
            'title': 'API Microlog',
            'uiversion': 3,
            'specs_route': "/api/docs/"
        }


app = MyServer(__name__)
app.set_config()

db = SQLAlchemy(app)
ma = Marshmallow(app)
