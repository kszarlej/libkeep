from project import app
from routes import init_routes


def get_app():
    init_routes()
    return app


def start_app():
    get_app().run(host=app.config['HOST'],
                  port=app.config['PORT'],
                  debug=app.config['DEBUG'])


if __name__ == '__main__':
    start_app()
