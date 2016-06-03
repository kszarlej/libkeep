from flask_restful import Resource
from flask import request

from project.db import db, Author, Book
from project.utils.auth import require_admin
from .parsers import AuthorAddParser, AuthorParser
from sqlalchemy.exc import IntegrityError
from sqlalchemy import event
from project.utils.status import return_error, return_ok

class List(Resource):

    def slug_listener(mapper, connection, target):
        target.slug = '{}-{}'.format(target.name, target.surname)

    def get(self, user_data):
        return [a.json for a in Author.query.all()]

    @require_admin
    def post(self, user_data):


        parser = AuthorAddParser(bundle_errors=True)
        args = parser.parse_args()

        author = Author()
        author.name = args['name']
        author.surname = args['surname']
        author.www = args['www']

        db.session.add(author)

        try:
            db.session.commit()
        except IntegrityError as err:
            return return_error(err, 400)
        else:
            return return_ok()

    event.listen(Author, 'before_insert', slug_listener)


class Return(Resource):

    @require_admin
    def delete(self, id, user_data):

        author = Author.query.filter_by(id=id).first()
        db.session.delete(author)

        try:
            db.session.commit()
        except IntegrityError as err:
            return return_error(err, 400)
        else:
            return return_ok()

class AuthorBooks(Resource):

    def get(self, id):
        parser = AuthorParser(bundle_errors=True)
        args = parser.parse_args()
        books = Book.query.filter_by(author_id=id)

        return [b.json for b in books]
