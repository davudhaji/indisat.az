FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV APP_ROOT /code

RUN apt-get update 

COPY mime.types /etc/mime.types

RUN mkdir ${APP_ROOT}
COPY . ${APP_ROOT}
WORKDIR ${APP_ROOT}

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN python manage.py collectstatic --noinput