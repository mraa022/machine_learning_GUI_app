from django import  forms

from .models import DatasSets

class DatasetsForm(forms.ModelForm):

	model = DatasSets

	fields = ('__all__')

	def clean(self):

		cleaned_data = self.cleaned_data()

		url = cleaned_data.get('link')
		file = cleaned_data.get('file') 

		if not (url and file):

			raise forms.ValidationError('One of the fileds MUST BE FILLED')

