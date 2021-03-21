from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Project, Task
from .mixins import ProjectMixin, TaskMixin


class ProjectListView(LoginRequiredMixin, ProjectMixin, ListView):
    model = Project
    context_object_name = 'projects'


class ProjectCreateView(LoginRequiredMixin, ProjectMixin, CreateView):
    model = Project
    fields = ('project_name',)
    success_url = reverse_lazy('projects')


class ProjectUpdateView(LoginRequiredMixin, ProjectMixin, UpdateView):
    model = Project
    fields = ('project_name',)
    template_name = 'backend/project_update_form.html'
    success_url = reverse_lazy('projects')


class ProjectDeleteView(LoginRequiredMixin, ProjectMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects')


class TaskCreateView(LoginRequiredMixin, TaskMixin, CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('projects')


class TaskUpdateView(LoginRequiredMixin, TaskMixin, UpdateView):
    model = Task
    fields = ('task_name', 'is_done',)
    template_name = 'backend/task_update_form.html'
    success_url = reverse_lazy('projects')


class TaskDeleteView(LoginRequiredMixin, TaskMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('projects')
