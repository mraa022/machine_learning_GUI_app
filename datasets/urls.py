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
	path('categorical_columns/', views.DataSetCategoricalColumns.as_view(),name='categorical_columns'),
	path('regression_or_classification/',views.ClassificationOrRegression.as_view(),name='classification_or_regression'),
	path('neural_network_graph_and_keras_model/',views.NeuralNetworkDiagramAndKerasModel.as_view(),name='neural_network_graph_and_keras_model'),
	path('numberical_columns/',views.DataSetNumericalColumns.as_view(),name='numerical_columns'),
	path('label_column/',views.DataSetLabelColumn.as_view(),name='label_column'),
	path('show_selected_columns/',views.ShowSelectedColumns.as_view(),name='show_selected_columns'),
	path('select_dataset_for_training/',views.SelectDataSet.as_view(),name='select_dataset_for_training'),
	path('select_model_type/',views.SelectModelType.as_view(),name='select_model_type')


	
]

