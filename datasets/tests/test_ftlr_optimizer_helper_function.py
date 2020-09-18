from tensorflow.keras.optimizers import Ftrl


from datasets.helper_functions import optimizer_options

class TestFtlrOptimizer():

	'''
		epsilon and amsgrad can not be inputted/changed
	'''

	def test_default_parameters(self):
		'''
			the user did not input any parameters (they are constants)
		'''
		optimizer = 'Ftrl'
		EPSILON = 1e-7
		default_parameters = {

						'learning_rate' : 0.001,
						'l1_regularization_strength':0.0,
                      	'l2_regularization_strength':0.0,
                      	'l2_shrinkage_regularization_strength':0.0,
                      	'learning_rate_power':-0.5,
                      	'initial_accumulator_value' : 0.1
		}
		
		assert optimizer_options(**{})[optimizer].get_config() ==Ftrl(
													learning_rate=default_parameters['learning_rate'],
													l1_regularization_strength = default_parameters['l1_regularization_strength'],
													l2_regularization_strength = default_parameters['l2_regularization_strength'],
													l2_shrinkage_regularization_strength = default_parameters['l2_shrinkage_regularization_strength'],
													learning_rate_power = default_parameters['learning_rate_power'],
													initial_accumulator_value = default_parameters['initial_accumulator_value']
													).get_config()
	
	def test_user_inputted_some_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Ftrl'
		default_l1_regularization_strength = 0.0
		inputted_parameters={
							'learning_rate' : 12,
	                      	'l2_regularization_strength':1,
	                      	'l2_shrinkage_regularization_strength':2,
	                      	'learning_rate_power':-50,
	                      	'initial_accumulator_value' : 7
		}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==Ftrl(
													learning_rate=inputted_parameters['learning_rate'],
													l1_regularization_strength = default_l1_regularization_strength,
													l2_regularization_strength = inputted_parameters['l2_regularization_strength'],
													l2_shrinkage_regularization_strength = inputted_parameters['l2_shrinkage_regularization_strength'],
													learning_rate_power = inputted_parameters['learning_rate_power'],
													initial_accumulator_value = inputted_parameters['initial_accumulator_value']
													).get_config()


	def test_user_inputted_all_parameters(self):
		'''
			if the user inputted some of the parameters on their own
		'''
		optimizer = 'Ftrl'
		inputted_parameters={
							'learning_rate' : 12,
							'l1_regularization_strength':1,
	                      	'l2_regularization_strength':1,
	                      	'l2_shrinkage_regularization_strength':2,
	                      	'learning_rate_power':-65,
	                      	'initial_accumulator_value' : 7
		}
		assert optimizer_options(**inputted_parameters)[optimizer].get_config() ==Ftrl(
													learning_rate=inputted_parameters['learning_rate'],
													l1_regularization_strength = inputted_parameters['l1_regularization_strength'],
													l2_regularization_strength = inputted_parameters['l2_regularization_strength'],
													l2_shrinkage_regularization_strength = inputted_parameters['l2_shrinkage_regularization_strength'],
													learning_rate_power = inputted_parameters['learning_rate_power'],
													initial_accumulator_value = inputted_parameters['initial_accumulator_value']
													).get_config()



















