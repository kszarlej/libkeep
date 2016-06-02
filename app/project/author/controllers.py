from flask_restful import Resource

from project.db import db, Author, Book
from project.utils.auth import require_admin
from .parsers import AuthorAddParser, AuthorParser

class List(Resource):

    def get(self, user_data):
        return [a.json for a in Author.query.all()]

class Add(Resource):

    @require_admin
    def post(self, user_data):
        parser = AuthorAddParser(bundle_errors=True)
        args = parser.parse_args()

        author = Author()
        author.name = args['name']
        author.surname = args['surname']
        author.www = args['www']
        author.slug = "{0}-{1}".format(args['name'].lower(), args['surname'].lower())

        test = Author.query.filter_by(slug=author.slug).first()

        if test:
            return {
                'status': 'error',
                'message': {
                    'default': 'This author already exists'
                }
            }, 400

        db.session.add(author)
        db.session.commit()

        return {'status': 'ok'}

class Delete(Resource):

    @require_admin
    def post(self, user_data):
        parser = AuthorParser(bundle_errors=True)
        args = parser.parse_args()

        slug = "{0}-{1}".format(args['name'].lower(), args['surname'].lower())
        author = Author.query.filter_by(slug=slug).first()

        if not author:
            return {
                'status': 'error',
                'message': {
                    'default': 'No such author'
                }
            }, 400

        db.session.delete(author)
        db.session.commit()
        return {'status': 'ok'}

class GetAuthorBooks(Resource):

    def post(self, user_data):
        parser = AuthorParser(bundle_errors=True)
        args = parser.parse_args()

        slug = "{0}-{1}".format(args['name'].lower(), args['surname'].lower())
        author_id = Author.query.filter_by(slug=slug).first().id
        books = Book.query.filter_by(author_id=author_id)

        return [b.json for b in books]
