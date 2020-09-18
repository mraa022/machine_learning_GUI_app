from tensorflow.keras.optimizers import Adadelta
from datasets.helper_functions import optimizer_options


class TestAdadeltaOptimizer():

	'''
		epsilon can not be inputted/changed
	'''

	def setup(self):
		self.EPSILON = 1e-7
	def test_default_parameters(self):
		'''
			the user did not input any parameters (they are constants)
		'''
		optimizer = 'Adadelta'
		EPSILON = 1e-7
		default_parameters = {'learning_rate':0.001, 'rho':0.9}
		
		assert optimizer_options(**{})[optimizer].get_config() ==Adadelta(
													learning_rate=default_parameters['learning_rate'],
													rho=default_parameters['rho'],
													epsilon=self.EPSILON,).get_config()
	def test_user_inputted_some_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Adadelta'
		default_learning_rate = 0.001
		inputted_parameters = {'rho':0.01}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==Adadelta(
													learning_rate=default_learning_rate,
													rho=inputted_parameters['rho'],
													epsilon=self.EPSILON).get_config()
	def test_user_inputted_all_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Adadelta'
		inputted_parameters = {'learning_rate':12, 'rho':0.1}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==Adadelta(
													learning_rate=inputted_parameters['learning_rate'],
													rho=inputted_parameters['rho'],
													epsilon=self.EPSILON,).get_config()


