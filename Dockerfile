FROM python:3.10-alpine AS builder

COPY . /flask
WORKDIR ./flask

RUN pip3 install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app:create_app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]