FROM python:3.6.8

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV SHELL=/bin/bash

RUN useradd -c 'pyuser' --home-dir /app -s /bin/bash pyuser
RUN echo 'pyuser:pyuser' | chpasswd

RUN pip install pipenv

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN cd /app && pipenv install --system --deploy

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
ENTRYPOINT ["/app/entrypoint.sh"]
