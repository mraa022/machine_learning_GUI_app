
from tensorflow.keras.optimizers import SGD


from datasets.helper_functions import optimizer_options

class TestSgdOptimizer():

	'''
		nesterov can not be inputted/changed
	'''

	def setup(self):
		self.NESTEROV = False
	def test_default_parameters(self):
		'''
			the user did not input any parameters (they are constants)
		'''
		optimizer = 'SGD'
		EPSILON = 1e-7
		default_parameters = {'learning_rate':0.001, 'momentum':0}
		
		assert optimizer_options(**{})[optimizer].get_config() ==SGD(
													learning_rate=default_parameters['learning_rate'],
													momentum = default_parameters['momentum'],
													nesterov=self.NESTEROV).get_config()
	def test_user_inputted_some_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'SGD'
		default_momuntum = 0
		inputted_parameters = {'learning_rate':12}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==SGD(
													learning_rate=inputted_parameters['learning_rate'],
													momentum = default_momuntum,
													nesterov=self.NESTEROV).get_config()


	def test_user_inputted_all_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'SGD'
		inputted_parameters =  {'learning_rate':12, 'momentum':1}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==SGD(
													learning_rate=inputted_parameters['learning_rate'],
													momentum = inputted_parameters['momentum'],
													nesterov=self.NESTEROV).get_config()





