import factory

from project.db import db, Book


class BookFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Book
        sqlalchemy_session = db.session   # the SQLAlchemy session object

    isbn = factory.Sequence(lambda n: '1-1234-1234-{}'.format(n))
    title = factory.Sequence(lambda n: 'Title {}'.format(n))
