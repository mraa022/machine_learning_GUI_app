from mixer.backend.django import  mixer
from datasets.models import path_and_rename
from django.contrib.auth.models import User
import pytest

@pytest.mark.django_db
class  TestModel():

	def test_file_title(self):

		dataset = mixer.blend('datasets.DataSets',file='breast_cancer.csv',link=None)
		assert dataset.title() == '<strong> <i> File Name: </i></strong> ' +'breast_cancer.csv'
	def test_url_title(self):

		dataset = mixer.blend('datasets.DataSets',file=None,link='https://www.youtube.com/watch?v=TzCWadHwdSs')
		assert dataset.title() == ' <strong> <i>URL: </i></strong> ' + 'https://www.youtube.com/watch?v=TzCWadHwdSs'

	def test_add_username_to_file_name(self):
		fake_user = User.objects.create(username='fake')
		dataset = mixer.blend('datasets.DataSets',file='breast_cancer.csv',link=None,user = fake_user)
		assert path_and_rename(dataset,'breast_cancer') == 'datasets/fakebreast_cancer'