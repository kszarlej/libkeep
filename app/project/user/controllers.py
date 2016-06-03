from flask_restful import Resource

from project.db import db, User
from project.utils.auth import get_token, require_admin
from sqlalchemy.exc import IntegrityError
from project.utils.status import return_error, return_ok

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

        return return_ok()

class Return(Resource):

    @require_admin
    def delete(self, id, user_data):

        user = User.query.filter_by(id=id).first()
        db.session.delete(user)

        try:
            db.session.commit()
        except IntegrityError as err:
            return return_error(err, 400)
        else:
            return return_ok()


class Login(Resource):

    def post(self):
        parser = LoginParser()
        args = parser.parse_args()

        user = User.query.filter_by(email=args['email']).first()
        if not user or not user.verify_password(args['password']):
            return return_error("Bad email or password", 400)

        return {'token': get_token(user)}
