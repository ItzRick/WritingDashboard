#!/bin/sh
flask db upgrade
gunicorn -b :5000 --workers=${NUMWORKERS} --threads=${NUMTHREADS} wsgi:app