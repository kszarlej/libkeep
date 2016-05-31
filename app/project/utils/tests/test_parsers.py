from ..parsers import Parser, Argument


class TestParser(Parser):

    arguments = (
        Argument('email', required=True, help='Email is required'),
        Argument('id', type=int, help='Unique id'),
    )


def test_parser_abort_called(mocker, client):
    mock_abort = mocker.patch('flask_restful.abort')
    parser = TestParser()

    parser.parse_args()

    mock_abort.assert_called_once_with(
        400, message={'email': 'Email is required'})


def test_parser_valid_data(mocker, Request):
    mock_abort = mocker.patch('flask_restful.abort')
    parser = TestParser()
    test_data = {
        'email': 'email',
        'id': 1,
    }

    data = parser.parse_args(req=Request(json=test_data))

    assert not mock_abort.called
    assert data == test_data
