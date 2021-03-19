from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.cache import cache


class Project(models.Model):
    name = models.CharField(max_length=250, default='', verbose_name='Проект')
    # active = models.BooleanField(default=True)

    def __str__(self):
        return self.name[:50]


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default='', verbose_name='Задача')
    date = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name[:50]


@receiver(post_delete, sender=Project)
def clear_cache(sender, instance, **kwargs):
    cache.clear()
