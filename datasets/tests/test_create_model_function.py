# def create_model(layers,number_of_inputs,activations,label_type,number_of_classes):
#     layers = [1] if not layers else layers  # one layer with one neuron is the default if the user did not provide any layers
#     activations = ['relu'] if not activations else activations
#     model = Sequential()
#     model.add(Dense(layers[0], input_shape=(number_of_inputs,),activation=activations[0] ))
#     if len(layers)>1:
#         [model.add(Dense(units,activation=activation)) for units,activation in zip(layers[1:],activations[1:])]
#     output = model.add(Dense(number_of_classes,activation='softmax')) if label_type == 'discrete' else model.add(Dense(1))
#     return model


from tensorflow.keras import Sequential
from keras.layers import Dense

from datasets.helper_functions import create_model
class TestClassificationFunction():

	'''
		INPUTS

		layers - a list of layers ===> [1,2,5,30]
		number_of_inputs - the number of features
		activations - a list of activation function corresponding to a layer ===> ['relu','softmax']
		label_type - discrete(classification) or continuous(regression)

	'''
	def test_default_classification_model(self):

		# default classification model is 1 input neuron with activation relu, and x(number of classes) output neurons with activation softmax

		number_of_inputs = 4
		label_type = 'discrete'
		number_of_classes = 2
		model = Sequential()
		model.add(Dense(1,input_shape=(number_of_inputs,),activation='relu'))
		model.add(Dense(number_of_classes,activation='softmax'))

		assert create_model(layers=[],number_of_inputs=number_of_inputs,activations=[],number_of_classes=number_of_classes,label_type=label_type)

	def test_inputted_classification_model(self):

		layers = [5,6]
		activations=['relu','sigmoid']
		number_of_inputs = 4
		label_type = 'discrete'
		number_of_classes = 22
		model = Sequential()
		model.add(Dense(layers[0],input_shape=(number_of_inputs,),activation=activations[0]))
		model.add(Dense(layers[1],input_shape=(number_of_inputs,),activation=activations[1]))
		model.add(Dense(number_of_classes,activation='softmax'))
		assert create_model(layers=layers,number_of_inputs=number_of_inputs,activations=activations,number_of_classes=number_of_classes,label_type=label_type)





class TestRegressionModel():

	def test_default_regression_model(self):

		# default regression model is 1 input neuron with activation relu, and x(number of classes) output neurons with no activation

		number_of_inputs = 4
		number_of_classes = 1
		label_type = 'continuous'
		model = Sequential()
		model.add(Dense(1,input_shape=(number_of_inputs,),activation='relu'))
		model.add(Dense(number_of_classes))

		assert create_model(layers=[],number_of_inputs=number_of_inputs,activations=[],number_of_classes=number_of_classes,label_type=label_type)

	def test_inputted_regression_model(self):
		number_of_classes = 1
		layers = [5,6]
		activations=['relu','sigmoid']
		number_of_inputs = 4
		label_type = 'continuous'
		model = Sequential()
		model.add(Dense(layers[0],input_shape=(number_of_inputs,),activation=activations[0]))
		model.add(Dense(layers[1],input_shape=(number_of_inputs,),activation=activations[1]))
		model.add(Dense(number_of_classes))
		assert create_model(layers=layers,number_of_inputs=number_of_inputs,activations=activations,number_of_classes=number_of_classes,label_type=label_type)




