from datasets.views import DataSetsList,DatasetDetailView,CreateDatasetView,UpdateDatasetView
from django.contrib.auth import get_user_model
import django
import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer
from django.urls import reverse

@pytest.mark.django_db
class TestViewsPermissions():

	def setup(self):

		self.factory = RequestFactory()
		self.user = mixer.blend('accounts.User',username='puddyy')
		dataset = mixer.blend('datasets.DataSets',file='breast_cancer.csv',link=None,user=self.user,pk=40)
	def test_cant_see_list_view_if_not_logged_in(self):

		request = self.factory.get('datasets:list')
		with pytest.raises(AttributeError):
			response = DataSetsList.as_view()(request)

	def test_can_see_list_view_if_logged_in(self):
		request = self.factory.get('datasets:list')
		request.user = self.user
		response = DataSetsList.as_view()(request)
		assert response.status_code == 200

	def test_cant_see_create_view_if_not_logged_in(self):

		request = self.factory.get('datasets:create')
		with pytest.raises(AttributeError):
			response = CreateDatasetView.as_view()(request,pk=140)

	def test_can_see_create_view_if_logged_in(self):
		request = self.factory.get('datasets:create')
		request.user = self.user
		response = CreateDatasetView.as_view()(request,pk=140)
		assert response.status_code == 200

	def test_cant_see_update_view_if_not_logged_in(self):

		request = self.factory.get('datasets:update')
		with pytest.raises(AttributeError): ## this is raised when the .user couldn't be called off of the request (when the user is not saved)
			response = UpdateDatasetView.as_view()(request,pk=140)

	def test_can_see_update_view_if_logged_in(self):
		
		request = self.factory.get('datasets:update')
		request.user = self.user

		with pytest.raises(django.http.response.Http404):
			response = UpdateDatasetView.as_view()(request,pk=140)
	def test_cant_see_detail_view_if_not_logged_in(self):

		request = self.factory.get('datasets:detail')
		with pytest.raises(AttributeError):
			response = DatasetDetailView.as_view()(request,pk=140)

	def test_can_see_detail_view_if_logged_in(self):
		request = self.factory.get('datasets:detail')
		request.user = self.user
		with pytest.raises(django.http.response.Http404):   ## all test datasets are blank, this is raised if everything is fine but the object couldn't be found in the dataset
			response = DatasetDetailView.as_view()(request,pk=140)





