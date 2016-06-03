from flask_restful import Resource

from project.db import db, User
from project.utils.auth import get_token, require_admin

from .parsers import RegisterParser, LoginParser, DeleteParser

class List(Resource):

    @require_admin
    def get(self, user_data):
        return [u.json for u in User.query.all()]


class Register(Resource):

    def post(self):
        parser = RegisterParser(bundle_errors=True)
        args = parser.parse_args()

        user = User()
        user.email = args['email']
        user.password = args['password']
        user.secure_password()

        db.session.add(user)
        db.session.commit()

        return {'status': 'ok'}, 201

class Delete(Resource):

    @require_admin
    def post(self, user_data):

        parser = DeleteParser(bundle_errors=True)
        args = parser.parse_args()

        user = User.query.filter_by(email = args['email']).first()

        if not user:
            return {
                'status': 'error',
                'message': {
                    'default': 'No such user'
                }
            }, 400

        db.session.delete(user)
        db.session.commit()
        return {'status': 'ok'}, 201


class Login(Resource):

    def post(self):
        parser = LoginParser()
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
