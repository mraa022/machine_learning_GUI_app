from django import  forms
import os
from django.core.files.storage import default_storage

from .models import DataSets
from django.contrib.auth import get_user_model
from machine_learning_gui import settings
import os








User = get_user_model()






class DataSetsForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		self.username = kwargs.pop('username',None)
		super().__init__(*args, **kwargs)

	class Meta():

		model = DataSets

		fields = ('link','file')

		widgets = {

			'link':forms.URLInput(attrs={'class':'link-text-area'}),
			# 'file':forms.FileInput(attrs = {'class':'file-field'})
		}


	def file_exists(self,file):

		user_and_file = self.username+str(file)
		base_dir = settings.media_dir
		file_path = os.path.join('datasets',str(user_and_file))
		full_path = os.path.join(base_dir,str(file_path))

		return True if os.path.isfile(full_path) else False

	def clean(self):

		
		url = self.cleaned_data.get('link')
		file = self.cleaned_data.get('file')
		print(' mmmmmmmmmmmmmmmm',self.username)
		file_with_media_dir = os.path.join('DataSets',str(file))  # this is needed when checking if a file exists in the database.the variable 'file' returns the file name while the file field in the model returns the media dir name / filename
		if DataSets.objects.filter(user__username__iexact=self.username).count() >10:

			raise forms.ValidationError(u"You run out of space. go to the 'DataSets' page and replace one ")

		elif not url and not file:

			raise forms.ValidationError(u'One of the fileds MUST BE FILLED')

		elif url and file:

			raise forms.ValidationError(u"Only one of the fields needs to be filled")

		elif url and (DataSets.objects.filter(user__username__iexact=self.username,link=url).exists()):
			
			
			raise forms.ValidationError('A DataSets with that link  already exists')

		elif  file and self.file_exists(file):
			
			raise forms.ValidationError('A DataSets with that file path  already exists')


		

