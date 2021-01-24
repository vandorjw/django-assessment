FROM python:3.8.5 as base_image

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV SHELL=/bin/bash

RUN apt update && apt install libpq-dev python3-dev -y

RUN useradd -c 'pyuser' --home-dir /app -s /bin/bash pyuser
RUN echo 'pyuser:pyuser' | chpasswd

COPY requirements.frozen.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod a+x /app/entrypoint.sh
RUN chown pyuser /app/entrypoint.sh

COPY ./demo /app/demo
COPY ./assessment /app/assessment

RUN mkdir /app/public

RUN chown pyuser:pyuser /app/demo
RUN chown pyuser:pyuser /app/public

USER pyuser

WORKDIR /app

EXPOSE 5000

## DEBUG IMAGE ##
FROM base_image as debug
USER root
RUN pip install debugpy
USER pyuser
ENTRYPOINT ["/app/entrypoint.sh"]

## PROD IMAGE ##
FROM base_image as prod
ENTRYPOINT ["/app/entrypoint.sh"]
