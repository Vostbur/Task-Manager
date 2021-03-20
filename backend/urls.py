from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='projects'),
    path('create', views.ProjectCreateView.as_view(), name='project-create'),
    path('task/create', views.TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/delete', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:pk>/update', views.ProjectUpdateView.as_view(), name='project-update'),
    path('task/<int:pk>/delete', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/update', views.TaskUpdateView.as_view(), name='task-update'),
]
