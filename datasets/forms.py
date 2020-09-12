from django import  forms
import os
from django.db.models.fields.files import FieldFile
from pandas import read_html
import pandas as pd
from .models import DataSets
from machine_learning_gui import settings
import requests

class Base():

	def raise_error(self):

		raise NotImplementedError('IT must be inherited')

class NotCsvFile(Base):

	def raise_error(self):

		raise forms.ValidationError('The file must be a csv file')

class AllFieldsFilled(Base):

	def raise_error(self):
		raise forms.ValidationError("Only one of the fields needs to be filled")

class AllFieldsEmpty(Base):

	def raise_error(self):

		raise forms.ValidationError("One of the fields  needs to be filled")

class FileNotUnique(Base):

	def raise_error(self):

		raise forms.ValidationError("A dataset with that file already exists")

class UrlNotUnique(Base):

	def raise_error(self):

		raise forms.ValidationError("A data set with that link already exists")

class RunOutOfSpace(Base):

	def raise_error(self):

		raise forms.ValidationError('You run out of space! go to the DataSets page and replace one')

class NoTablesFound(Base):

	def raise_error(self):

		raise forms.ValidationError('The website you provided does not have any tables')


class InvalidCsvFile(Base):
	def raise_error(self):

		raise forms.ValidationError('The file you provided is invalid')

def raise_error_message(obj):

	obj.raise_error()

class DataSetsForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		self.username = kwargs.pop('username',None)
		self.update_view_running = kwargs.pop('update_view_running',None)
		self.pk = kwargs.pop('pk',None)
		self.previous_file_cleared = kwargs.pop('clear_previous_file',None)  # get value of the clear file checkbox in update view
		self.saved_to_session_instead = kwargs.pop('saved_to_session_instead',None)
		super().__init__(*args, **kwargs)

	class Meta():

		model = DataSets

		fields = ('file','link')

	def more_than_10_datasets_found(self):

		 return DataSets.objects.filter(user__username__iexact=self.username).count() == 10 and not self.update_view_running # datasets can still be saved in update view

	def save_updated_data(self,file,url):

		current_dataset = DataSets.objects.get(pk=self.pk)  
		current_dataset.file = file
		current_dataset.link = url
		current_dataset.save()

	def file_exists(self,file): # returns if the chosen file is already taken

		'''
		when updating a dataset that had a file, if the previous file is not updated, the file-field input will return 'datasets/file-name', but if its updated it 
		will return 'file-name'. so there is no need to check if the file is a new one or a saved one.

		'''
		if not self.saved_to_session_instead: # if the person chose an existing dataset instead of a new one (if you chose a new dataset, the file/link does not have to be unique)
			base_dir = settings.media_dir
			saved_file_name = ''.join(map(lambda x: '' if x in ['(',')'] else x,str(file))).replace(' ','_') # removes () and replaces spaces with _, this is how django saves files
			file_path  = os.path.join('datasets',self.username+saved_file_name)
			full_path = os.path.join(base_dir,str(file_path))
			return  os.path.isfile(full_path) 


	def url_exists(self,url):

		return  not self.saved_to_session_instead and url and DataSets.objects.filter(user__username__iexact=self.username,link=url).exclude(pk=self.pk).exists() ## the 'exclude' is there if the user edits a dataset but does not make any changes, and saves it
		
	def no_tables_found(self,url):

		try:

			pd.read_html(requests.get(url).text)
		except:

			return True


	def clear_file_checkbox(self,cleaned_data): 

		'''
			implements django's clear file checkbox functionality. this functionality is implemented because when posting,
			ajax is used, and also form.PreventDefault() is used.
		'''
		
		if self.update_view_running:  # the checkbox is only in the update view

			is_checkbox_checked = eval(self.previous_file_cleared.capitalize())# since its gotten from a javascript POST the first letter of the bool will not be capitalized and its also of type <str>. converts 'false/true' to False/True
			current_file = cleaned_data.get('file')
			if is_checkbox_checked and  isinstance(current_file, FieldFile):  # if the current file is the  one saved in the model and the clear checkbox is clicked. clear it
				cleaned_data['file'] = None		

		return cleaned_data


	def file_is_csv(self,file):
		return str(file).endswith('.csv')
	def csv_file_valid(self,file):
		
		
		try:
			pd.read_csv(file)
			return True
		except:
			return False
		

	def clean(self):

		self.cleaned_data = self.clear_file_checkbox(self.cleaned_data)  # remove the saved file if the checbox is checked off
		url = self.cleaned_data.get('link')
		file = self.cleaned_data.get('file')
		possible_errors = { 'RunOutOfSpace()':self.more_than_10_datasets_found(),
							'AllFieldsEmpty()': not url and not file,
							'AllFieldsFilled()': url and file ,
							'FileNotUnique()': self.file_exists(file),
							'UrlNotUnique()':  self.url_exists(url),
							'NoTablesFound()': url and self.no_tables_found(url),
							'NotCsvFile()':   file and not self.file_is_csv(file),
							"InvalidCsvFile()": file and not self.csv_file_valid(file)
		}

		for obj,error in possible_errors.items():
			if error:
				
				object = eval(obj)

				raise_error_message(object)

		
		if self.update_view_running:
			self.save_updated_data(file,url)  # i did the saving here because if i did it in the update view it would override the functionality of the clear checkbox

