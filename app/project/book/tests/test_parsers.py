from pytest import mark

from ..parsers import BookParser


def test_parser_isbn_too_long(parser_failer, author, category):
    test_data = {
        'isbn': '1-1234-1124-1243-1',
        'title': 'Total new book',
        'category': category.id,
        'author': author.id,
    }

    parser_failer(BookParser(), test_data, expected_errors={
        'isbn': 'Isbn is too long (max 17 signs)'
    })


@mark.integration
def test_parser_missing_category(parser_failer, author):
    test_data = {
        'isbn': '1-1234-1124-1',
        'title': 'Total new book',
        'author': author.id,
    }

    parser_failer(BookParser(), test_data, expected_errors={
        'category': 'Category is required'
    })


@mark.integration
def test_parser_bad_category(parser_failer, author):
    test_data = {
        'isbn': '1-1234-1124-1',
        'title': 'Total new book',
        'category': 1,
        'author': author.id,
    }

    parser_failer(BookParser(), test_data, expected_errors={
        'category': 'Category 1 does not exist'
    })


@mark.integration
def test_parser_bad_author(parser_failer, category):
    test_data = {
        'isbn': '1-1234-1124-1',
        'title': 'Total new book',
        'category': category.id,
        'author': 1,
    }

    parser_failer(BookParser(), test_data, expected_errors={
        'author': 'Author 1 does not exist'
    })


@mark.integration
def test_parser_ok_data(Request, category, author):
    parser = BookParser()
    test_data = {
        'isbn': '1-1234-1124-1',
        'title': 'Total new book',
        'category': category.id,
        'author': author.id,
    }

    data = parser.parse_args(req=Request(test_data))

    assert data['isbn'] == test_data['isbn']
    assert data['title'] == test_data['title']
    assert data['category'] == category
    assert data['author'] == author
