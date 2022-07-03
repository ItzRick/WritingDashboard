#!/bin/sh
flask db upgrade
gunicorn -b 127.0.0.1:${PORT} --workers=${NUMWORKERS} --threads=${NUMTHREADS} wsgi:app