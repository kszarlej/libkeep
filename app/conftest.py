from pytest import fixture, mark

from run import get_app
from project.db import db as project_db, User, Book, Author, Category
from project.utils.test import TestRequest


@fixture
def app():
    return get_app()


@fixture
@mark.options(SQLALCHEMY_DATABASE_URI="sqlite://")
def db(app, request):
    with app.app_context():
        project_db.create_all()

    def fin():
        project_db.session.remove()
        project_db.drop_all()
    request.addfinalizer(fin)

    return project_db


@fixture
def Request():
    return TestRequest


@fixture
def parser_failer(Request, client, mocker):
    def wrapper(parser, data, expected_errors):
        mock_abort = mocker.patch('flask_restful.abort')

        data = parser.parse_args(req=Request(data))

        mock_abort.assert_called_with(400, message=expected_errors)

    return wrapper


@fixture
def user(db):
    user = User()
    user.email = 'test@example.com'
    user.password = 'test_password'
    user.secure_password()

    db.session.add(user)
    db.session.commit()

    return user


@fixture
def admin(db):
    user = User()
    user.email = 'admin@example.com'
    user.password = 'test_password'
    user.secure_password()
    user.is_admin = True

    db.session.add(user)
    db.session.commit()

    return user


@fixture
def author(db):
    author = Author()
    author.name = 'Mark Twain'

    db.session.add(author)
    db.session.commit()

    return author


@fixture
def category(db):
    category = Category()
    category.name = 'Fiction'

    db.session.add(category)
    db.session.commit()

    return category


@fixture
def book(db, author, category):
    book = Book()
    book.isbn = '123-1-1234-123-1'
    book.title = 'awesome book'
    book.author = author
    book.category = category

    db.session.add(book)
    db.session.commit()

    return book
