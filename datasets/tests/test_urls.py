from django.urls import reverse,resolve

class TestUrls():

	def test_detail_url(self):

		path = reverse('datasets:detail',kwargs={'pk':140})
		assert resolve(path).view_name == 'datasets:detail'

	def test_list_url(self):

		path = reverse('datasets:list')
		assert resolve(path).view_name == 'datasets:list'

	def test_create_url(self):

		path = reverse('datasets:create')
		assert resolve(path).view_name == 'datasets:create'

	def test_update_url(self):

		path = reverse('datasets:update',kwargs={'pk':140})
		assert resolve(path).view_name == 'datasets:update'