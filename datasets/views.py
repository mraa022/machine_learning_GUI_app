from django.shortcuts import render


from . import models
from django.views import  generic

from.forms import DatasetsForm
# Create your views here.


class DataSetsList(generic.ListView):



	model = models.DatasSets
	context_object_name = 'datasets'

	template_name = 'datasets/datasets_list.html'

	def get_queryset(self):

		return self.model.objects.all()


