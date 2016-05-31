import jwt

from project.app import app


def get_token(user):
    return jwt.encode(user.jwt_dict, app.config['JWT_SECRET'],
                      algorithm='HS256').decode('utf-8')


def decode_token(token):
    return jwt.decode(token.encode('utf-8'), app.config['JWT_SECRET'],
                      algorithms=['HS256'])
