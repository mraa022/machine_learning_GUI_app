from django.shortcuts import render
from django.shortcuts import get_object_or_404
# from django.template.response import TemplateResponse


import pandas as pd
from . import models
from django.views import  generic

from.forms import DatasetsForm
# Create your views here.


def remove_column(dataframe):

	'''

	when scrapping dataframes from pages, panda's read_html() adds a 'unnamed' column that has a buch of nans. this 
	method removes that

	'''

	return dataframe.drop('Unnamed: 0',axis=1)
	 



class DataSetsList(generic.ListView):



	model = models.DataSets
	context_object_name = 'datasets'

	template_name = 'datasets/datasets_list.html'

	def get_queryset(self):


		return self.model.objects.filter(user__username = self.request.user.username)




class DatasetDetailView(generic.DetailView):




	
	template_name = 'datasets/datasets_detail.html'
	model = models.DataSets



	# def get(self, request, *args, **kwargs):
	# 	return render(request, self.template_name,self.get_context_data())

  
	def get_context_data(self, **kwargs):
		return {
			"DataFrame": self.get_object(),
			'dataset':  get_object_or_404(self.model, pk=self.kwargs.get('pk'))
		}

	def get_object(self):
      
			data = get_object_or_404(self.model, pk=self.kwargs.get('pk'))


			
			return remove_column(pd.read_html(data.get_file_or_url_path())[0]).head() if data.link else pd.read_csv(data.get_file_or_url_path()).head()

		
		
		# return pd.read_table(data)[0]
		




	