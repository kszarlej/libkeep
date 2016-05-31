from flask_restful.reqparse import Argument, RequestParser


class Parser(RequestParser):

    arguments = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.args = self.arguments
