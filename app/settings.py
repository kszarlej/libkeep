import os


DEBUG = bool(int(os.environ['DEBUG']))  # value '0' or '1'
APP_NAME = 'library'

ROUTES = [
    ('/', 'controllers.hello.Hello'),
    ('/test', 'controllers.test.Test'),
]
