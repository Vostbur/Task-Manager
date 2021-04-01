from django.urls import path, include

from .views import ProjectListAPI, ProjectDetailAPI, TaskListAPI, TaskDetailAPI

urlpatterns = [
    path('projects/', ProjectListAPI.as_view(), name='project-list-api'),
    path('projects/<int:pk>/', ProjectDetailAPI.as_view(), name='project-detail-api'),
    path('tasks/', TaskListAPI.as_view(), name='task-list-api'),
    path('tasks/<int:pk>/', TaskDetailAPI.as_view(), name='task-detail-api'),
    path('api-auth/', include('rest_framework.urls')),
]
