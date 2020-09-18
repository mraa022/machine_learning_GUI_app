from tensorflow.keras.losses import (
        MeanSquaredError,
        MeanAbsoluteError,
        MeanAbsolutePercentageError,
        MeanSquaredLogarithmicError,
        CosineSimilarity,
        Huber,
        LogCosh,
        CategoricalCrossentropy,
        Poisson,
        KLDivergence,
        BinaryCrossentropy
    )
from tensorflow.keras.optimizers import (
        Adam,
        SGD,
        Adamax,
        RMSprop,
        Adagrad,
        Adadelta,
        Nadam,
        Ftrl
    )
from tensorflow.keras import Sequential
from keras.layers import Dense

def optimizer_options(
                      learning_rate=0.001,
                      beta_1=0.9,
                      beta_2=0.999,
                      rho=0.9,
                      momentum=0,
                      initial_accumulator_value=0.1,
                      l1_regularization_strength=0.0,
                      l2_regularization_strength=0.0,
                      l2_shrinkage_regularization_strength=0.0,
                      learning_rate_power=-0.5
                      ):
    optimizers = {
            'Adam':Adam(
                learning_rate=learning_rate, beta_1=beta_1, beta_2=beta_2, epsilon=1e-07, amsgrad=False,
                name='Adam'
                ),
            'Rmsprop':RMSprop(
                learning_rate=learning_rate,
                rho=rho,
                momentum=momentum,
                epsilon=1e-07,
                centered=False,
                name="RMSprop",
                ),
            'Adagrad':Adagrad(
                learning_rate=learning_rate,
                initial_accumulator_value=initial_accumulator_value,
                epsilon=1e-07
                ),
            'Adadelta':Adadelta(
                learning_rate=learning_rate, rho=rho, epsilon=1e-07
                ),
            'SGD':SGD(
                learning_rate=learning_rate, momentum=momentum, nesterov=False
                ),
            'Adamax':Adamax(
                learning_rate=learning_rate, beta_1=beta_1, beta_2=beta_2, epsilon=1e-07
                ),

            'Nadam':Nadam(
                learning_rate=learning_rate, beta_1=beta_1, beta_2=beta_2, epsilon=1e-07
                ),

            'Ftrl':Ftrl(
                learning_rate=learning_rate,
                learning_rate_power=learning_rate_power,
                initial_accumulator_value=initial_accumulator_value,
                l1_regularization_strength=l1_regularization_strength,
                l2_regularization_strength=l2_regularization_strength,
                l2_shrinkage_regularization_strength=l2_shrinkage_regularization_strength,
                )
            }
    return optimizers

def loss_options():
        losses = {
            'MeanSquaredError':MeanSquaredError(reduction="auto"),
            'MeanAbsoluteError':MeanAbsoluteError(reduction="auto"),
            'MeanAbsolutePercentageError':MeanAbsolutePercentageError(reduction="auto"),
            'MeanSquaredLogarithmicError':MeanSquaredLogarithmicError(reduction="auto"),
            'CosineSimilarity':CosineSimilarity(axis=-1, reduction="auto"),
            'Huber':Huber(delta=1.0, reduction="auto"),
            'LogCosh':LogCosh(reduction="auto", name="log_cosh"),
            'CategoricalCrossentropy':CategoricalCrossentropy(from_logits=False,label_smoothing=0,reduction="auto"),
            'Poisson':Poisson(reduction="auto", name="poisson"),
            'KLDivergence':KLDivergence(reduction="auto", name="kl_divergence"),
            'BinaryCrossentropy':BinaryCrossentropy(label_smoothing=0, reduction="auto", name="binary_crossentropy")
        }
        return losses
def create_model(layers,number_of_inputs,activations,label_type,number_of_classes):
    layers = [1] if not layers else layers  # one layer with one neuron is the default if the user did not provide any layers
    activations = ['relu'] if not activations else activations
    model = Sequential()
    model.add(Dense(layers[0], input_shape=(number_of_inputs,),activation=activations[0] ))
    if len(layers)>1:
        [model.add(Dense(units,activation=activation)) for units,activation in zip(layers[1:],activations[1:])]
    output = model.add(Dense(number_of_classes,activation='softmax')) if label_type == 'discrete' else model.add(Dense(1))
    return model





