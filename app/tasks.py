import logging

from celery import task

from django.conf import settings

from models import Task


logger = logging.getLogger(__name__)


def queue_task(task):
    handle_task.delay(task.id)


@task(queue=settings.QUEUES.WORKER)
def handle_task(task_id):
    task = Task.objects.get(id=task_id)

    if not task.completed:
        # Good
        task.completed = True
        task.save()
        return

    # Bad
    logger.error('REPEAT THING')
