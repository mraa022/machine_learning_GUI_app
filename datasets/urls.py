from django.urls import path
from . import views
app_name = 'datasets'

urlpatterns = [

	path('list/', views.DataSetsList.as_view(),name='list')

	
]