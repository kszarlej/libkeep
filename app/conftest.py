from pytest import fixture, mark

from run import get_app
from project import db as project_db


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
