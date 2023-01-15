# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR api/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "uvicorn", "itunes_app_scraper.api:app", "--host", "0.0.0.0"]
