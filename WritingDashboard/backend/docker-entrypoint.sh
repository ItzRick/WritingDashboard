#!/bin/sh
flask db upgrade
gunicorn -b :${PORT} --workers=${NUMWORKERS} --threads=${NUMTHREADS} wsgi:app