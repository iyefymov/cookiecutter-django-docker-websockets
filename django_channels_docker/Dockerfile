FROM python:3.12.4-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y postgresql-client

RUN pip install -r requirements.txt

COPY . /app/

CMD ["run.sh"]