from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Project, Task


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'


class ProjectCreateView(CreateView):
    model = Project
    fields = ('project_name',)
    success_url = reverse_lazy('projects')


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ('project_name',)
    template_name = 'backend/project_update_form.html'
    success_url = reverse_lazy('projects')


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('projects')


class TaskCreateView(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('projects')


class TaskUpdateView(UpdateView):
    model = Task
    fields = ('task_name', 'is_done',)
    template_name = 'backend/task_update_form.html'
    success_url = reverse_lazy('projects')


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('projects')

