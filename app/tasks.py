import logging

from celery import task

from django.conf import settings
from django.db import transaction

from models import Task


logger = logging.getLogger(__name__)


# Test Runner

def run_test(num_masters=4, num_tasks=4000):
    # Start by deleting all Task objects
    with transaction.commit_on_success():
        Task.objects.all().delete()

    tasks_per_master = num_tasks / num_masters
    for m in range(num_masters):
        queue_task_creation(str(m), tasks_per_master)


# Master Task Queue-er

def queue_task_creation(master_name, num_tasks):
    handle_task_creation.delay(master_name, num_tasks)

@task(queue=settings.QUEUES.MASTER)
def handle_task_creation(master_name, num_tasks):
    logger.info('Create tasks, Master:%s, Tasks:%s' % (master_name, num_tasks))

    for x in range(num_tasks):
        # Create task
        with transaction.commit_on_success():
            task_name = '%s.%s' % (master_name, x)
            task = Task(name=task_name)
            task.save()

        # Queue it for "completion"
        queue_task(task)

    logger.info('Create tasks complete, Master:%s' % (master_name))


# Task Worker

def queue_task(task):
    #handle_task.delay(task.id)
    handle_task.apply_async(args=[task.name], iron_mq_timeout=90)

@task(queue=settings.QUEUES.WORKER)
def handle_task(task_name):
    task = Task.objects.get(name=task_name)

    logger.info('Handle task: %s' % str(task))

    if task.complete:
        # Bad
        logger.error('Duplicate Task: %s' % str(task))

    # Good
    with transaction.commit_on_success():
        task.complete = True
        task.save()
