from rest_framework import generics

from backend.models import Project, Task

from .serializers import ProjectSerializer, TaskSerializer


class ProjectListAPI(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
