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
    path = "datasets"
    Format =  instance.user.username + str(instance.file) 
    return os.path.join(path, Format)

User = get_user_model()
class DataSets(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	link = models.URLField(blank=True,null=True)
	file = models.FileField(upload_to=path_and_rename,blank=True,validators=[validate_file_extension],null=True)
	# slug = models.SlugField(blank=True)

	def save(self, *args, **kwargs):

		super().save(*args, **kwargs)

	def get_absolute_url(self):

		return reverse('datasets:detail', kwargs={'pk':self.pk})

	def __str__(self):


		return  self.user.username+ ' ' + str(self.pk)



	def full(self):

		print('ffffffffff',self.objects.filter(user__username=self.user.username))
		return self.objects.filter(user__username__iexact=self.user.username) < 10

	def title(self):
		return "<strong> <i> File Name: </i></strong> " + os.path.basename(self.file.name) if not self.link else " <strong> <i>URL: </i></strong> " +self.link

	def get_file_or_url_path(self):

		return self.file.path if self.file else self.link