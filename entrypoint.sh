#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o allexport
set -o nounset

cmd="$@"

`which django-admin.py` migrate --no-input
`which django-admin.py` collectstatic --no-input


if [[ -z $cmd ]]; then
  gunicorn -b 0.0.0.0:5000 demo.wsgi
else
  exec $cmd
fi