release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn website.wsgi --log-file -
web: python manage.py process_tasks
