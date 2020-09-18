import pytest
from datasets.views import dataset_saved_in_session,dataset_location_is_url,get_dataframe_given_url_or_file,remove_column,filtered_data_frame,return_customized_dataframe
from django.core.validators import URLValidator
from urllib.parse import unquote
from pandas import read_html,read_csv
import requests
import pandas
class fake_request():
	def __init__(self):
		self.session = {''}
		self.COOKIES = {'dataset_location':'','primary_key':''}
class TestDataFrameSaveInSessionFunction():
	'''
		this function is run when the user is selecting a dataset to train their model.
		it identifies if the user selected a dataset that was saved in their account or if they selected a new dataset.
		if they selected an existing dataset, COOKIES['dataset_location'] = "the url/file location of that dataset (the database is used to retrieve this info)".
		if they chose a new dataset (one thats not saved in their account), COOKIES['dataset_location'] is cleared, and the dataset location is saved in the session 
	'''
	def setup(self):
		self.fake_request_object = fake_request()

	def test_dataset_saved_in_session_true(self):
		assert dataset_saved_in_session(self.fake_request_object) == True

	def test_dataset_saved_in_session_false(self):
		self.fake_request_object.COOKIES['dataset_location'] = 'some url/file location'
		self.fake_request_object.COOKIES['primary_key'] = '123'
		assert dataset_saved_in_session(self.fake_request_object) == False


class TestDatasetLocationIsUrl():
	def test_dataset_location_is_url(self):

		assert dataset_location_is_url(dataset_location='https://github.com/plotly/datasets/blob/master/2014_us_cities.csv') == True

	def test_dataset_location_isnt_url(self):
		assert dataset_location_is_url(dataset_location='datasets/some_file.csv') == False

class TestDataframeFromUrlOrFile():

	'''
		gets the dataframe given the url or the path to a .csv file
	'''
	def setup(self):
		self.fake_url_dataframe = 'https://github.com/plotly/datasets/blob/master/2014_us_cities.csv'
		self.fake_file_dataframe = 'breast_cancer.csv'

	def test_get_dataframe_given_url(self):

		test_dataframe = read_html(requests.get(self.fake_url_dataframe).text)[0].drop('Unnamed: 0',axis=1)
		assert test_dataframe.equals(get_dataframe_given_url_or_file(dataframe_location = self.fake_url_dataframe)) 


	def test_get_dataframe_given_file(self):
		test_dataframe = read_csv(self.fake_file_dataframe)
		assert test_dataframe.equals(get_dataframe_given_url_or_file(dataframe_location = self.fake_file_dataframe)) 

class TestFilteredDataframe():
	'''
		test anything that has something to do with the user customizing the dataset (selecting which columns are categorical,etc)
	'''
	def setup(self):
		self.fake_request_object = fake_request()


	def test_filtered_dataframe_that_has_all_column_types(self):
		'''
			test if the correct filtered dataframe is made if the user selects both numerical and categorical columns 
		'''	
		self.fake_request_object.COOKIES['categorical_columns'] = 'sovereign_external_debt_default,independence'
		self.fake_request_object.COOKIES['numerical_columns'] = 'inflation_annual_cpi'
		self.fake_request_object.COOKIES['label_column'] = 'currency_crises'
		test_dataframe = read_csv('breast_cancer.csv')
		assert test_dataframe[['sovereign_external_debt_default','independence','inflation_annual_cpi','currency_crises']].equals(filtered_data_frame(request = self.fake_request_object, dataframe = test_dataframe))

	def test_filtered_dataframe_that_has_no_numerical_columns(self):

		self.fake_request_object.COOKIES['categorical_columns'] = 'sovereign_external_debt_default,independence'
		self.fake_request_object.COOKIES['numerical_columns'] = ''
		self.fake_request_object.COOKIES['label_column'] = 'currency_crises'
		test_dataframe = read_csv('breast_cancer.csv')
		assert test_dataframe[['sovereign_external_debt_default','independence','currency_crises']].equals(filtered_data_frame(request = self.fake_request_object, dataframe = test_dataframe))


	def test_filtered_dataframe_that_has_no_categorical_columns(self):
			
		self.fake_request_object.COOKIES['categorical_columns'] = ''
		self.fake_request_object.COOKIES['numerical_columns'] = 'inflation_annual_cpi'
		self.fake_request_object.COOKIES['label_column'] = 'currency_crises'
		test_dataframe = read_csv('breast_cancer.csv')
		assert test_dataframe[['inflation_annual_cpi','currency_crises']].equals(filtered_data_frame(request = self.fake_request_object, dataframe = test_dataframe))

	def test_filtered_dataframe_that_has_only_label_column(self):
	
		self.fake_request_object.COOKIES['categorical_columns'] = ''
		self.fake_request_object.COOKIES['numerical_columns'] = ''
		self.fake_request_object.COOKIES['label_column'] = 'currency_crises'
		test_dataframe = read_csv('breast_cancer.csv')
		assert test_dataframe[['currency_crises']].equals(filtered_data_frame(request = self.fake_request_object, dataframe = test_dataframe))


	def test_categorical_columns_one_hot_encoded_given_1_categorical_column(self):

		dataframe = read_csv('breast_cancer.csv').dropna()
		categorical_columns = 'sovereign_external_debt_default'.split(',') # seperated by commas
		true_dataframe = pandas.get_dummies(data=dataframe,columns=categorical_columns,drop_first=True) 
		test_dataframe = return_customized_dataframe(dataframe,categorical_columns)
		assert test_dataframe.equals(test_dataframe)


	def test_categorical_columns_one_hot_encoded_given_more_than_1_categorical_column(self):

		dataframe = read_csv('breast_cancer.csv').dropna()
		categorical_columns = 'sovereign_external_debt_default,independence'.split(',') # seperated by commas
		true_dataframe = pandas.get_dummies(data=dataframe,columns=categorical_columns,drop_first=True) 
		test_dataframe = return_customized_dataframe(dataframe,categorical_columns)
		assert test_dataframe.equals(test_dataframe)

	def test_categorical_columns_one_hot_encoded_given_0_categorical_column(self):

		dataframe = read_csv('breast_cancer.csv').dropna()
		categorical_columns = ''.split(',') # seperated by commas
		true_dataframe = dataframe
		test_dataframe = return_customized_dataframe(dataframe,categorical_columns)
		assert test_dataframe.equals(test_dataframe)



	


