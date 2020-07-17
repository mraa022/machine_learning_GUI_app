from django import  forms
import os
from bootstrap_modal_forms.forms import BSModalModelForm
from pandas import read_html
from django.core.files.storage import default_storage
import pandas as pd
from .models import DataSets
from django.contrib.auth import get_user_model
from machine_learning_gui import settings
import os
import requests

User = get_user_model()

class Base():

	def raise_error(self):

		pass

class AllFieldsFilled(Base):

	def raise_error(self):
		raise forms.ValidationError(u"Only one of the fields needs to be filled")

class AllFieldsEmpty(Base):

	def raise_error(self):

		raise forms.ValidationError(u"One of the fields  needs to be filled")

class FileNotUnique(Base):

	def raise_error(self):

		raise forms.ValidationError(u"A dataset with that file already exists")

class UrlNotUnique(Base):

	def raise_error(self):

		raise forms.ValidationError(u"A data set with that link already exists")

class RunOutOfSpace(Base):

	def raise_error(self):

		raise forms.ValidationError('You run out of space! go the the DataSets page and replace one')

class NoTablesFound(Base):

	def raise_error(self):

		raise forms.ValidationError('The website you provided does not have any tables')

def raise_error_message(obj):

	obj.raise_error()

class DataSetsForm(BSModalModelForm):

	def __init__(self, *args, **kwargs):
		self.username = kwargs.pop('username',None)
		self.update_view_running = kwargs.pop('update_view_running',None),
		super().__init__(*args, **kwargs)

	class Meta():

		model = DataSets

		fields = ('file','link')

		


	def more_than_10_datasets_found(self):

		 return DataSets.objects.filter(user__username__iexact=self.username).count() == 10 and not self.update_view_running

		 
	def file_exists(self,file):

		saved_file_name = ''.join(map(lambda x: '' if x in ['(',')'] else x,str(file))).replace(' ','_') # this is needed because django  removes () from file names when saving them
		user_and_file = str(self.username)+ ''.join(saved_file_name) 
		base_dir = settings.media_dir
		file_path = os.path.join('datasets',str(user_and_file))
		full_path = os.path.join(base_dir,str(file_path))
		return  os.path.isfile(full_path) 

	def url_exists(self,url):

		return url and (DataSets.objects.filter(user__username__iexact=self.username,link=url).exists())

	def no_tables_found(self,url):

		try:

			pd.read_html(requests.get(url).text)
		except:

			return True

	def clean(self):
		url = self.cleaned_data.get('link')
		file = self.cleaned_data.get('file')
		print('kkkkkkkkkkkkkkk',file)
		possible_errors = { 'RunOutOfSpace()':self.more_than_10_datasets_found(),
							'AllFieldsEmpty()': not url and not file,
							'AllFieldsFilled()': url and file,
							'FileNotUnique()': self.file_exists(file),
							'UrlNotUnique()':  self.url_exists(url),
							'NoTablesFound()': url and self.no_tables_found(url)

		}
		
		for obj,error in possible_errors.items():

			if error:
				print('kkkkkkkkkkkkkkk',obj)
				object = eval(obj)
				raise_error_message(object)
