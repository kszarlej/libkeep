from flask_restful.reqparse import Argument, RequestParser


class Parser(RequestParser):

    arguments = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.args = self.arguments


class ModelByIdArgument(Argument):

    def __init__(self, model, *args, **kwargs):
        self.model = model

        super().__init__(*args, **kwargs)

    def parse(self, *args, **kwargs):
        pk, found = super().parse(*args, **kwargs)
        if not found:
            return ValueError(), {self.name: self.help}

        obj = self.model.query.filter_by(id=pk).first()
        if not obj:
            return ValueError(), {
                self.name: '{} {} does not exist'.format(self.name.title(), pk)
            }

        return obj, True


class MaxLengthArgument(Argument):

    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length

        super().__init__(*args, **kwargs)

    def parse(self, *args, **kwargs):
        string, found = super().parse(*args, **kwargs)
        if not found:
            return ValueError(), {self.name: self.help}

        if len(string) > self.max_length:
            return ValueError(), {
                self.name: '{} is too long (max {} signs)'.format(
                    self.name.title(), self.max_length)
            }

        return string, True
