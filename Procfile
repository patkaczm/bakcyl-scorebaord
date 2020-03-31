release: python manage.py makemigrations
release: python manage.py migrate
web: python manage.py process_tasks
web: gunicorn website.wsgi --log-file -
