from rest_framework import generics

from backend.models import Project, Task
from backend.mixins import ProjectMixin, TaskMixin

from .serializers import ProjectSerializer, TaskSerializer


class ProjectListAPI(ProjectMixin, generics.ListCreateAPIView):
    model = Project
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListAPI(TaskMixin, generics.ListCreateAPIView):
    model = Task
    serializer_class = TaskSerializer
