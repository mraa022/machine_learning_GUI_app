from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import os
# Create your models here.

User = get_user_model()
class DataSets(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='current_user')
	link = models.URLField(blank=True)
	file = models.FileField(upload_to='datasets',blank = True)
	# slug = models.SlugField(blank=True)

	def save(self, *args, **kwargs):

		

		super().save(*args, **kwargs)

	def get_absolute_url(self):

		return reverse('datasets:detail', kwargs={'pk':self.pk})

	def __str__(self):


		# print(file.title)
		return  self.user.username+ ' ' + str(self.pk)




	def title(self):
		return "File Name: " + os.path.basename(self.file.name) if not self.link else " URL: " +self.link
