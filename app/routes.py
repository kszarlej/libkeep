from importlib import import_module

from project.app import api


ROUTES = {
    'user': {
        'register': ('/user/register', 'user.controllers', 'Register'),
        'login': ('/user/login', 'user.controllers', 'Login'),
        'delete': ('/user/delete', 'user.controllers', 'Delete'),
        'list': ('/user/list', 'user.controllers', 'List'),
    },
    'books': {
        'list': ('/books', 'book.controllers', 'List'),
        'details': ('/books/<string:isbn>', 'book.controllers', 'Detail'),
        'loan': ('/books/<string:isbn>/loan', 'book.controllers', 'Loan'),
    },
    'authors': {
        'list': ('/author/list', 'author.controllers', 'List'),
        'add': ('/author/add', 'author.controllers', 'Add'),
        'delete': ('/author/delete', 'author.controllers', 'Delete'),
        'authorBooks': ('/author/getbooks', 'author.controllers', 'GetAuthorBooks'),
    }
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
