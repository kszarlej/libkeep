FROM python:latest

ENV APP_DIR /app
ENV PYTHONUSERBASE $APP_DIR/.vendor

RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}

RUN pip install --upgrade pip
