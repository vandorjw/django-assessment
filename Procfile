release: python ./demo/manage.py migrate --noinput
web: gunicorn demo.wsgi --log-file -
