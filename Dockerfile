FROM python:3.7-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

RUN pip install Flask matplotlib gunicorn pandas plotly chart_studio scikit-learn dash dash-bootstrap-components

COPY . .

ENV PORT 8080

CMD exec gunicorn --bind :8080 --workers 4 --timeout 100 main:server
