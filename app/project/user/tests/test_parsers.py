from ..parsers import RegisterParser


def test_parse_register_proper_data(Request):
    parser = RegisterParser()
    test_data = {
        'email': 'test_email',
        'password': 'test_password',
    }

    data = parser.parse_args(req=Request(test_data))

    assert data == test_data


def test_parse_register_missing_email(parser_failer):
    parser_failer(RegisterParser(), {'password': 'test_password'},
                  expected_errors={'email': 'Email is required'})


def test_parse_register_missing_password(parser_failer):
    parser_failer(RegisterParser(), {'email': 'test_email'},
                  expected_errors={'password': 'Password is required'})
