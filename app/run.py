from flask import Flask
from flask_restful import Api

import settings
from routes import init_routes


app = Flask(settings.APP_NAME)
api = Api(app)


if __name__ == '__main__':
    init_routes(api)
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
