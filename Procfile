web: python manage.py migrate && python manage.py collectstatic --noinput --clear && python manage.py runserver 0.0.0.0:$PORT && gunicorn ecomm.wsgi
