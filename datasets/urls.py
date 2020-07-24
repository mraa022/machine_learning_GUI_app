from django.urls import path
from . import views
app_name = 'datasets'

urlpatterns = [

	path('login_first/',views.Not_logged_in.as_view(),name='login_first'),
	path('list/', views.DataSetsList.as_view(),name='list'),
	path('dataset/<int:pk>/',views.DatasetDetailView.as_view(),name='detail'),
	path('create/',views.CreateDatasetView.as_view(), name='create'),
	path('update/<int:pk>/',views.UpdateDatasetView.as_view(),name='update')

	
]