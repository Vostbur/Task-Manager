from django.urls import path, include

from .views import ProjectListAPI, TaskListAPI

urlpatterns = [
    path('projects/', ProjectListAPI.as_view(), name='project-list-api'),
    path('tasks/', TaskListAPI.as_view(), name='task-list-api'),
    path('api-auth/', include('rest_framework.urls')),
]
