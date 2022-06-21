FROM python:3.8-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ADD ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
ADD . /app
WORKDIR /app
