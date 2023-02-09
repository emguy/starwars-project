FROM python:3.10-slim-buster

RUN set -x && \
    apt-get update && \
    apt-get install -y gcc && \
    pip install uwsgi && \
    apt-get remove -y gcc && \
    apt autoremove -y

COPY ./myapp/requirements.txt /tmp/requirements.txt

RUN set -x && \
    pip install --prefer-binary --no-cache-dir --trusted-host pypi.python.org -r /tmp/requirements.txt && \
    pip list

ENV PYTHONPATH=/opt/app:/usr/local/lib/python3.10/site-packages
ENV PYTHONHOME=/usr/local

RUN useradd uwsgi
RUN useradd uwsgi-dev
