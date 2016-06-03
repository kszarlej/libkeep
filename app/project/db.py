from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.event import listen

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)

    loans = db.relationship('Loan', back_populates='user')

    def __str__(self):
        return str(self.email)

    def secure_password(self):
        self.password = pwd_context.encrypt(self.password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    @property
    def json(self):
        return {
            'email': self.email,
            'admin': self.is_admin
        }

    @property
    def jwt_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_admin': self.is_admin,
        }


class Book(db.Model):

    __tablename__ = 'book'

    isbn = db.Column(db.String(17), primary_key=True)
    title = db.Column(db.String(1024))
    copies = db.Column(db.Integer, default=1)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    loans = db.relationship('Loan', back_populates='book')
    category = db.relationship('Category')
    author = db.relationship('Author')

    def __str__(self):
        return self.title

    @property
    def json(self):
        return {
            'title': self.title,
            'isbn': self.isbn,
            'author': self.author.name if self.author else None,
            'category': self.category.name if self.author else None,
            'users': [l.user.id for l in self.loans],
        }

    @property
    def free_copies(self):
        return self.copies - len(self.loans)


class Loan(db.Model):

    __tablename__ = 'loan'

    book_id = db.Column(db.String(17), db.ForeignKey('book.isbn'),
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    book = db.relationship('Book', back_populates='loans')
    user = db.relationship('User', back_populates='loans')


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), unique=True)

    def __str__(self):
        return self.name

def slug_listener(mapper, connect, target):
    target.generate_slug()

class Author(db.Model):

    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), unique=False)
    surname = db.Column(db.String(1024), unique=False)
    slug = db.Column(db.String(1024), unique=True)
    city = db.Column(db.String(1024), unique=False)
    www = db.Column(db.String(1024), unique=False)

    def generate_slug(self):
        self.slug = '{}-{}'.format(self.name.lower(), self.surname.lower())

    @property
    def json(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'city': self.city,
            'www': self.www if self.www else None,
            }

    def __str__(self):
        author = "{0} {1}".format(self.name, self.surname)
        return author

listen(Author, 'before_insert', slug_listener)
