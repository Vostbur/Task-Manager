from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=250, default='', verbose_name='Проект')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name[:50]


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default='', verbose_name='Задача')
    date = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name[:50]

