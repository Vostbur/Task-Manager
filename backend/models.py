from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    project_name = models.CharField(max_length=150, default='', verbose_name='Проект')
    user = models.ForeignKey(get_user_model(), null=True,
                             on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.project_name[:50]


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    task_name = models.CharField(max_length=250, default='', verbose_name='Задача')
    is_done = models.BooleanField(default=False, verbose_name='Выполнено')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.task_name[:50]
