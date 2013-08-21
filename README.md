ironmq_django_celery_heroku
===========================

Heroku Environment
------------------

#### _heroku addons_
```bash
=== brads-testing Configured Add-ons
cloudamqp:bunny
heroku-postgresql:crane  HEROKU_POSTGRESQL_GOLD
papertrail:fixa
```

#### _heroku ps_
```bash
=== celery_master (1X): python manage.py celeryd -E -Q master --loglevel=INFO
celery_master.1: up 2013/08/21 09:23:25 (~ 15m ago)
celery_master.2: up 2013/08/21 09:23:27 (~ 15m ago)
celery_master.3: up 2013/08/21 09:23:27 (~ 15m ago)
celery_master.4: up 2013/08/21 09:23:26 (~ 15m ago)

=== celery_worker (1X): `python manage.py celeryd -E -Q worker --loglevel=INFO`
celery_worker.1: up 2013/08/21 09:23:26 (~ 15m ago)
celery_worker.2: up 2013/08/21 09:23:26 (~ 15m ago)
celery_worker.3: up 2013/08/21 09:23:29 (~ 15m ago)
celery_worker.4: up 2013/08/21 09:23:29 (~ 15m ago)
```

#### _heroku config_
```bash
=== brads-testing Config Vars
CLOUDAMQP_URL:              amqp://user:password@lemur.cloudamqp.com/instance
DATABASE_URL:               postgres://user:password@ec2-54-235-174-222.compute-1.amazonaws.com:5692/database
HEROKU_POSTGRESQL_GOLD_URL: postgres://user:password@ec2-54-235-174-222.compute-1.amazonaws.com:5692/database
IRONMQ_URL:                 ironmq://[IRON_PROJECT_ID]:[IRON_TOKEN_ID]@
PAPERTRAIL_API_TOKEN:       asdf1234ghjk
```

Database Setup (after first deploy)
-----------------------------------

```bash
git push heroku origin
heroku run python manage.py syncdb
```

Running Duplicate Task Test
---------------------------

```bash
heroku run python manage.py shell
> from app.tasks import run_test
> run_test()
```

Results
-------

#### _(via papertrail)_
```bash
Aug 21 09:12:01 brads-testing app/celery_master.3:  CONSOLE INFO --> Queue task: Task[id=77734, name=2.999, complete=False] 
Aug 21 09:12:53 brads-testing app/celery_worker.2:  CONSOLE INFO --> Handle task: Task[id=77734, name=2.999, complete=False] 
Aug 21 09:14:23 brads-testing app/celery_worker.2:  CONSOLE INFO --> Handle task: Task[id=77734, name=2.999, complete=True] 
Aug 21 09:14:23 brads-testing app/celery_worker.2:  CONSOLE ERROR --> Duplicate Task: Task[id=77734, name=2.999, complete=True]
```

Task[id=77734] is queued once, but run twice. 
In a test using 4 producers, 4 workers, running 4000 tasks, there will be ~100 of these occurences.

Note: This doesn't happen when using CloudAMQP (see settings_custom.py)
