from django.urls import path
from . import views
app_name = 'datasets'

urlpatterns = [

	path('login_first/',views.Not_logged_in.as_view(),name='login_first'),
	path('list/', views.DataSetsList.as_view(),name='list'),
	path('dataset/<int:pk>/',views.DatasetDetailView.as_view(),name='detail'),
	path('create/',views.CreateDatasetView.as_view(), name='create'),
	path('update/<int:pk>/',views.UpdateDatasetView.as_view(),name='update'),
	path('choose_new_dataset/',views.ChooseNewDataset.as_view(),name='choose_new_dataset'),
	path('build_ANN/',views.BuildNeuralNetwork.as_view(), name='create_ann'),
	path('current_dataset_in_session/', views.ShowDatasetInSession.as_view(),name='dataset_in_session'),
	path('regression_or_classification/',views.ClassificationOrRegression.as_view(),name='classification_or_regression')

	
]