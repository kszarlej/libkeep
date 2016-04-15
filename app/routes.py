from importlib import import_module

import settings


def init_routes(api):
    # TODO split and import class
    for route, path, Controller in settings.ROUTES:
        api.add_resource(getattr(import_module(path), Controller), route)
