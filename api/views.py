# from rest_framework import generics
from rest_framework import viewsets

from backend.models import Project, Task
from backend.mixins import ProjectMixin, TaskMixin

from .mixins import ProjectAPIMixin
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(ProjectMixin, ProjectAPIMixin, viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet(TaskMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# class ProjectListAPI(ProjectMixin, ProjectAPIMixin, generics.ListCreateAPIView):
#     model = Project
#     serializer_class = ProjectSerializer
#
#
# class ProjectDetailAPI(ProjectMixin, ProjectAPIMixin, generics.RetrieveUpdateDestroyAPIView):
#     model = Project
#     serializer_class = ProjectSerializer


# class TaskListAPI(TaskMixin, generics.ListCreateAPIView):
#     model = Task
#     serializer_class = TaskSerializer
#
#
# class TaskDetailAPI(TaskMixin, generics.RetrieveUpdateDestroyAPIView):
#     model = Task
#     serializer_class = TaskSerializer
