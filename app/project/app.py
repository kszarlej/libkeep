from flask import Flask
from flask_restful import Api

from .db import db


app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db.init_app(app)
