DEBUG = False
WSGI_APPLICATION = 'wsgi.application'
ROOT_URLCONF = 'app.urls'

# Celery Queues.
class QUEUES:
    MASTER = 'master'
    WORKER = 'worker'

CELERY_DEFAULT_QUEUE = QUEUES.WORKER

CELERY_QUEUES = {
    QUEUES.MASTER: {
        'exchange': QUEUES.MASTER,
        'binding_key': QUEUES.MASTER,
    },
    QUEUES.WORKER: {
        'exchange': QUEUES.WORKER,
        'binding_key': QUEUES.WORKER
    }
}


# Heroku Postgres config
import dj_database_url
DATABASES = {'default': dj_database_url.config()}


# Celery (via IronMQ)
import iron_celery
#BROKER_URL = get_env_variable('IRONMQ_URL')
BROKER_URL = 'ironmq://521316ab49555e000d000003:Sm28C1eqTlrlC3gcC9aycUY9Jgs@'
BROKER_POOL_LIMIT = 1

INSTALLED_APPS = (
    'app'
)
