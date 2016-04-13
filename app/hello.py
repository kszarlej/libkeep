from flask import Flask
import sys
import time
import logging

app = Flask(__name__)

@app.route("/")
def hello():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.info('Hello World')
    logger.debug('Hello Debugging World')


    time.sleep(1)
    return "Hello Wolrd!!!"





if __name__ == "__main__":
    app.run(host='0.0.0.0')
