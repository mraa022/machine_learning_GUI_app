from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .forms import DataSetsForm
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from machine_learning_gui import settings
from urllib.parse import unquote
import pandas as pd
from . import models
from django.views import  generic
import os
from django.core.validators import URLValidator





def dataset_saved_in_session(request):

	return request.COOKIES['dataset_location'] == '' and request.COOKIES['primary_key'] == ''

def dataset_location_is_url(dataset_location):
	
	url_validator = URLValidator()

	try:
		return url_validator(dataset_location) == None # it returns none if its a valid url
	except:
		return False

def filtered_data_frame(request,dataframe):
	selected_columns  = unquote(request.COOKIES['categorical_columns']).split(',') + unquote(request.COOKIES['numerical_columns']).split(',') + [unquote(request.COOKIES['label_column'])]
	selected_columns = list(filter(None,selected_columns))  # if there are no categorical or numerical remove the epmpty spaces
	dataframe = dataframe[selected_columns]
	return dataframe

def get_dataframe_given_url_or_file(dataframe_location):

	if dataset_location_is_url(dataframe_location):

			dataframe = remove_column(pd.read_html(requests.get(dataframe_location).text)[0]) 
	else:
			dataframe = pd.read_csv(dataframe_location)

	return dataframe

def get_dataframe(request):

		if dataset_saved_in_session(request):

			dataset_location = unquote(request.session['dataset_location'])# its encoded in percents
			dataframe  = get_dataframe_given_url_or_file(dataset_location)
		else:  

			dataset_location = unquote(request.COOKIES['dataset_location'])  # its encoded in percents		
			dataframe  = get_dataframe_given_url_or_file(dataset_location)

		return dataframe.columns,dataframe


def remove_column(dataframe):

	'''

	when scrapping dataframes from pages, panda's read_html() adds a 'unnamed' column that has a buch of nans. this 
	method removes that

	'''
	try:
		return dataframe.drop('Unnamed: 0',axis=1)
	except:
		return dataframe
	
def return_customized_dataframe(dataframe,categorical_columns):
	'''
		drop rows that have missing cells, and onehot encode the categorical columns
	'''
	categorical_columns = list(filter(None,categorical_columns))  # return an empty list if there are no categorical columns. i.e  [''] = [] or ['','some categorical column'] = ['some categorical column']
	dataframe = dataframe.dropna()
	dataframe = pd.get_dummies(data = dataframe, columns =categorical_columns,drop_first=True) if categorical_columns else dataframe
	return dataframe
class Not_logged_in(generic.TemplateView):

	template_name = 'datasets/not_logged_in.html'

class ClassificationOrRegression(generic.TemplateView):
	template_name = 'datasets/regression_or_classification.html'


class DataSetsList(LoginRequiredMixin,generic.ListView):

	model = models.DataSets
	context_object_name = 'datasets'
	login_url = 'datasets:login_first'

	def get_queryset(self):
		return self.model.objects.filter(user__username = self.request.user.username)

class DatasetDetailView(LoginRequiredMixin,generic.DetailView):


	template_name = 'datasets/datasets_detail.html'
	model = models.DataSets

	login_url = 'datasets:login_first'

	def get_context_data(self, **kwargs):
		dataframe,num_rows,num_nans = self.get_object()
		return {
			"DataFrame": dataframe,
			'dataset':  get_object_or_404(self.model, pk=self.kwargs.get('pk')),
			'num_rows':num_rows,
			'num_nans':num_nans

		}

	def get_object(self):
      
			data = get_object_or_404(self.model, pk=self.kwargs.get('pk'))

			if data.link:
				dataframe = remove_column(pd.read_html(requests.get(data.link).text)[0])

			elif data.file:
				dataframe= pd.read_csv(data.file.path)

			return dataframe.head(),dataframe.shape[0],len(dataframe)-len(dataframe.dropna())

		
class CreateDatasetView(LoginRequiredMixin,generic.CreateView):

	form_class = DataSetsForm
	template_name = 'datasets/create.html'
	login_url = 'datasets:login_first'
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
			

