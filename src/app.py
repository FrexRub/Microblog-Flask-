import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from src.database import db_url
from src.config import PATH_PROJECT


UPLOAD_FOLDER: str = os.path.join(PATH_PROJECT, "media")
file_handler = RotatingFileHandler("microblog.log", maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
file_handler.setLevel(logging.INFO)

class MyServer(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_config(self):
        self.config['JSON_AS_ASCII'] = False
        self.config['JSON_SORT_KEYS'] = False
        self.config['SECRET_KEY'] = 'secret'
        self.config['SQLALCHEMY_DATABASE_URI'] = db_url
        self.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.config['SWAGGER'] = {
            'title': 'API Microlog',
            'openapi': '3.0.2',
            'specs_route': "/api/docs/"
        }


app = MyServer(__name__)
app.set_config()
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info("Microblog start")

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
