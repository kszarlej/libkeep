from project.app import app, db
from routes import init_routes


def get_app():
    init_routes()
    return app


def create_tables():
    with app.app_context():
        db.create_all()


def start_app():
    create_tables()
    get_app().run(host=app.config['HOST'],
                  port=app.config['PORT'],
                  debug=app.config['DEBUG'])


if __name__ == '__main__':
    start_app()
