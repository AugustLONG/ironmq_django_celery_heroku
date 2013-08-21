from django.http import HttpResponse


def index(request):
    return HttpResponse('ironmq_django_celery_heroku')
