from project.utils.parsers import Parser, Argument


class AuthorAddParser(Parser):

    arguments = (
        Argument('www', required=False, help='authors www page'),
        Argument('name', required=True, help='Author first name is required'),
        Argument('surname', required=False, help='author surname'),
        Argument('city', required=False, help='authors city'),
    )

class AuthorParser(Parser):

    arguments = (
        Argument('name', required=True, help='Author first name is required'),
        Argument('surname', required=True, help='Author first name is required'),
    )
