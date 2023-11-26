FROM python:3.10

ENV APP_HOME /app
COPY . $APP_HOME
WORKDIR $APP_HOME

RUN pip install Flask
RUN pip install mysql.connector

