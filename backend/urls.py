from django.urls import path

from .views import SignUpView, ProjectListView, ProjectDetailView, ProjectDelete

urlpatterns = [
    path('', ProjectListView.as_view(), name='home'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='project-delete'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
