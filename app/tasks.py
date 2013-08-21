import logging

from celery import task

from django.conf import settings

from models import Task


logger = logging.getLogger(__name__)


# Test Runner

def run_test(num_masters=4, num_tasks=100000):
    tasks_per_master = num_tasks / num_masters
    for m in range(num_masters):
        queue_task_creation(str(m), tasks_per_master)


# Master Task Queue-er

def queue_task_creation(master_name, num_tasks):
    handle_task_creation(master_name, num_tasks)

@task(queue=settings.QUEUES.MASTER)
def handle_task_creation(master_name, num_tasks):
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

    if not task.completed:
        # Good
        task.completed = True
        task.save()
        return

    # Bad
    logger.error('DUPLICATE TASK: %s' % str(task))
