from importlib import import_module

from project import api


ROUTES = [
    ('/', 'hello.views', 'Hello'),
]


def init_routes():
    for route, path, Controller in ROUTES:
        api.add_resource(
            getattr(import_module('project.{}'.format(path)), Controller),
            route)
