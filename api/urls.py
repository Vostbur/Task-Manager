from django.urls import path

from .views import ProjectListAPI

urlpatterns = [
    path('', ProjectListAPI.as_view(), name='project-list-api')
]
