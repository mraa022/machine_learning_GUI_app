from django.shortcuts import render
from django.views.generic import CreateView
from .forms import userCreateForm
from django.urls import  reverse_lazy
# Create your views here.

class SignUp(CreateView):

	context_object_name = 'form'
	template_name = 'accounts/signup.html'

	form_class = userCreateForm
	success_url = reverse_lazy('accounts:login')

	