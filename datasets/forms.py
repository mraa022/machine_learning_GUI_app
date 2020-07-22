from django import  forms
import os
from django.db.models.fields.files import FieldFile
from bootstrap_modal_forms.forms import BSModalModelForm
from pandas import read_html
from django.core.files.storage import default_storage
import pandas as pd
from .models import DataSets
from machine_learning_gui import settings
import os
import requests


class Base():

	def raise_error(self):

		pass

class NotCsvFile(Base):

	def raise_error(self):

		raise forms.ValidationError('The file must be a csv file')

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

class DataSetsForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		self.username = kwargs.pop('username',None)
		self.update_view_running = kwargs.pop('update_view_running',None)
		self.pk = kwargs.pop('pk',None)
		self.previous_file_cleared = kwargs.pop('clear_previous_file',None)  # get value of the clear file checkbox in update view
		super().__init__(*args, **kwargs)

	class Meta():

		model = DataSets

		fields = ('file','link')

	def more_than_10_datasets_found(self):

		 return DataSets.objects.filter(user__username__iexact=self.username).count() == 10 and not self.update_view_running

	def saved_updated_data(self,file,url):

		current_dataset = DataSets.objects.get(pk=self.pk)  
		current_dataset.file = file
		current_dataset.link = url
		current_dataset.save()

	def file_exists(self,file):

		'''
		when updating, if the previous file is not updated, the input 'file' will return 'datasets/file-name', but if its updated it 
		will return 'file-name'. so there is no need to check if the file is a new one or a saved one.

		'''

		saved_file_name = ''.join(map(lambda x: '' if x in ['(',')'] else x,str(file))).replace(' ','_') # this is needed because django  removes () from file names when saving them
		file_path  = os.path.join('datasets',self.username+saved_file_name)
		base_dir = settings.media_dir
		full_path = os.path.join(base_dir,str(file_path))
		return  os.path.isfile(full_path) 
 
	def url_exists(self,url):
		return url and DataSets.objects.filter(user__username__iexact=self.username,link=url).exclude(pk=self.pk).exists()
		
	def no_tables_found(self,url):

		try:

			pd.read_html(requests.get(url).text)
		except:

			return True


	def clear_file_checkbox(self,cleaned_data):
		
		if self.update_view_running:  

			is_checkbox_checked = eval(self.previous_file_cleared.capitalize())# since its gotten from a javascript POST the first letter of the bool will not be capitalized and its also of type <str>
			current_file = cleaned_data.get('file')
			if is_checkbox_checked and  isinstance(current_file, FieldFile):  # if the current file is the  on saved in the model and the clear checkbox is clicked. clear it
				cleaned_data['file'] = None		

		return cleaned_data

	def file_is_csv(self,file):
		if file:
			return  file.name.endswith('.csv')
		return True
	def clear_file_field(self):
		
		self.current_dataset = DataSets.objects.get(pk=self.pk)

		self.current_dataset.file = None

		return self.current_dataset.save()
	def clean(self):

		self.cleaned_data = self.clear_file_checkbox(self.cleaned_data)  # remove the saved file if the checbox is checked off
		url = self.cleaned_data.get('link')
		file = self.cleaned_data.get('file')
		possible_errors = { 'RunOutOfSpace()':self.more_than_10_datasets_found(),
							'AllFieldsEmpty()': not url and not file,
							'AllFieldsFilled()': url and file,
							'FileNotUnique()': self.file_exists(file),
							'UrlNotUnique()':  self.url_exists(url),
							'NoTablesFound()': url and self.no_tables_found(url),
							'NotCsvFile()':   not self.file_is_csv(file)
		}
		for obj,error in possible_errors.items():

			if error:
				object = eval(obj)
				raise_error_message(object)

		
		if self.update_view_running:
			self.saved_updated_data(file,url)  # i did the saving here because if i did it in the update view it would override the functionality of the clear checkbox (save both file and url)




