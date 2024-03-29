from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=256)
    complete = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Task[id=%d, name=%s, complete=%s]' % (self.id, self.name, self.complete)
