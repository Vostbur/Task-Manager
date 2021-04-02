from django.urls import path, include

from rest_framework.routers import SimpleRouter

# from .views import ProjectListAPI, ProjectDetailAPI, TaskListAPI, TaskDetailAPI
from .views import ProjectViewSet, TaskViewSet

router = SimpleRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    # path('projects/', ProjectListAPI.as_view(), name='project-list-api'),
    # path('projects/<int:pk>/', ProjectDetailAPI.as_view(), name='project-detail-api'),
    # path('tasks/', TaskListAPI.as_view(), name='task-list-api'),
    # path('tasks/<int:pk>/', TaskDetailAPI.as_view(), name='task-detail-api'),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns += router.urls
