FROM python:3.7-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080

CMD exec gunicorn --bind :8080 --workers 4 --timeout 100 main:server
