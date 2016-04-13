from importlib import import_module

import settings


def init_routes(api):
    # TODO split and import class
    for route, controller in settings.ROUTES:
        api.add_resource(import_module(controller), route)
