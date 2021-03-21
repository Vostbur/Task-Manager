from .models import Project, Task


class ProjectMixin:
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class TaskMixin:
    def get_queryset(self):
        return Task.objects.filter(project__user=self.request.user)
