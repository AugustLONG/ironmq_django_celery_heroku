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
BROKER_URL = get_env_variable('IRONMQ_URL')
BROKER_POOL_LIMIT = 1

import djcelery
import iron_celery

djcelery.setup_loader()


INSTALLED_APPS = (
    'djcelery',
    'app'
)
