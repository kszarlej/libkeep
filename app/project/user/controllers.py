from flask_restful import Resource, reqparse

from project.db import db, User
from project.utils.auth import get_token

from .parsers import RegisterParser, LoginParser


class Register(Resource):

    def post(self):
        parser = RegisterParser()
        args = parser.parse_args()

        user = User()
        user.email = args['email']
        user.password = args['password']
        user.secure_password()

        db.session.add(user)
        db.session.commit()

        return {'status': 'ok'}


class Login(Resource):

    def post(self):
        parser = RegisterParser()
        args = parser.parse_args()

        user = User.query.filter_by(email=args['email']).first()
        if not user or not user.verify_password(args['password']):
            return {
                'status': 'error',
                'message': {
                    'default': 'Bad email or password'
                }
            }, 400

        return {'token': get_token(user)}
