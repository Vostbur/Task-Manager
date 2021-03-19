from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

from django.shortcuts import render


def index(request):
    return render(request, template_name='index.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'
