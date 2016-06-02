from pytest import mark

from project.utils.test import get, post, put
from project.db import Loan, Book
from ..factories import BookFactory


_get_books = get(endpoint='books:list')
_post_books = post(endpoint='books:list')


@mark.integration
def test_list_books_empty_list(client, db):
    response = _get_books(client)

    assert response.json == []


@mark.integration
def test_list_books(client, book):
    response = _get_books(client)

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == book.title
    assert response.json[0]['isbn'] == book.isbn
    assert response.json[0]['author'] == book.author.name
    assert response.json[0]['category'] == book.category.name
    assert response.json[0]['users'] == []


@mark.integration
def test_list_books_with_one_loan(client, book, user, db):
    book_with_loan = BookFactory()
    loan = Loan()
    loan.user = user
    loan.book = book_with_loan
    db.session.add(loan)
    db.session.commit()

    response = _get_books(client)

    assert len(response.json) == 2
    index = response.json.index(book_with_loan.json)
    book_with_loan_dict = response.json[index]

    assert book_with_loan_dict['users'] == [user.id]


@mark.integration
def test_post_new_book_response(client, author, category, admin):
    test_data = {
        'isbn': '1-1234-1124-1',
        'title': 'Total new book',
        'category': category.id,
        'author': author.id,
    }

    response = _post_books(client, data=test_data, user=admin)

    assert response.status_code == 201
    assert response.json['status'] == 'ok'


@mark.integration
def test_post_new_book_bad_request(client, category, admin):
    test_data = {
        'isbn': '1-1234-1124-1',
        'title': 'Total new book',
        'category': category.id,
        'author': 1,
    }

    response = _post_books(client, data=test_data, user=admin)

    assert response.status_code == 400
    assert 'author' in response.json['message']


@mark.integration
def test_post_new_book_new_db_object(client, author, category, admin):
    test_data = {
        'isbn': '1-1234-1124-1',
        'title': 'Total new book',
        'category': category.id,
        'author': author.id,
    }

    response = _post_books(client, data=test_data, user=admin)

    assert response.status_code == 201
    book = Book.query.filter_by(isbn=test_data['isbn']).first()
    assert book
    assert book.category == category


@mark.integration
def test_post_new_book_not_admin(client, author, category, user):
    test_data = {
        'isbn': '1-1234-1124-1',
        'title': 'Total new book',
        'category': category.id,
        'author': author.id,
    }

    response = _post_books(client, data=test_data, user=user)

    assert response.status_code == 403
    assert response.json['message'] == {'Authorization': 'Unauthorized'}


@mark.integration
def test_post_new_book_unauthorized(client, author, category):
    test_data = {
        'isbn': '1-1234-1124-1',
        'title': 'Total new book',
        'category': category.id,
        'author': author.id,
    }

    response = _post_books(client, data=test_data)

    assert response.status_code == 401
    assert response.json['message'] == {'Authorization': 'Missing JWT'}


@mark.integration
def test_put_title_return_value(client, book):
    put_book = put(endpoint='books:details', isbn=book.isbn)
    test_data = {
        'isbn': book.isbn,
        'title': 'New title',
        'category': book.category_id,
        'author': book.author_id,
    }

    response = put_book(client, data=test_data)

    assert response.status_code == 200
    assert response.json == {}


@mark.integration
def test_put_title_update_book(client, book):
    put_book = put(endpoint='books:details', isbn=book.isbn)
    test_data = {
        'isbn': book.isbn,
        'title': 'New title',
        'category': book.category_id,
        'author': book.author_id,
    }

    response = put_book(client, data=test_data)

    assert response.status_code == 200
    fresh_book = Book.query.filter_by(isbn=book.isbn).first()
    assert fresh_book.title == test_data['title']
    assert fresh_book.category == book.category


@mark.integration
def test_put_bad_isbn(client, book):
    put_book = put(endpoint='books:details', isbn='not-exist')
    test_data = {
        'isbn': 'not-exist',
        'title': 'New title',
        'category': book.category_id,
        'author': book.author_id,
    }

    response = put_book(client, data=test_data)

    assert response.status_code == 400
    assert response.json == {'message': {'isbn': 'Book does not exist'}}


@mark.integration
def test_loan_book(client, user, admin, book):
    post_book = post(endpoint='books:loan', isbn=book.isbn)
    test_data = {'user': user.id}

    response = post_book(client, data=test_data, user=admin)

    assert response.status_code == 201
    assert response.json == {}


@mark.integration
def test_loan_book_new_loan(client, user, admin, book):
    post_book = post(endpoint='books:loan', isbn=book.isbn)
    test_data = {'user': user.id}

    response = post_book(client, data=test_data, user=admin)

    assert response.status_code == 201
    assert len(book.loans) == 1
    assert book.loans[0].user == user


@mark.integration
def test_loan_only_admin(client, user, admin, book, db):
    post_book = post(endpoint='books:loan', isbn=book.isbn)
    test_data = {'user': user.id}

    response = post_book(client, data=test_data, user=user)

    assert response.status_code == 403
    assert response.json == {'message': {'Authorization': 'Unauthorized'}}
    assert len(book.loans) == 0


@mark.integration
def test_loan_no_more_copies(client, user, admin, book, db):
    post_book = post(endpoint='books:loan', isbn=book.isbn)
    test_data = {'user': user.id}

    loan = Loan()
    loan.book = book
    loan.user = admin
    db.session.add(loan)
    db.session.commit()

    response = post_book(client, data=test_data, user=admin)

    assert response.status_code == 400
    assert response.json == {'message': {'book': 'No more free copies'}}
    assert len(book.loans) == 1


@mark.integration
def test_return_book(client, user, admin, book, db):
    post_book = post(endpoint='books:return', isbn=book.isbn)
    test_data = {'user': user.id}

    loan = Loan()
    loan.book = book
    loan.user = user
    db.session.add(loan)
    db.session.commit()

    response = post_book(client, data=test_data, user=admin)

    assert response.status_code == 200
    assert response.json == {}
    assert len(book.loans) == 0


@mark.integration
def test_return_user_has_not_loan_this_book(client, user, admin, book, db):
    post_book = post(endpoint='books:return', isbn=book.isbn)
    test_data = {'user': user.id}

    loan = Loan()
    loan.book = book
    loan.user = admin
    db.session.add(loan)
    db.session.commit()

    response = post_book(client, data=test_data, user=admin)

    assert response.status_code == 400
    assert response.json == {
        'message': {
            'loan': 'This user has not loan this book'
        }
    }
    assert len(book.loans) == 1
