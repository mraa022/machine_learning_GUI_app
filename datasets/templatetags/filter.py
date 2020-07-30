from django import template
import  pandas as pd


register = template.Library()


@register.filter
def get_data_in_column(dataframe,column):

	return pd.DataFrame(dataframe[column]).head(20).to_html()


@register.filter
def is_numerical(dataframe,column):

	df = dataframe[column]
	for data_point in df:
		if type(data_point) != int and type(data_point) != float:
			return False

	return True
