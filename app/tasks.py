import logging

from celery import task

from django.conf import settings
from django.db import transaction

from models import Task


logger = logging.getLogger(__name__)


# Test Runner

def run_test(num_masters=4, num_tasks=100000):
    tasks_per_master = num_tasks / num_masters
    for m in range(num_masters):
        queue_task_creation(str(m), tasks_per_master)


# Master Task Queue-er

def queue_task_creation(master_name, num_tasks):
    handle_task_creation.delay(master_name, num_tasks)

@task(queue=settings.QUEUES.MASTER)
def handle_task_creation(master_name, num_tasks):
    logger.error('Create tasks, Master:%s, Tasks:%s' % (master_name, num_tasks))

    with transaction.autocommit():
        for x in range(num_tasks):
            # Create task
            task_name = '%s-%s' % (master_name, x)
            task = Task(name=task_name)
            task.save()

            # Queue it for "completion"
            queue_task(task)


# Task Worker

def queue_task(task):
    handle_task.delay(task.id)

@task(queue=settings.QUEUES.WORKER)
def handle_task(task_id):
    task = Task.objects.get(id=task_id)

    if not task.complete:
        # Good
        with transaction.autocommit():
            task.complete = True
            task.save()
            return

    # Bad
    logger.error('Duplicate Task: %s' % str(task))
