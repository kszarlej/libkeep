import jwt

from flask import request
from flask_restful import abort

from project.app import app


def get_token(user):
    return jwt.encode(user.jwt_dict, app.config['JWT_SECRET'],
                      algorithm='HS256').decode('utf-8')


def decode_token(token):
    return jwt.decode(token.encode('utf-8'), app.config['JWT_SECRET'],
                      algorithms=['HS256'])


def get_user_data():
    try:
        auth_header = request.headers['Authorization']
    except KeyError:
        abort(401, message={'Authorization': 'Missing JWT'})

    token = auth_header.replace('JWT ', '')
    return decode_token(token)


def require_user(func):
    def wrapper(*args, **kwargs):
        user_data = get_user_data()

        return func(user_data=user_data, *args, **kwargs)

    return wrapper


def require_admin(func):
    def wrapper(*args, **kwargs):
        user_data = get_user_data()
        if not user_data['is_admin']:
            abort(403, message={'Authorization': 'Unauthorized'})

        return func(user_data=user_data, *args, **kwargs)

    return wrapper
