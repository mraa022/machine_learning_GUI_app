from tensorflow.keras.optimizers import RMSprop
from datasets.helper_functions import optimizer_options


class TestRmspropOptimizer():

	'''
		epsilon and centered can not be inputted/changed
	'''

	def setup(self):
		self.EPSILON = 1e-7
		self.CENTERED = False
	def test_default_parameters(self):
		'''
			the user did not input any parameters (they are constants)
		'''
		optimizer = 'Rmsprop'
		EPSILON = 1e-7
		default_parameters = {'learning_rate':0.001, 'rho':0.9, 'momentum':0}
		
		assert optimizer_options(**{})[optimizer].get_config() ==RMSprop(
													learning_rate=default_parameters['learning_rate'],
													rho=default_parameters['rho'],
													momentum=default_parameters['momentum'],
													centered = self.CENTERED,
													epsilon=self.EPSILON,).get_config()
	def test_user_inputted_some_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Rmsprop'
		default_learning_rate = 0.001
		inputted_parameters = {'rho':0, 'momentum':0.6}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==RMSprop(
													learning_rate=default_learning_rate,
													rho=inputted_parameters['rho'],
													momentum=inputted_parameters['momentum'],
													centered=self.CENTERED,
													epsilon=self.EPSILON).get_config()


	def test_user_inputted_all_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Rmsprop'
		inputted_parameters = {'learning_rate':12, 'rho':0, 'momentum':1}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==RMSprop(
													learning_rate=inputted_parameters['learning_rate'],
													rho=inputted_parameters['rho'],
													momentum=inputted_parameters['momentum'],
													centered = self.CENTERED,
													epsilon=self.EPSILON,).get_config()


