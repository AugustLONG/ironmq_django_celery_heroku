web: python manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 9

celery_master: python manage.py celeryd -E -Q master --loglevel=INFO
celery_worker: python manage.py celeryd -E -Q worker --loglevel=INFO
