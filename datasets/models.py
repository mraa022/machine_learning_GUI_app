from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import os
# Create your models here.

def validate_file_extension(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError(u'Only files of type .csv')


def path_and_rename(instance, filename):
    upload_to = "datasets"
    Format =  instance.user.username + str(instance.file) 
    return os.path.join(upload_to, Format)


User = get_user_model()

class DataSets(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	link = models.URLField(blank=True,null=True)
	file = models.FileField(upload_to=path_and_rename,blank=True,validators=[validate_file_extension],null=True,default=None)
	# slug = models.SlugField(blank=True)

	

	def get_absolute_url(self):

		return reverse('datasets:detail', kwargs={'pk':self.pk})

	def __str__(self):


		return  self.user.username+ ' ' + str(self.pk)


	def title(self):
		return "<strong> <i> File Name: </i></strong> " + str(os.path.basename(self.file.name)) if  self.file else " <strong> <i>URL: </i></strong> " + str(self.link)

