from tensorflow.keras.optimizers import Nadam


from datasets.helper_functions import optimizer_options

class TestNadamOptimizer():

	'''
		epsilon can not be inputted/changed
	'''

	def setup(self):
		self.EPSILON = 1e-7
	def test_default_parameters(self):
		'''
			the user did not input any parameters (they are constants)
		'''
		optimizer = 'Nadam'
		EPSILON = 1e-7
		default_parameters = {'learning_rate':0.001, 'beta_1':0.9, 'beta_2':0.999}
		
		assert optimizer_options(**{})[optimizer].get_config() ==Nadam(
													learning_rate=default_parameters['learning_rate'],
													beta_1=default_parameters['beta_1'],
													beta_2=default_parameters['beta_2'],
													epsilon=self.EPSILON,).get_config()
	def test_user_inputted_some_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Nadam'
		default_learning_rate = 0.001
		inputted_parameters = {'beta_1':0.99999, 'beta_2':0.1}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==Nadam(
													learning_rate=default_learning_rate,
													beta_1=inputted_parameters['beta_1'],
													beta_2=inputted_parameters['beta_2'],
													epsilon=self.EPSILON,).get_config()


	def test_user_inputted_all_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Nadam'
		inputted_parameters =  {'learning_rate':12, 'beta_1':54, 'beta_2':0.999}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==Nadam(
													learning_rate=inputted_parameters['learning_rate'],
													beta_1=inputted_parameters['beta_1'],
													beta_2=inputted_parameters['beta_2'],
													epsilon=self.EPSILON,).get_config()



















