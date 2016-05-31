from pytest import fixture, mark

from run import get_app
from project.db import db as project_db, User
from project.utils.test import TestRequest


@fixture
def app():
    return get_app()


@fixture
@mark.options(SQLALCHEMY_DATABASE_URI="sqlite://")
def db(request):
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

        mock_abort.assert_called_once_with(400, message=expected_errors)

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
