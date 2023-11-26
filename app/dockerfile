FROM python:3.10

ENV APP_HOME /app
COPY . $APP_HOME
WORKDIR $APP_HOME
EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt

