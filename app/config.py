import os

DEBUG = bool(os.getenv('DEBUG', 0))  # default false
HOST = os.environ['HOST']
PORT = int(os.environ['PORT'])
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']

JWT_SECRET = 'secret'

SQLALCHEMY_DATABASE_URI = \
    'postgresql://{user}:{password}@{host}/{name}'.format(
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        name=os.environ['DB_NAME'])
