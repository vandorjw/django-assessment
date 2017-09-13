release: python ./demo/manage.py migrate --noinput
web: newrelic-admin run-program gunicorn demo.wsgi --log-file -
