from flask_restful import Resource

from project.db import db, Book, Loan as LoanModel
from project.utils.auth import require_admin
from .parsers import BookParser, LoanParser


def update_book(book, args):
    book.title = args['title']
    book.isbn = args['isbn']
    book.category = args['category']
    book.author = args['author']


class List(Resource):

    def get(self):
        return [b.json for b in Book.query.all()]

    @require_admin
    def post(self, user_data):
        parser = BookParser(bundle_errors=True)
        args = parser.parse_args()

        book = Book()
        update_book(book, args)

        db.session.add(book)
        db.session.commit()

        return {'status': 'ok'}, 201


class Detail(Resource):

    def put(self, isbn):
        parser = BookParser(bundle_errors=True)
        args = parser.parse_args()

        book = Book.query.filter_by(isbn=isbn).first()
        if not book:
            return {'message': {'isbn': 'Book does not exist'}}, 400

        update_book(book, args)

        return {}


class Loan(Resource):

    @require_admin
    def post(self, isbn, user_data):
        parser = LoanParser(bundle_errors=True)
        args = parser.parse_args()

        book = Book.query.filter_by(isbn=isbn).first()
        if not book:
            return {'message': {'isbn': 'Book does not exist'}}, 400
        if book.free_copies < 1:
            return {'message': {'book': 'No more free copies'}}, 400

        loan = LoanModel()
        loan.book = book
        loan.user = args['user']

        db.session.add(loan)
        db.session.commit()

        return {}, 201
