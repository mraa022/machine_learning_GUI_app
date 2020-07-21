from django.shortcuts import render
from django.urls import  reverse_lazy,reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .forms import DataSetsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalCreateView,BSModalUpdateView
from django.db.models.fields.files import FieldFile
# from django.template.response import TemplateResponse

import requests
import pandas as pd
from . import models
from django.views import  generic

from .forms import DataSetsForm


def remove_column(dataframe):

	'''

	when scrapping dataframes from pages, panda's read_html() adds a 'unnamed' column that has a buch of nans. this 
	method removes that

	'''
	try:
		return dataframe.drop('Unnamed: 0',axis=1)
	except:
		return dataframe
	 

class DataSetsList(generic.ListView,LoginRequiredMixin):



	model = models.DataSets
	context_object_name = 'datasets'

	template_name = 'datasets/datasets_list.html'

	def get_queryset(self):


		return self.model.objects.filter(user__username = self.request.user.username)


class DatasetDetailView(generic.DetailView,LoginRequiredMixin):


	template_name = 'datasets/datasets_detail.html'
	model = models.DataSets

  
	def get_context_data(self, **kwargs):
		return {
			"DataFrame": self.get_object(),
			'dataset':  get_object_or_404(self.model, pk=self.kwargs.get('pk'))
		}

	def get_object(self):
      
			data = get_object_or_404(self.model, pk=self.kwargs.get('pk'))

			if data.link:
				return remove_column(pd.read_html(requests.get(data.link).text)[0]).head() 

			elif data.file:
				return pd.read_csv(data.file.path).head()

		
class CreateDatasetView(BSModalCreateView,LoginRequiredMixin):

	form_class = DataSetsForm
	template_name = 'datasets/create.html'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.file = self.request.FILES.get('file')
		
		self.object.save()
		return redirect('datasets:detail', pk=self.object.pk)					
	def get_form_kwargs(self): ## used to pass in the 'username' argument to the forms.py file


			kwargs = super(CreateDatasetView, self).get_form_kwargs()
			kwargs.update({

				'username': self.request.user.username,

				})
			
			return kwargs 
			

class UpdateDatasetView(BSModalUpdateView,LoginRequiredMixin):



	model = models.DataSets

	form_class = DataSetsForm
	template_name = 'datasets/update.html'

	context_object_name = 'form'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['id'] = self.kwargs.get('pk')

		return context
	def get_form_kwargs(self):
			kwargs = super(UpdateDatasetView, self).get_form_kwargs()
			kwargs.update({

				'update_view_running': True,
				'username':self.request.user.username,
				'pk':self.kwargs.get('pk'),
				'clear_previous_file':self.request.POST.get('clear-previous-file') # value of the clear file checkbox

				})
			
			return kwargs 
	
	def form_valid(self, form):
		
		return redirect('home')

	


	
	


	



