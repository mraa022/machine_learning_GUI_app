from django.shortcuts import render
from django.urls import  reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import DataSetsForm
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.template.response import TemplateResponse


import pandas as pd
from . import models
from django.views import  generic

from .forms import DataSetsForm
# Create your views here.

def file_already_exists(filename):

	pass




def remove_column(dataframe):

	'''

	when scrapping dataframes from pages, panda's read_html() adds a 'unnamed' column that has a buch of nans. this 
	method removes that

	'''
	return dataframe.drop('Unnamed: 0',axis=1)
	 

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
				return remove_column(pd.read_html(data.link)[0]).head() 

			
			return pd.read_csv(data.file.path).head()

		
class CreateDatasetView(generic.CreateView,LoginRequiredMixin):

	form_class = DataSetsForm
	template_name = 'datasets/create.html'




	def form_valid(self, form):
		
		self.object = form.save(commit=False)
		

		self.object.user = self.request.user
		if 'file' in self.request.FILES:



			self.object.file = self.request.FILES['file']
			

	
		self.object.save()
		

		return super().form_valid(form)


	def get_form_kwargs(self):


			kwargs = super(CreateDatasetView, self).get_form_kwargs()
			kwargs.update({

				'username': self.request.user.username,

				})
			
			return kwargs 
			

class UpdateDatasetView(generic.UpdateView,LoginRequiredMixin):



	model = models.DataSets

	form_class = DataSetsForm
	# fields = ['link','file']
	template_name = 'datasets/update.html'

	context_object_name = 'form'

	success_url = reverse_lazy('home')

	def get_form_kwargs(self):


			kwargs = super(UpdateDatasetView, self).get_form_kwargs()
			kwargs.update({

				'username': self.request.user.username,
				'update_view_running': True

				})
			
			return kwargs 
	

	


	
	


	



