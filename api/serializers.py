from rest_framework import serializers

from backend.models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name']


class TaskSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(user=user)

    class Meta:
        model = Task
        fields = ['id', 'task_name', 'is_done', 'project']
