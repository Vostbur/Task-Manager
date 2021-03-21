from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Project, Task


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ('project_name',)
    success_url = reverse_lazy('projects')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ('project_name',)
    template_name = 'backend/project_update_form.html'
    success_url = reverse_lazy('projects')


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('projects')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ('task_name', 'is_done',)
    template_name = 'backend/task_update_form.html'
    success_url = reverse_lazy('projects')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('projects')
