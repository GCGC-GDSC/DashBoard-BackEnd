web: gunicorn Dashboard.wsgi --log-file -
release: python Dashboard/manage.py makemigrations --noinput
release: python Dashboard/manage.py migrate --noinput