from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context


db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __str__(self):
        return str(self.email)

    def secure_password(self):
        self.password = pwd_context.encrypt(self.password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    @property
    def jwt_dict(self):
        return {
            'id': self.id,
            'email': self.email,
        }
