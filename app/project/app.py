from flask import Flask
from flask_restful import Api
from project.utils import admin

from .db import db

def create_admin():
    with app.app_context():
        admin.create_admin(admin_email=app.config['ADMIN_EMAIL'],
                           admin_password=app.config['ADMIN_PASSWORD'])

def create_tables():
    with app.app_context():
        db.create_all()

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db.init_app(app)

create_tables()
create_admin()
