FROM python:latest

ENV APP_DIR /app
ENV PYTHONPATH /app

RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}

ADD ./entrypoint.sh /entrypoint.sh
ADD ./app ${APP_DIR}

RUN pip install --upgrade pip

ENTRYPOINT ["/entrypoint.sh"]
CMD /entrypoint.sh install && /entrypoint.sh run
