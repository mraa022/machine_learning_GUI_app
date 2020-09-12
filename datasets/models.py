from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import os

# Create your models here.


def remove_username_from_filename(filename,username):
	return filename[len(username):]
def path_and_rename(instance, filename):
    upload_to = "datasets"
    Format =  instance.user.username + str(filename)
    return os.path.join(upload_to, Format)

User = get_user_model()

class DataSets(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='datasets')
	link = models.URLField(blank=True,null=True)
	file = models.FileField(upload_to=path_and_rename,blank=True,null=True,default=None)


	def get_absolute_url(self):


		return reverse('datasets:detail', kwargs={'pk':self.pk})

	def __str__(self):


		return  self.user.username+ ' ' + str(self.pk)

	def title(self):
		file_name = str(os.path.basename(self.file.name))
		# print(self.user.username)
		return "<strong> <i> File Name: </i></strong> " + remove_username_from_filename(file_name,self.user.username) if self.file else " <strong> <i>URL: </i></strong> " + str(self.link)



	