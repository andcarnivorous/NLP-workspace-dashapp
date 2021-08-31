FROM python:3.7-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python -m nltk.downloader 'punkt' -d /usr/local/nltk_data
RUN python -m nltk.downloader 'stopwords' -d /usr/local/nltk_data

ENV PORT 8080

CMD exec gunicorn --bind :8080 --workers 4 --timeout 130 maindash:server
