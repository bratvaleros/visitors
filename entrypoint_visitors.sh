#!/bin/bash

cd /code

#nohup gunicorn --daemon --bind unix:/var/spectacular/run/gunicorn.sock -c /code/visitors.gunicorn.py config.wsgi 2>&1 >> /var/log/spectacular/gunicorn_out.log
nohup gunicorn --daemon --bind 0.0.0.0:$VISITORS_PORT -c /code/visitors.gunicorn.py config.wsgi 2>&1 >> /var/log/spectacular/gunicorn_out.log

nginx -g 'daemon off;'
