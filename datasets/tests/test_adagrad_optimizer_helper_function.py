from tensorflow.keras.optimizers import Adagrad
from datasets.helper_functions import optimizer_options


class TestAdagradOptimizer():

	'''
		epsilon  can not be inputted/changed
	'''

	def setup(self):
		self.EPSILON = 1e-7
	def test_default_parameters(self):
		'''
			the user did not input any parameters (they are constants)
		'''
		optimizer = 'Adagrad'
		EPSILON = 1e-7
		default_parameters = {'learning_rate':0.001, 'initial_accumulator_value':0.1}
		
		assert optimizer_options(**{})[optimizer].get_config() ==Adagrad(
													learning_rate=default_parameters['learning_rate'],
													initial_accumulator_value = default_parameters['initial_accumulator_value'],
													epsilon=self.EPSILON).get_config()
	def test_user_inputted_some_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Adagrad'
		default_learning_rate = 0.001
		inputted_parameters = {'initial_accumulator_value':12}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==Adagrad(
													learning_rate=default_learning_rate,
													initial_accumulator_value = inputted_parameters['initial_accumulator_value'],
													epsilon=self.EPSILON).get_config()


	def test_user_inputted_all_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Adagrad'
		inputted_parameters =  {'learning_rate':12, 'initial_accumulator_value':54}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==Adagrad(
													learning_rate=inputted_parameters['learning_rate'],
													initial_accumulator_value = inputted_parameters['initial_accumulator_value'],
													epsilon=self.EPSILON).get_config()