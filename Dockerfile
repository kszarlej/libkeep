FROM python:latest

ENV APP_DIR /app

RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}
ADD requirements.txt ${APP_DIR}
ADD app/* ${APP_DIR}

EXPOSE 5000

RUN pip install --upgrade pip && pip install -r requirements.txt
