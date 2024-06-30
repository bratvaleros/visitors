#source ../../VENV/bin/activate
#export DJANGO_READ_DOT_ENV_FILE=True
export DJANGO_SETTINGS_MODULE=config.settings.production
export DJANGO_ALLOWED_HOSTS="*"
export DJANGO_ADMIN_URL="admin/"
export DJANGO_DEBUG=True
export DEBUG=True
export SECRET_KEY=SpectacularSecret
export DATABASE_URL=postgresql://visitors:visitors@localhost/visitors
export VISITORS_PORT=9099
export STATIC_DIR=/var/www/alldata/spectacular/static

#python manage.py makemigrations
#python manage.py migrate
#python manage.py createsuperuser
#python manage.py runserver 0.0.0.0:8000
#python manage.py collectstatic --no-input --clear
gunicorn --bind 0.0.0.0:$VISITORS_PORT -c visitors.gunicorn.py config.wsgi
