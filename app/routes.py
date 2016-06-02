from importlib import import_module

from project.app import api


ROUTES = {
    'user': {
        'register': ('/user/register', 'user.controllers', 'Register'),
        'login': ('/user/login', 'user.controllers', 'Login'),
    },
    'books': {
        'list': ('/books', 'book.controllers', 'List'),
        'details': ('/books/<string:isbn>', 'book.controllers', 'Detail'),
        'loan': ('/books/<string:isbn>/loan', 'book.controllers', 'Loan'),
        'return': ('/books/<string:isbn>/return', 'book.controllers',
                   'Return'),
    },
}


_enabled = False


def init_routes():
    global _enabled
    if _enabled:
        return

    for module, controllers in ROUTES.items():
        for controller, route_data in controllers.items():
            route, path, Controller = route_data
            endpoint = '{}:{}'.format(module, controller)

            api.add_resource(
                getattr(import_module('project.{}'.format(path)), Controller),
                route, endpoint=endpoint)
    _enabled = True
