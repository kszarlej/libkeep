import os

DEBUG = bool(os.getenv('DEBUG', 0))  # default false
HOST = os.environ['HOST']
PORT = int(os.environ['PORT'])

JWT_SECRET = 'secret'

SQLALCHEMY_DATABASE_URI = \
    'postgresql://{user}:{password}@{host}/{name}'.format(
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        name=os.environ['DB_NAME'])
