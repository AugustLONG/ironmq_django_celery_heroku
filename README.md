ironmq_django_celery_heroku
===========================

Heroku Environment
------------------
_heroku addons_
=== brads-testing Configured Add-ons
cloudamqp:bunny
heroku-postgresql:crane  HEROKU_POSTGRESQL_GOLD
papertrail:fixa

_heroku ps_
=== celery_master (1X): `python manage.py celeryd -E -Q master --loglevel=INFO`
celery_master.1: up 2013/08/21 09:23:25 (~ 15m ago)
celery_master.2: up 2013/08/21 09:23:27 (~ 15m ago)
celery_master.3: up 2013/08/21 09:23:27 (~ 15m ago)
celery_master.4: up 2013/08/21 09:23:26 (~ 15m ago)

=== celery_worker (1X): `python manage.py celeryd -E -Q worker --loglevel=INFO`
celery_worker.1: up 2013/08/21 09:23:26 (~ 15m ago)
celery_worker.2: up 2013/08/21 09:23:26 (~ 15m ago)
celery_worker.3: up 2013/08/21 09:23:29 (~ 15m ago)
celery_worker.4: up 2013/08/21 09:23:29 (~ 15m ago)

Running Test
------------

heroku run python manage.py shell

> from app.tasks import run_test
> run_test()
