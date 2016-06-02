from project.utils.parsers import Parser, Argument


class RegisterParser(Parser):

    arguments = (
        Argument('email', required=True, help='Email is required'),
        Argument('password', required=True, help='Password is required'),
    )

class DeleteParser(Parser):

    arguments = (
        Argument('email', required=True, help='Email is required'),
    )

class LoginParser(RegisterParser):
    pass
