import os
from django.core.exceptions import ImproperlyConfigured
def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
    raise ImproperlyConfigured(error_msg)


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
if True:
    BROKER_URL = get_env_variable('IRONMQ_URL')
    BROKER_POOL_LIMIT = 1

    import djcelery
    import iron_celery

    djcelery.setup_loader()

else:
    BROKER_URL = get_env_variable('CLOUDAMQP_URL')
    BROKER_POOL_LIMIT = 1

    import djcelery
    djcelery.setup_loader()


INSTALLED_APPS = (
    'djcelery',
    'gunicorn',
    'app'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console': {
            'format': 'CONSOLE %(levelname)s --> %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console':{
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}