class UpdateDatasetView(LoginRequiredMixin,generic.UpdateView):



	model = models.DataSets

	form_class = DataSetsForm
	template_name = 'datasets/update.html'

	context_object_name = 'form'
	login_url = 'datasets:login_first'
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


class ChooseNewDataset(generic.CreateView):

	form_class = DataSetsForm
	template_name = 'datasets/choose_new_dataset.html'

	def form_valid(self, form):

		self.object = form.save(commit=False)

		if not self.request.session or not self.request.session.session_key:
			self.request.session.save()


		if self.object.file:
			temparory_location = os.path.join(settings.MEDIA_ROOT,'datasets/temp_file.csv')
			with open(temparory_location ,'wb+') as f:
				for chunk in self.request.FILES['file'].chunks():
					f.write(chunk)
			self.request.session['dataset_location'] = temparory_location
		else:
			self.request.session['dataset_location'] = self.object.link

		return redirect('datasets:list')

	def get_form_kwargs(self):
			kwargs = super(ChooseNewDataset, self).get_form_kwargs()
			kwargs.update({

				'saved_to_session_instead':True

				})
			
			return kwargs 

class DataSetCategoricalColumns(generic.TemplateView):

	template_name = 'datasets/categorical_columns.html'

	

	def get_context_data(self, **kwargs):  

		context = super().get_context_data(**kwargs)
		numerical_columns = unquote(self.request.COOKIES['numerical_columns'])
		context['dataframe_columns'] = get_dataframe(self.request)[0] 
		context['dataframe'] = get_dataframe(self.request)[1]
		context['numerical_columns'] = numerical_columns  # used to higlight them in the grid

		return context

class DataSetNumericalColumns(generic.TemplateView):

	template_name = 'datasets/numerical_columns.html'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs) 
		context['dataframe_columns'] = get_dataframe(self.request)[0]  # it get_dataframe() returns the dataframe columns and the dataframe
		context['dataframe'] = get_dataframe(self.request)[1]

		return context

class DataSetLabelColumn(generic.TemplateView):
	template_name = 'datasets/label_column.html'
	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['dataframe_columns'] = get_dataframe(self.request)[0]
		context['dataframe'] = get_dataframe(self.request)[1]

		return context

class CurrentDataSet(generic.TemplateView):

	template_name = 'datasets/current_dataset.html'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		
		context['dataframe'] = get_dataframe(self.request)[1].head(10)

		return context

class ShowSelectedColumns(generic.TemplateView):
	template_name = 'datasets/show_selected_columns.html'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		numerical_columns = unquote(self.request.COOKIES['numerical_columns'])
		categorical_columns = unquote(self.request.COOKIES['categorical_columns'])
		context['dataframe_columns'] = get_dataframe(self.request)[0] 
		context['dataframe'] = get_dataframe(self.request)[1].head(10)
		context['numerical_columns'] = numerical_columns  # used to higlight them in the grid
		context['categorical_columns'] = categorical_columns


		return context
class NeuralNetworkDiagramAndKerasModel(generic.TemplateView):  

	template_name = 'datasets/model.html'
	def get_context_data(self, **kwargs):

		# all this method is needed for is access to the session and cookies (nothing is added to the context dict)
		context = super().get_context_data(**kwargs)
		media_path = os.path.join(settings.MEDIA_ROOT,'datasets/')
		dataframe  = get_dataframe_given_url_or_file(unquote(self.request.COOKIES['dataset_location'])) if not dataset_saved_in_session(self.request) else get_dataframe_given_url_or_file(unquote(self.request.session['dataset_location']))
		dataframe = filtered_data_frame(self.request,dataframe)  # only return the selected columns
		categorical_columns = unquote(self.request.COOKIES['categorical_columns']).split(',')
		dataframe = return_customized_dataframe(dataframe,categorical_columns) # remove nans and onehot encode categorical columns
		dataframe.to_csv(os.path.join(media_path,self.request.COOKIES['sessionid']+'formated_dataset.csv'))

		return context


class Main(generic.TemplateView):

	template_name = 'datasets/Main.html'
	
	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['id'] = self.kwargs.get('pk')

		return context


	



