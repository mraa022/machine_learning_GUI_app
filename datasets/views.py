from django.shortcuts import render

import pandas as pd
from . import models
from django.views import  generic

from.forms import DatasetsForm
# Create your views here.


class DataSetsList(generic.ListView):



	model = models.DataSets
	context_object_name = 'datasets'

	template_name = 'datasets/datasets_list.html'

	def get_queryset(self):

		return self.model.objects.all()



class DatasetDetailView(generic.DetailView):


	context_object_name = 'dataset'
	template_name = 'datasets/datasets_detail.html'
	model = models.DataSets
	# def get_context_data(self, **kwargs):
 #        # Call the base implementation first to get a context
	# 	context = super().get_context_data(**kwargs)
	# 	# Add in a QuerySet of all the books
	# 	print(self.model.objects.get('file'),'ffffffffffffffffff')
	# 	context['dataframe'] = pd.read_table(self.kwargs.get('file'))[0].head() if self.file else pd.read_table(self.kwargs.get('link'))[0].head()
	# 	context['dataframe'] = pd.to_html(context['dataframe'])
	# 	return context

	