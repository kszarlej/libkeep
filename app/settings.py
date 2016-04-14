import os

DEBUG = bool(os.getenv('DEBUG', 0))  # default false
APP_NAME = 'library'

ROUTES = [
    ('/', 'controllers.hello.Hello'),
    ('/test', 'controllers.test.Test'),
]
