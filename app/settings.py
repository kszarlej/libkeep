import os

DEBUG = bool(os.getenv('DEBUG', 0))  # default false
APP_NAME = 'library'
HOST = os.environ['HOST']
PORT = int(os.environ['PORT'])

ROUTES = [
    ('/', 'controllers.hello', 'Hello'),
    ('/test', 'controllers.test', 'Test'),
]
