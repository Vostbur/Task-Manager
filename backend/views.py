from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'index.html'
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    extra_context = {'projects': Project.objects.all()}
    context_object_name = 'project'


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project-detail', kwargs={'pk': 1})

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'
